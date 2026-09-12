# Source Release Receipt — v0.3.1

**Release type:** public reference  
**Date:** 2026-09-12

## Purpose

Close the v0.3 line with security and release-pipeline hardening while preserving the deliberately thin public FMA reference, Scientific Discovery Assurance contracts, synthetic-only examples, local-only runtime, and human-owned consequential decisions.

## Baseline

FMA v0.3.0 added the bounded Scientific Discovery Assurance profile on top of the stable v0.2.0 public assurance graph, research-receipt, decision-receipt, cross-platform V&V, OPSEC, reproducibility, package, and release-evidence lifecycle.

## Material changes in v0.3.1

- Move first-party GitHub Actions to current Node 24 runtimes while retaining immutable commit-SHA pins.
- Add high-severity dependency vulnerability review to the existing required pull-request V&V path.
- Add CodeQL Python analysis to the existing required Python 3.12 protected-main V&V path before stable release eligibility.
- Pin build-backend/tooling requirements and use non-isolated package construction in hosted package smoke to reduce release-time dependency drift.
- Add explicit supported-version and private-first vulnerability-reporting guidance.
- Preserve All Rights Reserved licensing, package-index upload guard, synthetic-only public fixtures, public/private OPSEC boundary, Scientific Discovery Assurance semantics, and human decision authority.

## Source-level evidence

The candidate must pass the checks documented in `VALIDATION_REPORT.md`, including core tests, scientific-discovery profile tests, schema/runtime alignment, OPSEC, reproducibility, package construction, link integrity, immutable Action pins, dependency review, main-line CodeQL, and release-surface validation.

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

This source receipt does not claim the current live state of GitHub Actions, repository administration, a future tag, scientific truth, legal priority, research-boundary enforcement, independent scientific acceptance, or the absence of all software vulnerabilities. Those states require their own evidence.

## Release gate

A source candidate may advance only when deterministic source validation passes. Stable release additionally requires successful hosted V&V on the exact commit, configured repository governance/security controls, intentional licensing, release-provenance, and final public UAT.
