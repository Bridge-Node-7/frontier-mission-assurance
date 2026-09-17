"""Evaluate the public FTQC Assurance synthetic reference.

The evaluator checks declared contracts and demonstrates change propagation. It does
not validate quantum hardware, QEC performance, resource-estimation truth, or mission
readiness.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict, deque
from pathlib import Path
from typing import Any

import yaml

try:
    import jsonschema
    from jsonschema.exceptions import SchemaError, ValidationError
except ImportError:
    jsonschema = None
    SchemaError = ValidationError = ValueError

PROFILE_VERSION = "0.1"
PROFILE_NAME = "ftqc-assurance"
ALLOWED_RECORD_CLASSES = {"synthetic", "private"}
URL_RE = re.compile(r"https?://", re.IGNORECASE)
EMAIL_RE = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE)


def _json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _yaml(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _assumptions(system: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {item["id"]: item for item in system.get("assumptions", [])}


def changed_assumptions(baseline: dict[str, Any], changed: dict[str, Any]) -> list[str]:
    before, after = _assumptions(baseline), _assumptions(changed)
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
    actual, expected = _subject_value(condition["subject"], system), condition["value"]
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
        return actual is not None and len(expected) == 2 and expected[0] <= actual <= expected[1]
    raise ValueError(f"unsupported applicability operator: {operator}")


def evaluate_envelope(envelope: dict[str, Any], system: dict[str, Any]) -> dict[str, Any]:
    failed = [
        item
        for item in envelope["applicability"]["conditions"]
        if not _condition_matches(item, system)
    ]
    return {
        "envelope_id": envelope["envelope_id"],
        "evidence_ref": envelope["evidence_ref"],
        "in_scope": not failed,
        "failed_subjects": [item["subject"] for item in failed],
    }


def _impact(
    graph: dict[str, Any], seeds: set[str], invalid_evidence: set[str], reopened_reviews: set[str]
) -> set[str]:
    reverse: dict[str, set[str]] = defaultdict(set)
    supported: dict[str, set[str]] = defaultdict(set)
    for edge in graph.get("edges", []):
        if edge["relation"] in {"depends_on", "requires"}:
            reverse[edge["to"]].add(edge["from"])
        elif edge["relation"] in {"supports", "verifies", "validates"}:
            supported[edge["from"]].add(edge["to"])

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


def _hold_reasons(envelopes: list[dict[str, Any]], reviews: list[dict[str, Any]]) -> list[str]:
    reasons: list[str] = []
    for envelope in envelopes:
        review = envelope["review"]
        if review["decision_gate"] and review["status"] != "IN_SCOPE":
            reasons.append(f"{envelope['envelope_id']} is not in scope")
        if review["decision_gate"] and review["authority_state"] != "ESTABLISHED":
            reasons.append(f"{envelope['envelope_id']} applicability is declared but not established")
    for review in reviews:
        if review["mandatory"] and review["conclusion"] != "SUPPORTED_WITHIN_SCOPE":
            reasons.append(f"{review['review_id']} mandatory expert gate remains open")
    return reasons


def _paths(root: Path) -> tuple[Path, Path, Path]:
    profile = root / "profiles" / PROFILE_NAME
    base = profile / "examples" / "synthetic-neutral-atom"
    return profile, base / "baseline", base / "changed-assumption"


def evaluate_case(root: Path) -> dict[str, Any]:
    _, baseline, changed = _paths(root)
    base_system, changed_system = _json(baseline / "system-concept.json"), _json(changed / "system-concept.json")
    resource = _json(baseline / "resource-estimate-receipt.json")
    envelopes = _json(baseline / "evidence-envelopes.json")["envelopes"]
    reviews = _json(baseline / "expert-adjudications.json")["reviews"]
    graph, decision = _yaml(baseline / "assurance-graph.yaml"), _yaml(baseline / "decision-receipt.yaml")

    changed_ids = set(changed_assumptions(base_system, changed_system))
    envelope_results = [evaluate_envelope(item, changed_system) for item in envelopes]
    stale = {resource["record_id"]} if changed_ids.intersection(resource["assumption_refs"]) else set()
    outside = {item["evidence_ref"] for item in envelope_results if not item["in_scope"]}
    reopened = {
        item["review_id"]
        for item in reviews
        if changed_ids.intersection(item.get("reopen_when_refs", []))
    }
    impacted = _impact(graph, changed_ids | stale, outside, reopened)

    return {
        "profile_version": PROFILE_VERSION,
        "baseline": {
            "software_contract_validation": "PASS",
            "technical_decision_readiness": decision["decision"]["disposition"],
            "hold_reasons": _hold_reasons(envelopes, reviews),
            "critical_claims": sum(
                node["kind"] == "claim" and node.get("criticality", 0) >= 4
                for node in graph["nodes"]
            ),
        },
        "change": {
            "changed_assumptions": sorted(changed_ids),
            "resource_estimates_stale": sorted(stale),
            "evidence_outside_envelope": sorted(outside),
            "expert_reviews_reopen": sorted(reopened),
            "impacted_nodes": sorted(item for item in impacted if item not in changed_ids),
            "decision_reopen_required": decision["decision"]["id"] in impacted or bool(changed_ids),
        },
        "boundary_note": (
            "PASS describes declared software and contract checks only; it does not "
            "establish quantum performance or mission approval."
        ),
    }


def validate_profile(root: Path) -> list[str]:
    profile, baseline, changed = _paths(root)
    problems: list[str] = []
    required = [
        profile / "README.md", profile / "ASSURANCE_SCOPE.md", profile / "PROFILE_CONTRACT.md",
        profile / "docs" / "FTQC_ASSURANCE_CHAIN.md",
        profile / "docs" / "RESOURCE_ESTIMATE_ASSURANCE.md",
        profile / "docs" / "EVIDENCE_VALIDITY_ENVELOPES.md",
        profile / "docs" / "EXPERT_REVIEW_GATES.md",
        profile / "docs" / "QBI_PUBLIC_CROSSWALK.md",
        profile / "docs" / "PRIVATE_WORKSPACE_PATTERN.md",
        profile / "docs" / "ADOPTION_PATH.md",
        root / "scripts" / "evaluate_ftqc_reference.py",
        root / "scripts" / "validate_ftqc_assurance.py",
    ]
    problems.extend(
        f"required FTQC surface missing: {path.relative_to(root)}"
        for path in required if not path.is_file()
    )

    schema_paths = {
        "system": profile / "schemas" / "ftqc-system-concept.schema.json",
        "resource": profile / "schemas" / "resource-estimate-receipt.schema.json",
        "envelopes": profile / "schemas" / "evidence-validity-envelope.schema.json",
        "experts": profile / "schemas" / "expert-adjudication-record.schema.json",
    }
    schemas: dict[str, dict[str, Any]] = {}
    for name, path in schema_paths.items():
        try:
            schema = _json(path)
            schemas[name] = schema
            if schema.get("properties", {}).get("profile_version", {}).get("const") != PROFILE_VERSION:
                problems.append(f"schema profile_version drifted: {path.name}")
            if jsonschema is not None:
                jsonschema.validators.validator_for(schema).check_schema(schema)
        except (OSError, json.JSONDecodeError, SchemaError) as exc:
            problems.append(f"schema invalid: {path.name}: {exc}")

    try:
        records = {
            "system": _json(baseline / "system-concept.json"),
            "resource": _json(baseline / "resource-estimate-receipt.json"),
            "envelopes": _json(baseline / "evidence-envelopes.json"),
            "experts": _json(baseline / "expert-adjudications.json"),
        }
        changed_system = _json(changed / "system-concept.json")
        graph, decision = _yaml(baseline / "assurance-graph.yaml"), _yaml(baseline / "decision-receipt.yaml")
        expected = _json(changed / "expected-impact.json")
    except (OSError, json.JSONDecodeError, yaml.YAMLError) as exc:
        return problems + [f"reference fixture invalid: {exc}"]

    if jsonschema is not None and len(schemas) == len(schema_paths):
        for name, record in records.items():
            try:
                jsonschema.validators.validator_for(schemas[name])(schemas[name]).validate(record)
            except (SchemaError, ValidationError) as exc:
                problems.append(f"example/schema mismatch: {name}: {exc}")
        try:
            jsonschema.validators.validator_for(schemas["system"])(schemas["system"]).validate(changed_system)
        except (SchemaError, ValidationError) as exc:
            problems.append(f"changed system/schema mismatch: {exc}")
        for schema_name, obj, label in (
            ("assurance-graph.schema.json", graph, "assurance-graph.yaml"),
            ("decision-receipt.schema.json", decision, "decision-receipt.yaml"),
        ):
            try:
                schema = _json(root / "schemas" / schema_name)
                jsonschema.validators.validator_for(schema)(schema).validate(obj)
            except (OSError, json.JSONDecodeError, SchemaError, ValidationError) as exc:
                problems.append(f"core contract mismatch: {label}: {exc}")

    for name, record in {**records, "changed_system": changed_system}.items():
        if record.get("profile_version") != PROFILE_VERSION:
            problems.append(f"record profile_version drifted: {name}")
        if record.get("record_class") not in ALLOWED_RECORD_CLASSES:
            problems.append(f"record_class invalid: {name}")
    if any(record["record_class"] != "synthetic" for record in records.values()) or changed_system["record_class"] != "synthetic":
        problems.append("public FTQC reference records must be synthetic")

    graph_ids = {node["id"] for node in graph["nodes"]}
    node_kind = {node["id"]: node["kind"] for node in graph["nodes"]}
    system, resource = records["system"], records["resource"]
    assumption_ids = set(_assumptions(system))
    for item_id in assumption_ids:
        if item_id not in graph_ids or node_kind.get(item_id) != "assumption":
            problems.append(f"system assumption does not resolve to graph assumption: {item_id}")
    if system["decision_ref"] not in graph_ids:
        problems.append("system decision_ref does not resolve in assurance graph")
    if resource["system_ref"] != system["system_id"]:
        problems.append("resource-estimate system_ref does not match system concept")
    for ref in resource["assumption_refs"]:
        if ref not in assumption_ids:
            problems.append(f"resource-estimate assumption_ref does not resolve: {ref}")
    if resource["record_id"] not in graph_ids:
        problems.append("resource-estimate record_id does not resolve in assurance graph")

    seen: set[str] = set()
    for envelope in records["envelopes"]["envelopes"]:
        if envelope["envelope_id"] in seen:
            problems.append(f"duplicate envelope id: {envelope['envelope_id']}")
        seen.add(envelope["envelope_id"])
        if envelope["evidence_ref"] not in graph_ids:
            problems.append(f"evidence envelope ref does not resolve: {envelope['evidence_ref']}")
        for ref in envelope["basis"]["refs"]:
            if ref not in graph_ids:
                problems.append(f"envelope basis ref does not resolve: {ref}")
        if envelope["review"]["authority_state"] == "ESTABLISHED" and envelope["basis"]["type"] == "declared_assumption":
            problems.append(f"established applicability cannot rest only on declared assumption: {envelope['envelope_id']}")

    for review in records["experts"]["reviews"]:
        if review["review_id"] not in graph_ids or review["claim_ref"] not in graph_ids:
            problems.append(f"expert review graph reference does not resolve: {review['review_id']}")
        for ref in review["evidence_refs"] + review["reopen_when_refs"]:
            if ref not in graph_ids:
                problems.append(f"expert review ref does not resolve: {ref}")

    if decision["decision"]["id"] != system["decision_ref"]:
        problems.append("decision receipt does not match system decision_ref")
    for ref in decision["basis"]["node_refs"]:
        if ref not in graph_ids:
            problems.append(f"decision basis ref does not resolve: {ref}")
    if _hold_reasons(records["envelopes"]["envelopes"], records["experts"]["reviews"]) and decision["decision"]["disposition"] == "APPROVE":
        problems.append("decision cannot APPROVE with unresolved mandatory FTQC gates")
    if decision["decision"]["disposition"] != "HOLD":
        problems.append("public baseline decision must remain HOLD")
    if changed_assumptions(system, changed_system) != ["ASSUMPTION-LOSS-001"]:
        problems.append("changed-assumption reference must change exactly ASSUMPTION-LOSS-001")
    try:
        if evaluate_case(root)["change"] != expected:
            problems.append("changed-assumption expected impact drifted from evaluator")
    except (KeyError, TypeError, ValueError) as exc:
        problems.append(f"change-impact evaluation failed: {exc}")

    for path in sorted(profile.rglob("*")):
        if path.is_file() and path.suffix.lower() in {".md", ".json", ".yaml", ".yml", ".txt"}:
            text = path.read_text(encoding="utf-8")
            if URL_RE.search(text):
                problems.append(f"external URL not allowed in FTQC profile: {path.relative_to(root)}")
            if EMAIL_RE.search(text):
                problems.append(f"email address not allowed in FTQC profile: {path.relative_to(root)}")
    return problems


def _report(result: dict[str, Any]) -> str:
    base, change = result["baseline"], result["change"]
    lines = [
        "# FTQC Decision Basis — Synthetic Reference", "", "## Software / contract validation", "",
        "**PASS**", "", "## Technical decision readiness", "", f"**{base['technical_decision_readiness']}**",
        "", "### Why", "",
    ]
    lines += [f"- {item}" for item in base["hold_reasons"]]
    lines += [
        "", "## Changed-assumption demonstration", "",
        f"- Changed assumptions: {', '.join(change['changed_assumptions'])}",
        f"- Stale resource estimates: {len(change['resource_estimates_stale'])}",
        f"- Evidence outside envelope: {len(change['evidence_outside_envelope'])}",
        f"- Expert reviews to reopen: {len(change['expert_reviews_reopen'])}",
        f"- Impacted graph nodes: {len(change['impacted_nodes'])}",
        f"- Decision reopen required: {str(change['decision_reopen_required']).upper()}",
        "", "## Boundary", "", result["boundary_note"], "",
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Evaluate the synthetic FTQC Assurance reference case.")
    parser.add_argument("root", nargs="?", default=".")
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    problems = validate_profile(root)
    if problems:
        print("FTQC ASSURANCE PROFILE FAIL")
        for problem in problems:
            print(f"FAIL: {problem}")
        return 2

    result = evaluate_case(root)
    build = root / "build"
    build.mkdir(parents=True, exist_ok=True)
    (build / "ftqc-decision-basis.md").write_text(_report(result), encoding="utf-8")
    if args.as_json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        base, change = result["baseline"], result["change"]
        print("SOFTWARE / CONTRACT VALIDATION\nPASS\n")
        print(f"TECHNICAL DECISION READINESS\n{base['technical_decision_readiness']}\n")
        print("WHY")
        for reason in base["hold_reasons"]:
            print(f"- {reason}")
        print("\nCHANGE APPLIED")
        for item in change["changed_assumptions"]:
            print(f"- {item}")
        print("\nIMPACT")
        print(f"- stale resource estimates: {len(change['resource_estimates_stale'])}")
        print(f"- evidence outside envelope: {len(change['evidence_outside_envelope'])}")
        print(f"- expert reviews to reopen: {len(change['expert_reviews_reopen'])}")
        print(f"- impacted graph nodes: {len(change['impacted_nodes'])}")
        print(f"- decision reopen required: {str(change['decision_reopen_required']).upper()}\n")
        print(result["boundary_note"])
        print("RESULT - FTQC REFERENCE EVALUATION PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
