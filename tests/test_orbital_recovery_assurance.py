from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REF = ROOT / "profiles" / "orbital-recovery-assurance" / "reference"


def load(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, REF / filename)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


d = load("ora_decision_kernel_clean", "decision_kernel.py")
e = load("ora_evidence_validation_clean", "evidence_validation.py")
t = load("ora_timeline_metrics_clean", "timeline_metrics.py")


def base_case():
    rf_ok = d.WorldState("STATE-RF-AVAILABLE", {"RF": d.PhysicalState.FUNCTIONAL})
    rf_dead = d.WorldState("STATE-RF-UNAVAILABLE", {"RF": d.PhysicalState.FAILED})
    unstable = d.WorldState("STATE-UNSTABLE-ATTITUDE", {"RF": d.PhysicalState.FUNCTIONAL})
    posterior = d.Posterior(((rf_ok, 0.70), (rf_dead, 0.20), (unstable, 0.10)))
    augment = d.RecoveryOption(
        name="external_augmentation",
        p_success_given_state=lambda state: (
            0.90 if state.subsystems["RF"] == d.PhysicalState.FUNCTIONAL else 0.15
        ),
        utility=d.UtilityModel(
            v_mission=120,
            v_residual=10,
            v_learning_success=5,
            c_intervention=40,
            c_operations=8,
            c_liability_on_failure=20,
        ),
        required_gates=frozenset(
            {d.GateName.AUTHORITY, d.GateName.COMMAND_TRUST, d.GateName.APPROACH_SAFETY}
        ),
        safe_under=lambda state: state.label != "STATE-UNSTABLE-ATTITUDE",
    )
    retire = d.RecoveryOption(
        name="controlled_retirement",
        p_success_given_state=lambda _state: 0.97,
        utility=d.UtilityModel(
            v_learning_success=1,
            c_intervention=6,
            c_operations=2,
            c_liability_on_failure=1,
        ),
        required_gates=frozenset({d.GateName.AUTHORITY, d.GateName.NATIVE_COMMAND_TRUST}),
        safe_under=lambda _state: True,
    )
    return rf_ok, rf_dead, unstable, posterior, augment, retire


def test_fail_closed_preserves_human_authority():
    _, _, _, posterior, augment, retire = base_case()
    result = d.assess_options(
        posterior,
        (augment, retire),
        d.GateInputs({d.GateName.APPROACH_SAFETY: True}),
        utility_space="normalized_multi_attribute_v1",
    )
    assert result.disposition == d.HOLD
    assert result.highest_ranked_eligible_option is None
    assert "GO" not in result.disposition
    assert "PROCEED" not in result.disposition
    assert "does not authorize" in result.authorization_note


def test_default_robust_coverage_uses_all_nonzero_hypotheses():
    _, _, _, posterior, augment, retire = base_case()
    gates = d.GateInputs(
        {
            d.GateName.AUTHORITY: True,
            d.GateName.COMMAND_TRUST: True,
            d.GateName.APPROACH_SAFETY: True,
            d.GateName.NATIVE_COMMAND_TRUST: True,
        }
    )
    result = d.assess_options(
        posterior, (augment, retire), gates, utility_space="normalized_multi_attribute_v1"
    )
    assert result.credible_coverage == 1.0
    assert "external_augmentation" not in result.robust_options
    assert "controlled_retirement" in result.robust_options


def test_credible_set_rejects_vacuous_or_invalid_coverage():
    _, _, _, posterior, _, _ = base_case()
    for value in (0.0, 1.1):
        try:
            posterior.credible_set(value)
        except ValueError:
            pass
        else:
            raise AssertionError(f"coverage {value} should fail")


def test_option_specific_gates_can_clear_one_option():
    _, _, _, posterior, _, retire = base_case()
    gates = d.GateInputs(
        {d.GateName.AUTHORITY: True, d.GateName.NATIVE_COMMAND_TRUST: True}
    )
    result = d.assess_options(
        posterior, (retire,), gates, utility_space="normalized_multi_attribute_v1"
    )
    assert result.disposition == d.ELIGIBLE
    assert result.highest_ranked_eligible_option == "controlled_retirement"


def test_negative_value_observation_is_not_surfaced():
    _, _, _, posterior, _, retire = base_case()
    observation = d.Observation(
        "expensive_noop",
        999.0,
        (d.ObservationOutcome(1.0, posterior, d.GateInputs({})),),
    )
    result = d.assess_options(
        posterior,
        (retire,),
        d.GateInputs({}),
        utility_space="normalized_multi_attribute_v1",
        candidate_observations=(observation,),
    )
    assert result.next_best_observation is None


def test_probability_and_cost_inputs_fail_closed():
    rf_ok, rf_dead, _, posterior, _, _ = base_case()
    for invalid in (((rf_ok, 1.1), (rf_dead, -0.1)),):
        try:
            d.Posterior(invalid)
        except ValueError:
            pass
        else:
            raise AssertionError("invalid posterior should fail")
    try:
        d.Observation("bad", -1.0, (d.ObservationOutcome(1.0, posterior, d.GateInputs({})),))
    except ValueError:
        pass
    else:
        raise AssertionError("negative observation cost should fail")


