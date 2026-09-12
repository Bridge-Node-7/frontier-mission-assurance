# Changelog

## 0.2.0-rc10 — public acceptance and zero-hidden-setup UX

- Corrected duplicate UAT numbering and made the acceptance sequence machine-verifiable.
- Added logged-out public GitHub, external clean-user, and exact release-provenance UATs.
- Removed custom-label dependencies from GitHub issue forms so intake does not depend on undisclosed repository administration.
- Added release-surface regressions for sequential UAT identifiers and label-independent issue forms.
- Extended maintenance, UX simulation, and release checklist guidance around public acceptance.
- Preserved RC9 evidence-lifecycle architecture, assurance behavior, public/private boundary, synthetic fixtures, All Rights Reserved posture, deterministic cross-platform reproduction, and immutable CI pins.

## 0.2.0-rc9 — evidence lifecycle and maintenance architecture

- Separated deterministic source validation from commit-specific hosted evidence and tagged-release evidence to prevent stale or recursive receipts.
- Reframed the release checklist as a reusable template rather than a live status board.
- Added explicit branch/dependency/release maintenance policy for a clean long-lived repository.
- Added the Research Reproducibility Contract as the human-facing companion to executable research receipts.
- Added release-surface regressions that prevent exact commit/run identifiers from being embedded in source-controlled validation receipts.
- Preserved RC8 assurance behavior, public/private boundary, synthetic fixtures, All Rights Reserved posture, deterministic cross-platform reproduction, and immutable CI pins.

## 0.2.0-rc8 — Git hygiene and line-ending determinism

- Removed the three trailing-whitespace defects caught by the pre-commit staged-diff gate.
- Added a repository-level `.gitattributes` policy that normalizes public text files to LF across Windows, macOS, and Linux while preserving common binary types as binary.
- Preserved RC7 assurance behavior, 31-test baseline, deterministic receipt reproduction, OPSEC controls, bounded dependency toolchain, and immutable CI pins.
- Kept the newly created GitHub repository private and empty until this corrected candidate is validated and committed.

## 0.2.0-rc7 — cross-platform receipt determinism

- Forced the synthetic research-receipt output writer to use LF newlines on every supported operating system so byte-level SHA-256 receipts reproduce identically on Windows, macOS, and Linux.
- Aligned the synthetic receipt environment declaration with the project Python floor (`>=3.11`).
- Added Windows reproduction to the hosted cross-platform smoke gate.
- Removed generated package metadata from the frozen public source candidate.
- Preserved the RC6 lint-clean behavior, 31-test suite, OPSEC boundary, bounded toolchain, and immutable CI pins.

## 0.2.0-rc6 — lint closure and deterministic Windows staging

- Closed all eight Ruff findings observed in the first supported-Python Windows staging rehearsal without changing assurance behavior.
- Preserved the 31-test functional baseline and public/private OPSEC boundary.
- Added a supported-Python Windows/Git-Bash staging path with bounded validation dependencies to avoid resolver backtracking.
- Updated release identity and evidence surfaces to RC6; RC5 remains immutable evidence of the failed lint gate.

## 0.2.0-rc5 — contract-alignment, runtime-privacy, and final public-quality hardening

- Aligned graph/runtime contract validation for version, statuses, root fields, edge fields, and criticality.
- Tightened research/decision receipt schemas to match runtime non-empty-string requirements.
- Replaced deprecated package-license metadata with PEP 639 `LicenseRef-Proprietary` metadata and explicit license-file packaging.
- Corrected stale `open-source` wording while the candidate remains All Rights Reserved.
- Added `fma --version`, a cross-platform bounded public-reference evaluator, and a public-safe environment fingerprint.
- Added runtime no-network regression coverage, stricter OPSEC handling for unapproved URLs and risky binary/log artifacts, and generic public-safe bug reporting.
- Added concise threat-model, CLI-contract, interoperability, and five-minute-evaluation documentation.

## 0.2.0-rc4 — release-operator and public-surface hardening

- Corrected the Windows PowerShell reproduction path.
- Clarified that external code contributions are not accepted while the All Rights Reserved release-candidate license remains unresolved.
- Hardened the private staging operator to be noninteractive and to clean generated validation caches before its final hygiene check.
- Preserved the RC3 public/private architectural boundary and synthetic-only public examples.

## 0.2.0-rc3 — public-reference boundary candidate

- Reframed the repository as a deliberately thin public reference/interoperability layer rather than an operational assurance kernel.
- Removed automated composite assumption-priority scoring from the public implementation.
- Added deterministic open-assumption visibility without assigning engineering priority.
- Removed internal operating-playbook, private-deployment, and speculative roadmap documents from the public candidate.
- Added an explicit public-reference architectural boundary.
- Reworked the quickstart into separate macOS/Linux and Windows PowerShell paths.
- Pinned GitHub Actions dependencies to immutable commit SHAs.
- Changed the pre-publication candidate from MIT to all-rights-reserved pending an explicit public licensing decision.
- Preserved synthetic-only examples and OPSEC/public-boundary controls.

## 0.2.0-rc2 — OPSEC hardening candidate

- Replaced target-specific examples with fully synthetic, company-agnostic fixtures.
- Removed external program names from public worked examples and playbooks.
- Added OPSEC guidance, automated disclosure-pattern scanning, and GitHub contribution attestations.
- Clarified that public GitHub must never contain live program evidence.

## 0.2.0-rc1 — pre-publication hardening

- Added explicit trusted reproduction separate from non-executing receipt verification.
- Added path-containment enforcement for numerical-check artifacts.
- Added schema conformance and package-install CI rehearsal.
- Hardened CLI error behavior, public boundary, and release hygiene.

## 0.1.0 — internal baseline

Initial reference implementation used for the first design and V&V rehearsal. Not recommended for publication.
