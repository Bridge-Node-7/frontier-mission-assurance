# Profile Contract

## Contract version

**Orbital Recovery Assurance profile contract:** `0.5`  
**Containing FMA release:** `0.7.2`

The profile contract version is independent from the containing FMA release version. Consumers should pin both the FMA release and the `profile_version` carried by profile records. Breaking profile-contract changes require a profile-version change.

## Purpose

Provide source-neutral assurance contracts and a deterministic reference policy for orbital recovery assessment under uncertain physical state, digital trust, authority, and post-intervention mission fitness.

## Architectural class

**Frontier Mission Assurance profile.** The profile is a portable assurance layer that integrates with governed evidence systems and human decision workflows through explicit references and contracts.

## Profile ownership

The profile owns:

- the public schemas under this directory;
- the synthetic validation fixtures and deterministic reference policy;
- profile-specific assurance invariants for evidence, option eligibility, and requalification;
- the portable Mission Recovery Chain view schema as a non-canonical projection;
- profile validation and synthetic benchmark contracts.

## Retained system ownership

The surrounding mission environment retains ownership of:

- canonical mission evidence and identity records;
- dependency and strategic-option records owned by other governed systems;
- generic decision-engine semantics;
- operational authority and command/control;
- the final consequential decision;
- institutional learning outside this profile's declared contracts.

The option-assessment policy is a reference implementation for the profile contract. Local mission policy, calibration, authority, and approval rules remain governed inputs.

## Inputs

- declared posterior over modeled world states;
- declared evidence and provenance;
- declared gate state;
- declared recovery-option models and safety predicates;
- declared utility space;
- declared mission requirements for requalification.

## Outputs

- Mission Recovery Chain projection;
- option assessment;
- robust-option membership;
- gate eligibility for decision preparation;
- positive-value next-observation candidate when available;
- requalification review state;
- recovery timeline and Time-to-Trust metrics;
- validation findings.

## Decision authority

Machine outputs provide evidence, filtering, ranking, and eligibility for downstream review. The accountable human and governing mission process retain consequential decision authority.

## Public release policy

Examples are synthetic or sanitized and contain no real personal, customer, partner, supplier, investor, operator, or asset identity. Mission-specific evidence and external identity mappings remain in governed environments.
