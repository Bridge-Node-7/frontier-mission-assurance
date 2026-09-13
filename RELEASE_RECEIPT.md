# Source Release Receipt — v0.3.5

**Release type:** stable public reference  
**Date:** 2026-09-12

## Purpose

Establish a durable public product baseline around mission-oriented technical review while preserving FMA runtime semantics, release integrity, and the synthetic-only public-data boundary.

## Material changes in v0.3.5

- Normalized release evidence and regression-test naming for a durable public surface.
- Kept the Mission Decision Packet and explicit reopen conditions as first-class parts of the public decision-review experience.
- Preserved Scientific Discovery Assurance semantics, cross-platform verification, immutable Action pins, dependency review, CodeQL, All Rights Reserved licensing, synthetic-only fixtures, local-only runtime, and human consequential decision authority.
- No assurance-graph, schema, CLI, runtime, or workflow semantics changed from v0.3.4.

## Source-level evidence

The candidate must pass the checks documented in `VALIDATION_REPORT.md`, including the full Python/cross-platform suite, core/profile tests, schema/runtime alignment, public-boundary validation, deterministic reproduction, packaging, dependency review, CodeQL, and release-surface validation.

## Hosted evidence rule

Commit-specific hosted evidence belongs in GitHub Actions and tagged release metadata, not in this source-controlled receipt. This avoids recursive receipts in which recording a commit SHA requires creating a new commit with a different SHA.

## Tagged-release evidence rule

The public release record binds the accepted tag to the exact commit, successful hosted Actions run, source archive, wheel, tracked-source SHA-256 manifest, and release-artifact SHA-256 manifest.

## Non-claims

This receipt does not claim scientific truth, mission readiness, legal priority, research-boundary enforcement, independent scientific acceptance, or the permanent absence of future dependency vulnerabilities.

## Release gate

A source candidate may advance only when deterministic source validation passes. Stable release additionally requires successful hosted V&V on the exact commit and successful clean-user verification of the published artifacts.
