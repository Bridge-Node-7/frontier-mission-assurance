from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

from frontier_assurance.constants import STATUSES
from frontier_assurance.io import load_structured
from frontier_assurance.receipt import reproduce_receipt, verify_receipt
from frontier_assurance.receipt_v3 import artifact_manifest_sha256
from frontier_assurance.validate import validate_graph

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas" / "research-receipt-v3.schema.json"
EXTERNAL_EXAMPLE = ROOT / "examples" / "research_receipt_v3_external" / "receipt.yaml"
GRAPH = ROOT / "examples" / "frontier_program" / "graph.yaml"


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _write_local_v3(
    tmp_path: Path,
    *,
    value: float = 1.0004,
    acceptance: str = "NUMERIC_CHECKS",
    reference_sha256: str | None = None,
    calibration: dict | None = None,
) -> Path:
    code_bytes = (
        "from pathlib import Path\n"
        "Path('outputs').mkdir(exist_ok=True)\n"
        f"Path('outputs/result.json').write_text('{{\"value\": {value}}}\\n', encoding='utf-8')\n"
    ).encode("utf-8")
    input_bytes = b"declared v3 input\n"
    output = {"path": "outputs/result.json"}
    if reference_sha256 is not None:
        output["reference_sha256"] = reference_sha256
    if calibration is None:
        calibration = {
            "policy": "NOT_APPLICABLE",
            "as_of": "2026-09-13T00:00:00Z",
            "instruments": [],
        }

    (tmp_path / "analysis.py").write_bytes(code_bytes)
    (tmp_path / "data").mkdir(exist_ok=True)
    (tmp_path / "data" / "input.txt").write_bytes(input_bytes)

    receipt = {
        "receipt_version": "3.0",
        "experiment": {
            "id": "LOCAL-V3",
            "command": "python analysis.py",
            "entrypoint": "analysis.py",
            "seed": 7,
        },
        "execution": {"mode": "LOCAL"},
        "output_acceptance": {"mode": acceptance},
        "calibration": calibration,
        "code": [{"path": "analysis.py", "sha256": _sha256(code_bytes)}],
        "inputs": [{"path": "data/input.txt", "sha256": _sha256(input_bytes)}],
        "outputs": [output],
        "checks": [
            {
                "name": "value",
                "path": "outputs/result.json",
                "json_path": "value",
                "expected": 1.0,
                "atol": 0.001,
                "rtol": 0.0,
            }
        ],
    }
    path = tmp_path / "receipt.yaml"
    path.write_text(yaml.safe_dump(receipt, sort_keys=False), encoding="utf-8")
    return path


def test_v3_schema_and_synthetic_external_example_are_valid():
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    document = load_structured(EXTERNAL_EXAMPLE)
    Draft202012Validator(schema).validate(document)


def test_v3_numeric_acceptance_allows_nonidentical_output_and_preserves_observed_hash(
    tmp_path: Path,
):
    receipt = _write_local_v3(tmp_path)
    result = reproduce_receipt(receipt, timeout=30)
    assert result.ok, result.errors
    assert result.acceptance_mode == "NUMERIC_CHECKS"
    assert result.numerical_checks == 1
    observed = result.observed_output_hashes["outputs/result.json"]
    expected_observed = _sha256(b'{"value": 1.0004}\n')
    assert observed == expected_observed
    assert any("observed output sha256" in check for check in result.checks)


def test_v3_exact_acceptance_rejects_reference_hash_mismatch(tmp_path: Path):
    receipt = _write_local_v3(
        tmp_path,
        acceptance="EXACT_SHA256",
        reference_sha256="0" * 64,
    )
    (tmp_path / "outputs").mkdir()
    (tmp_path / "outputs" / "result.json").write_text(
        '{"value": 1.0004}\n', encoding="utf-8"
    )
    result = verify_receipt(receipt)
    assert not result.ok
    assert any("reference sha256 mismatch" in error for error in result.errors)


def test_v3_code_and_input_hashes_remain_exact(tmp_path: Path):
    receipt = _write_local_v3(tmp_path)
    (tmp_path / "analysis.py").write_text("print('tampered')\n", encoding="utf-8")
    result = verify_receipt(receipt)
    assert not result.ok
    assert any("sha256 mismatch for analysis.py" in error for error in result.errors)


def test_v3_required_stale_calibration_fails(tmp_path: Path):
    calibration = {
        "policy": "REQUIRED",
        "as_of": "2026-09-13T00:00:00Z",
        "instruments": [
            {
                "instrument_id": "INST-SYN-001",
                "state_id": "STATE-SYN-001",
                "observed_at": "2026-09-09T23:00:00Z",
                "valid_from": "2026-09-01T00:00:00Z",
                "valid_until": "2026-09-10T00:00:00Z",
                "configuration_sha256": _sha256(b"calibration"),
                "lineage_ref": "synthetic://calibration/INST-SYN-001",
            }
        ],
    }
    receipt = _write_local_v3(tmp_path, calibration=calibration)
    (tmp_path / "outputs").mkdir()
    (tmp_path / "outputs" / "result.json").write_text(
        '{"value": 1.0004}\n', encoding="utf-8"
    )
    result = verify_receipt(receipt)
    assert not result.ok
    assert any("outside declared validity window" in error for error in result.errors)


