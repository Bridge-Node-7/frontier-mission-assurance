# Source Release Receipt — v0.10.0

**Release type:** stable public reference candidate  
**Date:** 2026-09-17  
**Canonical release gate:** READY

## Purpose

Make the FTQC Assurance profile usable for a governed private one-decision case without weakening the synthetic public reference, moving raw evidence into the repository, or increasing FMA's scientific or decision authority.

## Material changes in v0.10.0

- Advanced FTQC Assurance profile contract from `0.1` to `0.2`.
- Allowed private Resource Estimate Receipts to truthfully declare `synthetic_only: false`.
- Preserved the requirement that public synthetic FTQC reference records declare `synthetic_only: true`.
- Added a generic six-file FTQC case validator for external private case directories.
- Added a human-readable FTQC Decision Basis report.
- Added a private-case operator quickstart.
- Added governed previous/current FTQC case comparison for changed assumptions/context, stale reused estimates, out-of-envelope evidence, expert-review reopen triggers, downstream graph impact, and decision reconsideration.
- Added fail-closed tests for mixed record classes, unresolved decision-gate promotion, missing applicability references, and synthetic-boundary violations.
- Added the generic FTQC case workflow to local/hosted/release V&V.
- Preserved the universal FMA graph ontology, authoritative external evidence custody, expert-review boundaries, and accountable human consequential authority.

## Source-level evidence

Release eligibility requires the complete deterministic FMA validation surface to remain green, including package identity, public-boundary scanning, profile manifests, all assurance-profile validators, FTQC public reference evaluation, the generic FTQC case validator, cross-platform smoke paths, protected-main CodeQL, and clean wheel installation.

The generic FTQC case validator establishes only declared contract coherence and bounded cross-record linkage. It does not establish QEC/decoder correctness, resource-estimator correctness, quantum-hardware performance, independent V&V, government readiness, or permission for consequential action.

## Public/private boundary

No real customer, partner, supplier, architecture, laboratory, program, or controlled evidence is added to the public repository.

Operational private cases remain outside this public repository and reference authoritative evidence rather than relocating it.

## Hosted evidence rule

Commit-specific hosted evidence belongs in GitHub Actions and tagged release metadata, not in this source-controlled receipt.

## Release sequencing

The v0.9.1 source candidate reached READY on protected `main` but was not published as a stable GitHub Release. Its governance and FTQC verification-readiness changes are fully contained in v0.10.0.

To avoid publishing an immediately superseded intermediate artifact, v0.10.0 intentionally supersedes the unreleased v0.9.1 source candidate. The stable-release history therefore remains v0.9.0 until v0.10.0 completes its own protected-main source gate and explicit Stable Release workflow.

## Observed hosted evidence

- Pull-request exact-head V&V run `35296572792`: **PASS**, all seven required jobs.
- Protected-main V&V run `35297166566`: **PASS**, all seven required jobs, including CodeQL on `main`.
- Generic FTQC private-case validation and governed previous/current case comparison both executed inside the protected validation surface.

## Release gate

The v0.10.0 source gate is **READY**. This READY state attests only to the declared source, packaging, boundary, profile, FTQC case, change-impact, and hosted validation controls exercised by the repository.

Stable publication remains a separate explicit action performed only by the repository's `Stable Release` workflow. A source READY state does not itself create a tag or GitHub Release.
