"""Deterministic, source-neutral experimental harness for orbital logistics assurance.

This experiment prepares review state only. It does not authorize operations, command
spacecraft, qualify hardware, certify safety, authenticate source systems, or create a
new canonical authority. Records remain illustrative inputs owned by their governing
systems.
"""
from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

HOLD = "HOLD_FAIL_CLOSED"
ELIGIBLE = "ELIGIBLE_FOR_HUMAN_REVIEW"
READY = "READY_FOR_HUMAN_REVIEW"
READY_FOR_REQUALIFICATION = "READY_FOR_REQUALIFICATION_REVIEW"
ALLOWED_PHASES = {"pre_service", "post_service", "requalification_review"}
PUBLIC_RECORD_CLASSES = frozenset({"synthetic", "sanitized"})
PRIVATE_RECORD_CLASSES = frozenset({"private"})

SUPPORTED_MODEL_STATES = {"ESTABLISHED", "SUPPORTED"}
SUPPORTED_FITNESS_STATES = {"VERIFIED", "SUPPORTED"}


@dataclass(frozen=True)
class Finding:
    code: str
    message: str
    proof_needed: str | None = None


def _is_nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _proof_candidates(findings: list[Finding]) -> list[dict[str, str]]:
    candidates: list[dict[str, str]] = []
    seen: set[tuple[str, str]] = set()
    for finding in findings:
        if finding.proof_needed:
            key = (finding.code, finding.proof_needed)
            if key not in seen:
                seen.add(key)
                candidates.append({
                    "source_finding": finding.code,
                    "needed": finding.proof_needed,
                    "ownership_note": (
                        "Candidate only; Mission Graph owns governed ProofRequests."
                    ),
                })
    return candidates


