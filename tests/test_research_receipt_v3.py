from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

import pytest
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
    version: str = "3.1",
) -> Path:
    code_bytes = (
        "from pathlib import Path\n"
        "Path('outputs').mkdir(exist_ok=True)\n"
        f"Path('outputs/result.json').write_bytes(b'{{\"value\": {value}}}\\n')\n"
    ).encode()
    input_bytes = b"declared v3 input\n"
    output: dict[str, object] = {"path": "outputs/result.json"}
    check: dict[str, object] = {
        "name": "value",
        "path": "outputs/result.json",
        "json_path": "value",
        "expected": 1.0,
        "atol": 0.001,
        "rtol": 0.0,
    }
    if version == "3.1":
        check["id"] = "CHK-VALUE"
        if acceptance == "EXACT_SHA256":
            output["assurance"] = "EXACT"
        else:
            output["assurance"] = "SEMANTICALLY_CHECKED"
            output["semantic_check_ids"] = ["CHK-VALUE"]
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
        "receipt_version": version,
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
        "checks": [check],
    }
    path = tmp_path / "receipt.yaml"
    path.write_text(yaml.safe_dump(receipt, sort_keys=False), encoding="utf-8")
    return path


def test_v3_schema_and_synthetic_external_example_are_valid():
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    document = load_structured(EXTERNAL_EXAMPLE)
    Draft202012Validator(schema).validate(document)
    assert document["receipt_version"] == "3.1"


def test_v31_numeric_acceptance_allows_nonidentical_output_and_preserves_observed_hash(
    tmp_path: Path,
):
    receipt = _write_local_v3(tmp_path)
    result = reproduce_receipt(receipt, timeout=30)
    assert result.ok, result.errors
    assert result.acceptance_mode == "NUMERIC_CHECKS"
    assert result.numerical_checks == 1
    assert result.output_assurance_counts["semantic"] == 1
    observed = result.observed_output_hashes["outputs/result.json"]
    expected_observed = _sha256(b'{"value": 1.0004}\n')
    assert observed == expected_observed
    assert any("observed output sha256" in check for check in result.checks)


def test_v31_exact_acceptance_rejects_reference_hash_mismatch(tmp_path: Path):
    receipt = _write_local_v3(
        tmp_path,
        acceptance="EXACT_SHA256",
        reference_sha256="0" * 64,
    )
    (tmp_path / "outputs").mkdir()
    (tmp_path / "outputs" / "result.json").write_bytes(b'{"value": 1.0004}\n')
    result = verify_receipt(receipt)
    assert not result.ok
    assert any("reference sha256 mismatch" in error for error in result.errors)


def test_v31_semantic_output_must_reference_declared_check_for_same_output(tmp_path: Path):
    receipt = _write_local_v3(tmp_path)
    document = load_structured(receipt)
    document["outputs"][0]["semantic_check_ids"] = ["MISSING-CHECK"]
    receipt.write_text(yaml.safe_dump(document, sort_keys=False), encoding="utf-8")
    result = verify_receipt(receipt)
    assert not result.ok
    assert any("references unknown check" in error for error in result.errors)


def test_v31_record_only_output_does_not_claim_semantic_equivalence(tmp_path: Path):
    receipt = _write_local_v3(tmp_path)
    document = load_structured(receipt)
    document["outputs"].append(
        {"path": "outputs/trace.txt", "assurance": "RECORD_ONLY"}
    )
    code = (tmp_path / "analysis.py").read_text(encoding="utf-8")
    code += "Path('outputs/trace.txt').write_text('trace\\n', encoding='utf-8')\n"
    code_bytes = code.encode("utf-8")
    (tmp_path / "analysis.py").write_bytes(code_bytes)
    document["code"][0]["sha256"] = _sha256(code_bytes)
    receipt.write_text(yaml.safe_dump(document, sort_keys=False), encoding="utf-8")
    result = reproduce_receipt(receipt, timeout=30)
    assert result.ok, result.errors
    assert result.output_assurance_counts["record_only"] == 1
    assert any("record-only output recorded" in check for check in result.checks)


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
    (tmp_path / "outputs" / "result.json").write_bytes(b'{"value": 1.0004}\n')
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
    (tmp_path / "outputs" / "result.json").write_bytes(b'{"value": 1.0004}\n')
    result = verify_receipt(receipt)
    assert not result.ok
    assert any(
        "REVIEW_REQUIRED: calibration evidence is missing" in error
        for error in result.errors
    )


