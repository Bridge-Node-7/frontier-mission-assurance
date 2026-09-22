# Source Release Receipt — v0.11.1

**Release type:** stable public reference candidate  
**Date:** 2026-09-21  
**Validation status:** READY FOR HOSTED VALIDATION; PUBLICATION REQUIRES IMMUTABLE-RELEASE PROTECTION

## Purpose

Reduce cross-repository maintenance while preserving the fail-closed FTQC technical-evidence boundary, exact contract identity, explicit producer review, and accountable human authority.

## Material changes in v0.11.1

- Added low-churn `INTERFACES.json` declarations for the FMA Assurance Graph, Decision Receipt, assurance-context, and bounded FTQC input contracts.
- Separated portable contract versions and exact schema SHA-256 values from the FMA application version.
- Moved reviewed FTQC producer releases into a governed, human-review-required compatibility registry.
- Preserved exact schema/artifact integrity checks, one-input linkage, architecture consistency, evidence-class mapping, applicability semantics, and future-release fail-closed behavior.
- Added a release preflight that prevents a future stable publication unless repository immutable-release protection is enabled.
- Preserved FTQC profile contract `0.2`, assurance-context `0.1.0`, browser/user-facing behavior, and human consequential authority.

## Source-level evidence

Release eligibility requires the full deterministic FMA validation surface plus the interface-manifest, reviewed-producer-registry, and FTQC processor-evidence adapter regressions to remain green.

These controls establish only declared interoperability, integrity, reviewed implementation compatibility, and bounded assurance semantics. They do not establish quantum truth, hardware performance, independent V&V, certification, government readiness, or consequential decision authority.

## Hosted evidence rule

Hosted validation evidence is recorded in GitHub Actions and release metadata.

## Publication gate

The v0.11.1 source may be merged after native V&V passes. The Stable Release workflow must fail before publication unless GitHub immutable-release protection is enabled for future releases. Historical v0.11.0 is preserved as published.

## Validation status

The source candidate is **READY** when required native CI passes. Publication remains a separate governed action and must not occur until the immutable-release setting is verified.
