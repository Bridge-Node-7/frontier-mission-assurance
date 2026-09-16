# Source Release Receipt — v0.7.2

**Release type:** stable public reference candidate  
**Date:** 2026-09-15  
**Canonical release gate:** PENDING

## Purpose

Publish the refined Frontier Mission Assurance public experience as a coherent patch release while preserving the validated runtime, schema, assurance, authority, and release semantics of v0.7.1.

Version 0.7.2 presents the system with a capability-first information architecture: product value first, verification evidence second, scope stated once, and governed authority made explicit without defensive repetition.

## Material changes in v0.7.2

- Rebuilt the root README as a clear front door for technical evaluation and adoption.
- Reframed public assurance boundaries as `Assurance Scope`, `Public Release Policy`, `Decision Authority`, and `Verification Scope`.
- Replaced profile `LIMITATIONS.md` surfaces with `ASSURANCE_SCOPE.md` for both Orbital Recovery Assurance and Scientific Discovery Assurance.
- Replaced `REAL_WORLD_ADOPTION.md` with the source-neutral `ADOPTION_PATH.md` and refined the mission-case protocol and partner quickstart.
- Generalized Orbital profile interoperability language so public contracts expose stable interfaces rather than internal portfolio topology.
- Refined release notes, standards positioning, acceptance criteria, evaluation guidance, and machine-readable project facts for consistent product voice.
- Preserved the Mission Recovery Chain, physical/trust/authority separation, provenance-aware evidence handling, robust option eligibility, next-best evidence, requalification, Time-to-Trust, governed local-case validation, and synthetic benchmark semantics.
- Preserved accountable human consequential authority and source-neutral public examples.
- Changed no core assurance-graph, receipt, decision, schema, benchmark, or CLI semantics.

## Source-level evidence

The candidate must satisfy `VALIDATION_REPORT.md`, including the complete FMA regression surface, both assurance profile validators, Orbital cross-record invariants, deterministic benchmark/result binding, governed local-case lifecycle behavior, cross-platform validation, packaging, dependency review, CodeQL on protected main, and public-release controls.

## Hosted evidence rule

Commit-specific hosted evidence belongs in GitHub Actions and tagged release metadata, not in this source-controlled receipt. This avoids recursive receipts in which recording a commit SHA creates a different commit SHA.

## Tagged-release evidence rule

The stable release record binds the accepted tag to the exact protected-main commit, successful hosted Actions run, source archive, wheel, tracked-source SHA-256 manifest, release-artifact SHA-256 manifest, CycloneDX SBOM, and available provenance attestations. Clean-user verification exercises the published source archive and both assurance profiles.

## Verification scope

A PASS attests that the declared controls satisfied their acceptance criteria. Scientific validity, mission recoverability, flight safety, legal authority, mission-specific calibration, mission qualification, and consequential decision authority remain with the governing evidence and approval processes responsible for those determinations.

## Release gate

Deterministic source validation and protected hosted V&V on the exact `main` commit must pass before the canonical release gate advances to `READY`. Stable publication then requires successful clean-user verification of the published artifacts through the explicit release workflow.
