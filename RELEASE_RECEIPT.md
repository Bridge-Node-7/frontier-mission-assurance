# Source Release Receipt — v0.2.0

**Release type:** public reference
**Date:** 2026-09-12

## Purpose

Provide a deliberately thin, inspectable public reference for evidence-native verification, validation, reproducibility, and decision-basis traceability without exposing private operational systems or real program evidence.

## RC10 trigger

RC9 established the release-evidence lifecycle and maintenance architecture, then passed exact-tree hosted cross-platform V&V. Final UX/UAT review found two public-interface defects: duplicate UAT numbering and issue forms that depended on custom GitHub labels not guaranteed to exist. RC10 removes those hidden setup assumptions and completes the public acceptance contract.

## Material changes in RC10

- Make UAT identifiers unique and sequential.
- Add explicit logged-out public GitHub, external clean-user, and release-provenance acceptance tests.
- Remove custom-label dependencies from all issue forms so public-safe intake works without hidden repository setup.
- Add regression coverage for sequential UAT numbering and label-independent issue forms.
- Extend maintenance, UX simulation, and release-checklist guidance to preserve those guarantees.
- Preserve the bounded public product, release-evidence lifecycle, synthetic fixtures, All Rights Reserved posture, and existing assurance behavior.

## Source-level evidence

The candidate must pass the checks documented in `VALIDATION_REPORT.md`, including tests, schema/runtime alignment, OPSEC, reproducibility, package construction, link integrity, and release-surface validation.

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

This source receipt does not claim the current live state of GitHub Actions, repository administration, public visibility, or a future tagged release. Those states are verified at the GitHub/release layer.

## Release gate

A source candidate may advance only when deterministic source validation passes. Public release additionally requires successful hosted V&V on the exact commit, configured repository governance/security controls, intentional licensing, and final public UAT.

## Final promotion trigger

The final `v0.2.0` identity is a release-only promotion of the fully validated RC10 line after repository governance, public logged-out UAT, RC10 tagged pre-release, Bridge Node 7 profile integration, and external clean-user evaluation pass. Runtime behavior and the public/private architecture boundary are intentionally unchanged.
