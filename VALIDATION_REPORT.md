# Source Validation Report — v0.2.0-rc10

**Date:** 2026-09-12
**Candidate role:** thin public reference/interoperability layer

This report records deterministic validation properties of the source candidate. Commit-specific hosted CI evidence is intentionally maintained by GitHub Actions and tagged release metadata rather than embedded here. See [`docs/RELEASE_EVIDENCE_LIFECYCLE.md`](docs/RELEASE_EVIDENCE_LIFECYCLE.md).

## Functional V&V

- Python compilation: **PASS**
- Automated tests: **PASS required**
- Assurance-graph validation: **PASS required**
- Runtime/schema contract alignment regressions: **PASS required**
- Open-assumption visibility: **PASS required**
- Direct evidence-coverage analysis: **PASS required**
- Dependency-impact traversal: **PASS required**
- Research-receipt hash verification: **PASS required**
- Research-receipt numerical acceptance: **PASS required**
- Explicit trusted reproduction: **PASS required**
- Decision-basis receipt verification: **PASS required**
- Bounded public-reference evaluation: **PASS required**
- Markdown assurance-report generation: **PASS required**
- CLI version contract: **0.2.0rc10 required**
- Runtime no-network-client import regression: **PASS required**
- Public-safe environment-fingerprint regression: **PASS required**
- JSON / YAML / CFF parse checks: **PASS required**
- Local Markdown-link integrity: **PASS required**
- GitHub Actions immutable-SHA check: **PASS required**
- Checkout credential persistence disabled: **required**
- Hosted-job timeout / artifact-retention controls declared: **required**

## Packaging V&V

- Wheel and source-distribution build: **PASS required**
- PEP 639 license metadata: **`LicenseRef-Proprietary` required**
- License file included in wheel metadata: **required**
- Public package-index upload guard: **`Private :: Do Not Upload` required**
- Clean wheel install and CLI smoke: **PASS required**

## Public-boundary / OPSEC V&V

- Automated OPSEC scanner: **PASS required**
- Unapproved external URLs: **must fail scanner**
- High-risk binary/log artifact types: **must fail scanner**
- Worked examples: **synthetic only**
- No personal email addresses, credentials, private keys, local home paths, or private URLs in the public candidate
- Public reference boundary, threat model, and interoperability boundary present
- No private operating playbook, private deployment details, or proprietary prioritization logic in the public candidate
- Release-candidate contribution/IP boundary explicit

## Expected synthetic example behavior

The fixture intentionally contains three critical mission/claim nodes, two with direct evidence support:

- critical nodes: **3**
- directly covered: **2**
- direct coverage ratio: **66.7%**
- visible critical evidence gap: `CLAIM-CYCLE-TARGET`
- unresolved assumptions: **3**, listed without automated priority scoring

This is fixture behavior, not a claim about any external program.

## Hosted acceptance

The exact pushed commit must independently pass the declared hosted Python matrix, Ubuntu/macOS/Windows smoke tests, Ruff, OPSEC, deterministic reproduction, and fresh wheel installation. The Actions run attached to that commit is the authoritative hosted evidence.

## Disposition rule

**SOURCE PASS** means this candidate satisfies the deterministic source-level contract. It is not equivalent to public-release authorization. Public release additionally requires the GitHub administration, hosted V&V, licensing, and public-UAT gates in [`docs/RELEASE_CHECKLIST.md`](docs/RELEASE_CHECKLIST.md).
