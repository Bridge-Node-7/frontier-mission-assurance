"""Small scoring primitives for preregistered recovery hindcasts.

These functions score predictions; they do not establish calibration. Calibration
claims require sufficiently large, representative, class-appropriate cohorts.
"""

from __future__ import annotations

import math
from dataclasses import dataclass


def _prob(value: float) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError("probability must be finite")
    if not 0.0 <= value <= 1.0:
        raise ValueError("probability must be in [0, 1]")
    return float(value)


@dataclass(frozen=True)
class BinaryForecast:
    probability: float
    outcome: int

    def __post_init__(self) -> None:
        _prob(self.probability)
        if self.outcome not in (0, 1):
            raise ValueError("outcome must be 0 or 1")


@dataclass(frozen=True)
class DecisionCase:
    chosen_utility: float
    best_available_utility: float

    def __post_init__(self) -> None:
        for value in (self.chosen_utility, self.best_available_utility):
            if (
                isinstance(value, bool)
                or not isinstance(value, (int, float))
                or not math.isfinite(value)
            ):
                raise ValueError("utilities must be finite")


def brier_score(cases: list[BinaryForecast]) -> float:
    if not cases:
        raise ValueError("at least one forecast is required")
    return sum((case.probability - case.outcome) ** 2 for case in cases) / len(cases)


def log_loss(cases: list[BinaryForecast]) -> float:
    if not cases:
        raise ValueError("at least one forecast is required")
    losses = []
    for case in cases:
        p = case.probability
        if (case.outcome == 1 and p == 0.0) or (case.outcome == 0 and p == 1.0):
            return math.inf
        losses.append(-(case.outcome * math.log(p) + (1 - case.outcome) * math.log(1 - p)))
    return sum(losses) / len(losses)


def mean_decision_regret(cases: list[DecisionCase]) -> float:
    if not cases:
        raise ValueError("at least one decision case is required")
    total = sum(
        max(0.0, case.best_available_utility - case.chosen_utility)
        for case in cases
    )
    return total / len(cases)
