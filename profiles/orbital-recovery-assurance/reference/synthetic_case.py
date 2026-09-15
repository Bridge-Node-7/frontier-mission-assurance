"""Deterministic synthetic reference case used to bind fixtures to executable logic."""

from __future__ import annotations

import decision_kernel as d


def build():
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
            v_mission=120, v_residual=10, v_learning_success=5,
            c_intervention=40, c_operations=8, c_liability_on_failure=20,
        ),
        required_gates=frozenset({
            d.GateName.AUTHORITY, d.GateName.COMMAND_TRUST, d.GateName.APPROACH_SAFETY
        }),
        safe_under=lambda state: state.label != "STATE-UNSTABLE-ATTITUDE",
    )
    retire = d.RecoveryOption(
        name="controlled_retirement",
        p_success_given_state=lambda _state: 0.97,
        utility=d.UtilityModel(
            v_learning_success=1, c_intervention=6, c_operations=2,
            c_liability_on_failure=1,
        ),
        required_gates=frozenset({d.GateName.AUTHORITY, d.GateName.NATIVE_COMMAND_TRUST}),
        safe_under=lambda _state: True,
    )
    options = (augment, retire)
    gates = d.GateInputs({d.GateName.APPROACH_SAFETY: True})

    post_good = d.Posterior(((rf_ok, 1.0),))
    observation = d.Observation(
        "integrated_recovery_evidence_review",
        1.0,
        (
            d.ObservationOutcome(
                0.8,
                post_good,
                d.GateInputs({
                    d.GateName.AUTHORITY: True,
                    d.GateName.COMMAND_TRUST: True,
                    d.GateName.APPROACH_SAFETY: True,
                    d.GateName.NATIVE_COMMAND_TRUST: True,
                }),
            ),
            d.ObservationOutcome(0.2, posterior, d.GateInputs({})),
        ),
    )

    assessment = d.assess_options(
        posterior, options, gates,
        utility_space="normalized_multi_attribute_v1",
        candidate_observations=(observation,),
        credible_coverage=1.0,
    )
    return posterior, options, gates, observation, assessment


def assessment_json():
    posterior, options, _gates, observation, assessment = build()
    finding_by_name = {finding.name: finding for finding in assessment.option_findings}
    option_rows = []
    for option in options:
        finding = finding_by_name[option.name]
        option_rows.append({
            "name": option.name,
            "p_success": finding.p_success,
            "expected_utility": finding.expected_utility,
            "hold_utility": assessment.hold_utility,
            "utility_advantage_vs_hold": finding.utility_advantage_vs_hold,
            "robust": finding.robust,
            "unsafe_hypotheses": list(finding.unsafe_hypotheses),
            "required_gates": list(finding.required_gates),
            "gate_failures": list(finding.gate_failures),
            "eligible": finding.eligible,
        })
    return {
        "profile_version": "0.5",
        "record_class": "synthetic",
        "assessment_id": "ASSESSMENT-SYN-001",
        "evidence_record_ref": "EVIDENCE-RECORD-SYN-PRE",
        "asset_id": "ASSET-SYN-001",
        "as_of": "2030-01-01T00:00:00Z",
        "utility_space": assessment.utility_space,
        "credible_coverage": assessment.credible_coverage,
        "credible_hypotheses": list(assessment.credible_hypotheses),
        "hold_utility": assessment.hold_utility,
        "options": option_rows,
        "robust_options": list(assessment.robust_options),
        "eligible_options": list(assessment.eligible_options),
        "highest_ranked_eligible_option": assessment.highest_ranked_eligible_option,
        "candidate_observations": [{
            "name": observation.name,
            "nevoi": d.nevoi(observation, posterior, options, _gates, credible_coverage=1.0),
            "cost": observation.cost,
        }],
        "next_best_observation": assessment.next_best_observation,
        "disposition": assessment.disposition,
        "hold_reasons": list(assessment.hold_reasons),
        "reopen_conditions": list(assessment.reopen_conditions),
        "authorization_note": assessment.authorization_note,
    }