def evaluate(
    case: dict[str, Any],
    allowed_record_classes: set[str] | frozenset[str] = PUBLIC_RECORD_CLASSES,
) -> dict[str, Any]:
    """Evaluate one synthetic logistics case without granting consequential authority."""
    findings: list[Finding] = []

    if not isinstance(case, dict):
        case = {}
        findings.append(Finding("CASE_INPUT_INVALID", "case input must be a JSON object"))

    record_class = case.get("record_class")
    if record_class not in allowed_record_classes:
        findings.append(Finding(
            "PUBLIC_RECORD_CLASS_INVALID",
            "record_class is not permitted for this evaluation mode",
            "Use only the record classes permitted by the selected public or governed path.",
        ))

    case_id = case.get("case_id")
    if not _is_nonempty_string(case_id):
        findings.append(Finding("CASE_ID_MISSING", "case_id is required"))

    phase = case.get("phase")
    if phase not in ALLOWED_PHASES:
        findings.append(Finding(
            "PHASE_INVALID",
            "phase must be one of pre_service, post_service, or requalification_review",
            "Declare a supported lifecycle phase before evaluating the case.",
        ))

    assessment = case.get("pre_service_assessment") or {}
    if assessment.get("disposition") != "ELIGIBLE_FOR_DECISION_PREPARATION":
        findings.append(Finding(
            "PRE_SERVICE_ASSESSMENT_NOT_ELIGIBLE",
            "pre-service assessment must be eligible for decision preparation",
            "Resolve the pre-service assessment blockers under the governing mission process.",
        ))
    option_name = assessment.get("service_option")
    eligible_options = set(_list(assessment.get("eligible_options")))
    if not _is_nonempty_string(option_name) or option_name not in eligible_options:
        findings.append(Finding(
            "SERVICE_OPTION_NOT_ELIGIBLE",
            "the serviced option must be explicitly present in eligible_options",
            "Establish a supported eligible service option before execution.",
        ))

    pre_evidence = set(_list(case.get("pre_service_evidence_ids")))
    authority_refs = set(_list(case.get("authority_evidence_refs")))
    if not authority_refs:
        findings.append(Finding(
            "AUTHORITY_EVIDENCE_MISSING",
            "pre-service authority evidence is required",
            "Provide applicable authority evidence that existed before the service action.",
        ))
    elif not authority_refs.issubset(pre_evidence):
        findings.append(Finding(
            "AUTHORITY_NOT_PRE_SERVICE",
            "authority evidence must resolve in the pre-service evidence set",
            "Establish applicable authority before action; post-action evidence cannot "
            "create it retroactively.",
        ))

    interfaces = _list(case.get("interfaces"))
    if not interfaces:
        findings.append(Finding(
            "INTERFACE_BASIS_MISSING",
            "at least one material interface record is required",
            "Establish configuration-specific interface compatibility evidence.",
        ))
    for row in interfaces:
        iid = (
            row.get("interface_id", "UNKNOWN_INTERFACE")
            if isinstance(row, dict)
            else "UNKNOWN_INTERFACE"
        )
        if (
            not isinstance(row, dict)
            or row.get("state") != "COMPATIBLE"
            or _list(row.get("blockers"))
        ):
            findings.append(Finding(
                "INTERFACE_NOT_COMPATIBLE",
                f"interface {iid} is not demonstrably compatible without blockers",
                f"Establish configuration-specific compatibility for {iid}.",
            ))

    resources = _list(case.get("resources"))
    for row in resources:
        rid = (
            row.get("resource_id", "UNKNOWN_RESOURCE")
            if isinstance(row, dict)
            else "UNKNOWN_RESOURCE"
        )
        if not isinstance(row, dict) or row.get("presence") != "PRESENT":
            findings.append(Finding(
                "RESOURCE_NOT_PRESENT",
                f"resource {rid} is not established as present",
                f"Establish authoritative presence for {rid}.",
            ))
            continue
        if row.get("fitness") not in SUPPORTED_FITNESS_STATES:
            findings.append(Finding(
                "RESOURCE_FITNESS_UNSUPPORTED",
                f"resource {rid} fitness is not verified/supported",
                f"Establish fit-for-purpose evidence for {rid}.",
            ))
        if row.get("release_state") != "AUTHORIZED":
            findings.append(Finding(
                "RESOURCE_RELEASE_UNAUTHORIZED",
                f"resource {rid} is not authorized for release",
                f"Obtain release authority for {rid} through the governing system.",
            ))

    models = _list(case.get("models"))
    for row in models:
        mid = (
            row.get("model_id", "UNKNOWN_MODEL")
            if isinstance(row, dict)
            else "UNKNOWN_MODEL"
        )
        if (
            not isinstance(row, dict)
            or row.get("applicability") not in SUPPORTED_MODEL_STATES
        ):
            findings.append(Finding(
                "MODEL_APPLICABILITY_UNSUPPORTED",
                f"model {mid} is not established/supported for this decision use",
                f"Establish current applicability evidence for {mid} or remove it from "
                "the decision basis.",
            ))
        if isinstance(row, dict) and _list(row.get("blockers")):
            findings.append(Finding(
                "MODEL_BLOCKED",
                f"model {mid} has unresolved applicability blockers",
                f"Resolve or bound the applicability blockers for {mid}.",
            ))

    pre_service_blockers = list(findings)
    service = case.get("service") or {}

    if phase in {"post_service", "requalification_review"}:
        if service.get("execution_state") != "EXECUTED":
            findings.append(Finding(
                "SERVICE_NOT_EXECUTED",
                "post-service review requires an executed service record",
                "Provide execution evidence from the authoritative service system.",
            ))
        if service.get("verification_state") != "SUPPORTED":
            findings.append(Finding(
                "SERVICE_VERIFICATION_UNSUPPORTED",
                "service verification must be supported",
                "Acquire post-service verification evidence.",
            ))
        post_ids = set(_list(case.get("post_service_evidence_ids")))
        if not post_ids:
            findings.append(Finding(
                "POST_SERVICE_EVIDENCE_MISSING",
                "post-service evidence is required",
                "Acquire post-service evidence before requalification review.",
            ))
    if phase == "requalification_review":
        requal = case.get("requalification") or {}
        if requal.get("review_state") != READY:
            findings.append(Finding(
                "REQUALIFICATION_NOT_READY",
                "service completion does not establish mission requalification",
                "Satisfy the declared post-service requirements and obtain "
                "requalification review state.",
            ))

    if pre_service_blockers:
        disposition = HOLD
    elif phase == "pre_service":
        disposition = ELIGIBLE
    elif findings:
        disposition = HOLD
    elif phase == "post_service":
        disposition = READY_FOR_REQUALIFICATION
    elif phase == "requalification_review":
        disposition = READY
    else:
        disposition = HOLD

    proof_candidates = _proof_candidates(findings)

    return {
        "case_id": case_id,
        "phase": phase,
        "disposition": disposition,
        "findings": [finding.__dict__ for finding in findings],
        "proof_request_candidates": proof_candidates,
        "authority_note": (
            "Experimental decision-preparation output only. This result does not authorize, "
            "approve, certify, qualify, command, or record a consequential mission decision."
        ),
        "invariants": {
            "post_action_evidence_cannot_create_pre_action_authority": True,
            "service_completion_does_not_equal_mission_requalification": True,
            "machine_output_does_not_equal_operational_authority": True,
        },
    }


