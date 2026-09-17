# Source Release Receipt — v0.9.0

**Release type:** stable public reference candidate  
**Date:** 2026-09-17  
**Canonical release gate:** NOT READY

## Purpose

Add the smallest FMA-owned assurance-context export required for governed downstream interoperability while preserving existing FMA and FTQC semantics.

## Material changes in v0.9.0

- Added assurance-context export contract `0.1.0` with stable schema identity.
- Added a source-neutral changed-assumption fixture and fail-closed contract tests.
- Excluded raw evidence and preserved declared authority, external-reporting, review-required, HOLD, and reevaluation-opportunity states.
- Preserved FTQC profile contract `0.1`, the universal graph ontology, and accountable human consequential authority.

## Source-level evidence

Release eligibility requires the complete deterministic FMA validation surface, including the new assurance-context contract regressions, all existing assurance profiles, package identity checks, public-release scanning, cross-platform hosted verification, protected-main CodeQL, and clean wheel installation.

## Hosted evidence rule

Commit-specific hosted evidence belongs in GitHub Actions and tagged release metadata, not in this source-controlled receipt. This avoids recursive receipts in which recording a commit SHA creates a different commit SHA.

## Tagged-release evidence rule

The stable release record must bind the accepted tag to the exact protected-main commit, successful hosted Actions run, source archive, wheel, tracked-source SHA-256 manifest, release-artifact SHA-256 manifest, CycloneDX SBOM, and available provenance attestations.

## Verification scope

A PASS attests that the declared software and documentation controls satisfied their acceptance criteria. It does not establish scientific validity, evidence credibility, customer applicability, independent validation, or consequential decision authority.

## Release gate

The v0.9.0 source gate remains **NOT READY** until the bounded contract change passes protected pull-request V&V and the complete protected-main hosted V&V contract. Stable publication remains a separate explicit release action.
