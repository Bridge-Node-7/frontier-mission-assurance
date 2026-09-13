from __future__ import annotations

import hashlib
import json
import math
import os
import shlex
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .io import load_structured


SUPPORTED_RECEIPT_VERSIONS = {"1.0", "2.0"}
FRESH_REPRODUCTION_VERSION = "2.0"


@dataclass
class ReceiptResult:
    errors: list[str] = field(default_factory=list)
    checks: list[str] = field(default_factory=list)
    stdout: str = ""
    stderr: str = ""
    receipt_version: str = ""
    artifact_counts: dict[str, int] = field(
        default_factory=lambda: {"code": 0, "inputs": 0, "outputs": 0}
    )
    numerical_checks: int = 0

    @property
    def ok(self) -> bool:
        return not self.errors


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def _json_path(data: Any, path: str) -> Any:
    cur = data
    for part in path.split("."):
        if isinstance(cur, dict) and part in cur:
            cur = cur[part]
        else:
            raise KeyError(path)
    return cur


def _safe_target(base: Path, rel: Any, context: str, result: ReceiptResult) -> Path | None:
    if not isinstance(rel, str) or not rel.strip():
        result.errors.append(f"{context}: path must be a non-empty string")
        return None
    target = (base / rel).resolve()
    try:
        target.relative_to(base.resolve())
    except ValueError:
        result.errors.append(f"{context}: path escapes receipt directory: {rel}")
        return None
    return target


def _artifact_paths(doc: dict[str, Any], section: str) -> list[str]:
    items = doc.get(section, [])
    if not isinstance(items, list):
        return []
    return [
        item.get("path")
        for item in items
        if isinstance(item, dict) and isinstance(item.get("path"), str)
    ]


def _validate_document_shape(doc: dict[str, Any], result: ReceiptResult) -> None:
    version = str(doc.get("receipt_version"))
    result.receipt_version = version
    if version not in SUPPORTED_RECEIPT_VERSIONS:
        result.errors.append("receipt_version must be '1.0' or '2.0'")

    experiment = doc.get("experiment")
    if not isinstance(experiment, dict):
        result.errors.append("experiment must be a mapping")
        experiment = {}
    else:
        if not isinstance(experiment.get("id"), str) or not experiment.get("id", "").strip():
            result.errors.append("experiment.id is required")
        command = experiment.get("command")
        if not isinstance(command, str) or not command.strip():
            result.errors.append("experiment.command is required")

    for section in ("inputs", "outputs", "checks"):
        value = doc.get(section)
        if not isinstance(value, list):
            result.errors.append(f"{section} must be a list")
        elif version == FRESH_REPRODUCTION_VERSION and not value:
            result.errors.append(
                f"{section} must contain at least one entry for receipt_version 2.0"
            )

    if version == FRESH_REPRODUCTION_VERSION:
        code = doc.get("code")
        if not isinstance(code, list):
            result.errors.append("code must be a list for receipt_version 2.0")
        elif not code:
            result.errors.append("code must contain at least one entry for receipt_version 2.0")

        entrypoint = experiment.get("entrypoint")
        if not isinstance(entrypoint, str) or not entrypoint.strip():
            result.errors.append("experiment.entrypoint is required for receipt_version 2.0")
        else:
            code_paths = _artifact_paths(doc, "code")
            if entrypoint not in code_paths:
                result.errors.append(
                    "experiment.entrypoint must reference a declared code artifact"
                )

        source_paths = set(_artifact_paths(doc, "code")) | set(_artifact_paths(doc, "inputs"))
        output_paths = set(_artifact_paths(doc, "outputs"))
        overlap = sorted(source_paths & output_paths)
        if overlap:
            result.errors.append(
                "outputs must not overlap declared code or inputs: " + ", ".join(overlap)
            )

        for index, check in enumerate(doc.get("checks", [])):
            if isinstance(check, dict) and check.get("path") not in output_paths:
                result.errors.append(
                    f"checks[{index}].path must reference a declared output artifact"
                )


