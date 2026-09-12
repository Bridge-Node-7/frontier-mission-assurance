# Changelog

## 0.3.4 — mission decision UX and final public-surface cleanup

- Added the Mission Decision Packet as a bounded evidence-to-decision pattern with explicit reopen conditions.
- Upgraded the synthetic frontier-program example into a worked technical decision walkthrough.
- Simplified the README around mission, evidence, reproducibility, decision basis, and bounded evaluation.
- Replaced internal-facing security shorthand with public-boundary terminology across source, tests, CI, release automation, and contribution surfaces.
- Replaced internal-process-style acceptance/checklist documents with public Acceptance Criteria and Stable Release Acceptance contracts.
- Removed the redundant user-journey simulation artifact and consolidated the public-data boundary.
- Preserved runtime semantics, Scientific Discovery Assurance, cross-platform V&V, dependency review, CodeQL, immutable Action pins, local-only runtime, synthetic-only fixtures, All Rights Reserved licensing, and human consequential decision authority.

## 0.3.3 — pytest development-dependency security remediation

- Updated the pinned development test runner from pytest 8.4.2 to current stable pytest 9.1.1.
- Raised the optional development dependency floor to `pytest>=9.1.1,<10` so supported development installs do not resolve into the affected 8.x line.
- Added a release-surface regression that keeps the security-fixed pytest baseline aligned between `requirements-dev.txt` and package metadata.
- Preserved v0.3.2 build-tool security closure, Node 24 immutable Action pins, dependency review, protected-main CodeQL, Scientific Discovery Assurance behavior, synthetic-only examples, All Rights Reserved licensing, local-only runtime, public-data boundaries, and human consequential decision authority.

## 0.3.2 — build-tool dependency security closure

- Updated pinned setuptools from 80.9.0 to current stable 84.0.0.
- Updated pinned wheel from 0.45.1 to current stable 0.48.0, incorporating upstream security fixes including path-traversal protections.
- Kept package metadata, hosted package smoke, release construction, release-surface tests, and validation documentation aligned on the same build-tool versions.
- Preserved v0.3.1 security controls, Scientific Discovery Assurance behavior, synthetic-only examples, All Rights Reserved licensing, local-only runtime, public-data boundaries, and human consequential decision authority.

## 0.3.1 — security and release hardening

- Moved first-party GitHub Actions to current Node 24 runtimes while retaining immutable commit-SHA pins.
- Added high-severity dependency vulnerability review to the existing required pull-request V&V path.
- Added CodeQL Python analysis to the existing required Python 3.12 protected-main V&V path before stable release eligibility.
- Pinned build-backend/tooling requirements and made hosted package construction non-isolated to reduce release-time dependency drift.
- Added explicit supported-version and private-first vulnerability-reporting guidance.
- Preserved Scientific Discovery Assurance behavior, synthetic-only examples, All Rights Reserved licensing, local-only runtime, public-data boundaries, and human consequential decision authority.

## 0.3.0 — Scientific Discovery Assurance

- Added a bounded Scientific Discovery Assurance profile without creating a new repository or expanding the public runtime into an operational system.
- Added six portable public contracts: Discovery Passport, Research Priority Receipt, Research Boundary Attestation, Formal Proof Record, Replication Receipt, and bounded Agent Provenance Reference.
- Added a fully synthetic linked discovery case that remains visibly `REVIEW_REQUIRED` while specification equivalence and replication are incomplete.
- Added deterministic cross-record validation and negative tests for false priority, research-boundary overclaiming, proof/specification collapse, and incomplete replication.
- Added profile-specific public documentation for attribution, specification equivalence, and limitations.
- Extended hosted cross-platform V&V and stable-release clean-user verification to exercise the scientific-discovery profile.
- Preserved All Rights Reserved licensing, the package-index upload guard, local-only runtime, public-data boundary, and human consequential decision authority.

## 0.2.0 — initial public reference

- Promoted the fully validated RC10 line after public and clean-user acceptance.
- Finalized release identity without expanding runtime behavior or the public-data boundary.
- Retained the All Rights Reserved posture and public package-index upload guard.

## 0.2.0-rc10 — public acceptance and zero-hidden-setup UX

- Corrected duplicate acceptance numbering and made the acceptance sequence machine-verifiable.
- Added public GitHub, clean-user, and exact release-provenance acceptance criteria.
- Removed custom-label dependencies from GitHub issue forms so intake does not depend on undisclosed repository administration.
- Added release-surface regressions for sequential acceptance identifiers and label-independent issue forms.
- Extended maintenance and release-acceptance guidance around public acceptance.
- Preserved RC9 evidence-lifecycle architecture, assurance behavior, public-data boundary, synthetic fixtures, All Rights Reserved posture, deterministic cross-platform reproduction, and immutable CI pins.

## 0.2.0-rc9 — evidence lifecycle and maintenance architecture

