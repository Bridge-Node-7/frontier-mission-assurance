from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HERE = (
    ROOT
    / "profiles"
    / "orbital-recovery-assurance"
    / "experiments"
    / "orbital-logistics-assurance-harness"
)

spec = importlib.util.spec_from_file_location("ola_harness", HERE / "assurance_harness.py")
assert spec is not None and spec.loader is not None
h = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = h
spec.loader.exec_module(h)


def load(name: str):
    return json.loads((HERE / "scenarios" / name).read_text(encoding="utf-8"))


def test_nominal_pre_service_is_eligible():
    result = h.evaluate(load("01_nominal_pre_service.json"))
    assert result["disposition"] == h.ELIGIBLE
    assert result["findings"] == []


def test_interface_mismatch_fails_closed():
    result = h.evaluate(load("02_interface_mismatch.json"))
    assert result["disposition"] == h.HOLD
    assert "INTERFACE_NOT_COMPATIBLE" in {x["code"] for x in result["findings"]}


def test_resource_custody_or_release_gap_fails_closed():
    result = h.evaluate(load("03_resource_release_gap.json"))
    assert result["disposition"] == h.HOLD
    assert "RESOURCE_RELEASE_UNAUTHORIZED" in {x["code"] for x in result["findings"]}


def test_model_outside_envelope_fails_closed():
    result = h.evaluate(load("04_model_outside_envelope.json"))
    assert result["disposition"] == h.HOLD
    assert "MODEL_APPLICABILITY_UNSUPPORTED" in {x["code"] for x in result["findings"]}


def test_post_action_authority_cannot_backfill_pre_action_authority():
    result = h.evaluate(load("05_authority_only_post_service.json"))
    assert result["disposition"] == h.HOLD
    assert "AUTHORITY_NOT_PRE_SERVICE" in {x["code"] for x in result["findings"]}


def test_failed_requalification_blocks_return_to_service():
    result = h.evaluate(load("06_failed_requalification.json"))
    assert result["disposition"] == h.HOLD
    assert "REQUALIFICATION_NOT_READY" in {x["code"] for x in result["findings"]}


def test_nominal_requalification_review_reaches_review_not_authorization():
    result = h.evaluate(load("07_nominal_requalification_review.json"))
    assert result["disposition"] == h.READY
    assert "does not authorize" in result["authority_note"]
    assert result["invariants"]["service_completion_does_not_equal_mission_requalification"]


def test_proof_request_output_is_candidate_only():
    result = h.evaluate(load("02_interface_mismatch.json"))
    assert result["proof_request_candidates"]
    assert all(
        "Mission Graph owns" in x["ownership_note"]
        for x in result["proof_request_candidates"]
    )


def test_post_service_stage_is_ready_for_requalification_review_only():
    result = h.evaluate(load("08_nominal_post_service_before_requalification.json"))
    assert result["disposition"] == h.READY_FOR_REQUALIFICATION
    assert "does not authorize" in result["authority_note"]


def test_unknown_phase_fails_closed():
    result = h.evaluate(load("09_invalid_phase.json"))
    assert result["disposition"] == h.HOLD
    assert "PHASE_INVALID" in {x["code"] for x in result["findings"]}


def test_non_object_input_fails_closed_without_exception():
    result = h.evaluate([])
    assert result["disposition"] == h.HOLD
    assert "CASE_INPUT_INVALID" in {x["code"] for x in result["findings"]}


def test_private_record_class_is_rejected_by_public_experiment():
    case = load("01_nominal_pre_service.json")
    case["record_class"] = "private"
    result = h.evaluate(case)
    assert result["disposition"] == h.HOLD
    assert "PUBLIC_RECORD_CLASS_INVALID" in {x["code"] for x in result["findings"]}


def test_missing_record_class_fails_closed():
    case = load("01_nominal_pre_service.json")
    case.pop("record_class")
    result = h.evaluate(case)
    assert result["disposition"] == h.HOLD
    assert "PUBLIC_RECORD_CLASS_INVALID" in {x["code"] for x in result["findings"]}


def test_experiment_runtime_is_stdlib_only_and_network_free():
    import ast

    source = (HERE / "assurance_harness.py").read_text(encoding="utf-8")
    tree = ast.parse(source)
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module.split(".")[0])
    assert imported <= {"__future__", "json", "sys", "dataclasses", "pathlib", "typing"}
    assert not imported & {"requests", "httpx", "urllib", "socket", "aiohttp", "boto3"}


def test_dispositions_remain_bounded_review_states():
    allowed = {h.HOLD, h.ELIGIBLE, h.READY_FOR_REQUALIFICATION, h.READY}
    for path in sorted((HERE / "scenarios").glob("*.json")):
        result = h.evaluate(json.loads(path.read_text(encoding="utf-8")))
        assert result["disposition"] in allowed


def test_cli_invalid_path_does_not_echo_local_path():
    missing = HERE / "sensitive-local-name-that-must-not-echo.json"
    completed = subprocess.run(
        [sys.executable, str(HERE / "assurance_harness.py"), str(missing)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert completed.returncode == 2
    assert completed.stderr.strip() == "invalid case input"
    assert str(missing) not in completed.stderr