def _verify_artifact_section(
    doc: dict[str, Any], section: str, base: Path, result: ReceiptResult
) -> None:
    items = doc.get(section, [])
    if not isinstance(items, list):
        return
    seen_paths: set[str] = set()
    for index, item in enumerate(items):
        context = f"{section}[{index}]"
        if not isinstance(item, dict):
            result.errors.append(f"{context}: artifact entry must be a mapping")
            continue
        rel = item.get("path")
        expected = item.get("sha256")
        if isinstance(rel, str):
            if rel in seen_paths:
                result.errors.append(f"{context}: duplicate artifact path: {rel}")
                continue
            seen_paths.add(rel)
        target = _safe_target(base, rel, context, result)
        if target is None:
            continue
        if not isinstance(expected, str) or len(expected) != 64 or any(
            c not in "0123456789abcdef" for c in expected
        ):
            result.errors.append(f"{context}: sha256 must be 64 lowercase hexadecimal characters")
            continue
        if not target.exists() or not target.is_file():
            result.errors.append(f"{context}: missing artifact: {rel}")
            continue
        actual = sha256_file(target)
        if actual != expected:
            result.errors.append(f"{context}: sha256 mismatch for {rel}: {actual}")
        else:
            result.checks.append(f"hash OK: {rel}")
            result.artifact_counts[section] = result.artifact_counts.get(section, 0) + 1


def verify_receipt_inputs(receipt_path: str | Path) -> ReceiptResult:
    receipt_path = Path(receipt_path)
    doc = load_structured(receipt_path)
    base = receipt_path.parent
    result = ReceiptResult()
    _validate_document_shape(doc, result)
    if result.receipt_version == FRESH_REPRODUCTION_VERSION:
        _verify_artifact_section(doc, "code", base, result)
    _verify_artifact_section(doc, "inputs", base, result)
    return result


def verify_receipt(receipt_path: str | Path) -> ReceiptResult:
    receipt_path = Path(receipt_path)
    doc = load_structured(receipt_path)
    base = receipt_path.parent
    result = ReceiptResult()

    _validate_document_shape(doc, result)
    if result.receipt_version == FRESH_REPRODUCTION_VERSION:
        _verify_artifact_section(doc, "code", base, result)
    _verify_artifact_section(doc, "inputs", base, result)
    _verify_artifact_section(doc, "outputs", base, result)

    checks = doc.get("checks", [])
    if isinstance(checks, list):
        for index, check in enumerate(checks):
            context = f"checks[{index}]"
            if not isinstance(check, dict):
                result.errors.append(f"{context}: check entry must be a mapping")
                continue
            name = check.get("name", "unnamed")
            rel = check.get("path")
            json_path = check.get("json_path")
            target = _safe_target(base, rel, f"check {name}", result)
            if target is None:
                continue
            if not isinstance(json_path, str) or not json_path.strip():
                result.errors.append(f"check {name}: json_path is required")
                continue
            if not target.exists() or not target.is_file():
                result.errors.append(f"check {name}: missing result file {rel}")
                continue
            try:
                value = _json_path(json.loads(target.read_text(encoding="utf-8")), json_path)
                value = float(value)
                expected = float(check["expected"])
                atol = float(check.get("atol", 0.0))
                rtol = float(check.get("rtol", 0.0))
                if atol < 0 or rtol < 0:
                    raise ValueError("atol/rtol must be non-negative")
            except (ValueError, TypeError, KeyError, json.JSONDecodeError) as exc:
                result.errors.append(f"check {name}: cannot evaluate: {exc}")
                continue
            if not math.isclose(value, expected, rel_tol=rtol, abs_tol=atol):
                result.errors.append(
                    f"check {name}: observed {value} != expected {expected} "
                    f"within atol={atol}, rtol={rtol}"
                )
            else:
                result.checks.append(f"numeric OK: {name}={value}")
                result.numerical_checks += 1

    return result


def _normalized_command_path(value: str) -> str:
    normalized = value.replace("\\", "/")
    while normalized.startswith("./"):
        normalized = normalized[2:]
    return normalized


