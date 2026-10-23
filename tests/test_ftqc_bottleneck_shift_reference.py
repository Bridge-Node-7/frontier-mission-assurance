"""Boundary and regression tests for a synthetic bottleneck shift exercise."""

import copy
import importlib.util
import json
from pathlib import Path
import unittest

HERE = (Path(__file__).resolve().parents[1] / "profiles" / "ftqc-assurance" / "experiments" / "bottleneck-shift-reference")
spec = importlib.util.spec_from_file_location("synthetic_bottleneck_shift", HERE / "analyze.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class BottleneckShiftTests(unittest.TestCase):
    def setUp(self):
        self.case = json.loads((HERE / "case.json").read_text(encoding="utf-8"))

    def test_reference_expected_results(self):
        result = module.evaluate(self.case)
        self.assertEqual(result["evaluation_kind"], "SYNTHETIC_ARITHMETIC_ONLY")
        self.assertEqual(result["scenarios"][0]["baseline"]["total"], 1400)
        self.assertEqual(result["scenarios"][1]["baseline"]["total"], 1500)
        self.assertEqual(result["scenarios"][0]["baseline"]["dominant_stages"], ["circuit_generation"])
        self.assertEqual(result["scenarios"][0]["alternatives"]["circuit_restructure"]["dominant_stages"], ["preparation"])
        self.assertAlmostEqual(result["scenarios"][0]["alternatives"]["circuit_restructure"]["baseline_relative_speedup"], 1400 / 540, places=5)
        self.assertFalse(result["alternatives"]["circuit_restructure"]["all_scenarios_meet_target"])
        self.assertTrue(result["alternatives"]["hybrid_restructure"]["all_scenarios_meet_target"])
        self.assertEqual(result["decision_posture"], "HOLD_PENDING_REAL_WORKLOAD_AND_EXPERT_REVIEW")

    def test_deterministic(self):
        self.assertEqual(module.evaluate(self.case), module.evaluate(copy.deepcopy(self.case)))

    def test_unknown_evidence_class_refused(self):
        self.case["evidence_class"] = "REAL_HARDWARE"
        with self.assertRaises(module.CaseError):
            module.evaluate(self.case)

    def test_unverified_gates_required(self):
        self.case["unverified_gates"] = []
        with self.assertRaises(module.CaseError):
            module.evaluate(self.case)

    def test_missing_baseline_refused(self):
        del self.case["scenarios"][1]["durations"]["baseline"]
        with self.assertRaises(module.CaseError):
            module.evaluate(self.case)

    def test_negative_nonfinite_bool_refused(self):
        for invalid in (-1, float("nan"), float("inf"), True, "100"):
            with self.subTest(invalid=invalid):
                case = copy.deepcopy(self.case)
                case["scenarios"][0]["durations"]["baseline"]["preparation"] = invalid
                with self.assertRaises(module.CaseError):
                    module.evaluate(case)

    def test_zero_total_refused(self):
        self.case["scenarios"][0]["durations"]["baseline"] = dict.fromkeys(module.STAGES, 0)
        with self.assertRaises(module.CaseError):
            module.evaluate(self.case)

    def test_alternative_stage_mismatch_refused(self):
        del self.case["scenarios"][0]["durations"]["circuit_restructure"]["readout"]
        with self.assertRaises(module.CaseError):
            module.evaluate(self.case)

    def test_tied_dominant_stage_is_explicit(self):
        self.case["scenarios"][0]["durations"]["baseline"] = {
            "preparation": 500, "circuit_generation": 500, "quantum_execution": 300, "readout": 100
        }
        actual = module.evaluate(self.case)
        self.assertEqual(actual["scenarios"][0]["baseline"]["dominant_stages"], ["preparation", "circuit_generation"])

    def test_duplicate_scenarios_refused(self):
        self.case["scenarios"][1]["id"] = self.case["scenarios"][0]["id"]
        with self.assertRaises(module.CaseError):
            module.evaluate(self.case)

    def test_option_limit_enforced(self):
        self.case["options"] = self.case["options"] + [f"x-{i}" for i in range(15)]
        with self.assertRaises(module.CaseError):
            module.evaluate(self.case)

    def test_improvement_threshold_strict(self):
        self.case["min_speedup"] = 1
        with self.assertRaises(module.CaseError):
            module.evaluate(self.case)


if __name__ == "__main__":
    unittest.main()
