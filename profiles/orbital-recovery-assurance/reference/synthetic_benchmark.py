"""Deterministic synthetic known-truth benchmark for Orbital Recovery Assurance.

The benchmark is intentionally self-contained and synthetic. It evaluates the
reference option-assessment policy against preregistered naive baselines under a
declared generator. It does not establish real-world calibration or safety.
"""

from __future__ import annotations

import hashlib
import json
import math
import random
from pathlib import Path

import decision_kernel as d


def _true_eu(option: d.RecoveryOption, state: d.WorldState) -> float:
    p = option.p_success_given_state(state)
    return p * option.utility.u_success() + (1.0 - p) * option.utility.u_failure()


def _gate_clear(option: d.RecoveryOption, gates: d.GateInputs) -> bool:
    return gates.satisfies(option.required_gates)[0]


def _allowed(option: d.RecoveryOption, state: d.WorldState, gates: d.GateInputs) -> bool:
    return option.safe_under(state) and _gate_clear(option, gates)


def _brier(rows: list[tuple[float, int]]) -> float:
    return sum((p - y) ** 2 for p, y in rows) / len(rows)


def _log_loss(rows: list[tuple[float, int]]) -> float:
    eps = 1e-15
    return sum(
        -(y * math.log(max(p, eps)) + (1 - y) * math.log(max(1 - p, eps)))
        for p, y in rows
    ) / len(rows)


def _ece(rows: list[tuple[float, int]], bins: int = 10) -> float:
    buckets = [[] for _ in range(bins)]
    for probability, outcome in rows:
        index = min(bins - 1, int(probability * bins))
        buckets[index].append((probability, outcome))
    total = len(rows)
    error = 0.0
    for bucket in buckets:
        if not bucket:
            continue
        mean_p = sum(p for p, _ in bucket) / len(bucket)
        mean_y = sum(y for _, y in bucket) / len(bucket)
        error += (len(bucket) / total) * abs(mean_p - mean_y)
    return error


def _mean(values: list[float]) -> float:
    return sum(values) / len(values)


