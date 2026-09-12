# Validation Report — v0.2.0-rc8

**Date:** 2026-09-11
**Candidate role:** thin public reference/interoperability layer
**Pre-GitHub execution evidence:** CPython 3.13.5 / Linux x86_64; CPython 3.13.15 / Windows x86_64

## Functional V&V

- Python compilation: **PASS**
- Automated tests: **31/31 PASS**
- Assurance-graph validation: **PASS**
- Runtime/schema contract alignment regressions: **PASS**
- Open-assumption visibility: **PASS**
- Direct evidence-coverage analysis: **PASS**
- Dependency-impact traversal: **PASS**
- Research-receipt hash verification: **PASS**
- Research-receipt numerical acceptance: **PASS**
- Explicit trusted reproduction: **PASS**
- Decision-basis receipt verification: **PASS**
- Bounded public-reference evaluation: **PASS**
- Markdown assurance-report generation: **PASS**
- CLI version contract: **PASS — 0.2.0rc8**
- Runtime no-network-client import regression: **PASS**
- Public-safe environment-fingerprint regression: **PASS**
- JSON / YAML / CFF parse checks: **PASS**
- Local Markdown-link integrity: **PASS**
- GitHub Actions floating-tag check: **PASS** — workflow actions are pinned to immutable commit SHAs
- GitHub checkout credential persistence disabled: **PASS**
- Hosted-job timeout / artifact-retention controls declared: **PASS**

## Packaging V&V

- Wheel build with configured setuptools backend: **PASS**
- Source distribution build with configured setuptools backend: **PASS**
- PEP 639 license metadata: **PASS — `LicenseRef-Proprietary`**
- License file included in wheel metadata: **PASS**
- Public package-index upload guard: **PASS — `Private :: Do Not Upload`**
- Wheel target installation with local dependency context: **PASS**
- Installed package version: **0.2.0rc8 — PASS**
- Installed CLI graph validation: **PASS**
- Installed CLI receipt verification: **PASS**

A truly fresh network dependency-resolution test remains a hosted-CI gate.

## Public-boundary / OPSEC V&V

- Automated OPSEC scanner: **PASS**
- Unapproved external URLs fail the scanner: **PASS**
- High-risk binary/log artifact types fail the scanner: **PASS**
- Synthetic-only worked examples: **PASS**
- External private-context/proper-noun denylist scan performed outside the repository: **0 matches**
- No personal email addresses, credentials, private keys, local home paths, or private URLs detected by automated checks
- Public reference boundary document present: **PASS**
- Threat model present: **PASS**
- Interoperability boundary present: **PASS**
- Internal operating-playbook, private-deployment, and speculative roadmap documents absent from the public candidate: **PASS**
- Automated composite engineering-priority scoring absent from the public candidate: **PASS**
- Release-candidate contribution/IP boundary is explicit: **PASS**
- Stale `open-source` wording removed while the candidate remains All Rights Reserved: **PASS**

The public candidate does not describe private operational architecture, customer/program data, or proprietary analytics.

## Expected synthetic example behavior

The fixture intentionally contains three critical mission/claim nodes, two with direct evidence support:

- critical nodes: **3**
- directly covered: **2**
- direct coverage ratio: **66.7%**
- visible critical evidence gap: `CLAIM-CYCLE-TARGET`
- unresolved assumptions: **3**, listed without automated priority scoring

This is fixture behavior, not a claim about any external program.

## RC7 cross-platform correction

- RC6 pinned Ruff 0.16.7 on Windows: **PASS** before the receipt test gate.
- RC6 Windows reproduction test exposed newline-dependent output bytes: **FAIL / FIXED IN RC7**.
- Synthetic analysis now writes LF bytes explicitly on all supported platforms: **PASS by construction; hosted Windows reproduction remains the confirming gate**.
- Synthetic receipt runtime declaration aligned to Python >=3.11: **PASS**.
- Generated `.egg-info` metadata removed from the frozen public source tree: **PASS**.

## RC8 Git hygiene correction

- RC7 Windows local V&V: **Ruff PASS; 31/31 tests PASS; OPSEC PASS; deterministic reproduction PASS; clean wheel install PASS**.
- Pre-commit staged-diff check detected three trailing-whitespace defects in public release documentation: **FAIL / FIXED IN RC8**.
- Git Bash reported potential LF-to-CRLF conversion under local Git configuration: **MITIGATED IN RC8** with repository-level `.gitattributes` (`* text=auto eol=lf`).
- No RC7 source commit was pushed before the staged-diff failure. The hosted repository remained private and empty at the correction boundary.

## Local tooling limitations / hosted acceptance gates

The following are **not** proven by this local run and remain required before public release:

- Ruff on the exact GitHub commit (Ruff is not installed in this execution environment and network package resolution is unavailable);
- clean dependency resolution from the public package metadata;
- Python 3.11 hosted CI;
- Python 3.12 hosted CI;
- Python 3.13 hosted CI;
- Ubuntu/macOS/Windows hosted smoke jobs;
- fresh wheel installation in hosted CI;
- repository security/rules configuration;
- logged-out public UAT;
- explicit licensing decision for public visibility;
- external clean-user UAT before final `v0.2.0`.

## Disposition

**LOCAL FUNCTIONAL / PACKAGE / OPSEC RC PASS.**

**APPROVE for private GitHub staging only after the exact RC8 operator reports Ruff PASS, 31/31 tests PASS, OPSEC PASS, package smoke PASS, and manifest PASS.**

**HOLD public visibility and final release until the exact hosted commit passes required CI, the public license decision is intentional, repository controls are configured, and final human public-boundary review passes.**
