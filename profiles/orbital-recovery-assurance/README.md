# Orbital Recovery Assurance

**Profile contract version:** `0.5`  

A bounded Frontier Mission Assurance profile for evaluating whether recovery options
have a sufficiently explicit evidence, safety, trust, authority, and requalification
basis to enter accountable human decision preparation.

The profile is **advisory, synthetic-first, and non-operational**. It does not control
orbital assets, authorize operations, establish ownership, certify recoverability,
own canonical mission evidence, or record the final consequential decision.

## Problem

A degraded or legacy orbital system can retain valuable capability while its true
state, command trust, authority, or fitness for a new mission remains uncertain.

The profile structures:

`Observe → Establish State → Establish Trust → Acquire Decision-Relevant Evidence → Filter Robust Options → Assess Eligible Options → Human Decision Preparation → Requalify → Verify Capability`

## What the profile adds

- separate physical, trust, and authority semantics;
- evidence references, provenance-correlation roots, and validity envelopes;
- intervention-success marginalization over declared latent states;
- additive expected utility in one declared utility space with an explicit HOLD baseline;
- robust-action filtering over an explicit posterior-coverage policy;
- option-specific fail-closed gates and per-option blocking findings;
- net expected value of information over the admissible option set;
- recovery requalification records;
- Time-to-Trust family timeline metrics;
- generic hindcast scoring primitives;
- a preregistered synthetic known-truth benchmark with safe baselines and stress runs;
- deterministic synthetic examples;
- a machine-readable Mission Recovery Chain projection for operator-facing recovery-path analysis;
- source-neutral target/pathway taxonomy for responsiveness, interface preparedness, and Observe/Contact/Interface decomposition;
- bounded experimental-intervention guidance, including the SECOND LIGHT bench protocol;

## Architecture boundary

The profile owns its public contracts and synthetic checks only. It does not replace:

- governed evidence storage;
- Mission Graph dependency, ProofRequest, or strategic-option ownership;
- Frontier Decision Engine decision preparation;
- accountable human decision authority.

See `docs/BN7_INTEROPERABILITY.md`.

## Trust rule

Optimization may rank. Evidence may support. Robust filtering may exclude. A gate may
mark an option eligible for decision preparation. **None of those operations is a
decision or authorization.**

## Source-neutral public boundary

The profile contains no real customer, partner, supplier, operator, investor, asset,
or person identity. Named evidence and external identity mappings remain outside this
public profile.

## For real-world users

Start with `docs/PARTNER_QUICKSTART.md`.

Real mission evidence should remain in a partner-controlled private workspace or existing
governed system. See `docs/PRIVATE_WORKSPACE_PATTERN.md`.

For human review, `docs/RECOVERY_ASSURANCE_PACKAGE.md` provides a bounded handoff
structure for evidence basis, option eligibility, requalification, timeline metrics, and
reopen conditions. It is not an authorization record.

For a real partner-controlled case, use `python scripts/validate_orbital_recovery_case.py /path/to/private-case`. The command is local-only and validates structure/cross-references, not real-world truth or authorization.

See `docs/REAL_CASE_PROTOCOL.md` for bounded application to actual mission cases and
`docs/REAL_WORLD_ADOPTION.md` for the intended evaluate → map → count/exercise → assess →
decide → requalify → learn lifecycle.

## Mission Recovery Chain

Use `docs/RECOVERY_CHAIN.md` as the front-end recovery lens:

`Power → Contact → Telemetry → Command → Capability`

Trust and authority are modeled as cross-cutting overlays rather than a sixth serial link.
The chain is a projection over governed evidence, not a new canonical record or decision
authority. Count independent recovery paths, not merely assets.

The partner workflow begins with **Map → Count → Exercise** before option assessment.
The synthetic view is `examples/synthetic-recovery-case/recovery-chain-view.json`.

## Epistemic assurance

The profile keeps observed, calculated, inferred, simulated, and reported evidence classes distinct and applies an **Epistemic Firewall**: analysis may generate hypotheses or next tests, but it may not silently promote itself into observed or verified evidence. See `docs/EPISTEMIC_ASSURANCE.md`.

For multi-source corroboration, use provenance-correlation components rather than raw record count. See `docs/EVIDENCE_QUORUM_PATTERN.md`. Synthetic resilience exercises may use `docs/BLACK_SKY_EXERCISE_PATTERN.md`. Broader research concepts and their BN7 ownership boundaries are mapped in `docs/FUTURE_ARCHITECTURE_BOUNDARIES.md`.

## Distribution boundary

The Orbital Recovery Assurance profile is a **source-repository/source-archive profile**.
The FMA Python wheel provides the core `frontier_assurance` package and CLI; it does not
package this profile directory. Users who need the profile schemas, synthetic examples,
partner guidance, or benchmark assets should use a repository checkout or the verified
source archive for the matching release.

## Validate

```bash
python scripts/validate_orbital_recovery_assurance.py .
python -m unittest tests.test_orbital_recovery_assurance -v
python scripts/run_orbital_recovery_synthetic_benchmark.py .
```

## PASS meaning

A PASS establishes only the declared synthetic contracts, arithmetic invariants,
cross-record references, robust-envelope behavior, gate behavior, timeline calculations, and the
declared synthetic benchmark/stress acceptance checks exercised by the validation set.

It does **not** establish real-world safety, recoverability, authorization, mission
readiness, flight qualification, economic value, or scientific truth.

See `LIMITATIONS.md`, `PROFILE_CONTRACT.md`, and `docs/VALIDATION.md`.

## Engineering guidance

The profile intentionally avoids turning FMA into an orbital ontology. Domain guidance is kept source-neutral and bounded:

- `docs/RECOVERY_PATHWAY_TAXONOMY.md` — target responsiveness, interface preparedness, Observe/Contact/Interface layers, and generic recovery pathways.
- `docs/SECOND_LIGHT_BENCH_PROTOCOL.md` — mission-to-link-to-antenna bench protocol for a passive-aperture reuse hypothesis.

These documents support assurance reasoning; they do not establish live operational procedures or mission authority.
