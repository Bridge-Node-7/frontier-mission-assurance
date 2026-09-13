# Changelog

## 0.3.5 — durable public-release polish

- Refined release evidence and regression naming so the current source reads as a finished product rather than a maintenance narrative.
- Preserved the Mission Decision Packet, explicit reopen conditions, Scientific Discovery Assurance, and bounded public-data model introduced in the v0.3 line.
- Preserved cross-platform V&V, dependency review, CodeQL, immutable Action pins, local-only runtime, synthetic-only fixtures, All Rights Reserved licensing, and human consequential decision authority.
- No assurance-graph, schema, CLI, runtime, or workflow semantics changed from v0.3.4.

## 0.3.4 — mission decision UX and public-surface finalization

- Added the Mission Decision Packet as a bounded evidence-to-decision pattern with explicit reopen conditions.
- Upgraded the synthetic frontier-program example into a worked technical decision walkthrough.
- Simplified the README around mission, evidence, reproducibility, decision basis, and bounded evaluation.
- Standardized public-boundary terminology across source, tests, CI, release automation, and contribution surfaces.
- Consolidated acceptance and release documentation into user-facing contracts.
- Preserved runtime semantics, Scientific Discovery Assurance, cross-platform V&V, dependency review, CodeQL, immutable Action pins, local-only runtime, synthetic-only fixtures, All Rights Reserved licensing, and human consequential decision authority.

## 0.3.3 — development test-runner security remediation

- Updated the pinned development test runner to pytest 9.1.1.
- Raised the optional development dependency floor to `pytest>=9.1.1,<10`.
- Added a release-surface regression that keeps the supported pytest baseline aligned between `requirements-dev.txt` and package metadata.
- Preserved the v0.3.2 security, scientific-discovery, release, and runtime behavior.

## 0.3.2 — build-tool dependency security closure

- Updated pinned setuptools to 84.0.0.
- Updated pinned wheel to 0.48.0, incorporating upstream security fixes including path-traversal protections.
- Kept package metadata, hosted package smoke, release construction, release-surface tests, and validation documentation aligned on the same build-tool versions.

## 0.3.1 — security and release hardening

- Moved first-party GitHub Actions to current Node 24 runtimes while retaining immutable commit-SHA pins.
- Added high-severity dependency vulnerability review to the required pull-request V&V path.
- Added CodeQL Python analysis to protected-main V&V before stable release eligibility.
- Pinned build-backend/tooling requirements and made hosted package construction non-isolated to reduce release-time dependency drift.
- Added supported-version and private vulnerability-reporting guidance.

## 0.3.0 — Scientific Discovery Assurance

- Added six portable contracts: Discovery Passport, Research Priority Receipt, Research Boundary Attestation, Formal Proof Record, Replication Receipt, and bounded Agent Provenance Reference.
- Added a fully synthetic linked discovery case that remains visibly `REVIEW_REQUIRED` while specification equivalence and replication are incomplete.
- Added deterministic cross-record validation and negative tests for false priority, research-boundary overclaiming, proof/specification collapse, and incomplete replication.
- Added profile-specific documentation for attribution, specification equivalence, and limitations.
- Extended hosted cross-platform V&V and stable-release clean-user verification to exercise the scientific-discovery profile.

## 0.2.0 — initial public reference

- Established the portable assurance graph, assumption visibility, evidence coverage, dependency impact, research receipts, explicit trusted reproduction, decision receipts, synthetic examples, and cross-platform verification baseline.
- Established the bounded public-data and claim boundary.
- Established deterministic release provenance and clean-user artifact verification.
- Retained the All Rights Reserved posture and public package-index upload guard.

## Pre-0.2.0 development history

Earlier tagged release candidates remain available in Git history for exact reproducibility. The stable changelog focuses on supported public product evolution rather than intermediate staging iterations.