def test_v31_external_submission_collection_chronology_and_calibration_are_bound():
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


def _copy_external_fixture(tmp_path: Path) -> Path:
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
    receipt = tmp_path / "receipt.yaml"
    receipt.write_text(yaml.safe_dump(document, sort_keys=False), encoding="utf-8")
    return receipt


def test_v31_external_chronology_inversion_fails_closed(tmp_path: Path):
    receipt = _copy_external_fixture(tmp_path)
    document = load_structured(receipt)
    document["execution"]["collection_receipt"]["started_at"] = "2026-09-13T00:06:00Z"
    receipt.write_text(yaml.safe_dump(document, sort_keys=False), encoding="utf-8")
    result = verify_receipt(receipt)
    assert not result.ok
    assert any("external execution chronology" in error for error in result.errors)


def test_v31_external_execution_outside_calibration_window_fails(tmp_path: Path):
    receipt = _copy_external_fixture(tmp_path)
    document = load_structured(receipt)
    instrument = document["calibration"]["instruments"][0]
    instrument["valid_until"] = "2026-09-13T00:02:00Z"
    receipt.write_text(yaml.safe_dump(document, sort_keys=False), encoding="utf-8")
    result = verify_receipt(receipt)
    assert not result.ok
    assert any("does not cover declared execution interval" in error for error in result.errors)


def test_v31_external_job_mismatch_and_failed_terminal_state_fail_closed(tmp_path: Path):
    receipt = _copy_external_fixture(tmp_path)
    document = load_structured(receipt)
    document["execution"]["collection_receipt"]["job_ref"] = "OTHER-JOB"
    document["execution"]["collection_receipt"]["terminal_state"] = "FAILED"
    receipt.write_text(yaml.safe_dump(document, sort_keys=False), encoding="utf-8")
    result = verify_receipt(receipt)
    assert not result.ok
    assert any("job_ref values must match" in error for error in result.errors)
    assert any("external job did not succeed" in error for error in result.errors)


def test_v31_external_receipt_is_not_executed_as_local_subprocess():
    result = reproduce_receipt(EXTERNAL_EXAMPLE, timeout=30)
    assert not result.ok
    assert any("collection-verification only" in error for error in result.errors)


def test_v30_legacy_shape_remains_verifiable(tmp_path: Path):
    receipt = _write_local_v3(tmp_path, version="3.0")
    (tmp_path / "outputs").mkdir()
    (tmp_path / "outputs" / "result.json").write_bytes(b'{"value": 1.0004}\n')
    result = verify_receipt(receipt)
    assert result.ok, result.errors


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


# --- FMA-NUM-01 / FMA-NUM-02 regressions ------------------------------------


def _retune_check(receipt_path: Path, **overrides: object) -> None:
    document = yaml.safe_load(receipt_path.read_text(encoding="utf-8"))
    document["checks"][0].update(overrides)
    receipt_path.write_text(yaml.safe_dump(document, sort_keys=False), encoding="utf-8")


def test_v3_non_finite_tolerance_is_rejected(tmp_path: Path):
    """Infinite or NaN tolerance must never produce a numerical PASS.

    math.isclose(x, y, abs_tol=inf) is unconditionally true, and a NaN
    tolerance silently degrades to exact equality. YAML resolves .inf/.nan,
    so both reach the comparison as ordinary floats.
    """
    for field in ("atol", "rtol"):
        for bad in (float("inf"), float("-inf"), float("nan")):
            path = _write_local_v3(tmp_path, value=99999.0)
            _retune_check(path, **{field: bad})
            result = reproduce_receipt(path, timeout=30)
            assert not result.ok, f"{field}={bad} must not pass"
            assert any("must be finite" in e or "non-negative" in e for e in result.errors)


@pytest.mark.parametrize("literal", ["Infinity", "-Infinity", "NaN"])
def test_v3_non_finite_observed_value_is_rejected(tmp_path: Path, literal: str):
    """FMA-NUM-TEST-02: each pathological observed literal locked individually.

    json.loads accepts bare Infinity/-Infinity/NaN even though JSON does not
    define them, so a producer can emit them without any parse error.
    """
    path = _write_local_v3(tmp_path)
    outputs = tmp_path / "outputs"
    outputs.mkdir(exist_ok=True)
    (outputs / "result.json").write_text(f'{{"value": {literal}}}\n', encoding="utf-8")
    result = verify_receipt(path)
    assert not result.ok
    assert any("observed must be finite" in e for e in result.errors)


