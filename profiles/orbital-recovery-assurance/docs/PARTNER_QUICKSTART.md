# Partner Quickstart

This guide gives engineering, assurance, program, and integration teams the shortest path to evaluate and apply Orbital Recovery Assurance while keeping mission evidence under established governance.

The profile is designed to **map into existing systems rather than replace them**.

## Distribution and rights

Use a repository checkout or verified FMA source archive for the Orbital profile. The installed FMA wheel provides the core CLI/package; profile schemas, examples, benchmark assets, and mission guidance are distributed with the matching source release.

The public repository is a reference implementation under its stated license. Operational or commercial use follows the rights explicitly granted by Bridge Node 7 or a separate agreement.

## 1. Verify the reference

From the Frontier Mission Assurance repository root:

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

A PASS confirms the declared profile contracts, invariants, reference cases, and benchmark acceptance checks exercised by the validation set.

## 2. Review the reference case

Start with:

- `examples/synthetic-recovery-case/recovery-evidence-record.json`
- `examples/synthetic-recovery-case/recovery-chain-view.json`
- `examples/synthetic-recovery-case/recovery-option-assessment.json`
- `examples/synthetic-recovery-case/requalification-record.json`
- `examples/synthetic-recovery-case/recovery-timeline.json`

The reference case shows the complete structure before mission-specific evidence is mapped.

## 3. Map → Count → Exercise

Build a Mission Recovery Chain for each essential capability:

`Power → Contact → Telemetry → Command → Capability`

Treat trust and authority as cross-cutting overlays.

### MAP

Map the required state and evidence from the systems that already own it.

### COUNT

Count functionally capable independent recovery paths rather than raw asset totals. Preserve shared roots explicitly; separate assets may still depend on the same identity, timing, software/update, ground-capacity, communications, supplier, configuration, or authority dependency.

### EXERCISE

Use synthetic or controlled scenarios to combine technical failure, ambiguous diagnosis, communications degradation, trust degradation, authority uncertainty, and post-intervention evidence gaps.

Identify the binding constraint before selecting an intervention path.

## 4. Create a governed assessment workspace

Keep mission-specific evidence in an access-controlled workspace or the partner's existing governed systems.

Recommended local layout:

```text
assessment-governed/
├── evidence/
├── option-assessments/
├── requalification/
├── timelines/
├── local-mappings/
└── review/
```

Asset identifiers, telemetry, source identities, authority records, economics, and mission-sensitive evidence remain inside that governed boundary.

## 5. Map the minimum required evidence

Map only the fields required by the profile:

- physical state;
- trust state;
- authority state;
- evidence references and validity;
- modeled recovery options;
- declared safety predicates;
- declared utility space;
- requalification requirements.

Where another system owns a record, preserve that ownership and reference it through a local mapping or adapter instead of creating a second source of truth.

Posterior estimates, intervention-success calibration, safety predicates, and local admissibility rules remain governed mission inputs.

## 6. Validate the local case

From a matching FMA source checkout or verified source archive:

```bash
python scripts/validate_orbital_recovery_case.py /path/to/private-case --require-stage mapped
```

The validator performs local schema and cross-reference checks and makes no network calls. Evidence authenticity, mission calibration, and authorization remain inputs from the governing mission process.

Lifecycle gates are available through:

```text
mapped | assessed | post-intervention | requalification-review
```

Each stage proves only the artifacts required for that point in the lifecycle.

## 7. Run the assessment

Use the profile to answer:

1. What capability remains?
2. Which evidence is current, applicable, and trustworthy?
3. How many independent recovery paths are available?
4. Which pathways remain robust across the declared credible state set?
5. Which options are blocked by trust, authority, safety, or evidence gates?
6. Which observation has positive expected decision value?
7. What must be demonstrated before the resulting capability is requalified?

## 8. Prepare the decision-review package

Use [`RECOVERY_ASSURANCE_PACKAGE.md`](RECOVERY_ASSURANCE_PACKAGE.md) to present the current evidence basis, uncertainty, recovery-path state, option eligibility, requalification obligations, timeline metrics, and reopen conditions.

The package feeds the governing decision process while preserving accountable human authority.

## 9. Reassess on material change

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

A strong assurance basis stays synchronized with the system it describes.

## Next references

- [`RECOVERY_CHAIN.md`](RECOVERY_CHAIN.md) — recovery-path model.
- [`REAL_CASE_PROTOCOL.md`](REAL_CASE_PROTOCOL.md) — governed mission-case protocol.
- [`ADOPTION_PATH.md`](ADOPTION_PATH.md) — adoption lifecycle.
- [`PRIVATE_WORKSPACE_PATTERN.md`](PRIVATE_WORKSPACE_PATTERN.md) — data-handling pattern.
- [`../ASSURANCE_SCOPE.md`](../ASSURANCE_SCOPE.md) — profile verification and authority scope.
