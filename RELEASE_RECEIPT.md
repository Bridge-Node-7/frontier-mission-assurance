# Source Release Receipt — v0.7.1

**Release type:** stable public reference candidate  
**Date:** 2026-09-15  
**Canonical release gate:** READY

## Purpose

Publish the accepted post-v0.7.0 public-surface hardening as an exact patch release without expanding Frontier Mission Assurance into a new authority, platform, or operational control system. Version 0.7.1 aligns source identity, validation records, and the Orbital Recovery Assurance profile with the hardened source-neutral public surface already accepted on protected `main`.

## Material changes in v0.7.1

- Aligned the repository, package, citation, project-facts, validation, and profile release identity to `0.7.1`.
- Generalized Orbital Recovery Assurance interoperability and resilience terminology so public documentation stays source-neutral and reusable.
- Removed internal/private research-program detail, roadmap/topology material, and bench-specific internal research content from the public Orbital profile surface.
- Preserved the Mission Recovery Chain, physical/trust/authority separation, provenance-aware evidence handling, robust option eligibility, next-best evidence, requalification, Time-to-Trust, private-case validation, and synthetic benchmark semantics.
- Preserved the public/synthetic boundary and accountable human consequential authority.
- Added no new spacecraft-control, operational-authorization, certification, or real-world calibration claim.

## Source-level evidence

The candidate must satisfy `VALIDATION_REPORT.md`, including the complete existing FMA regression surface plus both bounded profile validators, Orbital synthetic cross-record invariants, deterministic benchmark/result binding, private-case lifecycle behavior, cross-platform validation, packaging, dependency review, and public-boundary controls.

## Hosted evidence rule

Commit-specific hosted evidence belongs in GitHub Actions and tagged release metadata, not in this source-controlled receipt. This avoids recursive receipts in which recording a commit SHA creates a different commit SHA.

## Tagged-release evidence rule

The public release record must bind the accepted tag to the exact commit, successful hosted Actions run, source archive, wheel, tracked-source SHA-256 manifest, release-artifact SHA-256 manifest, SBOM, and available provenance attestations. Clean-user verification of the published source archive must exercise both bounded profile validators.

## Claim boundary

A passing Orbital Recovery Assurance control establishes only its declared structural, arithmetic, reference-resolution, synthetic-policy, or timeline property. It does not establish legal authority, ownership, spacecraft recoverability, flight safety, real-world probability calibration, mission qualification, commercial demand, or authorization for consequential action.

An option may be robust and gate-clear yet still be unattractive relative to HOLD. Eligibility is not recommendation and is never operational authorization.

The public repository contains synthetic/source-neutral examples. Named real-world evidence and sensitive mission records remain outside the public release surface.

## Release gate

A source candidate may advance only when deterministic source validation passes. Stable release additionally requires successful protected hosted V&V on the exact `main` commit and successful clean-user verification of the published artifacts. The stable release remains a deliberate workflow-dispatch ceremony rather than an automatic side effect of merge.
