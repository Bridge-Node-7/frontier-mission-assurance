# Source Release Receipt — v0.3.2

**Release type:** public reference  
**Date:** 2026-09-12

## Purpose

Close the immediate build-tool dependency security findings discovered immediately after v0.3.1 while preserving FMA's deliberately thin public reference boundary and assurance semantics.

## Baseline

FMA v0.3.1 introduced current Node 24 GitHub Actions, pull-request dependency review, protected-main CodeQL, pinned build tooling, and private-first vulnerability-reporting guidance.

## Material changes in v0.3.2

- Update the pinned build backend from setuptools 80.9.0 to the current stable setuptools 84.0.0.
- Update the pinned wheel tooling from wheel 0.45.1 to the current stable wheel 0.48.0, incorporating upstream security fixes including path-traversal protections published in later wheel releases.
- Keep the same pinned build 1.6.1 release, which remains current.
- Keep build pins aligned across package metadata, hosted package smoke, stable-release construction, validation tests, and release documentation.
- Preserve Node 24 immutable Action pins, dependency review, CodeQL, All Rights Reserved licensing, synthetic-only fixtures, local-only runtime, Scientific Discovery Assurance behavior, and human decision authority.

## Source-level evidence

The candidate must pass the checks documented in `VALIDATION_REPORT.md`, including core tests, profile tests, schema/runtime alignment, OPSEC, deterministic reproduction, packaging, dependency review, CodeQL, and release-surface validation.

## Hosted evidence rule

Commit-specific hosted evidence belongs in GitHub Actions and tagged release metadata, not in this source-controlled receipt. This avoids recursive receipts in which recording a commit SHA requires creating a new commit with a different SHA.

## Tagged-release evidence rule

The public release record binds the accepted tag to the exact commit, successful hosted Actions run, source archive, wheel, tracked-source SHA-256 manifest, and release-artifact SHA-256 manifest.

## Non-claims

This receipt does not claim scientific truth, mission readiness, legal priority, research-boundary enforcement, independent scientific acceptance, or the permanent absence of future dependency vulnerabilities.

## Release gate

A source candidate may advance only when deterministic source validation passes. Stable release additionally requires successful hosted V&V on the exact commit and final clean-user public UAT.
