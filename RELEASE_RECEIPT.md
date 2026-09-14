# Source Release Receipt — v0.6.0

**Release type:** stable public reference candidate  
**Date:** 2026-09-13

## Purpose

Strengthen FMA's trust semantics and public-release boundary without expanding it into a universal assurance platform. Version 0.6.0 adds Git-tracked release-surface scanning, Research Receipt 3.1 chronology, explicit per-output assurance scope, and clearer non-claims around unsigned external provenance.

## Material changes in v0.6.0

- The authoritative public-boundary scan now evaluates every Git-tracked release file regardless of directory name; force-tracked content under build/cache paths cannot bypass the release boundary.
- Research Receipt 3.1 explicitly distinguishes `EXACT`, `SEMANTICALLY_CHECKED`, and `RECORD_ONLY` outputs while preserving an observed SHA-256 for every output.
- Semantic output acceptance must name the checks that define bounded equivalence for that output; record-only outputs carry no equivalence claim.
- External receipt evidence now binds `submitted_at`, `started_at`, `completed_at`, and `collected_at` chronology.
- Required calibration state must cover the declared external execution interval.
- Research Receipt 3.0 remains supported as a legacy compatibility contract; 3.1 receives the strengthened semantics.
- Public documentation now states the current v0.6 maturity line and surfaces the evaluation/reference-use licensing boundary near onboarding.
- Existing graph, decision, Scientific Discovery Assurance, fresh-workspace reproduction, cross-platform, immutable-Action, dependency-review, CodeQL, local-runtime, synthetic-fixture, and human-authority controls remain in scope.

## Source-level evidence

The candidate must satisfy `VALIDATION_REPORT.md`, including Python/cross-platform verification, schema/runtime alignment, public-boundary adversarial tests, exact/semantic/record-only output tests, external chronology and calibration-interval mutation tests, fresh reproduction integrity, deterministic reporting, packaging, dependency review, CodeQL, and release-surface validation.

## Hosted evidence rule

Commit-specific hosted evidence belongs in GitHub Actions and tagged release metadata, not in this source-controlled receipt. This avoids recursive receipts in which recording a commit SHA creates a different commit SHA.

## Tagged-release evidence rule

The public release record must bind the accepted tag to the exact commit, successful hosted Actions run, source archive, wheel, tracked-source SHA-256 manifest, and release-artifact SHA-256 manifest. Additional provenance or SBOM artifacts may strengthen supply-chain assurance, but absence of an external signature must never be presented as authenticated authorship.

## Non-claims

FMA does not claim invention of assurance cases, provenance records, content hashing, reproducible workflows, numerical regression checks, or cryptographic attestation. Core FMA receipts are unsigned unless wrapped by a separate authenticated mechanism and therefore do not independently establish authorship or signer identity.

An observed output hash establishes artifact identity. A semantic check establishes only the declared bounded criterion. Neither establishes scientific truth. The fresh reproduction workspace is an integrity control, not a sandbox or hermetic environment. External scheduler records are declarations unless a separate trust mechanism authenticates their issuer.

This receipt does not claim mission readiness, legal priority, research-boundary enforcement, independent scientific acceptance, authorization for consequential action, certification, compliance, or permanent absence of future vulnerabilities.

## Release gate

A source candidate may advance only when deterministic source validation passes. Stable release additionally requires successful hosted V&V on the exact commit and successful clean-user verification of the published artifacts.
