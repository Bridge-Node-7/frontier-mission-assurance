from __future__ import annotations

import importlib.util
import json
import math
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


d = load("ora_decision_kernel_closure", "decision_kernel.py")
e = load("ora_evidence_validation_closure", "evidence_validation.py")
h = load("ora_hindcast_metrics_closure", "hindcast_metrics.py")
t = load("ora_timeline_metrics_closure", "timeline_metrics.py")


def base_case():
    rf_ok = d.WorldState("STATE-RF-AVAILABLE", {"RF": d.PhysicalState.FUNCTIONAL})
    rf_dead = d.WorldState("STATE-RF-UNAVAILABLE", {"RF": d.PhysicalState.FAILED})
    unstable = d.WorldState("STATE-UNSTABLE-ATTITUDE", {"RF": d.PhysicalState.FUNCTIONAL})
    posterior = d.Posterior(((rf_ok, 0.70), (rf_dead, 0.20), (unstable, 0.10)))
    augment = d.RecoveryOption(
        name="external_augmentation",
        p_success_given_state=lambda state: 0.90 if state.subsystems["RF"] == d.PhysicalState.FUNCTIONAL else 0.15,
        utility=d.UtilityModel(v_mission=120, v_residual=10, v_learning_success=5, c_intervention=40, c_operations=8, c_liability_on_failure=20),
        required_gates=frozenset({d.GateName.AUTHORITY, d.GateName.COMMAND_TRUST, d.GateName.APPROACH_SAFETY}),
        safe_under=lambda state: state.label != "STATE-UNSTABLE-ATTITUDE",
    )
    retire = d.RecoveryOption(
        name="controlled_retirement",
        p_success_given_state=lambda _state: 0.97,
        utility=d.UtilityModel(v_learning_success=1, c_intervention=6, c_operations=2, c_liability_on_failure=1),
        required_gates=frozenset({d.GateName.AUTHORITY, d.GateName.NATIVE_COMMAND_TRUST}),
        safe_under=lambda _state: True,
    )
    return rf_ok, rf_dead, posterior, augment, retire


def test_nevoi_uses_admissible_policy():
    rf_ok, _, posterior, augment, retire = base_case()
    post_good = d.Posterior(((rf_ok, 1.0),))
    gates = d.GateInputs({d.GateName.AUTHORITY: True, d.GateName.COMMAND_TRUST: True, d.GateName.APPROACH_SAFETY: True, d.GateName.NATIVE_COMMAND_TRUST: True})
    obs = d.Observation("remote_characterization", 1.0, (d.ObservationOutcome(0.8, post_good, gates), d.ObservationOutcome(0.2, posterior, d.GateInputs({}))))
    assert math.isfinite(d.nevoi(obs, posterior, (augment, retire), d.GateInputs({})))


def test_hold_baseline_prevents_forced_negative_action():
    _, _, posterior, _, retire = base_case()
    gates = d.GateInputs({d.GateName.AUTHORITY: True, d.GateName.NATIVE_COMMAND_TRUST: True})
    result = d.assess_options(posterior, (retire,), gates, utility_space="u", hold_utility=0.0)
    assert result.ranked_all[0][1] < 0.0
    obs = d.Observation("gate_only_review", 1.0, (d.ObservationOutcome(1.0, posterior, gates),))
    assert d.nevoi(obs, posterior, (retire,), d.GateInputs({}), hold_utility=0.0) == -1.0


def test_all_robust_gate_failures_are_visible():
    _, _, posterior, _, retire = base_case()
    result = d.assess_options(posterior, (retire,), d.GateInputs({}), utility_space="u")
    assert any("authority" in reason for reason in result.hold_reasons)
    assert any("native_command_trust" in reason for reason in result.hold_reasons)


def test_hindcast_metrics():
    forecasts = [h.BinaryForecast(0.8, 1), h.BinaryForecast(0.3, 0)]
    assert abs(h.brier_score(forecasts) - 0.065) < 1e-12
    assert h.log_loss(forecasts) > 0
    assert h.mean_decision_regret([h.DecisionCase(8, 10), h.DecisionCase(5, 5)]) == 1.0


