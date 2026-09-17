# Source Release Receipt — v0.8.1

**Release type:** stable public reference candidate  
**Date:** 2026-09-17  
**Canonical release gate:** PENDING HOSTED V&V

## Purpose

Harden the external FTQC resource-estimate evidence boundary without changing the FTQC profile contract, universal FMA graph ontology, runtime semantics, or public synthetic fixtures.

Version 0.8.1 preserves the v0.8.0 FTQC Assurance architecture while making one external-artifact lesson explicit: a third-party reported resource estimate must not become a fresh-reproduction, independent-validation, or system-applicability claim merely because the number is recorded in FMA.

## Material changes in v0.8.1

- Clarified in the FTQC assurance scope that profile contract `0.1` Resource Estimate Receipts remain synthetic/reference-only.
- Added external-research adoption guidance for third-party resource estimates.
- Added regression coverage that protects the synthetic-only receipt contract and the documented external-evidence boundary.
- Preserved FTQC profile contract `0.1`, all existing schema identities, the public source-neutral fixture policy, the FMA core ontology, and accountable human consequential authority.
- Updated source/package/citation/project-facts identity to v0.8.1.

## Source-level evidence

Release eligibility requires the complete deterministic FMA validation surface, including the FTQC boundary regression, all existing assurance profiles, package identity checks, public-release scanning, cross-platform hosted verification, protected-main CodeQL, and clean wheel installation.

## Hosted evidence rule

Commit-specific hosted evidence belongs in GitHub Actions and tagged release metadata, not in this source-controlled receipt. This avoids recursive receipts in which recording a commit SHA creates a different commit SHA.

## Tagged-release evidence rule

The stable release record must bind the accepted tag to the exact protected-main commit, successful hosted Actions run, source archive, wheel, tracked-source SHA-256 manifest, release-artifact SHA-256 manifest, CycloneDX SBOM, and available provenance attestations.

## Verification scope

A PASS attests that the declared software and documentation controls satisfied their acceptance criteria. Scientific validity, FTQC performance, QEC validity, resource-estimator correctness, hardware readiness, independent V&V, customer applicability, supplier qualification, and consequential decision authority remain with the qualified evidence and approval processes responsible for those determinations.

## Release gate

The v0.8.1 source candidate is not READY merely because this source record exists. It becomes READY only after the protected pull-request checks and the complete protected-main hosted V&V contract pass on the exact accepted source state. Stable publication remains a separate explicit release action.
