# Source Release Receipt — v0.8.0

**Release type:** stable public reference candidate  
**Date:** 2026-09-17  
**Canonical release gate:** READY

## Purpose

Add FTQC Assurance as a bounded profile inside the existing Frontier Mission Assurance architecture while preserving one core assurance language, one release machinery, and one public/private evidence boundary.

Version 0.8.0 introduces **decision-basis continuity** for fault-tolerant quantum programs: when a declared assumption changes, the public synthetic reference can surface which resource estimate, evidence applicability, expert review, claims, and decision require reconsideration.

## Material changes in v0.8.0

- Added `profiles/ftqc-assurance/` as the third bounded FMA profile rather than creating another institutional repository.
- Preserved the universal FMA assurance-graph ontology; FTQC-specific concepts remain profile records and references.
- Added FTQC System Concept, Resource Estimate Receipt, Evidence Validity Envelope, and Expert Adjudication Record contracts.
- Added evidence-class and declared-versus-established applicability semantics so structural records cannot manufacture scientific authority.
- Added explicit internal, external, and independent-review classes.
- Added a modality-neutral Workload-to-System Assurance Chain and synthetic neutral-atom Algorithm-to-Atom reference view.
- Added a deterministic baseline/change pair demonstrating resource-estimate staleness, evidence-envelope invalidation, expert-review reopening, dependency impact, and decision reopening.
- Added a human-readable Decision Basis artifact that separates software/contract validation from technical decision readiness.
- Added one-command local evaluation, tests, Makefile integration, and hosted CI coverage without creating a parallel workflow.
- Added a bounded QBI public crosswalk with no readiness score, implied affiliation, or representation of evaluator internals.
- Aligned Research Receipt documentation with the current 3.1 contract while preserving 3.0, 2.0, and 1.0 compatibility semantics.
- Aligned the canonical local maintainer gate with hosted profile validation, including Scientific Discovery Assurance.
- Formalized the bounded profile architecture and added an explicit Scientific Discovery profile contract without changing the FMA core ontology.
- Refined the public front door around evaluation, one-decision adoption, bounded profiles, and reference material.
- Preserved local-first runtime, source-neutral public examples, existing Research Receipt and Decision Receipt semantics, and accountable human consequential authority.

## Source-level evidence

The candidate satisfies `VALIDATION_REPORT.md`, including the complete FMA regression surface, all assurance profile validators, FTQC changed-assumption impact invariants, cross-platform validation, packaging, dependency review, CodeQL on protected main, and public-release controls.

## Hosted evidence rule

Commit-specific hosted evidence belongs in GitHub Actions and tagged release metadata, not in this source-controlled receipt. This avoids recursive receipts in which recording a commit SHA creates a different commit SHA.

## Tagged-release evidence rule

The stable release record binds the accepted tag to the exact protected-main commit, successful hosted Actions run, source archive, wheel, tracked-source SHA-256 manifest, release-artifact SHA-256 manifest, CycloneDX SBOM, and available provenance attestations. Clean-user verification exercises the published source archive and all assurance profiles.

## Verification scope

A PASS attests that the declared controls satisfied their acceptance criteria. Scientific validity, FTQC performance, QEC validity, resource-estimator correctness, hardware readiness, independent V&V, government-program determinations, supplier qualification, and consequential decision authority remain with the qualified evidence and approval processes responsible for those determinations.

## Release gate

Deterministic source validation and protected hosted V&V have satisfied the source-level release gate. Stable publication remains a separate explicit release action and requires successful clean-user verification of the published artifacts through the Stable Release workflow.
