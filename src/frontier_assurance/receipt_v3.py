from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

V3 = "3.0"
ACCEPTANCE_MODES = {"EXACT_SHA256", "NUMERIC_CHECKS", "HYBRID"}
CALIBRATION_POLICIES = {"REQUIRED", "REVIEW_IF_MISSING", "NOT_APPLICABLE"}
EXECUTION_MODES = {"LOCAL", "EXTERNAL"}
TERMINAL_STATES = {"SUCCEEDED", "FAILED", "CANCELLED", "TIMED_OUT"}


def _is_sha256(value: Any) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 64
        and all(char in "0123456789abcdef" for char in value)
    )


def _parse_timestamp(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value.strip():
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return None
    return parsed.astimezone(timezone.utc)


def artifact_manifest_sha256(items: list[Any]) -> str:
    rows: list[str] = []
    for item in items:
        if not isinstance(item, dict):
            continue
        path = item.get("path")
        digest = item.get("sha256")
        if isinstance(path, str) and isinstance(digest, str):
            rows.append(f"{path}|{digest}\n")
    return hashlib.sha256("".join(sorted(rows)).encode("utf-8")).hexdigest()


def execution_mode(doc: dict[str, Any]) -> str:
    execution = doc.get("execution")
    if isinstance(execution, dict):
        mode = execution.get("mode")
        if isinstance(mode, str):
            return mode
    return "LOCAL"


def _validate_calibration(doc: dict[str, Any], result: Any) -> None:
    calibration = doc.get("calibration")
    if not isinstance(calibration, dict):
        result.errors.append("calibration must be a mapping for receipt_version 3.0")
        return

    policy = calibration.get("policy")
    if policy not in CALIBRATION_POLICIES:
        result.errors.append(
            "calibration.policy must be one of "
            + ", ".join(sorted(CALIBRATION_POLICIES))
        )
        return

    as_of = _parse_timestamp(calibration.get("as_of"))
    if as_of is None:
        result.errors.append("calibration.as_of must be an RFC3339 timestamp")
        return

    instruments = calibration.get("instruments")
    if not isinstance(instruments, list):
        result.errors.append("calibration.instruments must be a list")
        return

    if policy == "NOT_APPLICABLE":
        if instruments:
            result.errors.append(
                "calibration.instruments must be empty when policy is NOT_APPLICABLE"
            )
        return

    if not instruments:
        message = "calibration evidence is missing"
        if policy == "REQUIRED":
            result.errors.append(message)
        else:
            result.errors.append("REVIEW_REQUIRED: " + message)
        return

    seen: set[str] = set()
    stale: list[str] = []
    for index, instrument in enumerate(instruments):
        context = f"calibration.instruments[{index}]"
        if not isinstance(instrument, dict):
            result.errors.append(f"{context} must be a mapping")
            continue
        instrument_id = instrument.get("instrument_id")
        state_id = instrument.get("state_id")
        lineage_ref = instrument.get("lineage_ref")
        configuration_sha256 = instrument.get("configuration_sha256")
        observed_at = _parse_timestamp(instrument.get("observed_at"))
        valid_from = _parse_timestamp(instrument.get("valid_from"))
        valid_until = _parse_timestamp(instrument.get("valid_until"))
        if not isinstance(instrument_id, str) or not instrument_id.strip():
            result.errors.append(f"{context}.instrument_id is required")
        elif instrument_id in seen:
            result.errors.append(f"{context}.instrument_id is duplicated: {instrument_id}")
        else:
            seen.add(instrument_id)
        if not isinstance(state_id, str) or not state_id.strip():
            result.errors.append(f"{context}.state_id is required")
        if not isinstance(lineage_ref, str) or not lineage_ref.strip():
            result.errors.append(f"{context}.lineage_ref is required")
        if not _is_sha256(configuration_sha256):
            result.errors.append(f"{context}.configuration_sha256 must be sha256")
        if observed_at is None:
            result.errors.append(f"{context}.observed_at must be RFC3339")
        if valid_from is None:
            result.errors.append(f"{context}.valid_from must be RFC3339")
        if valid_until is None:
            result.errors.append(f"{context}.valid_until must be RFC3339")
        if valid_from and valid_until and valid_from > valid_until:
            result.errors.append(f"{context}: valid_from is after valid_until")
        if as_of and valid_from and valid_until and not (valid_from <= as_of <= valid_until):
            stale.append(str(instrument_id or index))

    if stale:
        message = "calibration outside declared validity window: " + ", ".join(sorted(stale))
        if policy == "REQUIRED":
            result.errors.append(message)
        else:
            result.errors.append("REVIEW_REQUIRED: " + message)


def _validate_external_execution(doc: dict[str, Any], result: Any) -> None:
    execution = doc.get("execution")
    if not isinstance(execution, dict):
        result.errors.append("execution must be a mapping for receipt_version 3.0")
        return

    mode = execution.get("mode")
    if mode not in EXECUTION_MODES:
        result.errors.append(
            "execution.mode must be one of " + ", ".join(sorted(EXECUTION_MODES))
        )
        return

    if mode == "LOCAL":
        unexpected = sorted(set(execution) - {"mode"})
        if unexpected:
            result.errors.append(
                "LOCAL execution has unsupported fields: " + ", ".join(unexpected)
            )
        return

    submission = execution.get("submission_receipt")
    collection = execution.get("collection_receipt")
    if not isinstance(submission, dict):
        result.errors.append("execution.submission_receipt is required for EXTERNAL mode")
        return
    if not isinstance(collection, dict):
        result.errors.append("execution.collection_receipt is required for EXTERNAL mode")
        return

    for field in ("scheduler", "submission_ref", "job_ref", "submitted_at"):
        value = submission.get(field)
        if not isinstance(value, str) or not value.strip():
            result.errors.append(f"execution.submission_receipt.{field} is required")
    if _parse_timestamp(submission.get("submitted_at")) is None:
        result.errors.append(
            "execution.submission_receipt.submitted_at must be RFC3339"
        )

    for field in ("code_manifest_sha256", "input_manifest_sha256"):
        if not _is_sha256(submission.get(field)):
            result.errors.append(
                f"execution.submission_receipt.{field} must be sha256"
            )

    environment = submission.get("environment")
    if not isinstance(environment, dict):
        result.errors.append(
            "execution.submission_receipt.environment must be a mapping"
        )
    else:
        for field in ("runtime", "environment_sha256"):
            value = environment.get(field)
            if field == "environment_sha256":
                if not _is_sha256(value):
                    result.errors.append(
                        "execution.submission_receipt.environment.environment_sha256 "
                        "must be sha256"
                    )
            elif not isinstance(value, str) or not value.strip():
                result.errors.append(
                    "execution.submission_receipt.environment.runtime is required"
                )
        container_digest = environment.get("container_digest")
        if container_digest is not None and (
            not isinstance(container_digest, str) or not container_digest.strip()
        ):
            result.errors.append(
                "execution.submission_receipt.environment.container_digest must be "
                "a non-empty string when present"
            )

    for field in ("job_ref", "collected_at", "terminal_state", "cancellation_semantics"):
        value = collection.get(field)
        if not isinstance(value, str) or not value.strip():
            result.errors.append(f"execution.collection_receipt.{field} is required")
    if _parse_timestamp(collection.get("collected_at")) is None:
        result.errors.append(
            "execution.collection_receipt.collected_at must be RFC3339"
        )
    if collection.get("terminal_state") not in TERMINAL_STATES:
        result.errors.append(
            "execution.collection_receipt.terminal_state must be one of "
            + ", ".join(sorted(TERMINAL_STATES))
        )
    timeout_seconds = collection.get("timeout_seconds")
    if (
        not isinstance(timeout_seconds, int)
        or isinstance(timeout_seconds, bool)
        or timeout_seconds <= 0
    ):
        result.errors.append(
            "execution.collection_receipt.timeout_seconds must be a positive integer"
        )
    if submission.get("job_ref") != collection.get("job_ref"):
        result.errors.append(
            "external submission and collection job_ref values must match"
        )
    outputs = collection.get("outputs")
    if not isinstance(outputs, list) or not outputs:
        result.errors.append(
            "execution.collection_receipt.outputs must be a non-empty list"
        )
    else:
        seen_paths: set[str] = set()
        for index, item in enumerate(outputs):
            context = f"execution.collection_receipt.outputs[{index}]"
            if not isinstance(item, dict):
                result.errors.append(f"{context} must be a mapping")
                continue
            path = item.get("path")
            if not isinstance(path, str) or not path.strip():
                result.errors.append(f"{context}.path is required")
            elif path in seen_paths:
                result.errors.append(f"{context}.path is duplicated: {path}")
            else:
                seen_paths.add(path)
            if not _is_sha256(item.get("sha256")):
                result.errors.append(f"{context}.sha256 must be sha256")


def validate_v3_shape(doc: dict[str, Any], result: Any) -> None:
    acceptance = doc.get("output_acceptance")
    if not isinstance(acceptance, dict):
        result.errors.append(
            "output_acceptance must be a mapping for receipt_version 3.0"
        )
        return

    mode = acceptance.get("mode")
    if mode not in ACCEPTANCE_MODES:
        result.errors.append(
            "output_acceptance.mode must be one of "
            + ", ".join(sorted(ACCEPTANCE_MODES))
        )
    else:
        result.acceptance_mode = mode

    outputs = doc.get("outputs")
    if isinstance(outputs, list):
        seen: set[str] = set()
        for index, item in enumerate(outputs):
            context = f"outputs[{index}]"
            if not isinstance(item, dict):
                continue
            rel = item.get("path")
            if isinstance(rel, str):
                if rel in seen:
                    result.errors.append(f"{context}: duplicate artifact path: {rel}")
                seen.add(rel)
            if "sha256" in item:
                result.errors.append(
                    f"{context}: receipt_version 3.0 uses reference_sha256, not sha256, "
                    "for output acceptance"
                )
            reference = item.get("reference_sha256")
            if mode in {"EXACT_SHA256", "HYBRID"} and not _is_sha256(reference):
                result.errors.append(
                    f"{context}.reference_sha256 is required for {mode}"
                )
            if mode == "NUMERIC_CHECKS" and reference is not None and not _is_sha256(reference):
                result.errors.append(
                    f"{context}.reference_sha256 must be sha256 when present"
                )

    checks = doc.get("checks")
    if mode in {"NUMERIC_CHECKS", "HYBRID"} and (
        not isinstance(checks, list) or not checks
    ):
        result.errors.append(f"{mode} requires at least one numerical check")

    _validate_calibration(doc, result)
    _validate_external_execution(doc, result)


def verify_v3_provenance(
    doc: dict[str, Any],
    base: Path,
    result: Any,
    safe_target: Callable[[Path, Any, str, Any], Path | None],
    sha256_file: Callable[[Path], str],
) -> None:
    acceptance = doc.get("output_acceptance", {})
    mode = acceptance.get("mode")
    outputs = doc.get("outputs", [])
    if not isinstance(outputs, list):
        return

    declared_output_paths: set[str] = set()
    for index, item in enumerate(outputs):
        context = f"outputs[{index}]"
        if not isinstance(item, dict):
            result.errors.append(f"{context}: artifact entry must be a mapping")
            continue
        rel = item.get("path")
        if not isinstance(rel, str):
            result.errors.append(f"{context}: path must be a non-empty string")
            continue
        if rel in declared_output_paths:
            continue
        declared_output_paths.add(rel)
        target = safe_target(base, rel, context, result)
        if target is None:
            continue
        if not target.exists() or not target.is_file():
            result.errors.append(f"{context}: missing artifact: {rel}")
            continue
        actual = sha256_file(target)
        result.observed_output_hashes[rel] = actual
        result.checks.append(f"observed output sha256: {rel}={actual}")
        result.artifact_counts["outputs"] = result.artifact_counts.get("outputs", 0) + 1
        reference = item.get("reference_sha256")
        if mode in {"EXACT_SHA256", "HYBRID"}:
            if actual != reference:
                result.errors.append(
                    f"{context}: reference sha256 mismatch for {rel}: {actual}"
                )
            else:
                result.checks.append(f"reference hash OK: {rel}")

    if execution_mode(doc) != "EXTERNAL":
        return

    execution = doc.get("execution", {})
    submission = execution.get("submission_receipt", {})
    collection = execution.get("collection_receipt", {})

    code_manifest = artifact_manifest_sha256(
        doc.get("code", []) if isinstance(doc.get("code"), list) else []
    )
    input_manifest = artifact_manifest_sha256(
        doc.get("inputs", []) if isinstance(doc.get("inputs"), list) else []
    )
    if submission.get("code_manifest_sha256") != code_manifest:
        result.errors.append(
            "external submission code_manifest_sha256 does not match declared code"
        )
    else:
        result.checks.append("external submission code manifest OK")
    if submission.get("input_manifest_sha256") != input_manifest:
        result.errors.append(
            "external submission input_manifest_sha256 does not match declared inputs"
        )
    else:
        result.checks.append("external submission input manifest OK")

    terminal_state = collection.get("terminal_state")
    if terminal_state != "SUCCEEDED":
        result.errors.append(
            f"external job did not succeed: terminal_state={terminal_state!r}"
        )

    collected: dict[str, str] = {}
    collection_outputs = collection.get("outputs", [])
    if isinstance(collection_outputs, list):
        for item in collection_outputs:
            if isinstance(item, dict) and isinstance(item.get("path"), str):
                collected[item["path"]] = str(item.get("sha256", ""))

    for rel in sorted(declared_output_paths):
        observed = result.observed_output_hashes.get(rel)
        expected = collected.get(rel)
        if expected is None:
            result.errors.append(
                f"external collection receipt missing declared output: {rel}"
            )
        elif observed != expected:
            result.errors.append(
                f"external collection sha256 mismatch for {rel}: observed={observed}"
            )
        else:
            result.checks.append(f"external collection provenance OK: {rel}")

    extras = sorted(set(collected) - declared_output_paths)
    if extras:
        result.errors.append(
            "external collection receipt includes undeclared outputs: "
            + ", ".join(extras)
        )