def _stage_artifacts(
    doc: dict[str, Any],
    section: str,
    source_base: Path,
    workspace: Path,
    result: ReceiptResult,
) -> None:
    staged: set[str] = set()
    for index, item in enumerate(doc.get(section, [])):
        if not isinstance(item, dict):
            continue
        rel = item.get("path")
        if not isinstance(rel, str) or rel in staged:
            continue
        source = _safe_target(source_base, rel, f"{section}[{index}]", result)
        target = _safe_target(workspace, rel, f"{section}[{index}]", result)
        if source is None or target is None:
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        staged.add(rel)


def reproduce_receipt(receipt_path: str | Path, timeout: int = 300) -> ReceiptResult:
    """Run a receipt v2 command in an isolated declared-artifact workspace.

    The workspace starts with only the receipt, declared code, and declared inputs. Declared
    outputs are deliberately absent, so a successful reproduction must create them fresh.
    This is an integrity boundary, not a sandbox or hermetic execution environment.
    """
    receipt_path = Path(receipt_path).resolve()
    doc = load_structured(receipt_path)
    result = verify_receipt_inputs(receipt_path)
    if not result.ok:
        return result
    if result.receipt_version != FRESH_REPRODUCTION_VERSION:
        result.errors.append(
            "fresh reproduction requires receipt_version 2.0 with code-bound execution"
        )
        return result

    experiment = doc.get("experiment", {})
    command = experiment.get("command") if isinstance(experiment, dict) else None
    entrypoint = experiment.get("entrypoint") if isinstance(experiment, dict) else None
    if not isinstance(command, str) or not command.strip():
        result.errors.append("experiment.command is required for reproduction")
        return result
    if not isinstance(entrypoint, str) or not entrypoint.strip():
        result.errors.append("experiment.entrypoint is required for reproduction")
        return result

    try:
        argv = shlex.split(command, posix=os.name != "nt")
    except ValueError as exc:
        result.errors.append(f"cannot parse experiment.command: {exc}")
        return result
    if not argv:
        result.errors.append("experiment.command produced an empty command")
        return result

    normalized_entrypoint = _normalized_command_path(entrypoint)
    command_paths = {_normalized_command_path(token) for token in argv[1:]}
    if _normalized_command_path(argv[0]) == normalized_entrypoint:
        command_paths.add(normalized_entrypoint)
    if normalized_entrypoint not in command_paths:
        result.errors.append("experiment.command must execute the declared experiment.entrypoint")
        return result

    if argv[0].lower() in {"python", "python3", "python.exe"}:
        argv[0] = sys.executable

    source_base = receipt_path.parent.resolve()
    with tempfile.TemporaryDirectory(prefix="fma-reproduce-") as temp_dir:
        workspace = Path(temp_dir).resolve()
        staged_receipt = workspace / receipt_path.name
        shutil.copy2(receipt_path, staged_receipt)
        _stage_artifacts(doc, "code", source_base, workspace, result)
        _stage_artifacts(doc, "inputs", source_base, workspace, result)
        if not result.ok:
            return result

        for index, item in enumerate(doc.get("outputs", [])):
            if not isinstance(item, dict):
                continue
            target = _safe_target(workspace, item.get("path"), f"outputs[{index}]", result)
            if target is not None:
                target.parent.mkdir(parents=True, exist_ok=True)
                if target.exists():
                    result.errors.append(
                        f"outputs[{index}]: declared output unexpectedly existed before execution"
                    )
        if not result.ok:
            return result

        try:
            completed = subprocess.run(
                argv,
                cwd=workspace,
                check=False,
                capture_output=True,
                text=True,
                timeout=timeout,
                shell=False,
            )
        except subprocess.TimeoutExpired:
            result.errors.append(f"experiment command exceeded timeout={timeout}s")
            return result
        except OSError as exc:
            result.errors.append(f"experiment command could not start: {exc}")
            return result

        result.stdout = completed.stdout
        result.stderr = completed.stderr
        if completed.returncode != 0:
            result.errors.append(f"experiment command exited with status {completed.returncode}")
            return result

        verified = verify_receipt(staged_receipt)
        verified.stdout = completed.stdout
        verified.stderr = completed.stderr
        verified.checks.insert(0, f"command exit OK: {command}")
        verified.checks.insert(
            1,
            "fresh output workspace OK: "
            f"{verified.artifact_counts.get('outputs', 0)} output artifact(s)",
        )
        return verified