def evaluate_bound_case(
    case: dict[str, Any],
    evidence_record: dict[str, Any],
    option_assessment: dict[str, Any],
    post_evidence_record: dict[str, Any] | None = None,
    requalification_record: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Bind service assurance to governed Orbital Recovery records.

    The supplied records remain authoritative under their existing profile contracts.
    This function projects only the minimum fields needed by the service experiment and
    fails closed when references do not resolve exactly.
    """
    linkage_findings: list[Finding] = []

    if not isinstance(case, dict):
        case = {}
        linkage_findings.append(Finding(
            "BOUND_CASE_INPUT_INVALID",
            "bound service case must be a JSON object",
        ))
    if not isinstance(evidence_record, dict):
        evidence_record = {}
        linkage_findings.append(Finding(
            "UPSTREAM_EVIDENCE_RECORD_INVALID",
            "pre-service evidence record must be a JSON object",
        ))
    if not isinstance(option_assessment, dict):
        option_assessment = {}
        linkage_findings.append(Finding(
            "UPSTREAM_ASSESSMENT_INVALID",
            "pre-service option assessment must be a JSON object",
        ))

    record_class = case.get("record_class")
    allowed_record_classes = (
        PRIVATE_RECORD_CLASSES if record_class == "private" else PUBLIC_RECORD_CLASSES
    )

    for label, record in (
        ("pre-service evidence", evidence_record),
        ("pre-service assessment", option_assessment),
    ):
        if record and record.get("record_class") != record_class:
            linkage_findings.append(Finding(
                "BOUND_RECORD_CLASS_MISMATCH",
                f"{label} record_class does not match the service case",
            ))

    declared_assessment = case.get("pre_service_assessment") or {}
    assessment_id = option_assessment.get("assessment_id")
    evidence_record_id = evidence_record.get("record_id")

    if declared_assessment.get("assessment_id") != assessment_id:
        linkage_findings.append(Finding(
            "UPSTREAM_ASSESSMENT_BINDING_MISMATCH",
            "service case assessment_id does not match the governed option assessment",
            "Bind the service case to the exact governed pre-service assessment.",
        ))
    if declared_assessment.get("evidence_record_ref") != evidence_record_id:
        linkage_findings.append(Finding(
            "UPSTREAM_EVIDENCE_BINDING_MISMATCH",
            "service case evidence_record_ref does not match the governed evidence record",
            "Bind the service case to the exact governed pre-service evidence record.",
        ))
    if option_assessment.get("evidence_record_ref") != evidence_record_id:
        linkage_findings.append(Finding(
            "UPSTREAM_ASSESSMENT_EVIDENCE_MISMATCH",
            "governed option assessment does not reference the supplied evidence record",
            "Resolve the assessment/evidence-record binding before service review.",
        ))
    if (
        evidence_record.get("asset_id")
        and option_assessment.get("asset_id")
        and evidence_record.get("asset_id") != option_assessment.get("asset_id")
    ):
        linkage_findings.append(Finding(
            "UPSTREAM_ASSET_MISMATCH",
            "pre-service evidence and option assessment refer to different assets",
            "Resolve the governed asset binding before service review.",
        ))

    linked_case = dict(case)
    linked_case["pre_service_assessment"] = {
        "disposition": option_assessment.get("disposition"),
        "service_option": declared_assessment.get("service_option"),
        "eligible_options": option_assessment.get("eligible_options", []),
    }
    linked_case["pre_service_evidence_ids"] = [
        row.get("id")
        for row in _list(evidence_record.get("evidence"))
        if isinstance(row, dict) and _is_nonempty_string(row.get("id"))
    ]

    phase = case.get("phase")
    if phase in {"post_service", "requalification_review"}:
        if not isinstance(post_evidence_record, dict):
            post_evidence_record = {}
            linkage_findings.append(Finding(
                "POST_SERVICE_EVIDENCE_RECORD_MISSING",
                "a governed post-service evidence record is required",
                "Provide the governed post-service evidence record before review.",
            ))
        elif post_evidence_record.get("record_class") != record_class:
            linkage_findings.append(Finding(
                "BOUND_RECORD_CLASS_MISMATCH",
                "post-service evidence record_class does not match the service case",
            ))

        if (
            case.get("post_service_evidence_record_ref")
            != post_evidence_record.get("record_id")
        ):
            linkage_findings.append(Finding(
                "POST_SERVICE_EVIDENCE_BINDING_MISMATCH",
                "service case post-service reference does not match the governed record",
                "Bind the service case to the exact governed post-service evidence record.",
            ))
        if (
            evidence_record.get("asset_id")
            and post_evidence_record.get("asset_id")
            and evidence_record.get("asset_id") != post_evidence_record.get("asset_id")
        ):
            linkage_findings.append(Finding(
                "POST_SERVICE_ASSET_MISMATCH",
                "pre-service and post-service evidence refer to different assets",
                "Resolve the governed asset binding before post-service review.",
            ))
        linked_case["post_service_evidence_ids"] = [
            row.get("id")
            for row in _list(post_evidence_record.get("evidence"))
            if isinstance(row, dict) and _is_nonempty_string(row.get("id"))
        ]

    if phase == "requalification_review":
        if not isinstance(requalification_record, dict):
            requalification_record = {}
            linkage_findings.append(Finding(
                "REQUALIFICATION_RECORD_MISSING",
                "a governed requalification record is required",
                "Provide the governed requalification record before review.",
            ))
        elif requalification_record.get("record_class") != record_class:
            linkage_findings.append(Finding(
                "BOUND_RECORD_CLASS_MISMATCH",
                "requalification record_class does not match the service case",
            ))

        declared_requalification = case.get("requalification") or {}
        if (
            declared_requalification.get("requalification_id")
            != requalification_record.get("requalification_id")
        ):
            linkage_findings.append(Finding(
                "REQUALIFICATION_BINDING_MISMATCH",
                "service case requalification_id does not match the governed record",
                "Bind the service case to the exact governed requalification record.",
            ))
        if (
            isinstance(post_evidence_record, dict)
            and requalification_record.get("evidence_record_ref")
            != post_evidence_record.get("record_id")
        ):
            linkage_findings.append(Finding(
                "REQUALIFICATION_EVIDENCE_MISMATCH",
                "requalification record does not reference the supplied post-service evidence",
                "Resolve the requalification/evidence-record binding before review.",
            ))
        linked_case["requalification"] = {
            "review_state": requalification_record.get("review_state")
        }

    result = evaluate(
        linked_case,
        allowed_record_classes=allowed_record_classes,
    )
    if linkage_findings:
        result["findings"] = [
            finding.__dict__ for finding in linkage_findings
        ] + result["findings"]
        result["proof_request_candidates"] = (
            _proof_candidates(linkage_findings)
            + result["proof_request_candidates"]
        )
        result["disposition"] = HOLD

    result["binding_note"] = (
        "Bound evaluation reuses governed Orbital Recovery records; "
        "it does not duplicate or supersede their authority."
    )
    result["bound_records"] = {
        "pre_service_assessment": option_assessment.get("assessment_id"),
        "pre_service_evidence": evidence_record.get("record_id"),
        "post_service_evidence": (
            post_evidence_record.get("record_id")
            if isinstance(post_evidence_record, dict)
            else None
        ),
        "requalification": (
            requalification_record.get("requalification_id")
            if isinstance(requalification_record, dict)
            else None
        ),
    }
    return result


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: assurance_harness.py CASE.json", file=sys.stderr)
        return 2
    path = Path(argv[1])
    try:
        case = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        print("invalid case input", file=sys.stderr)
        return 2
    result = evaluate(case)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["disposition"] != HOLD else 3


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
