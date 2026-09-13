# Source Release Receipt — v0.4.1

**Release type:** stable public reference  
**Date:** 2026-09-12

## Purpose

Harden FMA's portability boundary so the three core contracts are consistently identifiable, richer domain systems can map into FMA without losing local semantics, and public positioning is explicit about established assurance/provenance prior art and unsigned-receipt limits.

## Material changes in v0.4.1

- Added stable `$id` identifiers to the core Research Receipt v2 and Decision Receipt v1 schemas, completing stable identifiers across all three core portable contracts.
- Clarified interoperability as an adapter problem rather than a mandate for one universal evidence or decision ontology.
- Added explicit adapter rules: preserve source provenance, retain richer domain semantics in the owning system, and fail visibly on ambiguity or information loss.
- Added public standards positioning that does not claim novelty for established assurance-case, provenance, hashing, reproducibility, or regression-testing primitives.
- Clarified that unsigned core receipts establish declared integrity/consistency, not authorship or signer identity.
- Preserved the v0.4.0 fresh code-bound reproduction contract, Scientific Discovery Assurance, Mission Decision Packets, cross-platform verification, immutable Action pins, dependency review, CodeQL, All Rights Reserved licensing, synthetic-only fixtures, local-only runtime, and human consequential decision authority.

## Source-level evidence

The candidate must pass the checks documented in `VALIDATION_REPORT.md`, including the full Python/cross-platform suite, core/profile tests, schema/runtime alignment, stable core schema identifiers, public-boundary validation, fresh code-bound reproduction integrity, rejection-path regressions, deterministic report behavior, packaging, dependency review, CodeQL, and release-surface validation.

## Hosted evidence rule

Commit-specific hosted evidence belongs in GitHub Actions and tagged release metadata, not in this source-controlled receipt. This avoids recursive receipts in which recording a commit SHA requires creating a new commit with a different SHA.

## Tagged-release evidence rule

The public release record binds the accepted tag to the exact commit, successful hosted Actions run, source archive, wheel, tracked-source SHA-256 manifest, and release-artifact SHA-256 manifest.

## Non-claims

FMA does not claim invention of assurance cases, provenance records, content hashing, reproducible workflows, numerical regression checks, or cryptographic attestation. Core FMA receipts are unsigned and therefore do not independently establish authorship or signer identity. A version-2 reproduction workspace remains an integrity control, not a sandbox or hermetic environment.

This receipt does not claim scientific truth, mission readiness, legal priority, research-boundary enforcement, independent scientific acceptance, authorization for consequential action, or the permanent absence of future dependency vulnerabilities.

## Release gate

A source candidate may advance only when deterministic source validation passes. Stable release additionally requires successful hosted V&V on the exact commit and successful clean-user verification of the published artifacts.
