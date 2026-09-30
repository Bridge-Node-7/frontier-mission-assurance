"""Compare two governed FTQC Assurance case states.

The comparison derives bounded change impact from declared case records. It does not
infer the replacement scientific/engineering answer or authorize a consequential
decision.
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict, deque
from pathlib import Path
from typing import Any

from validate_ftqc_case import case_summary, evaluate_envelopes, validate_case


def _assumptions(system: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        item["id"]: item
        for item in system.get("assumptions", [])
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }


def changed_assumptions(
    previous: dict[str, Any], current: dict[str, Any]
) -> list[str]:
    before, after = _assumptions(previous), _assumptions(current)
    return sorted(
        item_id
        for item_id in set(before) | set(after)
        if before.get(item_id, {}).get("value") != after.get(item_id, {}).get("value")
    )


def _node_map(graph: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        item["id"]: item
        for item in graph.get("nodes", [])
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }


def _edge_set(graph: dict[str, Any]) -> set[tuple[str, str, str]]:
    return {
        (str(item.get("from")), str(item.get("relation")), str(item.get("to")))
        for item in graph.get("edges", [])
        if isinstance(item, dict)
    }


def _graph_changes(previous: dict[str, Any], current: dict[str, Any]) -> dict[str, Any]:
    before_nodes, after_nodes = _node_map(previous), _node_map(current)
    changed_nodes: list[dict[str, Any]] = []
    for node_id in sorted(set(before_nodes) & set(after_nodes)):
        fields = [
            field
            for field in ("kind", "status", "criticality", "title")
            if before_nodes[node_id].get(field) != after_nodes[node_id].get(field)
        ]
        if fields:
            changed_nodes.append({"node_id": node_id, "changed_fields": fields})
    before_edges, after_edges = _edge_set(previous), _edge_set(current)

    def edge_rows(items: set[tuple[str, str, str]]) -> list[dict[str, str]]:
        return [
            {"from": source, "relation": relation, "to": target}
            for source, relation, target in sorted(items)
        ]

    return {
        "added_nodes": sorted(set(after_nodes) - set(before_nodes)),
        "removed_nodes": sorted(set(before_nodes) - set(after_nodes)),
        "changed_nodes": changed_nodes,
        "added_relations": edge_rows(after_edges - before_edges),
        "removed_relations": edge_rows(before_edges - after_edges),
    }


def _envelope_map(doc: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        item["envelope_id"]: item
        for item in doc.get("envelopes", [])
        if isinstance(item, dict) and isinstance(item.get("envelope_id"), str)
    }


def _envelope_changes(previous: dict[str, Any], current: dict[str, Any]) -> dict[str, Any]:
    before, after = _envelope_map(previous), _envelope_map(current)
    changed: list[dict[str, Any]] = []
    fields = ("evidence_ref", "evidence_class", "basis", "applicability", "review")
    for envelope_id in sorted(set(before) & set(after)):
        changed_fields = [
            field for field in fields if before[envelope_id].get(field) != after[envelope_id].get(field)
        ]
        if changed_fields:
            changed.append({"envelope_id": envelope_id, "changed_fields": changed_fields})
    return {
        "added": sorted(set(after) - set(before)),
        "removed": sorted(set(before) - set(after)),
        "changed": changed,
    }


def _changed_fields(
    previous: dict[str, Any], current: dict[str, Any], fields: tuple[str, ...]
) -> list[str]:
    return [field for field in fields if previous.get(field) != current.get(field)]


def _impact(
    graph: dict[str, Any],
    seeds: set[str],
    invalid_evidence: set[str],
    reopened_reviews: set[str],
) -> set[str]:
    reverse: dict[str, set[str]] = defaultdict(set)
    supported: dict[str, set[str]] = defaultdict(set)
    for edge in graph.get("edges", []):
        if not isinstance(edge, dict):
            continue
        if edge.get("relation") in {"depends_on", "requires"}:
            reverse[str(edge.get("to"))].add(str(edge.get("from")))
        elif edge.get("relation") in {"supports", "verifies", "validates"}:
            supported[str(edge.get("from"))].add(str(edge.get("to")))

    impacted, queue = set(seeds), deque(seeds)
    for evidence_id in sorted(invalid_evidence | reopened_reviews):
        for target in sorted(supported.get(evidence_id, ())):
            if target not in impacted:
                impacted.add(target)
                queue.append(target)
    while queue:
        for dependent in sorted(reverse.get(queue.popleft(), ())):
            if dependent not in impacted:
                impacted.add(dependent)
                queue.append(dependent)
    return impacted


def compare_cases(
    root: Path, previous_dir: Path, current_dir: Path
) -> tuple[list[str], list[str], dict[str, Any]]:
    errors: list[str] = []
    warnings: list[str] = []

    prev_errors, prev_warnings, previous = validate_case(root, previous_dir)
    cur_errors, cur_warnings, current = validate_case(
        root, current_dir, allow_applicability_mismatch=True
    )
    errors.extend(f"previous: {item}" for item in prev_errors)
    errors.extend(f"current: {item}" for item in cur_errors)
    warnings.extend(f"previous: {item}" for item in prev_warnings)
    warnings.extend(f"current: {item}" for item in cur_warnings)
    if errors:
        return errors, warnings, {}

    prev_system = previous["system"]
    cur_system = current["system"]
    if prev_system["system_id"] != cur_system["system_id"]:
        errors.append("previous/current FTQC cases must refer to the same system_id")
    if previous["decision"]["decision"]["id"] != current["decision"]["decision"]["id"]:
        errors.append("previous/current FTQC cases must refer to the same decision id")
    if prev_system["record_class"] != cur_system["record_class"]:
        errors.append("previous/current FTQC cases must use the same record_class")
    if errors:
        return errors, warnings, {}

    changed_ids = set(changed_assumptions(prev_system, cur_system))
    context_changes: list[str] = []
    for field in ("modality", "architecture_revision"):
        if prev_system.get(field) != cur_system.get(field):
            context_changes.append(field)
    if prev_system.get("workload") != cur_system.get("workload"):
        context_changes.append("workload")

    prev_resource = previous["resource"]
    cur_resource = current["resource"]
    resource_reused = prev_resource["record_id"] == cur_resource["record_id"]
    controlling_change = bool(
        changed_ids.intersection(cur_resource.get("assumption_refs", []))
        or context_changes
    )
    stale_resources: set[str] = set()
    if resource_reused and controlling_change:
        stale_resources.add(cur_resource["record_id"])
    if cur_resource.get("review_state") == "STALE":
        stale_resources.add(cur_resource["record_id"])

    resource_changes = _changed_fields(
        prev_resource,
        cur_resource,
        (
            "record_id",
            "estimator",
            "problem",
            "assumption_refs",
            "result",
            "provenance",
            "applicability_envelope_ref",
            "review_state",
        ),
    )
    graph_changes = _graph_changes(previous["graph"], current["graph"])
    envelope_changes = _envelope_changes(previous["envelopes"], current["envelopes"])

    envelope_results = evaluate_envelopes(current["envelopes"], cur_system)
    outside = {
        item["evidence_ref"] for item in envelope_results if not item["in_scope"]
    }

    reopened_reviews = {
        item["review_id"]
        for item in previous["experts"].get("reviews", [])
        if changed_ids.intersection(item.get("reopen_when_refs", []))
    }

    impact_graph = {
        "edges": [
            *previous["graph"].get("edges", []),
            *current["graph"].get("edges", []),
        ]
    }
    seeds = changed_ids | stale_resources
    impacted = _impact(impact_graph, seeds, outside, reopened_reviews)
    decision_id = current["decision"]["decision"]["id"]
    decision_reopen = decision_id in impacted

    prev_decision = previous["decision"]["decision"]
    cur_decision = current["decision"]["decision"]
    decision_changes = _changed_fields(
        prev_decision, cur_decision, ("disposition", "rationale", "reopen_when")
    )
    if previous["decision"].get("basis") != current["decision"].get("basis"):
        decision_changes.append("basis")
    governance_review_required = bool(
        graph_changes["added_nodes"]
        or graph_changes["removed_nodes"]
        or graph_changes["changed_nodes"]
        or graph_changes["added_relations"]
        or graph_changes["removed_relations"]
        or envelope_changes["added"]
        or envelope_changes["removed"]
        or envelope_changes["changed"]
        or decision_changes
    )

    result = {
        "profile_version": "0.2",
        "system_id": cur_system["system_id"],
        "record_class": cur_system["record_class"],
        "previous_architecture_revision": prev_system["architecture_revision"],
        "current_architecture_revision": cur_system["architecture_revision"],
        "changed_assumptions": sorted(changed_ids),
        "context_changes": context_changes,
        "resource_estimates_stale": sorted(stale_resources),
        "resource_estimate_regenerated": not resource_reused,
        "resource_estimate_changes": resource_changes,
        "evidence_outside_envelope": sorted(outside),
        "envelope_results": envelope_results,
        "envelope_changes": envelope_changes,
        "expert_reviews_reopen": sorted(reopened_reviews),
        "graph_changes": graph_changes,
        "impacted_nodes": sorted(impacted - changed_ids),
        "decision_id": decision_id,
        "decision_changes": decision_changes,
        "decision_reopen_required": decision_reopen,
        "governance_review_required": governance_review_required,
        "current_case": case_summary(current),
        "boundary_note": (
            "Change impact is derived from declared case contracts and graph relationships. "
            "It does not establish the replacement quantum-engineering answer, estimator "
            "correctness, hardware performance, independent V&V, or decision authority."
        ),
    }
    return errors, warnings, result


def render_report(result: dict[str, Any], warnings: list[str]) -> str:
    lines = [
        "# FTQC Change Impact",
        "",
        f"- System: `{result['system_id']}`",
        f"- Previous revision: {result['previous_architecture_revision']}",
        f"- Current revision: {result['current_architecture_revision']}",
        f"- Decision: `{result['decision_id']}`",
        f"- Decision reopen required: **{str(result['decision_reopen_required']).upper()}**",
        f"- Governance review required: **{str(result['governance_review_required']).upper()}**",
        "",
        "## What changed",
        "",
    ]
    if result["changed_assumptions"]:
        lines.extend(f"- Assumption: `{item}`" for item in result["changed_assumptions"])
    if result["context_changes"]:
        lines.extend(f"- Context: {item}" for item in result["context_changes"])
    if not result["changed_assumptions"] and not result["context_changes"]:
        lines.append("- No declared assumption or context change detected.")

    graph_changes = result["graph_changes"]
    envelope_changes = result["envelope_changes"]
    lines += ["", "## Governance changes", ""]
    if any(
        (
            graph_changes["added_nodes"],
            graph_changes["removed_nodes"],
            graph_changes["changed_nodes"],
            graph_changes["added_relations"],
            graph_changes["removed_relations"],
            envelope_changes["added"],
            envelope_changes["removed"],
            envelope_changes["changed"],
            result["decision_changes"],
        )
    ):
        for item in graph_changes["added_nodes"]:
            lines.append(f"- Graph node added: `{item}`")
        for item in graph_changes["removed_nodes"]:
            lines.append(f"- Graph node removed: `{item}`")
        for item in graph_changes["changed_nodes"]:
            fields = ", ".join(item["changed_fields"])
            lines.append(f"- Graph node changed: `{item['node_id']}` ({fields})")
        for item in graph_changes["added_relations"]:
            lines.append(
                f"- Relation added: `{item['from']} --{item['relation']}→ {item['to']}`"
            )
        for item in graph_changes["removed_relations"]:
            lines.append(
                f"- Relation removed: `{item['from']} --{item['relation']}→ {item['to']}`"
            )
        for item in envelope_changes["added"]:
            lines.append(f"- Evidence envelope added: `{item}`")
        for item in envelope_changes["removed"]:
            lines.append(f"- Evidence envelope removed: `{item}`")
        for item in envelope_changes["changed"]:
            fields = ", ".join(item["changed_fields"])
            lines.append(f"- Evidence envelope changed: `{item['envelope_id']}` ({fields})")
        if result["decision_changes"]:
            lines.append(
                "- Decision governance changed: " + ", ".join(result["decision_changes"])
            )
    else:
        lines.append("- No graph, envelope, or decision-governance change detected.")

    lines += ["", "## Resource-estimate changes", ""]
    if result["resource_estimate_changes"]:
        lines.append("- Changed fields: " + ", ".join(result["resource_estimate_changes"]))
    else:
        lines.append("- No resource-estimate field changed.")

    lines += ["", "## What became stale", ""]
    if result["resource_estimates_stale"]:
        lines.extend(
            f"- Resource estimate: `{item}`" for item in result["resource_estimates_stale"]
        )
    else:
        lines.append("- No reused resource estimate became stale by the declared comparison.")

    lines += ["", "## Evidence applicability", ""]
    outside = {
        item["evidence_ref"]: item
        for item in result["envelope_results"]
        if not item["in_scope"]
    }
    if outside:
        for evidence_ref, item in outside.items():
            failed = ", ".join(item["failed_subjects"])
            lines.append(
                f"- `{evidence_ref}` → **OUTSIDE DECLARED ENVELOPE** "
                f"(failed: {failed})"
            )
    else:
        lines.append("- All declared evidence envelopes remain in scope.")

    lines += ["", "## Expert review", ""]
    if result["expert_reviews_reopen"]:
        lines.extend(
            f"- Reopen: `{item}`" for item in result["expert_reviews_reopen"]
        )
    else:
        lines.append("- No expert review reopen trigger was declared by this comparison.")

    lines += ["", "## Impacted graph nodes", ""]
    if result["impacted_nodes"]:
        lines.extend(f"- `{item}`" for item in result["impacted_nodes"])
    else:
        lines.append("- No downstream graph node was impacted by the declared change.")

    lines += [
        "",
        "## Current human disposition",
        "",
        f"- Disposition: **{result['current_case']['decision']['disposition']}**",
        f"- Rationale: {result['current_case']['decision']['rationale']}",
        "",
        "## Assurance boundary",
        "",
        result["boundary_note"],
        "",
    ]
    if warnings:
        lines += ["## Graph warnings", ""]
        lines.extend(f"- {item}" for item in warnings)
        lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Compare two governed FTQC case states under profile contract 0.2."
    )
    parser.add_argument("previous_case", help="Previous six-file FTQC case directory.")
    parser.add_argument("current_case", help="Current six-file FTQC case directory.")
    parser.add_argument(
        "--root",
        default=str(Path(__file__).resolve().parents[1]),
        help="FMA source root containing FTQC schemas.",
    )
    parser.add_argument("--report", help="Optional Markdown change-impact report path.")
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    errors, warnings, result = compare_cases(
        root, Path(args.previous_case).resolve(), Path(args.current_case).resolve()
    )
    if errors:
        if args.as_json:
            print(json.dumps({"status": "FAIL", "errors": errors, "warnings": warnings}, indent=2))
        else:
            print("FTQC CHANGE IMPACT FAIL")
            for error in errors:
                print(f"FAIL: {error}")
            for warning in warnings:
                print(f"WARN: {warning}")
        return 2

    if args.report:
        out = Path(args.report)
        if not out.is_absolute():
            out = Path.cwd() / out
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(render_report(result, warnings), encoding="utf-8")

    if args.as_json:
        print(
            json.dumps(
                {"status": "PASS", "warnings": warnings, "result": result},
                indent=2,
                sort_keys=True,
            )
        )
    else:
        print("FTQC CHANGE IMPACT PASS")
        print(
            "CHANGED ASSUMPTIONS: "
            + (", ".join(result["changed_assumptions"]) or "none")
        )
        print(
            "STALE RESOURCE ESTIMATES: "
            + (", ".join(result["resource_estimates_stale"]) or "none")
        )
        print(
            "EVIDENCE OUTSIDE ENVELOPE: "
            + (", ".join(result["evidence_outside_envelope"]) or "none")
        )
        print(
            "EXPERT REVIEWS TO REOPEN: "
            + (", ".join(result["expert_reviews_reopen"]) or "none")
        )
        print(
            f"DECISION REOPEN REQUIRED: {str(result['decision_reopen_required']).upper()}"
        )
        print(
            f"GOVERNANCE REVIEW REQUIRED: {str(result['governance_review_required']).upper()}"
        )
        if args.report:
            print(f"WROTE: {Path(args.report)}")
        print(result["boundary_note"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
