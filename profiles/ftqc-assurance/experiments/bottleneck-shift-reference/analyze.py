#!/usr/bin/env python3
"""Source-neutral, deterministic bottleneck-shift sensitivity analysis.

This is a synthetic arithmetic exercise, NOT a quantum resource estimator.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

STAGES = ("preparation", "circuit_generation", "quantum_execution", "readout")
MAX_SCENARIOS = 32
MAX_OPTIONS = 16


class CaseError(ValueError):
    """Input does not satisfy the declared synthetic comparison contract."""


def _positive_number(value: object, field: str, *, allow_zero: bool = False) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise CaseError(f"{field}: expected numeric value")
    number = float(value)
    if not math.isfinite(number) or number < 0 or (number == 0 and not allow_zero):
        raise CaseError(f"{field}: expected finite {'nonnegative' if allow_zero else 'positive'} value")
    return number


def _required_dict(value: object, field: str) -> dict:
    if not isinstance(value, dict):
        raise CaseError(f"{field}: expected object")
    return value


def _ids(values: object, field: str, minimum: int, maximum: int) -> list[str]:
    if not isinstance(values, list) or not minimum <= len(values) <= maximum:
        raise CaseError(f"{field}: expected {minimum}..{maximum} identifiers")
    if any(not isinstance(v, str) or not v or len(v) > 64 for v in values):
        raise CaseError(f"{field}: identifiers must be nonempty strings <=64 characters")
    if len(values) != len(set(values)):
        raise CaseError(f"{field}: duplicate identifiers")
    return values


def evaluate(case: object) -> dict:
    case = _required_dict(case, "case")
    if set(case) != {"schema_version", "case_id", "evidence_class", "unit", "baseline", "options", "min_speedup", "scenarios", "unverified_gates"}:
        raise CaseError("case: required keys only; no implicit defaults")
    if case["schema_version"] != "1.0" or case["evidence_class"] != "SYNTHETIC":
        raise CaseError("Only synthetic case schema_version 1.0 supported")
    if not isinstance(case["case_id"], str) or not case["case_id"].startswith("SYN-"):
        raise CaseError("case_id must have SYN- prefix")
    if case["unit"] != "synthetic_latency_units":
        raise CaseError("Unit must be synthetic_latency_units; no hardware timing implied")
    options = _ids(case["options"], "options", 2, MAX_OPTIONS)
    baseline = case["baseline"]
    if baseline not in options:
        raise CaseError("baseline not in options")
    min_speedup = _positive_number(case["min_speedup"], "min_speedup")
    if min_speedup <= 1:
        raise CaseError("min_speedup must be >1 for meaningful improvement")
    gates = _ids(case["unverified_gates"], "unverified_gates", 1, 20)
    scenario_inputs = case["scenarios"]
    if not isinstance(scenario_inputs, list) or not 1 <= len(scenario_inputs) <= MAX_SCENARIOS:
        raise CaseError("scenarios must be 1..32")
    scenarios = []
    scenario_ids = set()
    aggregate = {option: [] for option in options if option != baseline}
    for idx, scenario in enumerate(scenario_inputs):
        scenario = _required_dict(scenario, f"scenarios[{idx}]")
        if set(scenario) != {"id", "durations"}:
            raise CaseError("scenario requires id and durations only")
        scenario_id = scenario["id"]
        if not isinstance(scenario_id, str) or not scenario_id or scenario_id in scenario_ids:
            raise CaseError("scenario id missing or duplicate")
        scenario_ids.add(scenario_id)
        entries = _required_dict(scenario["durations"], "scenario.durations")
        if set(entries) != set(options):
            raise CaseError(f"{scenario_id}: options must match the declared options exactly")
        measures = {}
        for option in options:
            stages = _required_dict(entries[option], f"{scenario_id}.{option}")
            if set(stages) != set(STAGES):
                raise CaseError(f"{scenario_id}.{option}: stage names do not match contract")
            numbers = {stage: _positive_number(stages[stage], f"{scenario_id}.{option}.{stage}", allow_zero=True) for stage in STAGES}
            total = sum(numbers.values())
            if total <= 0 or not math.isfinite(total):
                raise CaseError(f"{scenario_id}.{option}: invalid total")
            maximum = max(numbers.values())
            measures[option] = {
                "total": round(total, 6),
                "dominant_stages": [stage for stage in STAGES if numbers[stage] == maximum],
            }
        baseline_total = measures[baseline]["total"]
        comparisons = {}
        for option in options:
            if option == baseline:
                continue
            speedup = baseline_total / measures[option]["total"]
            if not math.isfinite(speedup):
                raise CaseError(f"{scenario_id}.{option}: invalid speedup")
            aggregate[option].append(speedup)
            comparisons[option] = {
                **measures[option],
                "baseline_relative_speedup": round(speedup, 6),
                "dominant_stage_shift": measures[option]["dominant_stages"] != measures[baseline]["dominant_stages"],
            }
        scenarios.append({"id": scenario_id, "baseline": measures[baseline], "alternatives": comparisons})
    alternatives = {}
    for option, ratios in aggregate.items():
        alternatives[option] = {
            "worst_case_speedup": round(min(ratios), 6),
            "all_scenarios_meet_target": all(value >= min_speedup for value in ratios),
        }
    return {
        "case_id": case["case_id"],
        "evaluation_kind": "SYNTHETIC_ARITHMETIC_ONLY",
        "decision_authority": "HUMAN_REVIEW_REQUIRED",
        "scientific_claim": "NONE",
        "stage_model": "SEQUENTIAL_SUM; dominant stage is largest modeled contribution, not a proved binding constraint",
        "unit": case["unit"],
        "target_speedup": min_speedup,
        "scenarios": scenarios,
        "alternatives": alternatives,
        "unverified_gates": gates,
        "decision_posture": "HOLD_PENDING_REAL_WORKLOAD_AND_EXPERT_REVIEW",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("case", type=Path, help="Bounded synthetic JSON fixture")
    parser.add_argument("--output", type=Path, help="Optional generated JSON report location")
    args = parser.parse_args()
    try:
        result = evaluate(json.loads(args.case.read_text(encoding="utf-8")))
    except (CaseError, json.JSONDecodeError, UnicodeError, OSError) as exc:
        parser.exit(2, f"NO_RESULT: {exc}\n")
    encoded = json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + "\n"
    if args.output:
        args.output.write_text(encoded, encoding="utf-8")
    else:
        print(encoded, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
