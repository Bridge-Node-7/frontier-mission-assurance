# Source Release Receipt — v0.11.0

**Release type:** stable public reference release  
**Date:** 2026-09-18  
**Validation status:** READY

## Purpose

Add a bounded FTQC technical-evidence consumer while preserving the separation
between evidence production, processor technical evaluation, institutional
assurance, downstream decision preparation, and accountable human authority.

## Material changes in v0.11.0

- Added exact-artifact and exact-schema verification for reviewed
  `ExperimentResult 2.0.0` plus linked `ProcessorEvidenceReceipt 2.0.0`.
- Added explicit reviewed producer-release gates.
- Added structural-integrity, one-input linkage, and architecture-consistency checks.
- Mapped current generated decoder-backlog model evidence to
  `SIMULATED / NOT_ASSESSED / DECLARED`.
- Preserved cross-architecture evidence as `REVIEW_REQUIRED`.
- Preserved positive technical evidence as `RE-EVALUATION_OPPORTUNITY`, never
  automatic approval.
- Reused FTQC profile contract `0.2` and assurance-context `0.1.0`.
- Kept producer-owned schema bytes outside the public FMA source tree; exact
  reviewed schema digests are verified against supplied schema files.

## Source-level evidence

Release eligibility requires the full deterministic FMA validation surface plus
the FTQC processor-evidence adapter regressions to remain green.

The adapter establishes only structural integrity, reviewed interface identity,
bounded evidence classification, and declared applicability semantics. It does
not establish quantum truth, real hardware performance, independent V&V,
certification, government readiness, or consequential decision authority.

## Release surface

The public reference includes the adapter, contracts, source-neutral examples,
and validation evidence required to evaluate the released behavior. Operational
case evidence remains referenced at its authoritative source rather than copied
into the repository.

## Hosted evidence rule

Hosted validation evidence is recorded in GitHub Actions and release metadata.

## Validation status

The v0.11.0 source is **READY** after required hosted validation completed successfully. This status attests only to the declared source, packaging, profile, adapter, and validation controls; it does not expand the authority or claims described above.