def _protocol_hash(protocol: dict) -> str:
    canonical = json.dumps(protocol, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(canonical).hexdigest()


def run(protocol: dict) -> dict:
    rng = random.Random(protocol["seed"])
    count = int(protocol["case_count"])

    rf_ok = d.WorldState("RF_OK", {"RF": d.PhysicalState.FUNCTIONAL})
    rf_dead = d.WorldState("RF_DEAD", {"RF": d.PhysicalState.FAILED})
    unstable = d.WorldState("UNSTABLE", {"RF": d.PhysicalState.FUNCTIONAL})
    states = (rf_ok, rf_dead, unstable)

    augment = d.RecoveryOption(
        name="external_augmentation",
        p_success_given_state=lambda state: (
            0.90 if state.label == "RF_OK" else 0.70 if state.label == "UNSTABLE" else 0.15
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
        safe_under=lambda state: state.label != "UNSTABLE",
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
    options = (augment, retire)
    base_success = {
        "external_augmentation": float(protocol["generator"]["augment_unconditional_success_rate"]),
        "controlled_retirement": 0.97,
    }

    baseline_names = tuple(protocol["safe_baselines"]) + tuple(protocol["contrast_baselines"])
    regret = {name: [] for name in ("policy", *baseline_names)}
    unsafe = {name: 0 for name in ("policy", *baseline_names)}
    choices = {name: {} for name in ("policy", *baseline_names)}
    model_forecasts: list[tuple[float, int]] = []
    base_forecasts: list[tuple[float, int]] = []

    for _index in range(count):
        stable_class = rng.random() < protocol["generator"]["stable_class_probability"]
        if stable_class:
            alpha, beta = protocol["generator"]["stable_posterior_beta"]
            q = rng.betavariate(alpha, beta)
            probabilities = [q, 1.0 - q, 0.0]
        else:
            alphas = protocol["generator"]["uncertain_posterior_dirichlet"]
            raw = [rng.gammavariate(alpha, 1) for alpha in alphas]
            total = sum(raw)
            probabilities = [value / total for value in raw]

        posterior = d.Posterior(tuple(zip(states, probabilities)))
        true_state = rng.choices(list(states), probabilities)[0]

        gates = d.GateInputs(
            {
                d.GateName.AUTHORITY: rng.random() < 0.90,
                d.GateName.COMMAND_TRUST: rng.random() < 0.82,
                d.GateName.APPROACH_SAFETY: rng.random() < 0.85,
                d.GateName.NATIVE_COMMAND_TRUST: rng.random() < 0.85,
            }
        )

        oracle = [("HOLD", protocol["hold_utility"])]
        oracle.extend(
            (option.name, _true_eu(option, true_state))
            for option in options
            if _allowed(option, true_state, gates)
        )
        _oracle_name, oracle_utility = max(oracle, key=lambda row: row[1])

        assessment = d.assess_options(
            posterior,
            options,
            gates,
            utility_space=protocol["utility_space"],
            credible_coverage=protocol["credible_coverage"],
            hold_utility=protocol["hold_utility"],
        )
        policy_name = assessment.highest_ranked_eligible_option or "HOLD"
        policy_option = next((o for o in options if o.name == policy_name), None)
        policy_utility = (
            protocol["hold_utility"]
            if policy_option is None
            else _true_eu(policy_option, true_state)
        )
        if policy_option is not None and not _allowed(policy_option, true_state, gates):
            unsafe["policy"] += 1
        regret["policy"].append(max(0.0, oracle_utility - policy_utility))
        choices["policy"][policy_name] = choices["policy"].get(policy_name, 0) + 1

        regret["always_hold"].append(max(0.0, oracle_utility - protocol["hold_utility"]))
        choices["always_hold"]["HOLD"] = choices["always_hold"].get("HOLD", 0) + 1

        retire_name = "controlled_retirement" if _gate_clear(retire, gates) else "HOLD"
        retire_utility = (
            _true_eu(retire, true_state)
            if retire_name != "HOLD"
            else protocol["hold_utility"]
        )
        if retire_name != "HOLD" and not _allowed(retire, true_state, gates):
            unsafe["always_retire_when_gate_clear"] += 1
        regret["always_retire_when_gate_clear"].append(
            max(0.0, oracle_utility - retire_utility)
        )
        choices["always_retire_when_gate_clear"][retire_name] = (
            choices["always_retire_when_gate_clear"].get(retire_name, 0) + 1
        )

        base_candidates = [("HOLD", protocol["hold_utility"])]
        for option in options:
            if _gate_clear(option, gates):
                p = base_success[option.name]
                eu = p * option.utility.u_success() + (1.0 - p) * option.utility.u_failure()
                base_candidates.append((option.name, eu))
        base_name, _base_expected = max(base_candidates, key=lambda row: row[1])
        base_option = next((o for o in options if o.name == base_name), None)
        base_utility = (
            protocol["hold_utility"]
            if base_option is None
            else _true_eu(base_option, true_state)
        )
        if base_option is not None and not _allowed(base_option, true_state, gates):
            unsafe["gate_only_base_rate_ranker"] += 1
        regret["gate_only_base_rate_ranker"].append(max(0.0, oracle_utility - base_utility))
        choices["gate_only_base_rate_ranker"][base_name] = (
            choices["gate_only_base_rate_ranker"].get(base_name, 0) + 1
        )

        true_p = augment.p_success_given_state(true_state)
        realized = 1 if rng.random() < true_p else 0
        model_forecasts.append((augment.p_success(posterior), realized))
        base_forecasts.append((base_success[augment.name], realized))

    result = {
        "benchmark_version": "1.2",
        "record_class": "synthetic",
        "protocol_sha256": _protocol_hash(protocol),
        "seed": protocol["seed"],
        "case_count": count,
        "policy": {
            "mean_decision_regret": _mean(regret["policy"]),
            "unsafe_action_rate": unsafe["policy"] / count,
            "choices": choices["policy"],
        },
        "safe_baselines": {},
        "contrast_baselines": {},
        "forecast": {
            "model_augment_brier": _brier(model_forecasts),
            "base_rate_augment_brier": _brier(base_forecasts),
            "model_augment_log_loss": _log_loss(model_forecasts),
            "base_rate_augment_log_loss": _log_loss(base_forecasts),
            "model_augment_ece_10bin": _ece(model_forecasts, 10),
            "base_rate_augment_ece_10bin": _ece(base_forecasts, 10),
        },
    }
    for name in protocol["safe_baselines"]:
        result["safe_baselines"][name] = {
            "mean_decision_regret": _mean(regret[name]),
            "unsafe_action_rate": unsafe[name] / count,
            "choices": choices[name],
        }
    for name in protocol["contrast_baselines"]:
        result["contrast_baselines"][name] = {
            "mean_decision_regret": _mean(regret[name]),
            "unsafe_action_rate": unsafe[name] / count,
            "choices": choices[name],
        }

    acceptance = protocol["acceptance"]
    checks = {
        "policy_unsafe_action_rate": (
            result["policy"]["unsafe_action_rate"]
            <= acceptance["policy_unsafe_action_rate_max"]
        ),
        "policy_regret_vs_safe_baselines": all(
            result["policy"]["mean_decision_regret"]
            < result["safe_baselines"][name]["mean_decision_regret"]
            for name in protocol["safe_baselines"]
        ),
        "forecast_brier_vs_base_rate": (
            result["forecast"]["model_augment_brier"]
            < result["forecast"]["base_rate_augment_brier"]
        ),
        "forecast_log_loss_vs_base_rate": (
            result["forecast"]["model_augment_log_loss"]
            < result["forecast"]["base_rate_augment_log_loss"]
        ),
    }
    result["acceptance_checks"] = checks
    result["status"] = "PASS" if all(checks.values()) else "FAIL"
    result["claim_boundary"] = protocol["claim_boundary"]
    return result


def run_from_paths(protocol_path: Path) -> dict:
    protocol = json.loads(protocol_path.read_text(encoding="utf-8"))
    return run(protocol)


def run_stress_matrix(protocol: dict, stress: dict) -> dict:
    runs = []
    for stable_probability in stress["stable_class_probabilities"]:
        for seed in stress["seeds"]:
            variant = json.loads(json.dumps(protocol))
            variant["seed"] = seed
            variant["case_count"] = stress["case_count_per_run"]
            variant["generator"]["stable_class_probability"] = stable_probability
            variant["generator"]["augment_unconditional_success_rate"] = (
                stable_probability * 0.65 + (1.0 - stable_probability) * 0.6625
            )
            result = run(variant)
            runs.append(
                {
                    "seed": seed,
                    "stable_class_probability": stable_probability,
                    "status": result["status"],
                    "policy_unsafe_action_rate": result["policy"]["unsafe_action_rate"],
                    "policy_mean_decision_regret": result["policy"]["mean_decision_regret"],
                    "always_hold_mean_decision_regret": result["safe_baselines"][
                        "always_hold"
                    ]["mean_decision_regret"],
                    "always_retire_mean_decision_regret": result["safe_baselines"][
                        "always_retire_when_gate_clear"
                    ]["mean_decision_regret"],
                    "model_augment_brier": result["forecast"]["model_augment_brier"],
                    "base_rate_augment_brier": result["forecast"]["base_rate_augment_brier"],
                }
            )
    return {
        "record_class": "synthetic",
        "run_count": len(runs),
        "runs": runs,
        "status": "PASS" if all(row["status"] == "PASS" for row in runs) else "FAIL",
        "claim_boundary": stress["claim_boundary"],
    }
