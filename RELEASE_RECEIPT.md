# Source Release Receipt — v0.10.0

**Release type:** stable public reference candidate  
**Date:** 2026-09-17  
**Canonical release gate:** PENDING HOSTED VALIDATION

## Purpose

Make the FTQC Assurance profile usable for a governed private one-decision case without weakening the synthetic public reference, moving raw evidence into the repository, or increasing FMA's scientific or decision authority.

## Material changes in v0.10.0

- Advanced FTQC Assurance profile contract from `0.1` to `0.2`.
- Allowed private Resource Estimate Receipts to truthfully declare `synthetic_only: false`.
- Preserved the requirement that public synthetic FTQC reference records declare `synthetic_only: true`.
- Added a generic six-file FTQC case validator for external private case directories.
- Added a human-readable FTQC Decision Basis report.
- Added a private-case operator quickstart.
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

## Stable-release prerequisite

This v0.10.0 branch must not replace the source-READY v0.9.1 line on protected `main` until stable v0.9.1 has been published through the explicit Stable Release workflow or the release sequence is otherwise intentionally superseded by an accountable operator.

## Release gate

The v0.10.0 source gate remains **PENDING HOSTED VALIDATION** until the complete protected pull-request and protected-main V&V contract passes for the exact candidate state. Stable publication is a separate explicit release action.
