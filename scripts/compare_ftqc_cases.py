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

from validate_ftqc_case import case_summary, validate_case


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


def _subject_value(subject: str, system: dict[str, Any]) -> Any:
    if subject == "modality":
        return system.get("modality")
    if subject == "architecture_revision":
        return system.get("architecture_revision")
    if subject.startswith("assumption:"):
        item = _assumptions(system).get(subject.split(":", 1)[1])
        return None if item is None else item.get("value")
    raise ValueError(f"unsupported applicability subject: {subject}")


def _condition_matches(condition: dict[str, Any], system: dict[str, Any]) -> bool:
    actual = _subject_value(condition["subject"], system)
    expected = condition["value"]
    operator = condition["operator"]
    if operator == "eq":
        return actual == expected
    if operator == "in":
        return actual in expected
    if operator == "lte":
        return actual is not None and actual <= expected
    if operator == "gte":
        return actual is not None and actual >= expected
    if operator == "between":
        return (
            actual is not None
            and isinstance(expected, list)
            and len(expected) == 2
            and expected[0] <= actual <= expected[1]
        )
    raise ValueError(f"unsupported applicability operator: {operator}")


def evaluate_envelopes(
    envelope_doc: dict[str, Any], system: dict[str, Any]
) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for envelope in envelope_doc.get("envelopes", []):
        failed = [
            condition
            for condition in envelope["applicability"]["conditions"]
            if not _condition_matches(condition, system)
        ]
        results.append(
            {
                "envelope_id": envelope["envelope_id"],
                "evidence_ref": envelope["evidence_ref"],
                "in_scope": not failed,
                "failed_subjects": [item["subject"] for item in failed],
            }
        )
    return results


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
    cur_errors, cur_warnings, current = validate_case(root, current_dir)
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
    stale_resources = (
        {cur_resource["record_id"]} if resource_reused and controlling_change else set()
    )

    envelope_results = evaluate_envelopes(current["envelopes"], cur_system)
    outside = {
        item["evidence_ref"] for item in envelope_results if not item["in_scope"]
    }

    reopened_reviews = {
        item["review_id"]
        for item in previous["experts"].get("reviews", [])
        if changed_ids.intersection(item.get("reopen_when_refs", []))
    }

    graph = current["graph"]
    seeds = changed_ids | stale_resources
    impacted = _impact(graph, seeds, outside, reopened_reviews)
    decision_id = current["decision"]["decision"]["id"]
    decision_reopen = decision_id in impacted

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
        "evidence_outside_envelope": sorted(outside),
        "envelope_results": envelope_results,
        "expert_reviews_reopen": sorted(reopened_reviews),
        "impacted_nodes": sorted(impacted - changed_ids),
        "decision_id": decision_id,
        "decision_reopen_required": decision_reopen,
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
        if args.report:
            print(f"WROTE: {Path(args.report)}")
        print(result["boundary_note"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