def test_nevoi_ignores_improvement_to_still_inadmissible_option():
    rf_ok = d.WorldState("STATE-X", {"RF": d.PhysicalState.FUNCTIONAL})
    posterior = d.Posterior(((rf_ok, 1.0),))
    option = d.RecoveryOption("augmentation_x", lambda _s: 0.99, d.UtilityModel(v_mission=100, c_intervention=1), frozenset({d.GateName.AUTHORITY, d.GateName.COMMAND_TRUST}), lambda _s: True)
    obs = d.Observation("better_but_still_untrusted", 2.0, (d.ObservationOutcome(1.0, posterior, d.GateInputs({})),))
    assert d.nevoi(obs, posterior, (option,), d.GateInputs({}), hold_utility=0.0) == -2.0


def test_missing_requalification_evidence_is_unresolved():
    record = {"evidence": [{"id": "EVIDENCE-OK"}]}
    assert e.resolve_refs(["EVIDENCE-OK", "EVIDENCE-MISSING"], [record]) == ["EVIDENCE-MISSING"]


def test_timeline_metrics_include_ttv():
    metrics = t.compute_timeline_metrics({"anomaly_recognized": "2030-01-01T00:00:00Z", "trust_reestablished": "2030-01-01T00:28:00Z", "recovery_verified": "2030-01-01T00:35:00Z"})
    assert metrics["TTT"] == 1680.0
    assert metrics["TTV"] == 2100.0


def test_recovery_chain_overlay_keys_present():
    view = json.loads((ROOT / "profiles/orbital-recovery-assurance/examples/synthetic-recovery-case/recovery-chain-view.json").read_text())
    assert "command_path" in view["trust_overlay"]
    assert "command_authority" in view["authority_overlay"]


def test_recovery_chain_nonunknown_stages_have_evidence():
    view = json.loads((ROOT / "profiles/orbital-recovery-assurance/examples/synthetic-recovery-case/recovery-chain-view.json").read_text())
    for stage in view["chain"].values():
        if stage["state"] != "unknown":
            assert stage["evidence_refs"]


def _load_private_validator():
    path = ROOT / "scripts/validate_orbital_recovery_case.py"
    spec = importlib.util.spec_from_file_location("ora_private_case_closure", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules["ora_private_case_closure"] = module
    spec.loader.exec_module(module)
    return module


def _private_case(case: Path, names: tuple[str, ...] | None = None):
    src = ROOT / "profiles/orbital-recovery-assurance/examples/synthetic-recovery-case"
    paths = list(src.glob("*.json")) if names is None else [src / n for n in names]
    for path in paths:
        obj = json.loads(path.read_text())
        obj["record_class"] = "private"
        (case / path.name).write_text(json.dumps(obj, indent=2) + "\n")


def test_private_case_direct_validation():
    validator = _load_private_validator()
    with tempfile.TemporaryDirectory() as td:
        case = Path(td)
        _private_case(case)
        assert validator.validate_case(case, ROOT, "requalification-review") == []


def test_profile_contract_version_consistency():
    profile = ROOT / "profiles/orbital-recovery-assurance"
    for path in (profile / "schemas").glob("*.json"):
        schema = json.loads(path.read_text())
        assert schema["properties"]["profile_version"]["const"] == "0.5"
        assert "private" in schema["properties"]["record_class"]["enum"]
    for path in (profile / "examples/synthetic-recovery-case").glob("*.json"):
        record = json.loads(path.read_text())
        assert record["profile_version"] == "0.5"
        assert record["record_class"] == "synthetic"


def test_nonrobust_option_names_unsafe_hypothesis():
    ok = d.WorldState("STATE-OK", {"RF": d.PhysicalState.FUNCTIONAL})
    unsafe = d.WorldState("STATE-UNSAFE", {"RF": d.PhysicalState.FUNCTIONAL})
    posterior = d.Posterior(((ok, 0.9), (unsafe, 0.1)))
    option = d.RecoveryOption("contact_action", lambda _s: 0.9, d.UtilityModel(v_mission=10), frozenset(), lambda s: s.label != "STATE-UNSAFE")
    result = d.assess_options(posterior, (option,), d.GateInputs({}), utility_space="u")
    assert result.option_findings[0].unsafe_hypotheses == ("STATE-UNSAFE",)


def test_mapped_case_does_not_satisfy_assessed_gate():
    validator = _load_private_validator()
    with tempfile.TemporaryDirectory() as td:
        case = Path(td)
        _private_case(case, ("recovery-evidence-record.json", "recovery-chain-view.json"))
        assert validator.validate_case(case, ROOT, "mapped") == []
        assert any("required stage 'assessed' is incomplete" in p for p in validator.validate_case(case, ROOT, "assessed"))
