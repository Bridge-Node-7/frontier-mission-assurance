from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "evaluate_ftqc_reference.py"


def _load_evaluator():
    spec = importlib.util.spec_from_file_location("ftqc_reference_test", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


evaluator = _load_evaluator()


def test_ftqc_profile_release_surface_is_present():
    required = [
        ROOT / "profiles" / "ftqc-assurance" / "README.md",
        ROOT / "profiles" / "ftqc-assurance" / "PROFILE_CONTRACT.md",
        ROOT / "profiles" / "ftqc-assurance" / "ASSURANCE_SCOPE.md",
        ROOT / "profiles" / "ftqc-assurance" / "schemas" / "ftqc-system-concept.schema.json",
        ROOT / "profiles" / "ftqc-assurance" / "schemas" / "resource-estimate-receipt.schema.json",
        ROOT / "profiles" / "ftqc-assurance" / "schemas" / "evidence-validity-envelope.schema.json",
        ROOT / "profiles" / "ftqc-assurance" / "schemas" / "expert-adjudication-record.schema.json",
        ROOT / "scripts" / "validate_ftqc_assurance.py",
        ROOT / "scripts" / "evaluate_ftqc_reference.py",
    ]
    assert all(path.is_file() for path in required)


def test_profile_validator_passes():
    completed = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "validate_ftqc_assurance.py"), str(ROOT)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert "FTQC ASSURANCE PROFILE PASS" in completed.stdout


def test_changed_assumption_produces_expected_impact():
    result = evaluator.evaluate_case(ROOT)
    expected = json.loads(
        (ROOT / "profiles" / "ftqc-assurance" / "examples" / "synthetic-neutral-atom" / "changed-assumption" / "expected-impact.json").read_text(encoding="utf-8")
    )
    assert result["change"] == expected
    assert result["baseline"]["technical_decision_readiness"] == "HOLD"


def test_evaluator_is_deterministic_and_human_readable():
    command = [sys.executable, str(SCRIPT), str(ROOT)]
    first = subprocess.run(command, capture_output=True, text=True, check=False)
    second = subprocess.run(command, capture_output=True, text=True, check=False)
    assert first.returncode == 0, first.stdout + first.stderr
    assert second.returncode == 0, second.stdout + second.stderr
    assert first.stdout == second.stdout
    assert "SOFTWARE / CONTRACT VALIDATION\nPASS" in first.stdout
    assert "TECHNICAL DECISION READINESS\nHOLD" in first.stdout
    assert "decision reopen required: TRUE" in first.stdout
    assert first.stdout.rstrip().endswith("RESULT - FTQC REFERENCE EVALUATION PASS")


def test_declared_applicability_does_not_become_established_by_structure():
    envelopes = json.loads(
        (ROOT / "profiles" / "ftqc-assurance" / "examples" / "synthetic-neutral-atom" / "baseline" / "evidence-envelopes.json").read_text(encoding="utf-8")
    )
    loss = next(item for item in envelopes["envelopes"] if item["envelope_id"] == "ENV-LOSS-001")
    assert loss["basis"]["type"] == "declared_assumption"
    assert loss["review"]["authority_state"] == "DECLARED"
    assert loss["review"]["decision_gate"] is True


def test_stable_release_reverifies_ftqc_profile_and_reference():
    workflow = (ROOT / ".github" / "workflows" / "release.yml").read_text(encoding="utf-8")
    assert "python scripts/validate_ftqc_assurance.py ." in workflow
    assert "python scripts/evaluate_ftqc_reference.py ." in workflow
    assert workflow.count("scripts/validate_ftqc_assurance.py .") >= 2
    assert workflow.count("scripts/evaluate_ftqc_reference.py .") >= 2
