# Source Release Receipt — v0.3.0

**Release type:** public reference  
**Date:** 2026-09-12

## Purpose

Extend the deliberately thin FMA public reference with Scientific Discovery Assurance contracts for provenance, priority evidence, research-boundary declarations, proof/specification separation, replication, attribution chronology, and bounded machine-run references without exposing private operational systems or real research evidence.

## Baseline

FMA v0.2.0 established the stable public assurance graph, research-receipt, decision-receipt, cross-platform V&V, OPSEC, reproducibility, package, and release-evidence lifecycle. v0.3.0 preserves those behaviors and boundaries.

## Material changes in v0.3.0

- Add a public-safe `profiles/scientific-discovery/` contract set.
- Add `DiscoveryPassport`, `ResearchPriorityReceipt`, `ResearchBoundaryAttestation`, `FormalProofRecord`, `ReplicationReceipt`, and bounded `AgentProvenanceRef` schemas.
- Add a fully synthetic linked discovery case that intentionally remains `REVIEW_REQUIRED`.
- Add deterministic cross-record validation for the synthetic profile.
- Add explicit safeguards that local time alone does not establish trusted priority, a declared research boundary is not proof of enforcement, proof-checker success does not collapse specification-equivalence review, and incomplete replication cannot become overall `PASS`.
- Preserve All Rights Reserved licensing, the package-index upload guard, public/private boundaries, human decision authority, and the core v0.2.0 runtime semantics.

## Source-level evidence

The candidate must pass the checks documented in `VALIDATION_REPORT.md`, including core tests, scientific-discovery profile tests, schema/runtime alignment, OPSEC, reproducibility, package construction, link integrity, and release-surface validation.

## Hosted evidence rule

Commit-specific hosted evidence belongs in GitHub Actions and tagged release metadata, not in this source-controlled receipt. This avoids recursive receipts in which recording a commit SHA requires creating a new commit with a different SHA.

## Tagged-release evidence rule

The public release record binds the accepted tag to:

- exact commit SHA;
- successful hosted Actions run;
- source archive;
- wheel;
- external SHA-256 manifest;
- final public-boundary / governance acceptance.

## Non-claims

This source receipt does not claim the current live state of GitHub Actions, repository administration, a future tag, scientific truth, legal priority, research-boundary enforcement, or independent scientific acceptance. Those states require their own evidence.

## Release gate

A source candidate may advance only when deterministic source validation passes. Stable release additionally requires successful hosted V&V on the exact commit, configured repository governance/security controls, intentional licensing, and final public UAT.