def test_v3_review_if_missing_calibration_is_review_required(tmp_path: Path):
    calibration = {
        "policy": "REVIEW_IF_MISSING",
        "as_of": "2026-09-13T00:00:00Z",
        "instruments": [],
    }
    receipt = _write_local_v3(tmp_path, calibration=calibration)
    (tmp_path / "outputs").mkdir()
    (tmp_path / "outputs" / "result.json").write_text(
        '{"value": 1.0004}\n', encoding="utf-8"
    )
    result = verify_receipt(receipt)
    assert not result.ok
    assert any(
        "REVIEW_REQUIRED: calibration evidence is missing" in error
        for error in result.errors
    )


def test_v3_external_submission_and_collection_are_provenance_bound():
    result = verify_receipt(EXTERNAL_EXAMPLE)
    assert result.ok, result.errors
    assert any("external submission code manifest OK" in check for check in result.checks)
    assert any("external collection provenance OK" in check for check in result.checks)
    document = load_structured(EXTERNAL_EXAMPLE)
    assert (
        document["execution"]["submission_receipt"]["code_manifest_sha256"]
        == artifact_manifest_sha256(document["code"])
    )
    assert (
        document["execution"]["submission_receipt"]["input_manifest_sha256"]
        == artifact_manifest_sha256(document["inputs"])
    )


def test_v3_external_job_mismatch_and_failed_terminal_state_fail_closed(tmp_path: Path):
    source_dir = EXTERNAL_EXAMPLE.parent
    (tmp_path / "analysis.py").write_bytes((source_dir / "analysis.py").read_bytes())
    (tmp_path / "data").mkdir()
    (tmp_path / "data" / "input.txt").write_bytes(
        (source_dir / "data" / "input.txt").read_bytes()
    )
    (tmp_path / "outputs").mkdir()
    (tmp_path / "outputs" / "result.json").write_bytes(
        (source_dir / "outputs" / "result.json").read_bytes()
    )
    document = load_structured(EXTERNAL_EXAMPLE)
    document["execution"]["collection_receipt"]["job_ref"] = "OTHER-JOB"
    document["execution"]["collection_receipt"]["terminal_state"] = "FAILED"
    receipt = tmp_path / "receipt.yaml"
    receipt.write_text(yaml.safe_dump(document, sort_keys=False), encoding="utf-8")
    result = verify_receipt(receipt)
    assert not result.ok
    assert any("job_ref values must match" in error for error in result.errors)
    assert any("external job did not succeed" in error for error in result.errors)


def test_v3_external_receipt_is_not_executed_as_local_subprocess():
    result = reproduce_receipt(EXTERNAL_EXAMPLE, timeout=30)
    assert not result.ok
    assert any("collection-verification only" in error for error in result.errors)


def test_undeclared_helper_diagnostic_preserves_raw_child_error_and_adds_bounded_hint(
    tmp_path: Path,
):
    code_bytes = b"import missing_declared_helper_xyz\n"
    input_bytes = b"input\n"
    expected_output = b'{"value": 1.0}\n'
    (tmp_path / "analysis.py").write_bytes(code_bytes)
    (tmp_path / "data").mkdir()
    (tmp_path / "data" / "input.txt").write_bytes(input_bytes)
    document = {
        "receipt_version": "2.0",
        "experiment": {
            "id": "MISSING-HELPER",
            "command": "python analysis.py",
            "entrypoint": "analysis.py",
        },
        "code": [{"path": "analysis.py", "sha256": _sha256(code_bytes)}],
        "inputs": [{"path": "data/input.txt", "sha256": _sha256(input_bytes)}],
        "outputs": [
            {"path": "outputs/result.json", "sha256": _sha256(expected_output)}
        ],
        "checks": [
            {
                "name": "value",
                "path": "outputs/result.json",
                "json_path": "value",
                "expected": 1.0,
            }
        ],
    }
    receipt = tmp_path / "receipt.yaml"
    receipt.write_text(yaml.safe_dump(document, sort_keys=False), encoding="utf-8")

    completed = subprocess.run(
        [sys.executable, "-m", "frontier_assurance.cli", "reproduce", str(receipt)],
        capture_output=True,
        text=True,
        check=False,
    )
    combined = completed.stdout + completed.stderr
    assert completed.returncode == 2
    assert "ModuleNotFoundError" in combined
    assert "missing a declared code artifact or runtime dependency" in combined


def test_invalid_graph_status_lists_sorted_allowed_values():
    graph = load_structured(GRAPH)
    graph["nodes"][0]["status"] = "mystery"
    result = validate_graph(graph)
    assert not result.ok
    expected = ", ".join(sorted(STATUSES))
    assert any(
        "unsupported status 'mystery'" in error and expected in error
        for error in result.errors
    )
