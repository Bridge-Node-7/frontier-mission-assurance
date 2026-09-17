"""Evaluate the public FTQC Assurance reference case.

This script validates declared profile contracts and demonstrates change propagation
across a synthetic FTQC decision basis. It does not validate quantum hardware,
QEC performance, resource-estimation truth, or mission readiness.
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
PUBLIC_FORBIDDEN_MARKERS = ("oratomic", "monarch quantum")
URL_RE = re.compile(r"https?://", re.IGNORECASE)
EMAIL_RE = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE)


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _load_yaml(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _assumptions(system: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {item["id"]: item for item in system.get("assumptions", [])}


def changed_assumptions(baseline: dict[str, Any], changed: dict[str, Any]) -> list[str]:
    before = _assumptions(baseline)
    after = _assumptions(changed)
    ids = set(before) | set(after)
    return sorted(
        item_id
        for item_id in ids
        if before.get(item_id, {}).get("value") != after.get(item_id, {}).get("value")
    )


def _subject_value(subject: str, system: dict[str, Any]) -> Any:
    if subject == "modality":
        return system.get("modality")
    if subject == "architecture_revision":
        return system.get("architecture_revision")
    if subject.startswith("assumption:"):
        assumption_id = subject.split(":", 1)[1]
        item = _assumptions(system).get(assumption_id)
        return None if item is None else item.get("value")
    raise ValueError(f"unsupported applicability subject: {subject}")


def _condition_matches(condition: dict[str, Any], system: dict[str, Any]) -> bool:
    actual = _subject_value(condition["subject"], system)
    operator = condition["operator"]
    expected = condition["value"]
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


def evaluate_envelope(envelope: dict[str, Any], system: dict[str, Any]) -> dict[str, Any]:
    failed = [
        condition
        for condition in envelope.get("applicability", {}).get("conditions", [])
        if not _condition_matches(condition, system)
    ]
    return {
        "envelope_id": envelope["envelope_id"],
        "evidence_ref": envelope["evidence_ref"],
        "in_scope": not failed,
        "failed_subjects": [item["subject"] for item in failed],
        "authority_state": envelope["review"]["authority_state"],
        "decision_gate": envelope["review"]["decision_gate"],
    }


def _dependency_impact(
    graph: dict[str, Any],
    seeds: set[str],
    invalid_evidence: set[str],
    reopened_reviews: set[str],
) -> set[str]:
    reverse_dependency: dict[str, set[str]] = defaultdict(set)
    support_targets: dict[str, set[str]] = defaultdict(set)
    for edge in graph.get("edges", []):
        relation = edge["relation"]
        if relation in {"depends_on", "requires"}:
            reverse_dependency[edge["to"]].add(edge["from"])
        elif relation in {"supports", "verifies", "validates"}:
            support_targets[edge["from"]].add(edge["to"])

    queue = deque(seeds)
    impacted = set(seeds)
    for evidence_id in sorted(invalid_evidence | reopened_reviews):
        for target in sorted(support_targets.get(evidence_id, set())):
            if target not in impacted:
                impacted.add(target)
                queue.append(target)
    while queue:
        current = queue.popleft()
        for dependent in sorted(reverse_dependency.get(current, set())):
            if dependent not in impacted:
                impacted.add(dependent)
                queue.append(dependent)
    return impacted


def _baseline_hold_reasons(envelopes: list[dict[str, Any]], reviews: list[dict[str, Any]]) -> list[str]:
    reasons: list[str] = []
    for envelope in envelopes:
        if not envelope["review"]["decision_gate"]:
            continue
        if envelope["review"]["status"] != "IN_SCOPE":
            reasons.append(f"{envelope['envelope_id']} is not in scope")
        if envelope["review"]["authority_state"] != "ESTABLISHED":
            reasons.append(f"{envelope['envelope_id']} applicability is declared but not established")
    for review in reviews:
        if review.get("mandatory") and review.get("conclusion") != "SUPPORTED_WITHIN_SCOPE":
            reasons.append(f"{review['review_id']} mandatory expert gate remains open")
    return reasons


def evaluate_case(root: Path) -> dict[str, Any]:
    profile = root / "profiles" / PROFILE_NAME
    baseline = profile / "examples" / "synthetic-neutral-atom" / "baseline"
    changed = profile / "examples" / "synthetic-neutral-atom" / "changed-assumption"
    baseline_system = _load_json(baseline / "system-concept.json")
    changed_system = _load_json(changed / "system-concept.json")
    resource = _load_json(baseline / "resource-estimate-receipt.json")
    envelope_set = _load_json(baseline / "evidence-envelopes.json")
    expert_set = _load_json(baseline / "expert-adjudications.json")
    graph = _load_yaml(baseline / "assurance-graph.yaml")
    decision = _load_yaml(baseline / "decision-receipt.yaml")

    changed_ids = set(changed_assumptions(baseline_system, changed_system))
    changed_envelopes = [evaluate_envelope(item, changed_system) for item in envelope_set["envelopes"]]
    stale_resources = {resource["record_id"]} if changed_ids.intersection(resource["assumption_refs"]) else set()
    outside_evidence = {item["evidence_ref"] for item in changed_envelopes if not item["in_scope"]}
    reopened_reviews = {
        item["review_id"]
        for item in expert_set["reviews"]
        if changed_ids.intersection(item.get("reopen_when_refs", []))
    }
    impacted = _dependency_impact(graph, set(changed_ids) | stale_resources, outside_evidence, reopened_reviews)
    decision_id = decision["decision"]["id"]
    decision_reopen = decision_id in impacted or bool(changed_ids or outside_evidence or reopened_reviews or stale_resources)

    return {
        "profile_version": PROFILE_VERSION,
        "baseline": {
            "software_contract_validation": "PASS",
            "technical_decision_readiness": decision["decision"]["disposition"],
            "hold_reasons": _baseline_hold_reasons(envelope_set["envelopes"], expert_set["reviews"]),
            "critical_claims": sum(1 for node in graph["nodes"] if node["kind"] == "claim" and node.get("criticality", 0) >= 4),
        },
        "change": {
            "changed_assumptions": sorted(changed_ids),
            "resource_estimates_stale": sorted(stale_resources),
            "evidence_outside_envelope": sorted(outside_evidence),
            "expert_reviews_reopen": sorted(reopened_reviews),
            "impacted_nodes": sorted(item for item in impacted if item not in changed_ids),
            "decision_reopen_required": decision_reopen,
        },
        "boundary_note": "PASS describes declared software and contract checks only; it does not establish quantum performance or mission approval.",
    }


def validate_profile(root: Path) -> list[str]:
    profile = root / "profiles" / PROFILE_NAME
    baseline = profile / "examples" / "synthetic-neutral-atom" / "baseline"
    changed = profile / "examples" / "synthetic-neutral-atom" / "changed-assumption"
    schemas_dir = profile / "schemas"
    problems: list[str] = []

    required = [
        profile / "README.md",
        profile / "ASSURANCE_SCOPE.md",
        profile / "PROFILE_CONTRACT.md",
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
    for path in required:
        if not path.is_file():
            problems.append(f"required FTQC surface missing: {path.relative_to(root)}")

    schema_files = {
        "system": schemas_dir / "ftqc-system-concept.schema.json",
        "resource": schemas_dir / "resource-estimate-receipt.schema.json",
        "envelopes": schemas_dir / "evidence-validity-envelope.schema.json",
        "experts": schemas_dir / "expert-adjudication-record.schema.json",
    }
    schemas: dict[str, dict[str, Any]] = {}
    for name, path in schema_files.items():
        try:
            schema = _load_json(path)
            schemas[name] = schema
            if schema.get("properties", {}).get("profile_version", {}).get("const") != PROFILE_VERSION:
                problems.append(f"schema profile_version drifted: {path.name}")
            if jsonschema is not None:
                jsonschema.validators.validator_for(schema).check_schema(schema)
        except (OSError, json.JSONDecodeError, SchemaError) as exc:
            problems.append(f"schema invalid: {path.name}: {exc}")

    try:
        records = {
            "system": _load_json(baseline / "system-concept.json"),
            "resource": _load_json(baseline / "resource-estimate-receipt.json"),
            "envelopes": _load_json(baseline / "evidence-envelopes.json"),
            "experts": _load_json(baseline / "expert-adjudications.json"),
        }
        changed_system = _load_json(changed / "system-concept.json")
        graph = _load_yaml(baseline / "assurance-graph.yaml")
        decision = _load_yaml(baseline / "decision-receipt.yaml")
        expected_impact = _load_json(changed / "expected-impact.json")
    except (OSError, json.JSONDecodeError, yaml.YAMLError) as exc:
        problems.append(f"reference fixture invalid: {exc}")
        return problems

    if jsonschema is not None and len(schemas) == len(schema_files):
        for name, record in records.items():
            try:
                jsonschema.validators.validator_for(schemas[name])(schemas[name]).validate(record)
            except (SchemaError, ValidationError) as exc:
                problems.append(f"example/schema mismatch: {name}: {exc}")
        try:
            jsonschema.validators.validator_for(schemas["system"])(schemas["system"]).validate(changed_system)
        except (SchemaError, ValidationError) as exc:
            problems.append(f"changed system/schema mismatch: {exc}")
        for schema_name, core_record, label in (
            ("assurance-graph.schema.json", graph, "assurance-graph.yaml"),
            ("decision-receipt.schema.json", decision, "decision-receipt.yaml"),
        ):
            try:
                core_schema = _load_json(root / "schemas" / schema_name)
                jsonschema.validators.validator_for(core_schema)(core_schema).validate(core_record)
            except (OSError, json.JSONDecodeError, SchemaError, ValidationError) as exc:
                problems.append(f"core contract mismatch: {label}: {exc}")

    for name, record in {**records, "changed_system": changed_system}.items():
        if record.get("profile_version") != PROFILE_VERSION:
            problems.append(f"record profile_version drifted: {name}")
        if record.get("record_class") not in ALLOWED_RECORD_CLASSES:
            problems.append(f"record_class invalid: {name}")
    if any(record.get("record_class") != "synthetic" for record in records.values()) or changed_system.get("record_class") != "synthetic":
        problems.append("public FTQC reference records must be synthetic")

    graph_ids = {node["id"] for node in graph.get("nodes", [])}
    node_kind = {node["id"]: node["kind"] for node in graph.get("nodes", [])}
    system = records["system"]
    assumption_ids = set(_assumptions(system))
    for assumption_id in assumption_ids:
        if assumption_id not in graph_ids or node_kind.get(assumption_id) != "assumption":
            problems.append(f"system assumption does not resolve to graph assumption: {assumption_id}")
    if system["decision_ref"] not in graph_ids:
        problems.append("system decision_ref does not resolve in assurance graph")

    resource = records["resource"]
    if resource["system_ref"] != system["system_id"]:
        problems.append("resource-estimate system_ref does not match system concept")
    for ref in resource["assumption_refs"]:
        if ref not in assumption_ids:
            problems.append(f"resource-estimate assumption_ref does not resolve: {ref}")
    if resource["record_id"] not in graph_ids:
        problems.append("resource-estimate record_id does not resolve in assurance graph")

    envelope_set = records["envelopes"]
    envelope_ids: set[str] = set()
    for envelope in envelope_set["envelopes"]:
        if envelope["envelope_id"] in envelope_ids:
            problems.append(f"duplicate envelope id: {envelope['envelope_id']}")
        envelope_ids.add(envelope["envelope_id"])
        if envelope["evidence_ref"] not in graph_ids:
            problems.append(f"evidence envelope ref does not resolve: {envelope['evidence_ref']}")
        for ref in envelope["basis"]["refs"]:
            if ref not in graph_ids:
                problems.append(f"envelope basis ref does not resolve: {ref}")
        if envelope["review"]["authority_state"] == "ESTABLISHED" and envelope["basis"]["type"] == "declared_assumption":
            problems.append(f"established applicability cannot rest only on declared assumption: {envelope['envelope_id']}")

    expert_set = records["experts"]
    for review in expert_set["reviews"]:
        if review["review_id"] not in graph_ids:
            problems.append(f"expert review does not resolve in assurance graph: {review['review_id']}")
        if review["claim_ref"] not in graph_ids:
            problems.append(f"expert claim_ref does not resolve: {review['claim_ref']}")
        for ref in review["evidence_refs"] + review.get("reopen_when_refs", []):
            if ref not in graph_ids:
                problems.append(f"expert review ref does not resolve: {ref}")

    if decision.get("decision", {}).get("id") != system["decision_ref"]:
        problems.append("decision receipt does not match system decision_ref")
    for ref in decision.get("basis", {}).get("node_refs", []):
        if ref not in graph_ids:
            problems.append(f"decision basis ref does not resolve: {ref}")
    if _baseline_hold_reasons(envelope_set["envelopes"], expert_set["reviews"]) and decision["decision"]["disposition"] == "APPROVE":
        problems.append("decision cannot APPROVE with unresolved mandatory FTQC gates")
    if decision["decision"]["disposition"] != "HOLD":
        problems.append("public baseline decision must remain HOLD")

    if changed_assumptions(system, changed_system) != ["ASSUMPTION-LOSS-001"]:
        problems.append("changed-assumption reference must change exactly ASSUMPTION-LOSS-001")
    try:
        if evaluate_case(root)["change"] != expected_impact:
            problems.append("changed-assumption expected impact drifted from evaluator")
    except (KeyError, TypeError, ValueError) as exc:
        problems.append(f"change-impact evaluation failed: {exc}")

    for path in sorted(profile.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in {".md", ".json", ".yaml", ".yml", ".txt"}:
            continue
        text = path.read_text(encoding="utf-8")
        lower = text.lower()
        if URL_RE.search(text):
            problems.append(f"external URL not allowed in FTQC profile: {path.relative_to(root)}")
        if EMAIL_RE.search(text):
            problems.append(f"email address not allowed in FTQC profile: {path.relative_to(root)}")
        for marker in PUBLIC_FORBIDDEN_MARKERS:
            if marker in lower:
                problems.append(f"customer-specific marker not allowed in FTQC profile: {path.relative_to(root)}")
    return problems


def _report_markdown(result: dict[str, Any]) -> str:
    baseline = result["baseline"]
    change = result["change"]
    lines = [
        "# FTQC Decision Basis — Synthetic Reference",
        "",
        "## Software / contract validation",
        "",
        "**PASS**",
        "",
        "## Technical decision readiness",
        "",
        f"**{baseline['technical_decision_readiness']}**",
        "",
        "### Why",
        "",
    ]
    lines.extend(f"- {item}" for item in baseline["hold_reasons"])
    lines.extend([
        "",
        "## Changed-assumption demonstration",
        "",
        f"- Changed assumptions: {', '.join(change['changed_assumptions'])}",
        f"- Stale resource estimates: {len(change['resource_estimates_stale'])}",
        f"- Evidence outside envelope: {len(change['evidence_outside_envelope'])}",
        f"- Expert reviews to reopen: {len(change['expert_reviews_reopen'])}",
        f"- Impacted graph nodes: {len(change['impacted_nodes'])}",
        f"- Decision reopen required: {str(change['decision_reopen_required']).upper()}",
        "",
        "## Boundary",
        "",
        result["boundary_note"],
        "",
    ])
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
    (build / "ftqc-decision-basis.md").write_text(_report_markdown(result), encoding="utf-8")

    if args.as_json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        baseline = result["baseline"]
        change = result["change"]
        print("SOFTWARE / CONTRACT VALIDATION")
        print("PASS")
        print()
        print("TECHNICAL DECISION READINESS")
        print(baseline["technical_decision_readiness"])
        print()
        print("WHY")
        for reason in baseline["hold_reasons"]:
            print(f"- {reason}")
        print()
        print("CHANGE APPLIED")
        for item in change["changed_assumptions"]:
            print(f"- {item}")
        print()
        print("IMPACT")
        print(f"- stale resource estimates: {len(change['resource_estimates_stale'])}")
        print(f"- evidence outside envelope: {len(change['evidence_outside_envelope'])}")
        print(f"- expert reviews to reopen: {len(change['expert_reviews_reopen'])}")
        print(f"- impacted graph nodes: {len(change['impacted_nodes'])}")
        print(f"- decision reopen required: {str(change['decision_reopen_required']).upper()}")
        print()
        print(result["boundary_note"])
        print("RESULT - FTQC REFERENCE EVALUATION PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
