# Source Release Receipt — v0.7.0

**Release type:** stable public reference candidate  
**Date:** 2026-09-15

## Purpose

Add bounded Orbital Recovery Assurance to FMA without expanding the repository into a universal orbital platform or operational command system. Version 0.7.0 adds a source-distributed profile for mission recovery-chain mapping, evidence integrity, robust option eligibility, next-best evidence, private local case validation, post-intervention requalification, and Time-to-Trust while preserving accountable human authority.

## Material changes in v0.7.0

- Added `profiles/orbital-recovery-assurance/` as a bounded FMA profile rather than a new repository.
- Added the Mission Recovery Chain view `Power → Contact → Telemetry → Command → Capability`, with trust and authority retained as overlays.
- Added provenance-aware evidence handling, validity envelopes, robust-action filtering, option-specific fail-closed gates, explicit HOLD utility, next-best-evidence evaluation, requalification, and event-derived recovery metrics.
- Added a deterministic synthetic known-truth benchmark, preserved invalidated protocol history, and required a stress matrix rather than treating one passing run as sufficient evidence.
- Added a local-only validator for governed private cases with explicit lifecycle gates; real mission evidence is not uploaded to this public repository or public CI.
- Added evaluation/adoption, private-workspace, epistemic-assurance, evidence-quorum, evidence-degradation exercise, recovery-pathway, real-case, Recovery Assurance Package, and bounded intervention-experiment guidance.
- Added Orbital profile validation to existing source, Python-matrix, cross-platform, and stable-release verification paths.
- Kept the core wheel boundary unchanged: bounded profile assets are distributed through the repository/source archive rather than silently becoming wheel runtime authority.
- Preserved governed evidence/dependency ownership, downstream human decision preparation, and accountable human consequential authority.

## Source-level evidence

The candidate must satisfy `VALIDATION_REPORT.md`, including the complete existing FMA regression surface plus Orbital profile contracts, synthetic cross-record invariants, 27 Orbital-specific closure/regression tests across the two Orbital test modules, deterministic benchmark/result binding, private-case lifecycle behavior, cross-platform profile validation, packaging, dependency review, and public-boundary controls.

## Hosted evidence rule

Commit-specific hosted evidence belongs in GitHub Actions and tagged release metadata, not in this source-controlled receipt. This avoids recursive receipts in which recording a commit SHA creates a different commit SHA.

## Tagged-release evidence rule

The public release record must bind the accepted tag to the exact commit, successful hosted Actions run, source archive, wheel, tracked-source SHA-256 manifest, release-artifact SHA-256 manifest, SBOM, and available provenance attestations. Clean-user verification of the published source archive must exercise both bounded profile validators.

## Claim boundary

A passing Orbital Recovery Assurance control establishes only its declared structural, arithmetic, reference-resolution, synthetic-policy, or timeline property. It does not establish legal authority, ownership, spacecraft recoverability, flight safety, real-world probability calibration, mission qualification, commercial demand, or authorization for consequential action.

An option may be robust and gate-clear yet still be unattractive relative to HOLD. Eligibility is not recommendation and is never operational authorization.

The public repository contains synthetic/source-neutral examples. Named real-world evidence and sensitive mission records remain outside the public release surface.

## Release gate

A source candidate may advance only when deterministic source validation passes. Stable release additionally requires successful protected hosted V&V on the exact main commit and successful clean-user verification of the published artifacts. The stable release remains a deliberate workflow-dispatch ceremony rather than an automatic side effect of merge.
