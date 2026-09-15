# Profile Contract

## Contract version

**Orbital Recovery Assurance profile contract:** `0.5`  
**Prospective containing FMA release:** `0.7.0`

The profile contract version is independent from the containing FMA release version. Consumers should pin both the FMA release and the `profile_version` carried by profile records. Breaking profile-contract changes require a profile-version change.

## Purpose

Provide bounded public assurance contracts and a synthetic reference policy for orbital
recovery assessment under uncertain physical state, digital trust, authority, and
post-intervention mission fitness.

## Architectural class

**Frontier Mission Assurance profile.** This is not a standalone system of record and
not a new decision authority.

## Owns

- the public profile schemas under this directory;
- the synthetic validation fixtures and reference policy used to exercise them;
- profile-specific assurance invariants for evidence, option eligibility, and
  requalification;
- the portable Mission Recovery Chain view schema as a non-canonical projection.

## Does not own

- canonical institutional evidence;
- real mission or customer records;
- Mission Graph dependency relations, ProofRequests, or strategic options;
- a consequential human decision;
- generic decision-engine semantics;
- operational authority;
- orbital command/control;
- a universal spacecraft ontology;
- generalized institutional learning.

The synthetic option-assessment policy is a reference demonstrator, not a portable
BN7 decision standard.

## Inputs

- declared posterior over modeled world states;
- declared evidence and provenance;
- declared gate state;
- declared recovery-option models and safety predicates;
- declared utility space;
- declared mission requirements for requalification.

## Outputs

- optional Mission Recovery Chain projection;
- advisory option assessment;
- robust-action membership;
- gate eligibility for downstream decision preparation;
- positive-value next-observation candidate;
- requalification review state;
- recovery timeline metrics;
- bounded validation findings.

## Decision authority

Human and downstream governed decision workflow. Machine output does not authorize,
approve, select, or record a consequential action.

## Public content rule

Examples are synthetic or sanitized and contain no real personal, customer, partner,
supplier, investor, operator, or asset identity.
