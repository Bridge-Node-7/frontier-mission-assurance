# Partner Quickstart

This guide is for engineering, assurance, program, and integration teams evaluating
Orbital Recovery Assurance from the public Frontier Mission Assurance repository. For an
actual mission case, use this quickstart together with `REAL_CASE_PROTOCOL.md`.

The profile is intentionally designed so real mission evidence does **not** need to be
committed to the public repository.

## Operational-use and distribution boundary

Use a repository checkout or verified FMA source archive when evaluating this profile. The installed FMA wheel provides the core CLI/package but does not install bounded profile directories.

The public repository is an evaluation/reference implementation under its stated license. Operational or commercial use must remain within rights explicitly granted by Bridge Node 7 or a separate agreement; public visibility alone is not an operational-use license.

For a real private case, keep the case directory outside the public repository and run:

```bash
python scripts/validate_orbital_recovery_case.py /path/to/private-case
```

That command performs local structural and cross-reference validation only. It does not upload the case, authenticate the evidence, establish real-world probability calibration, or authorize an action.

Use `--require-stage mapped|assessed|post-intervention|requalification-review` when the workflow requires a minimum artifact stage. A structural PASS at an earlier stage is not a claim that later recovery or requalification work is complete.

## 1. Verify the public reference

### Distribution note

Use a repository checkout or verified FMA source archive when evaluating this profile.
The installed FMA wheel contains the core CLI/package but does not install bounded profile
directories such as `profiles/orbital-recovery-assurance/`.

From the Frontier Mission Assurance repository root, install the bounded profile validator dependency in the evaluation environment, then run the profile checks:

```bash
python -m pip install "jsonschema==4.26.0"
python scripts/validate_orbital_recovery_assurance.py .
python -m unittest tests.test_orbital_recovery_assurance -v
python scripts/run_orbital_recovery_synthetic_benchmark.py .
```

A PASS establishes only the declared public contracts, invariants, synthetic fixtures,
and benchmark behavior. It does not establish mission readiness, flight safety,
recoverability, authorization, ownership, or real-world probability calibration.

## 2. Review the synthetic example

Start with:

- `examples/synthetic-recovery-case/recovery-evidence-record.json`
- `examples/synthetic-recovery-case/recovery-option-assessment.json`
- `examples/synthetic-recovery-case/requalification-record.json`
- `examples/synthetic-recovery-case/recovery-timeline.json`

Use the example to understand structure and semantics before mapping any real program data.

## 3. Map → Count → Exercise the recovery chain

Before ranking recovery options, build a recovery-chain view for each essential mission capability.
See `RECOVERY_CHAIN.md`.

### MAP

Identify what must remain available, trustworthy, and recoverable across:

`Power → Contact → Telemetry → Command → Capability`

Treat trust and authority as cross-cutting overlays.

### COUNT

Count functionally capable independent recovery paths rather than raw asset totals. Preserve
shared dependencies explicitly; separate assets may still depend on the same identity, timing,
software/update, cloud, ground-capacity, communications, supplier, or authority root.

### EXERCISE

Use synthetic or controlled scenarios to combine technical failure, ambiguous diagnosis,
communications degradation, trust degradation, authority uncertainty, and post-intervention
evidence gaps. Identify the binding constraint before choosing the response.

The solution follows the bottleneck; the profile must not begin with a favored intervention.

## 4. Create a private assessment workspace

Create a workspace **outside the public repository** and outside any automatically
published or synchronized location.

Recommended private layout:

```text
assessment-private/
├── evidence/
├── option-assessments/
├── requalification/
├── timelines/
├── local-mappings/
└── review/
```

Real asset identifiers, telemetry, source identities, authority records, economics,
and mission-sensitive evidence stay in that private workspace or in the partner's
existing governed systems.

## 5. Map rather than migrate

Do not copy an entire mission data environment into Frontier Mission Assurance.
Map only the bounded fields required by the profile:

- physical state;
- trust state;
- authority state;
- evidence references and validity;
- modeled recovery options;
- declared safety predicates;
- declared utility space;
- requalification requirements.

Where a richer system already owns a record, retain that ownership and use a local
reference or adapter rather than creating a second source of truth.

The public reference does not infer your real posterior, calibrate intervention success, or determine your local safety predicates. Those remain governed partner inputs.

## 6. Run the assessment

Use the profile to answer:

1. What capability may remain?
2. Which evidence is trustworthy and applicable?
3. Which recovery pathways are robust across the declared credible state set?
4. Which options remain blocked by trust, authority, safety, or evidence gates?
5. Which observation has positive expected decision value?
6. What must be demonstrated after intervention before the intended capability can be
   considered requalified?

## 7. Prepare the human review artifact

Use `RECOVERY_ASSURANCE_PACKAGE.md` as the bounded handoff structure.

The package presents the evidence basis, uncertainty, option eligibility,
requalification state, and reopen conditions. It is not an authorization record.

## 8. Reassess after material change

Re-run the assessment when any declared condition materially changes, including:

- configuration;
- software or firmware;
- evidence validity;
- authority;
- physical state;
- interface state;
- mission requirement;
- intervention design;
- post-intervention test result.

The profile is useful only while its declared basis remains current.
