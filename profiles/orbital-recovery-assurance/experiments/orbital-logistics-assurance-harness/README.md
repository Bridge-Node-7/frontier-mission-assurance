# Orbital Logistics Assurance Harness — Experimental Reference

This source-neutral experiment tests one bounded question:

> Does the declared evidence basis support preparing a proposed cross-system logistics service for accountable human review, and after execution, does the changed configuration have enough evidence to enter requalification review?

The harness is deliberately **non-actuating**. It does not command spacecraft, approve servicing, certify safety, authenticate external records, or create operational authority.

## Why this exists

Persistent orbital logistics introduces cross-system dependence among independently governed assets, interfaces, resources, models, and authorities. The experiment probes the smallest reusable assurance logic without creating a new repository, top-level profile, graph ontology, or autonomy runtime.

## Tested invariants

- the exact pre-service option must already be eligible for decision preparation;
- authority evidence required for execution must exist in the pre-service evidence set;
- material interfaces must be configuration-compatible and unblocked;
- referenced resources must be present, fit for purpose, and authorized for release;
- decision-relevant models must be applicable to the current use and unblocked;
- service execution and service verification remain distinct;
- post-service evidence is required before requalification review;
- `post_service` can only reach `READY_FOR_REQUALIFICATION_REVIEW`;
- `requalification_review` can only reach `READY_FOR_HUMAN_REVIEW` after declared requalification evidence;
- service completion never implies mission requalification or operational authorization;
- generated proof needs are only candidates; governed ProofRequests remain Mission Graph authority.

## Scenarios

1. nominal pre-service eligibility;
2. interface mismatch;
3. resource release/custody gap;
4. model outside its supported envelope;
5. authority appearing only after service;
6. failed requalification;
7. nominal requalification-review readiness;
8. nominal post-service readiness for requalification review;
9. unsupported lifecycle phase fails closed.

## Public data boundary

This public experiment is for **synthetic or sanitized evaluation data only**. Do not place real mission evidence, protected identifiers, customer records, credentials, controlled technical data, or other sensitive operational material in this directory, public issues, pull requests, Actions logs, or checked-in fixtures.

Governed operational cases belong in an access-controlled environment. Keep authoritative evidence at its source and pass only the minimum approved references or projections needed for the review. The experiment deliberately rejects inputs marked `private`.

## NLP / ML boundary

The reference harness is deterministic and has **no NLP or machine-learning runtime dependency**. That is intentional: a simpler deterministic control establishes the baseline behavior that future automation must beat without weakening provenance or authority boundaries.

If an NLP or ML adapter is later evaluated, it may assist retrieval, extraction, classification, anomaly detection, prediction, or candidate proof generation only when its output preserves source references and declared model identity/version and stays within a reviewed evaluation envelope. Model output begins as candidate information; it must not silently create evidence, applicability, eligibility, requalification, or operational authority.

A future model-dependent path should remain optional, observable, replaceable, and reversible, with a deterministic fallback or explicit fail-closed state when the model is unavailable or outside its validated envelope.

## Publication boundary

This experiment exposes only the minimum reusable behavior needed to evaluate the declared assurance invariants. It is not a complete logistics architecture, customer/program roadmap, autonomy policy, optimization strategy, or commercialization design. Mission-specific policy, thresholds, calibration, integration adapters, and operating authority remain outside this public reference.

## Governed case binding

For an access-controlled Orbital Recovery case, bind the service experiment to the
existing governed records instead of re-declaring physical, trust, authority, or
requalification state inside the experiment.

Keep the service-assurance JSON **outside** the Orbital Recovery case directory so
the existing case validator continues to recognize only its canonical profile
records.

Example:

```bash
python profiles/orbital-recovery-assurance/experiments/orbital-logistics-assurance-harness/bound_case.py \
  /path/to/private-orbital-recovery-case \
  /path/to/service-assurance-case.json
```

The binding helper first runs the existing private Orbital Recovery case validator
at the lifecycle stage required by the service case. It then binds:

- the exact governed pre-service option assessment;
- the exact governed pre-service evidence record;
- the governed post-service evidence record when required;
- the governed requalification record when required.

A mismatched assessment, evidence record, asset, post-service record, record class,
or requalification reference fails closed. Private records are accepted only
through this governed binding path; the direct public experiment continues to
accept synthetic or sanitized inputs only.

The helper remains local-only and non-actuating. Structural PASS does not establish
evidence authenticity, mission fitness, safety, ownership, or authorization.

## Run

From the experiment directory:

```bash
python assurance_harness.py scenarios/01_nominal_pre_service.json
```

From the repository root:

```bash
python -m pytest -q tests/test_orbital_logistics_assurance_experiment.py
```

## Architectural boundary

This experiment is not a new portable contract. If repeated governed cases demonstrate that the same fields and invariants are necessary across adopters, the minimum stable subset may later be proposed through the existing Orbital Recovery profile versioning and review process.
