# Source Release Receipt — v0.3.4

**Release type:** stable public reference  
**Date:** 2026-09-12

## Purpose

Finalize the public product surface around mission-oriented technical review while preserving FMA runtime semantics, release integrity, and the synthetic-only public-data boundary.

## Material changes in v0.3.4

- Added the Mission Decision Packet pattern and worked synthetic decision walkthrough.
- Made explicit reopen conditions a first-class part of the public decision-review experience.
- Simplified the README around mission, evidence, reproducibility, decision basis, and bounded evaluation.
- Replaced internal-facing security shorthand and process-artifact naming with product-facing public-boundary and acceptance terminology.
- Consolidated public-boundary documentation and removed redundant internal-process-style documents from the current tree.
- Preserved Scientific Discovery Assurance semantics, cross-platform verification, immutable Action pins, dependency review, CodeQL, All Rights Reserved licensing, synthetic-only fixtures, local-only runtime, and human consequential decision authority.

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