def test_transitive_provenance_correlation_is_preserved():
    record = {
        "evidence": [
            {"id": "E1", "provenance_roots": {"clock_source": "CLOCK-1"}},
            {"id": "E2", "provenance_roots": {"clock_source": "CLOCK-1", "identity_source": "ID-2"}},
            {"id": "E3", "provenance_roots": {"identity_source": "ID-2"}},
            {"id": "E4", "provenance_roots": {"clock_source": "CLOCK-2"}},
        ]
    }
    assert e.provenance_correlation_components(record) == [["E1", "E2", "E3"], ["E4"]]


def test_unknown_provenance_is_conservative():
    assert e.provenance_correlation_components({"evidence": [{"id": "E1"}, {"id": "E2"}]}) == [["E1", "E2"]]


def test_time_to_trust_is_event_derived():
    first = t.compute_timeline_metrics({"anomaly_recognized": "2030-01-01T00:00:00Z", "trust_reestablished": "2030-01-01T00:28:00Z"})["TTT"]
    second = t.compute_timeline_metrics({"anomaly_recognized": "2030-01-01T00:00:00Z", "trust_reestablished": "2030-01-01T00:31:00Z"})["TTT"]
    assert first == 1680.0
    assert second == 1860.0


def test_recovery_chain_keeps_trust_and_authority_as_overlays():
    path = ROOT / "profiles" / "orbital-recovery-assurance" / "examples" / "synthetic-recovery-case" / "recovery-chain-view.json"
    view = json.loads(path.read_text(encoding="utf-8"))
    assert set(view["chain"]) == {"power", "contact", "telemetry", "command", "capability"}
    assert "trust" not in view["chain"]
    assert "authority" not in view["chain"]


def _private_case(case_dir: Path) -> None:
    src = ROOT / "profiles" / "orbital-recovery-assurance" / "examples" / "synthetic-recovery-case"
    for path in src.glob("*.json"):
        obj = json.loads(path.read_text(encoding="utf-8"))
        obj["record_class"] = "private"
        (case_dir / path.name).write_text(json.dumps(obj, indent=2) + "\n", encoding="utf-8")


def test_private_case_is_order_independent_and_requalification_ready():
    validator = ROOT / "scripts" / "validate_orbital_recovery_case.py"
    with tempfile.TemporaryDirectory() as tmp:
        case_dir = Path(tmp) / "case"
        case_dir.mkdir()
        _private_case(case_dir)
        for path in case_dir.glob("*.json"):
            obj = json.loads(path.read_text(encoding="utf-8"))
            path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        completed = subprocess.run([sys.executable, str(validator), str(case_dir), "--require-stage", "requalification-review"], capture_output=True, text=True, check=False)
        assert completed.returncode == 0, completed.stdout + completed.stderr


def test_private_case_fails_bad_evidence_reference_without_echoing_it_in_quiet_mode():
    validator = ROOT / "scripts" / "validate_orbital_recovery_case.py"
    with tempfile.TemporaryDirectory() as tmp:
        case_dir = Path(tmp) / "case"
        case_dir.mkdir()
        _private_case(case_dir)
        path = case_dir / "recovery-chain-view.json"
        obj = json.loads(path.read_text(encoding="utf-8"))
        obj["chain"]["telemetry"]["evidence_refs"] = ["EVIDENCE-NOT-THERE"]
        path.write_text(json.dumps(obj, indent=2) + "\n", encoding="utf-8")
        completed = subprocess.run([sys.executable, str(validator), str(case_dir), "--quiet"], capture_output=True, text=True, check=False)
        assert completed.returncode == 2
        assert "EVIDENCE-NOT-THERE" not in completed.stdout


def test_profile_validator_passes():
    completed = subprocess.run([sys.executable, str(ROOT / "scripts" / "validate_orbital_recovery_assurance.py"), str(ROOT)], capture_output=True, text=True, check=False)
    assert completed.returncode == 0, completed.stdout + completed.stderr


def test_synthetic_benchmark_is_deterministic_and_passes():
    command = [sys.executable, str(ROOT / "scripts" / "run_orbital_recovery_synthetic_benchmark.py"), str(ROOT)]
    first = subprocess.run(command, capture_output=True, text=True, check=False)
    second = subprocess.run(command, capture_output=True, text=True, check=False)
    assert first.returncode == 0, first.stdout + first.stderr
    assert second.returncode == 0, second.stdout + second.stderr
    assert first.stdout == second.stdout
    payload = json.loads(first.stdout)
    assert payload["primary"]["status"] == "PASS"
    assert payload["stress"]["status"] == "PASS"
    assert payload["primary"]["policy"]["unsafe_action_rate"] == 0.0
