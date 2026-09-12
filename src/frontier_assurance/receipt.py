from __future__ import annotations

import hashlib
import json
import math
import os
import shlex
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .io import load_structured


@dataclass
class ReceiptResult:
    errors: list[str] = field(default_factory=list)
    checks: list[str] = field(default_factory=list)
    stdout: str = ""
    stderr: str = ""

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


def _validate_document_shape(doc: dict[str, Any], result: ReceiptResult) -> None:
    if str(doc.get("receipt_version")) != "1.0":
        result.errors.append("receipt_version must be '1.0'")

    experiment = doc.get("experiment")
    if not isinstance(experiment, dict):
        result.errors.append("experiment must be a mapping")
    else:
        if not isinstance(experiment.get("id"), str) or not experiment.get("id", "").strip():
            result.errors.append("experiment.id is required")
        if not isinstance(experiment.get("command"), str) or not experiment.get("command", "").strip():
            result.errors.append("experiment.command is required")

    for section in ("inputs", "outputs", "checks"):
        if not isinstance(doc.get(section), list):
            result.errors.append(f"{section} must be a list")


def _verify_artifact_section(
    doc: dict[str, Any], section: str, base: Path, result: ReceiptResult
) -> None:
    items = doc.get(section, [])
    if not isinstance(items, list):
        return
    for index, item in enumerate(items):
        context = f"{section}[{index}]"
        if not isinstance(item, dict):
            result.errors.append(f"{context}: artifact entry must be a mapping")
            continue
        rel = item.get("path")
        expected = item.get("sha256")
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


def verify_receipt_inputs(receipt_path: str | Path) -> ReceiptResult:
    receipt_path = Path(receipt_path)
    doc = load_structured(receipt_path)
    base = receipt_path.parent
    result = ReceiptResult()
    _validate_document_shape(doc, result)
    _verify_artifact_section(doc, "inputs", base, result)
    return result


def verify_receipt(receipt_path: str | Path) -> ReceiptResult:
    receipt_path = Path(receipt_path)
    doc = load_structured(receipt_path)
    base = receipt_path.parent
    result = ReceiptResult()

    _validate_document_shape(doc, result)
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

    return result


def reproduce_receipt(receipt_path: str | Path, timeout: int = 300) -> ReceiptResult:
    """Explicitly execute the declared command, then verify the resulting receipt.

    This intentionally does not run during ordinary receipt verification. Reproduction
    executes code from the receipt's repository and must only be used with trusted code.
    """
    receipt_path = Path(receipt_path)
    doc = load_structured(receipt_path)
    result = verify_receipt_inputs(receipt_path)
    if not result.ok:
        return result

    experiment = doc.get("experiment", {})
    command = experiment.get("command") if isinstance(experiment, dict) else None
    if not isinstance(command, str) or not command.strip():
        result.errors.append("experiment.command is required for reproduction")
        return result

    try:
        argv = shlex.split(command, posix=os.name != "nt")
    except ValueError as exc:
        result.errors.append(f"cannot parse experiment.command: {exc}")
        return result
    if not argv:
        result.errors.append("experiment.command produced an empty command")
        return result
    if argv[0].lower() in {"python", "python3", "python.exe"}:
        argv[0] = sys.executable

    try:
        completed = subprocess.run(
            argv,
            cwd=receipt_path.parent,
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

    verified = verify_receipt(receipt_path)
    verified.stdout = completed.stdout
    verified.stderr = completed.stderr
    verified.checks.insert(0, f"command exit OK: {command}")
    return verified
