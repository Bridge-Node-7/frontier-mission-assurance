# Source Release Receipt — v0.11.0

**Release type:** stable public reference candidate  
**Date:** 2026-09-18  
**Canonical release gate:** WORKING

## Purpose

Add a bounded FTQC technical-evidence consumer while preserving the separation
between evidence production, processor technical evaluation, institutional
assurance, downstream decision preparation, and accountable human authority.

## Material changes in v0.11.0

- Added exact-artifact and exact-schema verification for reviewed
  `ExperimentResult 2.0.0` plus linked `ProcessorEvidenceReceipt 2.0.0`.
- Added explicit reviewed producer-release gates.
- Added internal-integrity, one-input linkage, and architecture-consistency checks.
- Mapped current generated decoder-backlog model evidence to
  `SIMULATED / NOT_ASSESSED / DECLARED`.
- Preserved cross-architecture evidence as `REVIEW_REQUIRED`.
- Preserved positive technical evidence as `RE-EVALUATION_OPPORTUNITY`, never
  automatic approval.
- Reused FTQC profile contract `0.2` and assurance-context `0.1.0`.
- Kept producer-owned schema bytes outside the public FMA source tree; exact
  reviewed schema digests are verified against operator-supplied schema files.

## Source-level evidence

Release eligibility requires the full deterministic FMA validation surface plus
the FTQC processor-evidence adapter regressions to remain green.

The adapter establishes only structural integrity, reviewed interface identity,
bounded evidence classification, and declared applicability semantics. It does
not establish quantum truth, real hardware performance, independent V&V,
certification, government readiness, or consequential decision authority.

## Public/private boundary

No customer, partner, supplier, private architecture, raw protected evidence, or
private producer artifact is added to this public repository.

## Hosted evidence rule

Commit-specific hosted evidence belongs in GitHub Actions and tagged release metadata, not in this source-controlled receipt.

## Release gate

The source candidate remains **WORKING** until protected-main hosted V&V is green
for the exact merged commit. Stable publication remains a separate explicit action
performed only by the repository's `Stable Release` workflow.
