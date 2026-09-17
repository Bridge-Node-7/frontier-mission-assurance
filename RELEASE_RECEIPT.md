# Source Release Receipt — v0.8.0

**Release type:** stable public reference candidate  
**Date:** 2026-09-17  
**Canonical release gate:** READY

## Purpose

Finalize FTQC Assurance as a bounded profile inside the existing Frontier Mission Assurance architecture and close the last-mile operational-adoption gaps needed for a technical team to evaluate FMA on work it already owns.

Version 0.8.0 preserves **decision-basis continuity** for fault-tolerant quantum programs while adding a source-neutral existing-work path, profile discovery manifests, stable-install guidance, bounded automation guidance, and explicit evaluation/use boundaries.

## Material changes in v0.8.0

- Added `profiles/ftqc-assurance/` as the third bounded FMA profile rather than creating another institutional repository.
- Preserved the universal FMA assurance-graph ontology; FTQC-specific concepts remain profile records and references.
- Added FTQC System Concept, Resource Estimate Receipt, Evidence Validity Envelope, and Expert Adjudication Record contracts.
- Added evidence-class and declared-versus-established applicability semantics so structural records cannot manufacture scientific authority.
- Added explicit internal, external, and independent-review classes.
- Added a modality-neutral Workload-to-System Assurance Chain and synthetic neutral-atom reference view.
- Added a deterministic baseline/change pair demonstrating resource-estimate staleness, evidence-envelope invalidation, expert-review reopening, dependency impact, and decision reopening.
- Added a human-readable Decision Basis artifact that separates software/contract validation from technical decision readiness.
- Aligned Research Receipt documentation with the current 3.1 contract while preserving 3.0, 2.0, and 1.0 compatibility semantics.
- Aligned the canonical local maintainer gate with hosted profile validation, including Scientific Discovery Assurance.
- Formalized the bounded profile architecture and added an explicit Scientific Discovery profile contract without changing the FMA core ontology.
- Added machine-readable profile manifests plus deterministic manifest validation without creating a plugin runtime.
- Added a source-neutral existing-repository sidecar and validation path showing how FMA can wrap external work without modifying the authoritative source repository.
- Added adoption guidance for repositories, papers, paper-plus-code, models, simulations, experiments, and external execution.
- Added stable-release installation and verification guidance for source archives, wheels, checksums, SBOMs, and provenance attestations.
- Added a bounded AI/automation quickstart that defaults to read-only treatment of authoritative external work and preserves human consequential authority.
- Added explicit evaluation/use documentation that preserves the All Rights Reserved license and directs use beyond public evaluation to separate written permission or agreement.
- Refined the public front door around product value, a 90-second changed-assumption walkthrough, evaluation, existing-work adoption, bounded profiles, and reference material.
- Restored bounded monthly dependency-update proposals while preserving human review and full V&V before acceptance.
- Preserved local-first runtime, source-neutral public examples, Research Receipt and Decision Receipt semantics, public/private evidence boundaries, and accountable human consequential authority.

## Source-level evidence

This candidate satisfies `VALIDATION_REPORT.md`, including the complete FMA regression surface, profile-manifest validation, external-research sidecar validation, all assurance profile validators, FTQC changed-assumption impact invariants, cross-platform validation, packaging, CodeQL on protected main, and public-release controls. Pull-request dependency review also passed before the operational-adoption change entered `main`.

## Hosted evidence rule

Commit-specific hosted evidence belongs in GitHub Actions and tagged release metadata, not in this source-controlled receipt. This avoids recursive receipts in which recording a commit SHA creates a different commit SHA.

## Tagged-release evidence rule

The stable release record binds the accepted tag to the exact protected-main commit, successful hosted Actions run, source archive, wheel, tracked-source SHA-256 manifest, release-artifact SHA-256 manifest, CycloneDX SBOM, and available provenance attestations. Clean-user verification exercises the published source archive, profile manifests, existing-work sidecar, and all assurance profiles.

## Verification scope

A PASS attests that the declared controls satisfied their acceptance criteria. Scientific validity, FTQC performance, QEC validity, resource-estimator correctness, hardware readiness, independent V&V, government-program determinations, supplier qualification, and consequential decision authority remain with the qualified evidence and approval processes responsible for those determinations.

## Release gate

The operational-adoption change passed its protected pull-request V&V gate and then passed the complete protected-main hosted V&V contract, including CodeQL and cross-platform verification. The v0.8.0 source gate is therefore **READY**. Stable publication remains a separate explicit release action and requires the Stable Release workflow to bind the published artifacts to the final READY protected-main commit and complete its clean-user verification.
