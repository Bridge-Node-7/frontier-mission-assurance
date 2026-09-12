# Source Release Receipt — v0.2.0-rc9

**Candidate type:** public-reference release candidate
**Date:** 2026-09-12

## Purpose

Provide a deliberately thin, inspectable public reference for evidence-native verification, validation, reproducibility, and decision-basis traceability without exposing private operational systems or real program evidence.

## RC9 trigger

RC8 achieved exact source-tree parity and successful hosted cross-platform V&V. The final audit then identified a documentation-lifecycle weakness: source-controlled evidence files still described hosted checks as unproven even after those checks had passed. RC9 corrects that architecture rather than embedding another mutable live status into source.

## Material changes in RC9

- Separate deterministic source validation from commit-specific hosted evidence and tagged-release evidence.
- Make the release checklist explicitly a reusable template rather than a live status board.
- Add maintenance/branch/dependency policy for a clean long-lived repository.
- Add a Research Reproducibility Contract that formalizes the human-facing companion to executable research receipts.
- Add regression coverage preventing commit-specific SHA/run state from being embedded in source-controlled validation/receipt files.
- Preserve the bounded public product, synthetic fixtures, All Rights Reserved posture, and existing assurance behavior.

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
