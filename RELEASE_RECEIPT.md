# Source Release Receipt — v0.3.3

**Release type:** public reference  
**Date:** 2026-09-12

## Purpose

Close the open pytest development-dependency security finding while preserving FMA's deliberately thin public reference boundary and assurance semantics.

## Baseline

FMA v0.3.2 closed the build-tool dependency security findings and retained Node 24 immutable Action pins, pull-request dependency review, protected-main CodeQL, pinned build tooling, clean-user release UAT, and private-first vulnerability-reporting guidance.

## Material changes in v0.3.3

- Update the pinned development test runner from pytest 8.4.2 to pytest 9.1.1.
- Raise the optional development dependency floor to pytest >=9.1.1,<10 so supported development environments do not resolve back into the affected 8.x line.
- Add a release-surface regression that keeps the security-fixed pytest baseline aligned between `requirements-dev.txt` and package metadata.
- Preserve runtime dependencies, Scientific Discovery Assurance semantics, Node 24 immutable Action pins, dependency review, CodeQL, All Rights Reserved licensing, synthetic-only fixtures, local-only runtime, OPSEC boundaries, and human decision authority.

## Source-level evidence

The candidate must pass the checks documented in `VALIDATION_REPORT.md`, including the full Python/cross-platform suite, core/profile tests, schema/runtime alignment, OPSEC, deterministic reproduction, packaging, dependency review, CodeQL, and release-surface validation under pytest 9.1.1.

## Hosted evidence rule

Commit-specific hosted evidence belongs in GitHub Actions and tagged release metadata, not in this source-controlled receipt. This avoids recursive receipts in which recording a commit SHA requires creating a new commit with a different SHA.

## Tagged-release evidence rule

The public release record binds the accepted tag to the exact commit, successful hosted Actions run, source archive, wheel, tracked-source SHA-256 manifest, and release-artifact SHA-256 manifest.

## Non-claims

This receipt does not claim scientific truth, mission readiness, legal priority, research-boundary enforcement, independent scientific acceptance, or the permanent absence of future dependency vulnerabilities.

## Release gate

A source candidate may advance only when deterministic source validation passes. Stable release additionally requires successful hosted V&V on the exact commit and final clean-user public UAT.
