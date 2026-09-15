"""Orbital Recovery Assurance reference option-assessment policy v0.5.

Bounded reference only:
- evaluates declared recovery options in one declared utility space,
- filters options through a robust-action envelope,
- applies intervention-specific fail-closed gates,
- selects positive net-value observations,
- never records or authorizes a consequential decision.

The posterior, intervention models, safety predicates, and gate states are declared inputs.
This module performs no inference and establishes no real-world recoverability, safety,
ownership, authority, readiness, or decision.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from enum import Enum
from typing import Callable, Optional, Sequence

__version__ = "0.5.0"
_SUM_TOL = 1e-9


def _finite(value: float, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError(f"{name} must be a finite number")
    return float(value)


def _prob(value: float, name: str) -> float:
    value = _finite(value, name)
    if not 0.0 <= value <= 1.0:
        raise ValueError(f"{name} must be in [0, 1]")
    return value


def _nonnegative(value: float, name: str) -> float:
    value = _finite(value, name)
    if value < 0.0:
        raise ValueError(f"{name} must be non-negative")
    return value


class PhysicalState(str, Enum):
    FUNCTIONAL = "functional"
    DEGRADED = "degraded"
    FAILED = "failed"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class WorldState:
    label: str
    subsystems: dict[str, PhysicalState]

    def __post_init__(self) -> None:
        if not self.label:
            raise ValueError("world-state label is required")
        if not self.subsystems:
            raise ValueError("at least one subsystem state is required")
        for key, state in self.subsystems.items():
            if not key or not isinstance(state, PhysicalState):
                raise ValueError("subsystem states must use PhysicalState")


@dataclass(frozen=True)
class Posterior:
    """Validated discrete P(x|E)."""

    items: tuple[tuple[WorldState, float], ...]

    def __post_init__(self) -> None:
        if not self.items:
            raise ValueError("posterior must not be empty")
        labels: set[str] = set()
        total = 0.0
        normalized: list[tuple[WorldState, float]] = []
        for state, probability in self.items:
            if state.label in labels:
                raise ValueError(f"duplicate world-state label: {state.label}")
            labels.add(state.label)
            probability = _prob(probability, f"P({state.label})")
            total += probability
            normalized.append((state, probability))
        if not math.isclose(total, 1.0, abs_tol=_SUM_TOL):
            raise ValueError("posterior probabilities must sum to 1")
        object.__setattr__(self, "items", tuple(normalized))

    def credible_set(self, coverage: float = 1.0) -> tuple[WorldState, ...]:
        """Highest-probability non-zero states whose cumulative mass reaches coverage."""
        coverage = _prob(coverage, "credible_coverage")
        if coverage <= 0.0:
            raise ValueError("credible_coverage must be > 0")
        ranked = sorted(
            ((state, probability) for state, probability in self.items if probability > 0.0),
            key=lambda item: item[1],
            reverse=True,
        )
        if not ranked:
            raise ValueError("posterior has no non-zero state")
        selected: list[WorldState] = []
        mass = 0.0
        for state, probability in ranked:
            selected.append(state)
            mass += probability
            if mass + _SUM_TOL >= coverage:
                break
        return tuple(selected)


@dataclass(frozen=True)
class UtilityModel:
    """Additive utility in exactly one declared utility space."""

    v_mission: float = 0.0
    v_residual: float = 0.0
    v_network: float = 0.0
    v_learning_success: float = 0.0
    v_learning_failure: float = 0.0
    c_intervention: float = 0.0
    c_operations: float = 0.0
    c_liability_on_failure: float = 0.0

    def __post_init__(self) -> None:
        for name in (
            "v_mission",
            "v_residual",
            "v_network",
            "v_learning_success",
            "v_learning_failure",
        ):
            _finite(getattr(self, name), name)
        for name in ("c_intervention","c_operations","c_liability_on_failure"):
            _nonnegative(getattr(self, name), name)

    def u_success(self) -> float:
        return _finite(
            self.v_mission + self.v_residual + self.v_network + self.v_learning_success
            - self.c_intervention - self.c_operations,
            "success utility",
        )

    def u_failure(self) -> float:
        return _finite(
            self.v_learning_failure - self.c_intervention - self.c_operations
            - self.c_liability_on_failure,
            "failure utility",
        )


class GateName(str, Enum):
    AUTHORITY = "authority"
    COMMAND_TRUST = "command_trust"
    NATIVE_COMMAND_TRUST = "native_command_trust"
    APPROACH_SAFETY = "approach_safety"
    OBSERVATION_AUTHORITY = "observation_authority"


@dataclass(frozen=True)
class GateInputs:
    """Declared gate state after the currently available evidence.

    Missing gate == unsatisfied. Each recovery option declares its own gate requirements.
    """

    statuses: dict[GateName, bool]

    def __post_init__(self) -> None:
        for gate, value in self.statuses.items():
            if not isinstance(gate, GateName) or not isinstance(value, bool):
                raise ValueError("gate statuses must map GateName to bool")

    def satisfies(self, required: frozenset[GateName]) -> tuple[bool, tuple[str, ...]]:
        reasons = tuple(
            f"gate '{gate.value}' not satisfied"
            for gate in sorted(required, key=lambda item: item.value)
            if not self.statuses.get(gate, False)
        )
        return (not reasons, reasons)


@dataclass(frozen=True)
class RecoveryOption:
    name: str
    p_success_given_state: Callable[[WorldState], float]
    utility: UtilityModel
    required_gates: frozenset[GateName]
    safe_under: Callable[[WorldState], bool]

    def __post_init__(self) -> None:
        if not self.name:
            raise ValueError("recovery option name is required")

    def p_success(self, posterior: Posterior) -> float:
        result = sum(
            probability * _prob(
                self.p_success_given_state(state),
                f"P(success:{self.name}|{state.label})",
            )
            for state, probability in posterior.items
        )
        return _prob(result, f"P(success:{self.name})")

    def expected_utility(self, posterior: Posterior) -> float:
        p = self.p_success(posterior)
        return _finite(
            p * self.utility.u_success() + (1.0 - p) * self.utility.u_failure(),
            f"EU({self.name})",
        )


@dataclass(frozen=True)
class ObservationOutcome:
    probability: float
    posterior: Posterior
    gates: GateInputs

    def __post_init__(self) -> None:
        _prob(self.probability, "observation-outcome probability")


@dataclass(frozen=True)
class Observation:
    name: str
    cost: float
    outcomes: tuple[ObservationOutcome, ...]

    def __post_init__(self) -> None:
        if not self.name:
            raise ValueError("observation name is required")
        _nonnegative(self.cost, f"cost({self.name})")
        if not self.outcomes:
            raise ValueError("observation must have outcomes")
        total = sum(_prob(x.probability, "observation-outcome probability") for x in self.outcomes)
        if not math.isclose(total, 1.0, abs_tol=_SUM_TOL):
            raise ValueError("observation-outcome probabilities must sum to 1")


ELIGIBLE = "ELIGIBLE_FOR_DECISION_PREPARATION"
HOLD = "HOLD_FAIL_CLOSED"
_AUTHORIZATION_NOTE = (
    "Advisory assessment only. This record does not authorize, approve, select, or "
    "record a consequential decision. Accountable human authority remains external."
)


@dataclass(frozen=True)
class OptionFinding:
    name: str
    robust: bool
    unsafe_hypotheses: tuple[str, ...]
    required_gates: tuple[str, ...]
    gate_failures: tuple[str, ...]
    eligible: bool
    p_success: float
    expected_utility: float
    utility_advantage_vs_hold: float


@dataclass(frozen=True)
class OptionAssessment:
    utility_space: str
    credible_coverage: float
    credible_hypotheses: tuple[str, ...]
    ranked_all: tuple[tuple[str, float], ...]
    hold_utility: float
    option_findings: tuple[OptionFinding, ...]
    robust_options: tuple[str, ...]
    eligible_options: tuple[str, ...]
    highest_ranked_eligible_option: Optional[str]
    disposition: str
    hold_reasons: tuple[str, ...]
    next_best_observation: Optional[str]
    next_best_nevoi: Optional[float]
    reopen_conditions: tuple[str, ...]
    authorization_note: str = _AUTHORIZATION_NOTE


def _robust_options(
    posterior: Posterior,
    options: Sequence[RecoveryOption],
    credible_coverage: float,
) -> tuple[RecoveryOption, ...]:
    credible = posterior.credible_set(credible_coverage)
    return tuple(option for option in options if all(option.safe_under(s) for s in credible))


def _eligible_options(
    posterior: Posterior,
    options: Sequence[RecoveryOption],
    gates: GateInputs,
    credible_coverage: float,
) -> tuple[RecoveryOption, ...]:
    robust = _robust_options(posterior, options, credible_coverage)
    return tuple(option for option in robust if gates.satisfies(option.required_gates)[0])


def _best_eligible_eu(
    posterior: Posterior,
    options: Sequence[RecoveryOption],
    gates: GateInputs,
    credible_coverage: float,
    hold_utility: float,
) -> float:
    hold = _finite(hold_utility, "hold_utility")
    eligible = _eligible_options(posterior, options, gates, credible_coverage)
    if not eligible:
        return hold
    return max(hold, max(option.expected_utility(posterior) for option in eligible))


def nevoi(
    observation: Observation,
    current_posterior: Posterior,
    options: Sequence[RecoveryOption],
    current_gates: GateInputs,
    *,
    credible_coverage: float = 1.0,
    hold_utility: float = 0.0,
) -> float:
    """Net expected value of information over the admissible option set."""
    if not options:
        raise ValueError("at least one recovery option is required")
    current = _best_eligible_eu(
        current_posterior, options, current_gates, credible_coverage, hold_utility
    )
    expected_after = sum(
        outcome.probability
        * _best_eligible_eu(
            outcome.posterior, options, outcome.gates, credible_coverage, hold_utility
        )
        for outcome in observation.outcomes
    )
    return _finite(expected_after - current - observation.cost, f"NEVOI({observation.name})")


def assess_options(
    posterior: Posterior,
    options: Sequence[RecoveryOption],
    gates: GateInputs,
    *,
    utility_space: str,
    candidate_observations: Sequence[Observation] = (),
    credible_coverage: float = 1.0,
    hold_utility: float = 0.0,
) -> OptionAssessment:
    if not options:
        raise ValueError("at least one recovery option is required")
    if not utility_space.strip():
        raise ValueError("utility_space must be declared")
    _finite(hold_utility, "hold_utility")
    credible = posterior.credible_set(credible_coverage)

    hold = _finite(hold_utility, "hold_utility")
    ranked = tuple(sorted(
        ((x.name, x.expected_utility(posterior)) for x in options),
        key=lambda item: item[1],
        reverse=True,
    ))
    findings: list[OptionFinding] = []
    for option in options:
        unsafe = tuple(state.label for state in credible if not option.safe_under(state))
        robust_flag = not unsafe
        _, gate_reasons = gates.satisfies(option.required_gates)
        gate_failures = gate_reasons
        eligible_flag = robust_flag and not gate_failures
        eu = option.expected_utility(posterior)
        findings.append(OptionFinding(
            name=option.name,
            robust=robust_flag,
            unsafe_hypotheses=unsafe,
            required_gates=tuple(sorted(g.value for g in option.required_gates)),
            gate_failures=gate_failures,
            eligible=eligible_flag,
            p_success=option.p_success(posterior),
            expected_utility=eu,
            utility_advantage_vs_hold=eu - hold,
        ))
    robust = tuple(option for option in options if next(f for f in findings if f.name == option.name).robust)
    eligible = tuple(option for option in options if next(f for f in findings if f.name == option.name).eligible)
    eligible_ranked = sorted(eligible, key=lambda x: x.expected_utility(posterior), reverse=True)
    highest = eligible_ranked[0].name if eligible_ranked else None

    hold_reasons: list[str] = []
    if not robust:
        hold_reasons.append(
            "no recovery option is safe across the declared credible hypothesis set"
        )
    if not eligible:
        for finding in sorted(findings, key=lambda x: x.expected_utility, reverse=True):
            hold_reasons.extend(
                f"{finding.name}: unsafe under credible hypothesis '{label}'"
                for label in finding.unsafe_hypotheses
            )
            hold_reasons.extend(
                f"{finding.name}: {reason}" for reason in finding.gate_failures
            )

    best_observation: Optional[str] = None
    best_nevoi: Optional[float] = None
    for observation in candidate_observations:
        value = nevoi(
            observation, posterior, options, gates,
            credible_coverage=credible_coverage, hold_utility=hold_utility,
        )
        if value > 0.0 and (best_nevoi is None or value > best_nevoi):
            best_observation, best_nevoi = observation.name, value

    disposition = ELIGIBLE if highest is not None else HOLD
    reopen = (
        ("material evidence changes", "gate state changes", "modeled hypothesis set changes")
        if highest is not None
        else tuple(f"resolve: {reason}" for reason in hold_reasons)
    )
    return OptionAssessment(
        utility_space=utility_space,
        credible_coverage=credible_coverage,
        credible_hypotheses=tuple(s.label for s in credible),
        ranked_all=ranked,
        hold_utility=hold,
        option_findings=tuple(findings),
        robust_options=tuple(x.name for x in robust),
        eligible_options=tuple(x.name for x in eligible_ranked),
        highest_ranked_eligible_option=highest,
        disposition=disposition,
        hold_reasons=tuple(hold_reasons),
        next_best_observation=best_observation,
        next_best_nevoi=best_nevoi,
        reopen_conditions=tuple(reopen),
    )