@pytest.mark.parametrize("bad", [float("inf"), float("-inf"), float("nan")])
def test_v3_non_finite_expected_value_is_rejected(tmp_path: Path, bad: float):
    """FMA-NUM-TEST-02: a non-finite expectation is never a valid criterion."""
    path = _write_local_v3(tmp_path)
    _retune_check(path, expected=bad)
    outputs = tmp_path / "outputs"
    outputs.mkdir(exist_ok=True)
    (outputs / "result.json").write_text('{"value": 1.0}\n', encoding="utf-8")
    result = verify_receipt(path)
    assert not result.ok
    assert any("expected must be finite" in e for e in result.errors)


def test_v3_non_finite_observed_or_expected_is_rejected(tmp_path: Path):
    """The JSON decoder accepts bare Infinity/NaN; acceptance must not."""
    path = _write_local_v3(tmp_path)
    _retune_check(path, expected=float("inf"), atol=1e-12)
    outputs = tmp_path / "outputs"
    outputs.mkdir(exist_ok=True)
    # json.loads accepts bare Infinity even though JSON does not define it.
    (outputs / "result.json").write_text('{"value": Infinity}\n', encoding="utf-8")
    result = verify_receipt(path)
    assert not result.ok
    assert any("must be finite" in e for e in result.errors)


def test_v3_successful_numeric_check_reports_declared_tolerance(tmp_path: Path):
    """A wide tolerance is a valid declaration, but it must be visible.

    Without this, an atol of 1e-12 and an atol of 1e9 render identically.
    """
    path = _write_local_v3(tmp_path, value=99999.0)
    _retune_check(path, atol=1e9)
    result = reproduce_receipt(path, timeout=30)
    assert result.ok
    line = next(c for c in result.checks if c.startswith("numeric OK"))
    assert "atol=1000000000.0" in line
    assert "observed=99999.0" in line and "expected=1.0" in line


@pytest.mark.parametrize(
    "literal,fragment",
    [('"1.0"', "must be a number"), ("true", "must be a number")],
)
def test_v3_non_numeric_observed_value_is_rejected(tmp_path: Path, literal: str, fragment: str):
    """FMA-CONTRACT: float() promoted schema-invalid types into valid numbers.

    The schema declares these fields as JSON numbers; "1.0" and true are not.
    """
    path = _write_local_v3(tmp_path)
    outputs = tmp_path / "outputs"
    outputs.mkdir(exist_ok=True)
    (outputs / "result.json").write_text(f'{{"value": {literal}}}\n', encoding="utf-8")
    result = verify_receipt(path)
    assert not result.ok
    assert any(fragment in e for e in result.errors)


@pytest.mark.parametrize("bad", ["1.0", True, None])
def test_v3_non_numeric_expected_or_tolerance_is_rejected(tmp_path: Path, bad: object):
    for index, field in enumerate(("expected", "atol")):
        work = tmp_path / f"case{index}"
        work.mkdir()
        path = _write_local_v3(work)
        _retune_check(path, **{field: bad})
        (work / "outputs").mkdir(exist_ok=True)
        (work / "outputs" / "result.json").write_text('{"value": 1.0}\n', encoding="utf-8")
        result = verify_receipt(path)
        assert not result.ok
        assert any("must be a number" in e for e in result.errors)


def test_v3_over_range_integer_is_a_controlled_failure(tmp_path: Path):
    """An int too large for float raised OverflowError outside the handler."""
    path = _write_local_v3(tmp_path)
    _retune_check(path, expected=10**400)
    (tmp_path / "outputs").mkdir(exist_ok=True)
    (tmp_path / "outputs" / "result.json").write_text('{"value": 1.0}\n', encoding="utf-8")
    result = verify_receipt(path)
    assert not result.ok
    assert any("not representable as a float" in e for e in result.errors)


def test_numeric_receipt_version_is_rejected(tmp_path: Path):
    """FMA-CONTRACT-02: the v3 schema enumerates strings '3.0' and '3.1'."""
    path = _write_local_v3(tmp_path)
    document = yaml.safe_load(path.read_text(encoding="utf-8"))
    document["receipt_version"] = 3.1
    path.write_text(yaml.safe_dump(document, sort_keys=False), encoding="utf-8")
    result = verify_receipt(path)
    assert not result.ok
    assert any("receipt_version" in e for e in result.errors)
