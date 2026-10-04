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


def _bound_pre_service_records():
    evidence_record = {
        "record_class": "private",
        "record_id": "EVIDENCE-RECORD-BOUND-PRE",
        "asset_id": "ASSET-BOUND-001",
        "evidence": [{"id": "EVIDENCE-AUTH-BOUND"}],
    }
    option_assessment = {
        "record_class": "private",
        "assessment_id": "ASSESSMENT-BOUND-001",
        "evidence_record_ref": "EVIDENCE-RECORD-BOUND-PRE",
        "asset_id": "ASSET-BOUND-001",
        "disposition": "ELIGIBLE_FOR_DECISION_PREPARATION",
        "eligible_options": ["refuel_and_inspect"],
    }
    service_case = {
        "record_class": "private",
        "case_id": "BOUND-SERVICE-001",
        "phase": "pre_service",
        "pre_service_assessment": {
            "assessment_id": "ASSESSMENT-BOUND-001",
            "evidence_record_ref": "EVIDENCE-RECORD-BOUND-PRE",
            "service_option": "refuel_and_inspect",
        },
        "authority_evidence_refs": ["EVIDENCE-AUTH-BOUND"],
        "interfaces": [
            {
                "interface_id": "IF-BOUND-A",
                "state": "COMPATIBLE",
                "blockers": [],
            }
        ],
        "resources": [],
        "models": [],
        "service": {
            "execution_state": "NOT_EXECUTED",
            "verification_state": "NOT_ASSESSED",
        },
    }
    return service_case, evidence_record, option_assessment


def test_bound_private_case_reuses_governed_assessment_and_evidence():
    service_case, evidence_record, option_assessment = _bound_pre_service_records()
    result = h.evaluate_bound_case(
        service_case,
        evidence_record,
        option_assessment,
    )
    assert result["disposition"] == h.ELIGIBLE
    assert result["findings"] == []
    assert result["bound_records"]["pre_service_assessment"] == "ASSESSMENT-BOUND-001"
    assert result["bound_records"]["pre_service_evidence"] == "EVIDENCE-RECORD-BOUND-PRE"
    assert "does not duplicate or supersede" in result["binding_note"]


def test_bound_case_rejects_assessment_binding_mismatch():
    service_case, evidence_record, option_assessment = _bound_pre_service_records()
    service_case["pre_service_assessment"]["assessment_id"] = "ASSESSMENT-WRONG"
    result = h.evaluate_bound_case(
        service_case,
        evidence_record,
        option_assessment,
    )
    assert result["disposition"] == h.HOLD
    assert "UPSTREAM_ASSESSMENT_BINDING_MISMATCH" in {
        row["code"] for row in result["findings"]
    }


def test_bound_post_service_requires_governed_post_service_evidence():
    service_case, evidence_record, option_assessment = _bound_pre_service_records()
    service_case["phase"] = "post_service"
    service_case["post_service_evidence_record_ref"] = "EVIDENCE-RECORD-BOUND-POST"
    service_case["service"] = {
        "execution_state": "EXECUTED",
        "verification_state": "SUPPORTED",
    }
    result = h.evaluate_bound_case(
        service_case,
        evidence_record,
        option_assessment,
    )
    assert result["disposition"] == h.HOLD
    assert "POST_SERVICE_EVIDENCE_RECORD_MISSING" in {
        row["code"] for row in result["findings"]
    }


def test_bound_requalification_uses_governed_post_service_records():
    service_case, evidence_record, option_assessment = _bound_pre_service_records()
    service_case["phase"] = "requalification_review"
    service_case["post_service_evidence_record_ref"] = "EVIDENCE-RECORD-BOUND-POST"
    service_case["service"] = {
        "execution_state": "EXECUTED",
        "verification_state": "SUPPORTED",
    }
    service_case["requalification"] = {
        "requalification_id": "REQUAL-BOUND-001",
    }
    post_evidence_record = {
        "record_class": "private",
        "record_id": "EVIDENCE-RECORD-BOUND-POST",
        "asset_id": "ASSET-BOUND-001",
        "evidence": [{"id": "EVIDENCE-POST-BOUND"}],
    }
    requalification_record = {
        "record_class": "private",
        "requalification_id": "REQUAL-BOUND-001",
        "evidence_record_ref": "EVIDENCE-RECORD-BOUND-POST",
        "review_state": h.READY,
    }
    result = h.evaluate_bound_case(
        service_case,
        evidence_record,
        option_assessment,
        post_evidence_record=post_evidence_record,
        requalification_record=requalification_record,
    )
    assert result["disposition"] == h.READY
    assert result["findings"] == []
    assert result["bound_records"]["post_service_evidence"] == (
        "EVIDENCE-RECORD-BOUND-POST"
    )
    assert result["bound_records"]["requalification"] == "REQUAL-BOUND-001"


