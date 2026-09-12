# Release Receipt — v0.2.0-rc8

**Candidate type:** public-reference release candidate
**Date:** 2026-09-11

## Purpose

Provide a deliberately thin, inspectable public reference for evidence-native verification, validation, reproducibility, and decision-basis traceability without exposing private operational systems or real program evidence.

## RC8 trigger

RC7 passed the supported-Python Windows lint, test, OPSEC, reproduction, evaluation, and package-smoke gates. The pre-commit staged-diff check then detected three trailing-whitespace defects in public release documentation, while local Git warned that its Windows configuration could rewrite LF text to CRLF. RC8 removes the whitespace defects and adds a repository-level LF-normalization policy before the first source commit is published.

## Material changes carried into RC8

- Removed all trailing whitespace detected by the staged-diff gate.
- Added `.gitattributes` with `* text=auto eol=lf` so public text has deterministic line endings across supported developer platforms.
- Aligned published schemas and runtime behavior for graph versions, statuses, root/edge fields, criticality, and non-empty receipt fields.
- Modernized package license metadata to PEP 639 `LicenseRef-Proprietary` form and explicitly packaged the license file.
- Added `Private :: Do Not Upload` to block accidental public package-index publication during the licensing gate.
- Corrected stale open-source wording while the candidate remains All Rights Reserved.
- Added `fma --version`, bounded cross-platform evaluation, and a public-safe environment fingerprint.
- Added runtime no-network regression coverage, stricter public OPSEC scanning, and public-safe generic bug reporting.
- Added concise threat-model, CLI-contract, interoperability, and five-minute-evaluation documentation.
- Hardened hosted CI with read-only permissions, immutable Action SHAs, non-persistent checkout credentials, job timeouts, dependency-consistency checks, and short artifact retention.
- Closed all eight Ruff 0.16.7 findings observed on the supported-Python Windows rehearsal and added bounded direct validation dependencies for CI/operator use.
- Forced deterministic LF output for the synthetic research receipt across supported operating systems and aligned its runtime declaration to Python >=3.11.
- Added explicit trusted-reproduction coverage to the Windows/macOS/Linux hosted smoke matrix.

## Local validation evidence

- Python compile: PASS
- tests: **31/31 PASS**
- graph validation: PASS
- schema/runtime contract alignment: PASS
- assumptions visibility: PASS
- evidence coverage: PASS
- dependency impact: PASS
- receipt verification: PASS
- explicit trusted reproduction: PASS
- decision-basis verification: PASS
- bounded public-reference evaluation: PASS
- report generation: PASS
- runtime no-network regression: PASS
- OPSEC scanner: PASS
- unapproved external URL rejection: PASS
- risky binary/log artifact rejection: PASS
- external private-context denylist scan: 0 matches
- JSON/YAML/CFF parse checks: PASS
- local Markdown links: PASS
- GitHub Actions immutable-SHA check: PASS
- wheel build: PASS
- source distribution build: PASS
- PEP 639 proprietary license metadata: PASS
- package-index upload guard: PASS
- wheel target install/import: PASS
- installed version: 0.2.0rc8

## Non-claims

This receipt does not claim:

- Ruff success in this local execution environment;
- hosted GitHub CI success;
- macOS or Windows runtime execution in this local environment;
- fresh network dependency resolution;
- scientific truth or real-system validation;
- customer/program qualification;
- public-release authorization.

## Release gate

Private staging is justified after the source archive and manifest are frozen.

Public visibility remains **HOLD** until:

1. the exact GitHub commit passes required hosted CI;
2. the public licensing decision is intentional;
3. repository security and branch/rules controls are configured;
4. final manual public-boundary review passes;
5. logged-out public UAT is ready to execute immediately after visibility changes.
