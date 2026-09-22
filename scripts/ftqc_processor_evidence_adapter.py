"""Fail-closed adapter for bounded FTQC technical evidence.

This source-profile adapter consumes one ExperimentResult and one linked
ProcessorEvidenceReceipt without importing either producer implementation.
The exact portable schemas remain owned by the producing domain system; callers
supply those schema files and FMA verifies their exact reviewed SHA-256 values
before validation.

The adapter does not establish scientific truth, hardware validity, independent
V&V, mission readiness, certification, or consequential decision authority.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

EXPERIMENT_CONTRACT_ID = "na-ftqc.experiment-result"
EXPERIMENT_CONTRACT_VERSION = "2.0.0"
EXPERIMENT_SCHEMA_SHA256 = "923f28bd45729008f54eea09281caacf359311f9a7e0486344d41a336a4c3c33"

PROCESSOR_CONTRACT_ID = "na-ftqc.processor-evidence-receipt"
PROCESSOR_CONTRACT_VERSION = "2.0.0"
PROCESSOR_SCHEMA_SHA256 = "1e8c164ddabbf1f6a1f0274e3b3225ec2ba81a1a566a33d69d00b91e1788ccdb"

ROOT = Path(__file__).resolve().parents[1]
REVIEWED_PRODUCERS_PATH = (
    ROOT / "profiles" / "ftqc-assurance" / "compatibility" / "reviewed-producers.json"
)


def _load_reviewed_producers(path: Path = REVIEWED_PRODUCERS_PATH) -> tuple[dict[str, set[str]], dict[str, set[str]]]:
    try:
        registry = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"reviewed FTQC producer registry is unavailable or invalid: {exc}") from exc
    if not isinstance(registry, dict):
        raise RuntimeError("reviewed FTQC producer registry must be a JSON object")
    if registry.get("format") != "bn7.fma.ftqc-reviewed-producers/0.1":
        raise RuntimeError("unsupported reviewed FTQC producer registry format")
    if registry.get("authority") != "HUMAN_REVIEW_REQUIRED_FOR_CHANGES":
        raise RuntimeError("reviewed FTQC producer registry authority boundary is invalid")
    reviewed = registry.get("reviewed")
    if not isinstance(reviewed, list):
        raise RuntimeError("reviewed FTQC producer registry entries must be an array")

    expected = {
        "ExperimentResult": (
            EXPERIMENT_CONTRACT_ID,
            EXPERIMENT_CONTRACT_VERSION,
            EXPERIMENT_SCHEMA_SHA256,
        ),
        "ProcessorEvidenceReceipt": (
            PROCESSOR_CONTRACT_ID,
            PROCESSOR_CONTRACT_VERSION,
            PROCESSOR_SCHEMA_SHA256,
        ),
    }
    by_artifact: dict[str, dict[str, set[str]]] = {}
    for entry in reviewed:
        if not isinstance(entry, dict):
            raise RuntimeError("reviewed FTQC producer entry must be an object")
        artifact = entry.get("artifact")
        if artifact not in expected or artifact in by_artifact:
            raise RuntimeError("reviewed FTQC producer registry has an unsupported or duplicate artifact entry")
        contract_id, contract_version, schema_sha256 = expected[artifact]
        if (
            entry.get("contract_id") != contract_id
            or entry.get("contract_version") != contract_version
            or entry.get("schema_sha256") != schema_sha256
        ):
            raise RuntimeError(f"{artifact} registry contract identity does not match the reviewed adapter contract")
        application = entry.get("application")
        releases = entry.get("releases")
        if not isinstance(application, str) or not application or not isinstance(releases, list) or not releases:
            raise RuntimeError(f"{artifact} registry producer identity is incomplete")
        if any(not isinstance(item, str) or not item for item in releases):
            raise RuntimeError(f"{artifact} registry releases must be non-empty strings")
        if len(set(releases)) != len(releases):
            raise RuntimeError(f"{artifact} registry releases must be unique")
        by_artifact[artifact] = {application: set(releases)}

    if set(by_artifact) != set(expected):
        raise RuntimeError("reviewed FTQC producer registry must cover both bounded input artifacts")
    return by_artifact["ExperimentResult"], by_artifact["ProcessorEvidenceReceipt"]


REVIEWED_EXPERIMENT_PRODUCERS, REVIEWED_PROCESSOR_PRODUCERS = _load_reviewed_producers()
EVIDENCE_CLASS_BY_KIND = {"decoder_backlog": "SIMULATED"}

_HEX = set("0123456789abcdef")


class FTQCEvidenceAdapterError(ValueError):
    """Raised when a technical-evidence handoff fails closed."""


def _validate_sha256(value: str, field: str) -> None:
    if len(value) != 64 or any(ch not in _HEX for ch in value):
        raise FTQCEvidenceAdapterError(
            f"{field} must be a lowercase 64-character SHA-256"
        )


def _raw_sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _canonical_sha256(value: Any) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def _read_object(path: Path, *, expected_sha256: str, label: str) -> tuple[dict[str, Any], str]:
    _validate_sha256(expected_sha256, f"{label} expected SHA-256")
    raw = path.read_bytes()
    actual = _raw_sha256(raw)
    if actual != expected_sha256:
        raise FTQCEvidenceAdapterError(
            f"{label} artifact SHA-256 does not match the trusted expected value"
        )
    try:
        value = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise FTQCEvidenceAdapterError(f"{label} is not valid JSON: {exc.msg}") from exc
    if not isinstance(value, dict):
        raise FTQCEvidenceAdapterError(f"{label} must be a JSON object")
    return value, actual


def _read_exact_schema(
    path: Path,
    *,
    expected_sha256: str,
    label: str,
) -> dict[str, Any]:
    raw = path.read_bytes()
    actual = _raw_sha256(raw)
    if actual != expected_sha256:
        raise FTQCEvidenceAdapterError(
            f"{label} schema SHA-256 is not the exact reviewed schema"
        )
    try:
        schema = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise FTQCEvidenceAdapterError(
            f"{label} schema is not valid JSON: {exc.msg}"
        ) from exc
    if not isinstance(schema, dict):
        raise FTQCEvidenceAdapterError(f"{label} schema must be a JSON object")
    Draft202012Validator.check_schema(schema)
    return schema


def _validate_schema(document: dict[str, Any], schema: dict[str, Any], label: str) -> None:
    errors = sorted(
        Draft202012Validator(schema).iter_errors(document),
        key=lambda item: list(item.path),
    )
    if errors:
        rendered = "; ".join(
            f"{'.'.join(str(part) for part in error.path) or '<root>'}: {error.message}"
            for error in errors
        )
        raise FTQCEvidenceAdapterError(f"{label} schema validation failed: {rendered}")


def _verify_reviewed_producer(
    document: dict[str, Any],
    *,
    reviewed: dict[str, set[str]],
    label: str,
) -> None:
    producer = document.get("producer")
    if not isinstance(producer, dict):
        raise FTQCEvidenceAdapterError(f"{label} missing producer identity")
    application = producer.get("application")
    release = producer.get("release")
    if not isinstance(application, str) or not isinstance(release, str):
        raise FTQCEvidenceAdapterError(f"{label} producer identity is incomplete")
    if release not in reviewed.get(application, set()):
        raise FTQCEvidenceAdapterError(
            f"{label} producer release is not explicitly reviewed by this adapter"
        )


def _verify_contract(
    document: dict[str, Any],
    *,
    contract_id: str,
    contract_version: str,
    schema_sha256: str,
    label: str,
) -> None:
    contract = document.get("contract")
    if not isinstance(contract, dict):
        raise FTQCEvidenceAdapterError(f"{label} missing contract identity")
    if contract.get("id") != contract_id or contract.get("version") != contract_version:
        raise FTQCEvidenceAdapterError(f"unsupported {label} contract identity")
    if contract.get("schema_digest") != schema_sha256:
        raise FTQCEvidenceAdapterError(
            f"{label} declared schema digest is not the exact reviewed schema"
        )


def _verify_experiment_integrity(document: dict[str, Any]) -> None:
    integrity = document.get("integrity")
    inputs = document.get("inputs")
    result = document.get("result")
    if not isinstance(integrity, dict) or not isinstance(inputs, dict) or not isinstance(result, dict):
        raise FTQCEvidenceAdapterError(
            "ExperimentResult integrity, inputs, and result must be objects"
        )
    payload = {key: value for key, value in document.items() if key != "integrity"}
    expected = {
        "inputs_sha256": _canonical_sha256(inputs),
        "scientific_payload_sha256": _canonical_sha256(result),
        "evidence_run_sha256": _canonical_sha256({"inputs": inputs, "result": result}),
        "artifact_payload_sha256": _canonical_sha256(payload),
    }
    wrong = [name for name, digest in expected.items() if integrity.get(name) != digest]
    if wrong:
        raise FTQCEvidenceAdapterError(
            "ExperimentResult internal integrity failed: " + ", ".join(sorted(wrong))
        )


def _verify_processor_integrity(document: dict[str, Any]) -> None:
    integrity = document.get("integrity")
    if not isinstance(integrity, dict):
        raise FTQCEvidenceAdapterError("ProcessorEvidenceReceipt missing integrity object")
    payload = {key: value for key, value in document.items() if key != "integrity"}
    expected = _canonical_sha256(payload)
    if integrity.get("artifact_payload_sha256") != expected:
        raise FTQCEvidenceAdapterError(
            "ProcessorEvidenceReceipt internal artifact payload integrity failed"
        )


def _verify_architecture_comparison(receipt: dict[str, Any]) -> tuple[str, bool | None]:
    comparison = receipt.get("architecture_comparison")
    if not isinstance(comparison, dict):
        raise FTQCEvidenceAdapterError(
            "ProcessorEvidenceReceipt missing architecture_comparison"
        )
    state = comparison.get("state")
    identical = comparison.get("architectures_identical")
    expected = {
        "SAME_DECLARED_CONFIGURATION": True,
        "CROSS_ARCHITECTURE": False,
        "NOT_APPLICABLE": None,
    }
    if state not in expected or identical is not expected[state]:
        raise FTQCEvidenceAdapterError(
            "ProcessorEvidenceReceipt architecture comparison is contradictory"
        )
    return str(state), identical


def _verify_linkage(
    experiment: dict[str, Any],
    experiment_sha256: str,
    receipt: dict[str, Any],
) -> dict[str, Any]:
    evidence = receipt.get("input_evidence")
    if not isinstance(evidence, list) or len(evidence) != 1 or not isinstance(evidence[0], dict):
        raise FTQCEvidenceAdapterError(
            "ProcessorEvidenceReceipt 2.0.0 must reference exactly one input artifact"
        )
    link = evidence[0]
    exp_contract = experiment["contract"]
    exp_producer = experiment["producer"]
    exp_identity = experiment["experiment"]
    expected = {
        "artifact_sha256": experiment_sha256,
        "contract_id": exp_contract["id"],
        "contract_version": exp_contract["version"],
        "schema_digest": exp_contract["schema_digest"],
        "producer_application": exp_producer["application"],
        "producer_release": exp_producer["release"],
        "experiment_id": exp_identity["id"],
        "experiment_kind": exp_identity["kind"],
    }
    mismatch = [key for key, value in expected.items() if link.get(key) != value]
    if mismatch:
        raise FTQCEvidenceAdapterError(
            "ProcessorEvidenceReceipt input linkage mismatch: " + ", ".join(sorted(mismatch))
        )
    integrity = receipt.get("integrity", {})
    if integrity.get("input_artifact_sha256") != experiment_sha256:
        raise FTQCEvidenceAdapterError(
            "ProcessorEvidenceReceipt integrity does not bind the ExperimentResult artifact"
        )
    return link


def _reproduction_state(value: str) -> str:
    if value == "REPRODUCED":
        return "REPRODUCED"
    if value in {"GENERATED", "HISTORICAL"}:
        return "NOT_ASSESSED"
    raise FTQCEvidenceAdapterError(
        f"unsupported ExperimentResult reproduction_state: {value!r}"
    )


def _applicability_state(architecture_state: str) -> str:
    if architecture_state == "CROSS_ARCHITECTURE":
        return "REVIEW_REQUIRED"
    if architecture_state == "NOT_APPLICABLE":
        return "OUTSIDE_ENVELOPE"
    if architecture_state == "SAME_DECLARED_CONFIGURATION":
        return "IN_SCOPE"
    raise FTQCEvidenceAdapterError(
        f"unsupported architecture comparison state: {architecture_state!r}"
    )


def adapt_verified_documents(
    experiment: dict[str, Any],
    *,
    experiment_sha256: str,
    receipt: dict[str, Any],
    receipt_sha256: str,
    evidence_ref: str,
) -> dict[str, Any]:
    """Map already schema-validated documents into bounded FMA semantics."""
    _validate_sha256(experiment_sha256, "ExperimentResult SHA-256")
    _validate_sha256(receipt_sha256, "ProcessorEvidenceReceipt SHA-256")
    _verify_reviewed_producer(
        experiment,
        reviewed=REVIEWED_EXPERIMENT_PRODUCERS,
        label="ExperimentResult",
    )
    _verify_reviewed_producer(
        receipt,
        reviewed=REVIEWED_PROCESSOR_PRODUCERS,
        label="ProcessorEvidenceReceipt",
    )
    _verify_contract(
        experiment,
        contract_id=EXPERIMENT_CONTRACT_ID,
        contract_version=EXPERIMENT_CONTRACT_VERSION,
        schema_sha256=EXPERIMENT_SCHEMA_SHA256,
        label="ExperimentResult",
    )
    _verify_contract(
        receipt,
        contract_id=PROCESSOR_CONTRACT_ID,
        contract_version=PROCESSOR_CONTRACT_VERSION,
        schema_sha256=PROCESSOR_SCHEMA_SHA256,
        label="ProcessorEvidenceReceipt",
    )
    _verify_experiment_integrity(experiment)
    _verify_processor_integrity(receipt)
    link = _verify_linkage(experiment, experiment_sha256, receipt)
    architecture_state, architectures_identical = _verify_architecture_comparison(receipt)

    experiment_kind = str(experiment["experiment"]["kind"])
    evidence_class = EVIDENCE_CLASS_BY_KIND.get(experiment_kind)
    if evidence_class is None:
        raise FTQCEvidenceAdapterError(
            "experiment kind has no reviewed FMA evidence-class mapping"
        )

    reproduction_state = _reproduction_state(str(experiment["reproduction_state"]))
    applicability = _applicability_state(architecture_state)
    processor_status = str(receipt["status"])
    if processor_status == "WITHIN_TARGET_ENVELOPE":
        assurance_effect = "RE-EVALUATION_OPPORTUNITY"
    else:
        assurance_effect = "REVIEW_REQUIRED"

    envelope = {
        "profile_version": "0.2",
        "record_class": "synthetic",
        "envelopes": [
            {
                "envelope_id": f"ENV-{evidence_ref}",
                "evidence_ref": evidence_ref,
                "evidence_class": evidence_class,
                "basis": {
                    "type": "model",
                    "refs": [evidence_ref],
                },
                "applicability": {
                    "conditions": [
                        {
                            "subject": "source_contract",
                            "operator": "eq",
                            "value": (
                                f"{PROCESSOR_CONTRACT_ID}/{PROCESSOR_CONTRACT_VERSION}"
                            ),
                        },
                        {
                            "subject": "source_artifact_sha256",
                            "operator": "eq",
                            "value": receipt_sha256,
                        },
                        {
                            "subject": "architecture_comparison_state",
                            "operator": "eq",
                            "value": architecture_state,
                        },
                        {
                            "subject": "configuration_ref",
                            "operator": "eq",
                            "value": experiment["experiment"]["configuration_ref"],
                        },
                    ]
                },
                "review": {
                    "status": applicability,
                    "authority_state": "DECLARED",
                    "decision_gate": True,
                },
            }
        ],
    }

    return {
        "adapter": "bn7.ftqc-processor-evidence-adapter/0.1",
        "source": {
            "experiment_result": {
                "artifact_sha256": experiment_sha256,
                "contract": f"{EXPERIMENT_CONTRACT_ID}/{EXPERIMENT_CONTRACT_VERSION}",
                "schema_sha256": EXPERIMENT_SCHEMA_SHA256,
                "producer": experiment["producer"],
                "experiment_id": link["experiment_id"],
                "experiment_kind": link["experiment_kind"],
            },
            "processor_receipt": {
                "artifact_sha256": receipt_sha256,
                "contract": f"{PROCESSOR_CONTRACT_ID}/{PROCESSOR_CONTRACT_VERSION}",
                "schema_sha256": PROCESSOR_SCHEMA_SHA256,
                "producer": receipt["producer"],
            },
        },
        "fma_evidence": {
            "evidence_class": evidence_class,
            "authority_state": "DECLARED",
            "reproduction_state": reproduction_state,
            "applicability": applicability,
            "processor_technical_status": processor_status,
            "architecture_comparison": {
                "state": architecture_state,
                "architectures_identical": architectures_identical,
            },
            "assurance_effect": assurance_effect,
            "expert_review_required": True,
            "automatic_decision_authorized": False,
        },
        "evidence_validity_envelope": envelope,
        "not_claimed": [
            "Mission approval, certification, or consequential decision authority.",
            "Independent V&V or scientific truth from structural/integrity validation alone.",
            "Applicability to another architecture unless qualified review establishes transfer.",
            "Hardware validation from simulated or model-derived evidence.",
        ],
    }


def adapt_files(
    *,
    experiment_path: Path,
    experiment_schema_path: Path,
    expected_experiment_sha256: str,
    receipt_path: Path,
    processor_schema_path: Path,
    expected_receipt_sha256: str,
    evidence_ref: str,
) -> dict[str, Any]:
    experiment, experiment_sha = _read_object(
        experiment_path,
        expected_sha256=expected_experiment_sha256,
        label="ExperimentResult",
    )
    receipt, receipt_sha = _read_object(
        receipt_path,
        expected_sha256=expected_receipt_sha256,
        label="ProcessorEvidenceReceipt",
    )
    experiment_schema = _read_exact_schema(
        experiment_schema_path,
        expected_sha256=EXPERIMENT_SCHEMA_SHA256,
        label="ExperimentResult",
    )
    processor_schema = _read_exact_schema(
        processor_schema_path,
        expected_sha256=PROCESSOR_SCHEMA_SHA256,
        label="ProcessorEvidenceReceipt",
    )
    _validate_schema(experiment, experiment_schema, "ExperimentResult")
    _validate_schema(receipt, processor_schema, "ProcessorEvidenceReceipt")
    return adapt_verified_documents(
        experiment,
        experiment_sha256=experiment_sha,
        receipt=receipt,
        receipt_sha256=receipt_sha,
        evidence_ref=evidence_ref,
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Validate and map bounded FTQC ExperimentResult + ProcessorEvidenceReceipt "
            "artifacts into existing FMA evidence/applicability semantics."
        )
    )
    parser.add_argument("--experiment-result", type=Path, required=True)
    parser.add_argument("--experiment-schema", type=Path, required=True)
    parser.add_argument("--expected-experiment-sha256", required=True)
    parser.add_argument("--processor-receipt", type=Path, required=True)
    parser.add_argument("--processor-schema", type=Path, required=True)
    parser.add_argument("--expected-processor-sha256", required=True)
    parser.add_argument("--evidence-ref", required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)

    try:
        result = adapt_files(
            experiment_path=args.experiment_result,
            experiment_schema_path=args.experiment_schema,
            expected_experiment_sha256=args.expected_experiment_sha256,
            receipt_path=args.processor_receipt,
            processor_schema_path=args.processor_schema,
            expected_receipt_sha256=args.expected_processor_sha256,
            evidence_ref=args.evidence_ref,
        )
    except (OSError, FTQCEvidenceAdapterError, ValueError) as exc:
        parser.error(str(exc))

    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
