"""Validate and summarize one governed FTQC Assurance case directory.

This tool validates portable FTQC profile records without assuming the case is the
bundled public synthetic reference. It does not establish quantum truth, resource-
estimator correctness, hardware performance, independent V&V, or decision authority.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator

from frontier_assurance.decision import verify_decision
from frontier_assurance.validate import validate_graph

PROFILE_VERSION = "0.2"
REQUIRED_FILES = {
    "system": "system-concept.json",
    "resource": "resource-estimate-receipt.json",
    "envelopes": "evidence-envelopes.json",
    "experts": "expert-adjudications.json",
    "graph": "assurance-graph.yaml",
    "decision": "decision-receipt.yaml",
}
SCHEMAS = {
    "system": "ftqc-system-concept.schema.json",
    "resource": "resource-estimate-receipt.schema.json",
    "envelopes": "evidence-validity-envelope.schema.json",
    "experts": "expert-adjudication-record.schema.json",
}
ALLOWED_RECORD_CLASSES = {"synthetic", "private"}


def _json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError(f"{path}: document must be an object")
    return value


def _yaml(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError(f"{path}: document must be a mapping")
    return value


def _schema(root: Path, name: str) -> dict[str, Any]:
    return _json(root / "profiles" / "ftqc-assurance" / "schemas" / name)


def _hold_reasons(envelopes: dict[str, Any], experts: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    for envelope in envelopes.get("envelopes", []):
        review = envelope.get("review", {})
        if review.get("decision_gate") and review.get("status") != "IN_SCOPE":
            reasons.append(f"{envelope.get('envelope_id')} is not in scope")
        if review.get("decision_gate") and review.get("authority_state") != "ESTABLISHED":
            reasons.append(
                f"{envelope.get('envelope_id')} applicability is declared but not established"
            )
    for review in experts.get("reviews", []):
        if review.get("mandatory") and review.get("conclusion") != "SUPPORTED_WITHIN_SCOPE":
            reasons.append(f"{review.get('review_id')} mandatory expert gate remains open")
    return reasons


def validate_case(root: Path, case_dir: Path) -> tuple[list[str], list[str], dict[str, Any]]:
    errors: list[str] = []
    warnings: list[str] = []
    docs: dict[str, Any] = {}

    for key, filename in REQUIRED_FILES.items():
        path = case_dir / filename
        if not path.is_file():
            errors.append(f"missing required case file: {filename}")
            continue
        try:
            docs[key] = _yaml(path) if path.suffix in {".yaml", ".yml"} else _json(path)
        except (OSError, UnicodeError, json.JSONDecodeError, yaml.YAMLError, TypeError) as exc:
            errors.append(f"{filename}: {exc}")

    if errors:
        return errors, warnings, docs

    for key, schema_name in SCHEMAS.items():
        try:
            schema = _schema(root, schema_name)
            Draft202012Validator.check_schema(schema)
            validator = Draft202012Validator(schema)
            for error in sorted(
                validator.iter_errors(docs[key]), key=lambda item: list(item.path)
            ):
                location = ".".join(str(part) for part in error.path) or "<root>"
                errors.append(
                    f"{REQUIRED_FILES[key]}:{location}: {error.message}"
                )
        except (OSError, UnicodeError, json.JSONDecodeError, TypeError) as exc:
            errors.append(f"{schema_name}: {exc}")

    if errors:
        return errors, warnings, docs

    records = [docs["system"], docs["resource"], docs["envelopes"], docs["experts"]]
    record_classes = {item.get("record_class") for item in records}
    if len(record_classes) != 1:
        errors.append("FTQC case records must use one consistent record_class")
    case_class = next(iter(record_classes), None)
    if case_class not in ALLOWED_RECORD_CLASSES:
        errors.append(f"unsupported record_class: {case_class!r}")
    if any(item.get("profile_version") != PROFILE_VERSION for item in records):
        errors.append(f"all FTQC records must use profile_version {PROFILE_VERSION}")

    graph = docs["graph"]
    graph_validation = validate_graph(graph)
    errors.extend(f"assurance-graph.yaml: {item}" for item in graph_validation.errors)
    warnings.extend(f"assurance-graph.yaml: {item}" for item in graph_validation.warnings)

    metadata = graph.get("metadata")
    if not isinstance(metadata, dict):
        errors.append("assurance-graph.yaml: metadata must be a mapping")
        metadata = {}
    if metadata.get("profile") != "ftqc-assurance":
        errors.append("assurance-graph.yaml: metadata.profile must be ftqc-assurance")
    if str(metadata.get("profile_version")) != PROFILE_VERSION:
        errors.append(
            f"assurance-graph.yaml: metadata.profile_version must be {PROFILE_VERSION}"
        )
    if metadata.get("record_class") != case_class:
        errors.append("assurance-graph.yaml: metadata.record_class must match case records")

    node_ids = {
        node.get("id")
        for node in graph.get("nodes", [])
        if isinstance(node, dict) and isinstance(node.get("id"), str)
    }
    node_kinds = {
        node.get("id"): node.get("kind")
        for node in graph.get("nodes", [])
        if isinstance(node, dict) and isinstance(node.get("id"), str)
    }

    system = docs["system"]
    resource = docs["resource"]
    envelopes = docs["envelopes"]
    experts = docs["experts"]
    decision = docs["decision"]

    assumption_ids = {
        item.get("id")
        for item in system.get("assumptions", [])
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }
    for ref in assumption_ids:
        if ref not in node_ids or node_kinds.get(ref) != "assumption":
            errors.append(f"system assumption does not resolve to graph assumption: {ref}")

    if system.get("decision_ref") not in node_ids:
        errors.append("system decision_ref does not resolve in assurance graph")
    elif node_kinds.get(system.get("decision_ref")) != "decision":
        errors.append("system decision_ref must resolve to a decision node")

    if resource.get("system_ref") != system.get("system_id"):
        errors.append("resource-estimate system_ref does not match system concept")
    if resource.get("problem", {}).get("workload_ref") != system.get("workload", {}).get("id"):
        errors.append("resource-estimate workload_ref does not match system workload")
    for ref in resource.get("assumption_refs", []):
        if ref not in assumption_ids:
            errors.append(f"resource-estimate assumption_ref does not resolve: {ref}")
    if resource.get("record_id") not in node_ids:
        errors.append("resource-estimate record_id does not resolve in assurance graph")

    if case_class == "synthetic" and resource.get("result", {}).get("synthetic_only") is not True:
        errors.append("synthetic FTQC cases must declare result.synthetic_only=true")

    envelope_ids: set[str] = set()
    for envelope in envelopes.get("envelopes", []):
        envelope_id = envelope.get("envelope_id")
        if envelope_id in envelope_ids:
            errors.append(f"duplicate envelope id: {envelope_id}")
        if isinstance(envelope_id, str):
            envelope_ids.add(envelope_id)

        evidence_ref = envelope.get("evidence_ref")
        if evidence_ref not in node_ids:
            errors.append(f"evidence envelope ref does not resolve: {evidence_ref}")
        basis = envelope.get("basis", {})
        for ref in basis.get("refs", []):
            if ref not in node_ids:
                errors.append(f"envelope basis ref does not resolve: {ref}")
        review = envelope.get("review", {})
        if (
            review.get("authority_state") == "ESTABLISHED"
            and basis.get("type") == "declared_assumption"
        ):
            errors.append(
                f"established applicability cannot rest only on declared assumption: {envelope_id}"
            )

    if resource.get("applicability_envelope_ref") not in envelope_ids:
        errors.append("resource-estimate applicability_envelope_ref does not resolve")

    for review in experts.get("reviews", []):
        review_id = review.get("review_id")
        claim_ref = review.get("claim_ref")
        if review_id not in node_ids:
            errors.append(f"expert review does not resolve in assurance graph: {review_id}")
        if claim_ref not in node_ids or node_kinds.get(claim_ref) != "claim":
            errors.append(f"expert review claim_ref does not resolve to graph claim: {claim_ref}")
        for ref in list(review.get("evidence_refs", [])) + list(
            review.get("reopen_when_refs", [])
        ):
            if ref not in node_ids:
                errors.append(f"expert review ref does not resolve: {ref}")

    decision_doc = decision.get("decision", {})
    if decision_doc.get("id") != system.get("decision_ref"):
        errors.append("decision receipt does not match system decision_ref")
    basis = decision.get("basis", {})
    for ref in basis.get("node_refs", []):
        if ref not in node_ids:
            errors.append(f"decision basis ref does not resolve: {ref}")

    decision_result = verify_decision(
        case_dir / REQUIRED_FILES["graph"], case_dir / REQUIRED_FILES["decision"]
    )
    errors.extend(f"decision-receipt.yaml: {item}" for item in decision_result.errors)

    hold_reasons = _hold_reasons(envelopes, experts)
    if hold_reasons and decision_doc.get("disposition") == "APPROVE":
        errors.append(
            "decision cannot APPROVE while mandatory FTQC applicability/expert gates remain open"
        )

    return errors, warnings, docs


def case_summary(docs: dict[str, Any]) -> dict[str, Any]:
    system = docs["system"]
    resource = docs["resource"]
    envelopes = docs["envelopes"]
    experts = docs["experts"]
    decision = docs["decision"]["decision"]
    hold_reasons = _hold_reasons(envelopes, experts)
    return {
        "profile_version": PROFILE_VERSION,
        "record_class": system["record_class"],
        "system_id": system["system_id"],
        "modality": system["modality"],
        "architecture_revision": system["architecture_revision"],
        "mission_objective": system["mission_objective"],
        "workload": system["workload"],
        "decision": {
            "id": decision["id"],
            "disposition": decision["disposition"],
            "rationale": decision["rationale"],
            "reopen_when": decision["reopen_when"],
        },
        "assumptions": system["assumptions"],
        "resource_estimate": {
            "record_id": resource["record_id"],
            "review_state": resource["review_state"],
            "synthetic_only": resource["result"]["synthetic_only"],
            "physical_qubits": resource["result"]["physical_qubits"],
            "runtime_seconds": resource["result"]["runtime_seconds"],
            "provenance_status": resource["provenance"]["status"],
            "applicability_envelope_ref": resource["applicability_envelope_ref"],
        },
        "evidence_envelopes": [
            {
                "envelope_id": item["envelope_id"],
                "evidence_ref": item["evidence_ref"],
                "evidence_class": item["evidence_class"],
                "status": item["review"]["status"],
                "authority_state": item["review"]["authority_state"],
                "decision_gate": item["review"]["decision_gate"],
            }
            for item in envelopes["envelopes"]
        ],
        "expert_reviews": [
            {
                "review_id": item["review_id"],
                "review_class": item["review_class"],
                "mandatory": item["mandatory"],
                "conclusion": item["conclusion"],
                "question": item["question"],
            }
            for item in experts["reviews"]
        ],
        "hold_reasons": hold_reasons,
    }


def render_report(summary: dict[str, Any], warnings: list[str]) -> str:
    decision = summary["decision"]
    resource = summary["resource_estimate"]
    lines = [
        "# FTQC Decision Basis",
        "",
        "## Decision",
        "",
        f"- Decision: `{decision['id']}`",
        f"- Disposition: **{decision['disposition']}**",
        f"- Accountable rationale: {decision['rationale']}",
        "",
        "## System under review",
        "",
        f"- System: `{summary['system_id']}`",
        f"- Modality: {summary['modality']}",
        f"- Architecture revision: {summary['architecture_revision']}",
        f"- Mission objective: {summary['mission_objective']}",
        f"- Workload: {summary['workload']['id']} — {summary['workload']['description']}",
        "",
        "## Resource estimate",
        "",
        f"- Receipt: `{resource['record_id']}`",
        f"- Review state: **{resource['review_state']}**",
        f"- Synthetic only: **{str(resource['synthetic_only']).upper()}**",
        f"- Physical qubits: {resource['physical_qubits']}",
        f"- Runtime seconds: {resource['runtime_seconds']}",
        f"- Provenance: {resource['provenance_status']}",
        f"- Applicability envelope: `{resource['applicability_envelope_ref']}`",
        "",
        "## Assumptions",
        "",
    ]
    for item in summary["assumptions"]:
        lines.append(
            f"- `{item['id']}` — {item['name']}: {item['value']} "
            f"({item['status']})"
        )

    lines += ["", "## Evidence validity envelopes", ""]
    for item in summary["evidence_envelopes"]:
        lines.append(
            f"- `{item['envelope_id']}` / `{item['evidence_ref']}` — "
            f"{item['status']}; authority={item['authority_state']}; "
            f"decision_gate={str(item['decision_gate']).upper()}"
        )

    lines += ["", "## Expert review gates", ""]
    for item in summary["expert_reviews"]:
        lines.append(
            f"- `{item['review_id']}` — {item['conclusion']} "
            f"({item['review_class']}; mandatory={str(item['mandatory']).upper()}): "
            f"{item['question']}"
        )

    lines += ["", "## Reopen conditions", ""]
    lines.extend(f"- {item}" for item in decision["reopen_when"])

    lines += ["", "## Current gate", ""]
    if summary["hold_reasons"]:
        lines.append("The declared FTQC contracts contain unresolved decision gates:")
        lines.extend(f"- {item}" for item in summary["hold_reasons"])
    else:
        lines.append(
            "No unresolved FTQC applicability/expert gate is declared by these records. "
            "This does not establish scientific validity or mission readiness."
        )

    if warnings:
        lines += ["", "## Graph warnings", ""]
        lines.extend(f"- {item}" for item in warnings)

    lines += [
        "",
        "## Assurance boundary",
        "",
        (
            "This report validates declared FTQC profile structure, cross-record references, "
            "bounded applicability/review state, and decision-basis linkage. It does not "
            "establish quantum performance, QEC/decoder correctness, resource-estimator "
            "correctness, hardware validity, independent V&V, government readiness, or "
            "authorization for a consequential decision."
        ),
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate one FTQC Assurance case directory against profile contract 0.2."
    )
    parser.add_argument("case_dir", help="Directory containing the six governed FTQC case files.")
    parser.add_argument(
        "--root",
        default=str(Path(__file__).resolve().parents[1]),
        help="FMA source root containing the FTQC profile schemas.",
    )
    parser.add_argument("--report", help="Optional path for a human-readable Markdown report.")
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    case_dir = Path(args.case_dir).resolve()
    errors, warnings, docs = validate_case(root, case_dir)
    if errors:
        if args.as_json:
            print(json.dumps({"status": "FAIL", "errors": errors, "warnings": warnings}, indent=2))
        else:
            print("FTQC CASE FAIL")
            for error in errors:
                print(f"FAIL: {error}")
            for warning in warnings:
                print(f"WARN: {warning}")
        return 2

    summary = case_summary(docs)
    if args.report:
        out = Path(args.report)
        if not out.is_absolute():
            out = Path.cwd() / out
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(render_report(summary, warnings), encoding="utf-8")

    if args.as_json:
        print(
            json.dumps(
                {"status": "PASS", "warnings": warnings, "summary": summary},
                indent=2,
                sort_keys=True,
            )
        )
    else:
        print("FTQC CASE PASS")
        print(f"PROFILE: {PROFILE_VERSION}")
        print(f"RECORD CLASS: {summary['record_class']}")
        print(f"DECISION: {summary['decision']['id']} -> {summary['decision']['disposition']}")
        print(
            "RESOURCE ESTIMATE: "
            f"{summary['resource_estimate']['record_id']} "
            f"({summary['resource_estimate']['review_state']})"
        )
        print(f"OPEN FTQC GATES: {len(summary['hold_reasons'])}")
        for warning in warnings:
            print(f"WARN: {warning}")
        if args.report:
            print(f"WROTE: {Path(args.report)}")
        print(
            "NOTE: PASS validates declared FTQC contracts and cross-record linkage only; "
            "quantum truth and consequential authority remain external."
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