- Separated deterministic source validation from commit-specific hosted evidence and tagged-release evidence to prevent stale or recursive receipts.
- Reframed release acceptance as a reusable contract rather than a live status board.
- Added explicit branch/dependency/release maintenance policy for a clean long-lived repository.
- Added the Research Reproducibility Contract as the human-facing companion to executable research receipts.
- Added release-surface regressions that prevent exact commit/run identifiers from being embedded in source-controlled validation receipts.
- Preserved RC8 assurance behavior, public-data boundary, synthetic fixtures, All Rights Reserved posture, deterministic cross-platform reproduction, and immutable CI pins.

## 0.2.0-rc8 — Git hygiene and line-ending determinism

- Removed the three trailing-whitespace defects caught by the pre-commit staged-diff gate.
- Added a repository-level `.gitattributes` policy that normalizes public text files to LF across Windows, macOS, and Linux while preserving common binary types as binary.
- Preserved RC7 assurance behavior, 31-test baseline, deterministic receipt reproduction, public-boundary controls, bounded toolchain, and immutable CI pins.
- Kept the newly created GitHub repository private and empty until this corrected candidate was validated and committed.

## 0.2.0-rc7 — cross-platform receipt determinism

- Forced the synthetic research-receipt output writer to use LF newlines on every supported operating system so byte-level SHA-256 receipts reproduce identically on Windows, macOS, and Linux.
- Aligned the synthetic receipt environment declaration with the project Python floor (`>=3.11`).
- Added Windows reproduction to the hosted cross-platform smoke gate.
- Removed generated package metadata from the frozen public source candidate.
- Preserved the RC6 lint-clean behavior, 31-test suite, public-data boundary, bounded toolchain, and immutable CI pins.

## 0.2.0-rc6 — lint closure and deterministic Windows staging

- Closed all eight Ruff findings observed in the first supported-Python Windows staging rehearsal without changing assurance behavior.
- Preserved the 31-test functional baseline and public-data boundary.
- Added a supported-Python Windows/Git-Bash staging path with bounded validation dependencies to avoid resolver backtracking.
- Updated release identity and evidence surfaces to RC6; RC5 remains immutable evidence of the failed lint gate.

## 0.2.0-rc5 — contract-alignment, runtime-privacy, and final public-quality hardening

- Aligned graph/runtime contract validation for version, statuses, root fields, edge fields, and criticality.
- Tightened research/decision receipt schemas to match runtime non-empty-string requirements.
- Replaced deprecated package-license metadata with PEP 639 `LicenseRef-Proprietary` metadata and explicit license-file packaging.
- Corrected stale `open-source` wording while the candidate remains All Rights Reserved.
- Added `fma --version`, a cross-platform bounded public-reference evaluator, and a public-safe environment fingerprint.
- Added runtime no-network regression coverage, stricter public-boundary handling for unapproved URLs and risky binary/log artifacts, and generic public-safe bug reporting.
- Added concise threat-model, CLI-contract, interoperability, and five-minute-evaluation documentation.

## 0.2.0-rc4 — release-operator and public-surface hardening

- Corrected the Windows PowerShell reproduction path.
- Clarified that external code contributions are not accepted while the All Rights Reserved release-candidate license remains unresolved.
- Hardened the staging operator to be noninteractive and to clean generated validation caches before its final hygiene check.
- Preserved the RC3 public-data boundary and synthetic-only public examples.

## 0.2.0-rc3 — public-reference boundary candidate

- Reframed the repository as a deliberately thin public reference/interoperability layer rather than an operational assurance kernel.
- Removed automated composite assumption-priority scoring from the public implementation.
- Added deterministic open-assumption visibility without assigning engineering priority.
- Removed internal operating-playbook, deployment, and speculative roadmap documents from the public candidate.
- Added an explicit public-reference boundary.
- Reworked the quickstart into separate macOS/Linux and Windows PowerShell paths.
- Pinned GitHub Actions dependencies to immutable commit SHAs.
- Changed the pre-publication candidate from MIT to all-rights-reserved pending an explicit public licensing decision.
- Preserved synthetic-only examples and public-boundary controls.

## 0.2.0-rc2 — public-boundary hardening candidate

- Replaced target-specific examples with fully synthetic, company-agnostic fixtures.
- Removed external program names from public worked examples and playbooks.
- Added public-boundary guidance, automated disclosure-pattern scanning, and GitHub contribution attestations.
- Clarified that public GitHub must never contain live program evidence.

## 0.2.0-rc1 — pre-publication hardening

- Added explicit trusted reproduction separate from non-executing receipt verification.
- Added path-containment enforcement for numerical-check artifacts.
- Added schema conformance and package-install CI rehearsal.
- Hardened CLI error behavior, public boundary, and release hygiene.

## 0.1.0 — internal baseline

Initial reference implementation used for the first design and V&V rehearsal. Not recommended for publication.