def test_bound_case_cli_reuses_private_orbital_recovery_validation(tmp_path):
    source = (
        ROOT
        / "profiles"
        / "orbital-recovery-assurance"
        / "examples"
        / "synthetic-recovery-case"
    )
    case_dir = tmp_path / "governed-case"
    case_dir.mkdir()
    for name in (
        "recovery-evidence-record.json",
        "recovery-chain-view.json",
        "recovery-option-assessment.json",
    ):
        record = json.loads((source / name).read_text(encoding="utf-8"))
        record["record_class"] = "private"
        (case_dir / name).write_text(
            json.dumps(record, indent=2) + "\n",
            encoding="utf-8",
        )

    assessment = json.loads(
        (case_dir / "recovery-option-assessment.json").read_text(encoding="utf-8")
    )
    evidence = json.loads(
        (case_dir / "recovery-evidence-record.json").read_text(encoding="utf-8")
    )
    service_case = {
        "record_class": "private",
        "case_id": "BOUND-CLI-001",
        "phase": "pre_service",
        "pre_service_assessment": {
            "assessment_id": assessment["assessment_id"],
            "evidence_record_ref": evidence["record_id"],
            "service_option": "controlled_retirement",
        },
        "authority_evidence_refs": ["EVIDENCE-004"],
        "interfaces": [
            {
                "interface_id": "IF-BOUND-CLI",
                "state": "COMPATIBLE",
                "blockers": [],
            }
        ],
        "resources": [],
        "models": [],
        "service": {
            "execution_state": "NOT_EXECUTED",
            "verification_state": "NOT_ASSESSED",
        },
    }
    service_path = tmp_path / "service-assurance-case.json"
    service_path.write_text(
        json.dumps(service_case, indent=2) + "\n",
        encoding="utf-8",
    )

    completed = subprocess.run(
        [
            sys.executable,
            str(HERE / "bound_case.py"),
            str(case_dir),
            str(service_path),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    assert completed.returncode == 3
    result = json.loads(completed.stdout)
    assert result["disposition"] == h.HOLD
    assert result["bound_records"]["pre_service_assessment"] == (
        assessment["assessment_id"]
    )
    assert result["bound_records"]["pre_service_evidence"] == evidence["record_id"]


def test_integrated_logistics_enterprise_scenario_covers_all_function_families():
    case = load("10_integrated_logistics_enterprise.json")
    assert set(case["demonstrated_functions"]) == {
        "resource_management",
        "transfer_vehicle_integration",
        "network_coordination",
        "orbital_warehousing",
        "service_recovery",
        "health_monitoring",
    }
    result = h.evaluate(case)
    assert result["disposition"] == h.ELIGIBLE
    assert result["findings"] == []
    assert len(case["interfaces"]) == 3
    assert len(case["resources"]) == 2
    assert len(case["models"]) == 2


def test_integrated_logistics_enterprise_fails_closed_on_cross_system_breaks():
    import copy

    base = load("10_integrated_logistics_enterprise.json")

    broken_interface = copy.deepcopy(base)
    broken_interface["interfaces"][1]["state"] = "INCOMPATIBLE"
    assert h.evaluate(broken_interface)["disposition"] == h.HOLD

    held_resource = copy.deepcopy(base)
    held_resource["resources"][0]["release_state"] = "HELD"
    assert h.evaluate(held_resource)["disposition"] == h.HOLD

    invalid_model = copy.deepcopy(base)
    invalid_model["models"][0]["applicability"] = "OUTSIDE_ENVELOPE"
    assert h.evaluate(invalid_model)["disposition"] == h.HOLD

    missing_authority = copy.deepcopy(base)
    missing_authority["authority_evidence_refs"] = []
    assert h.evaluate(missing_authority)["disposition"] == h.HOLD
