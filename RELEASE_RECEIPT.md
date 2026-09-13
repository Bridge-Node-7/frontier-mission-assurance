# Source Release Receipt — v0.4.0

**Release type:** stable public reference  
**Date:** 2026-09-12

## Purpose

Strengthen Frontier Mission Assurance so a reproduction PASS means the declared version-2 code and inputs were checked, the trusted entrypoint ran from a fresh declared-artifact workspace, and the declared outputs were present only after that execution and passed their declared integrity and numerical checks.

## Material changes in v0.4.0

- Introduced the executable Research Receipt v2 contract with explicit code artifacts and `experiment.entrypoint`.
- Bound declared analysis code by SHA-256 before execution.
- Changed `fma reproduce` to stage only the receipt, declared code, and declared inputs into a fresh temporary workspace; declared outputs are intentionally absent before execution.
- Made a zero-exit command that produces no required output fail closed instead of permitting a stale source-tree output to satisfy reproduction.
- Retained legacy version-1 receipts for non-executing historical verification while requiring version 2 for a current fresh-reproduction PASS.
- Made receipt PASS messages enumerate the controls actually executed and reject empty version-2 assurance sections.
- Added controlled exit-2 handling for malformed inputs, CLI discoverability improvements, dependency-cycle/self-loop warnings, deterministic report support through `SOURCE_DATE_EPOCH`, and expanded adversarial rejection-path regressions.
- Preserved Scientific Discovery Assurance, Mission Decision Packets, cross-platform verification, immutable Action pins, dependency review, CodeQL, All Rights Reserved licensing, synthetic-only fixtures, local-only runtime, and human consequential decision authority.

## Source-level evidence

The candidate must pass the checks documented in `VALIDATION_REPORT.md`, including the full Python/cross-platform suite, core/profile tests, schema/runtime alignment, public-boundary validation, fresh code-bound reproduction integrity, rejection-path regressions, deterministic report behavior, packaging, dependency review, CodeQL, and release-surface validation.

## Hosted evidence rule

Commit-specific hosted evidence belongs in GitHub Actions and tagged release metadata, not in this source-controlled receipt. This avoids recursive receipts in which recording a commit SHA requires creating a new commit with a different SHA.

## Tagged-release evidence rule

The public release record binds the accepted tag to the exact commit, successful hosted Actions run, source archive, wheel, tracked-source SHA-256 manifest, and release-artifact SHA-256 manifest.

## Non-claims

A version-2 reproduction workspace is an integrity control, not a sandbox or hermetic environment. This receipt does not claim scientific truth, mission readiness, legal priority, research-boundary enforcement, independent scientific acceptance, authorization for consequential action, or the permanent absence of future dependency vulnerabilities.

## Release gate

A source candidate may advance only when deterministic source validation passes. Stable release additionally requires successful hosted V&V on the exact commit and successful clean-user verification of the published artifacts.
