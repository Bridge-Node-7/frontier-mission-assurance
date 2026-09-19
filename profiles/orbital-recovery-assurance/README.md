# Orbital Recovery Assurance

**Profile contract version:** `0.5`

**Evidence-driven recovery assurance for degraded, legacy, or uncertain orbital capability.**

Orbital Recovery Assurance organizes the path from uncertain system state to trusted mission capability. It brings physical condition, digital trust, authority, recovery-path diversity, evidence lineage, option robustness, requalification, and Time-to-Trust into one inspectable assurance flow.

Mission systems retain their established sources of record, command paths, and decision authority. Orbital Recovery Assurance provides the evidence and verification layer that makes the recovery basis clear, reviewable, and reproducible.

## Mission objective

A degraded or legacy orbital system may retain valuable capability even when its current condition, command path, authority state, or mission fitness is incomplete or contested. The profile helps teams establish:

- what capability remains;
- which evidence is current, applicable, and trustworthy;
- how many independent recovery paths are actually available;
- which recovery options remain robust across the declared credible state set;
- which evidence would most improve the decision basis;
- what must be demonstrated before the resulting capability is requalified.

The assurance path is:

`Observe → Establish State → Establish Trust → Map Recovery Paths → Acquire Decision-Relevant Evidence → Assess Robust Options → Human Decision → Requalify → Verify Capability`

## Mission Recovery Chain

The operator-facing recovery lens is:

`Power → Contact → Telemetry → Command → Capability`

Trust and authority are cross-cutting overlays across the chain. Recovery resilience is measured by **independent recovery paths**, not raw asset count.

The working sequence is:

**Map → Count → Exercise → Assess → Acquire Evidence → Decide → Requalify → Measure Time to Trust → Reassess**

See [`docs/RECOVERY_CHAIN.md`](docs/RECOVERY_CHAIN.md).

## Assurance capabilities

The profile adds:

- distinct physical, trust, and authority state semantics;
- evidence references with provenance-correlation roots and validity envelopes;
- intervention-success marginalization over declared latent states;
- expected utility in one declared utility space with an explicit HOLD baseline;
- robust-option filtering over a declared credible-state coverage policy;
- option-specific trust, authority, safety, and evidence gates;
- net expected value of information over admissible options;
- recovery requalification records;
- Time-to-Trust timeline metrics;
- hindcast scoring primitives;
- a preregistered synthetic known-truth benchmark with safety-respecting baselines and stress runs;
- deterministic synthetic reference cases;
- a machine-readable Mission Recovery Chain projection;
- source-neutral recovery-pathway taxonomy for responsiveness and interface preparedness;
- structured experiment patterns for recovery-enabling hypotheses.

## Decision authority

Optimization can rank. Evidence can support. Robust filtering can exclude. Gates can establish eligibility for decision preparation.

**Consequential decisions remain with the accountable human and the governing mission process.**

That separation is deliberate: the system automates what can be proven while preserving human authority where judgment and authorization matter.

## System role

Orbital Recovery Assurance owns its public contracts, reference policy, synthetic fixtures, and profile-specific verification logic.

Canonical mission evidence, dependency ownership, operational authority, command/control, and final decision records remain with the governed systems responsible for them. Integration is performed through references and portable contracts rather than duplicate sources of truth.

See [`PROFILE_CONTRACT.md`](PROFILE_CONTRACT.md) and [`docs/INTEROPERABILITY.md`](docs/INTEROPERABILITY.md).

## Public evaluation scope

The public profile is source-neutral and uses synthetic examples so its
contracts, validation behavior, and limitations can be evaluated independently
of any particular mission. See [`ASSURANCE_SCOPE.md`](ASSURANCE_SCOPE.md) and
[`docs/GOVERNED_WORKSPACE.md`](docs/GOVERNED_WORKSPACE.md).

## Adoption path

Start with [`docs/PARTNER_QUICKSTART.md`](docs/PARTNER_QUICKSTART.md).

For an applied mission case, retain authoritative evidence at its source and validate the assessment workspace with:

```bash
python scripts/validate_orbital_recovery_case.py /path/to/case --require-stage mapped
```

The validator checks schema and cross-record integrity while authoritative evidence remains at its source.

Use [`docs/RECOVERY_ASSURANCE_PACKAGE.md`](docs/RECOVERY_ASSURANCE_PACKAGE.md) for the decision-review handoff, [`docs/REAL_CASE_PROTOCOL.md`](docs/REAL_CASE_PROTOCOL.md) for mission-case application, and [`docs/ADOPTION_PATH.md`](docs/ADOPTION_PATH.md) for the evaluate → map → count/exercise → assess → decide → requalify → learn lifecycle.

## Epistemic assurance

The profile keeps observed, calculated, inferred, simulated, and reported evidence classes distinct and applies an **Epistemic Firewall**: analysis may generate hypotheses and next tests, while evidence-state promotion requires admissible evidence under the declared policy.

For multi-source corroboration, provenance-correlation components are used instead of raw record count. See [`docs/EPISTEMIC_ASSURANCE.md`](docs/EPISTEMIC_ASSURANCE.md), [`docs/EVIDENCE_QUORUM_PATTERN.md`](docs/EVIDENCE_QUORUM_PATTERN.md), and [`docs/EVIDENCE_DEGRADATION_EXERCISE_PATTERN.md`](docs/EVIDENCE_DEGRADATION_EXERCISE_PATTERN.md).

## Distribution

Orbital Recovery Assurance is distributed with the FMA repository and verified source archive. The FMA Python wheel provides the core `frontier_assurance` package and CLI; profile schemas, examples, benchmark assets, and mission guidance remain in the matching source release.

## Verify

```bash
python -m pip install "jsonschema==4.26.0"
python scripts/validate_orbital_recovery_assurance.py .
python -m unittest tests.test_orbital_recovery_assurance -v
python scripts/run_orbital_recovery_synthetic_benchmark.py .
```

Expected profile result:

```text
ORBITAL RECOVERY ASSURANCE PROFILE PASS
```

## Verification scope

A PASS confirms the declared profile contracts, arithmetic invariants, cross-record references, robust-envelope behavior, gate behavior, timeline calculations, and synthetic benchmark acceptance checks exercised by the validation set.

Mission qualification, operational authority, flight safety, and mission-specific probability calibration remain governed by the evidence and approval processes responsible for the actual system.

See [`ASSURANCE_SCOPE.md`](ASSURANCE_SCOPE.md) and [`docs/VALIDATION.md`](docs/VALIDATION.md).

## Engineering model

The profile publishes a portable assurance layer rather than a universal orbital ontology. Domain systems retain their richer operational semantics; FMA carries the reusable evidence, verification, requalification, and decision-preparation contracts.

See [`docs/RECOVERY_PATHWAY_TAXONOMY.md`](docs/RECOVERY_PATHWAY_TAXONOMY.md) for the source-neutral recovery pathway model and [`docs/INTERVENTION_EXPERIMENT_PATTERN.md`](docs/INTERVENTION_EXPERIMENT_PATTERN.md) for structured experiment design.