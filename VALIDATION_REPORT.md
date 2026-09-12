# Source Validation Report — v0.3.3

**Date:** 2026-09-12  
**Candidate role:** thin public reference/interoperability layer with Scientific Discovery Assurance

This report records deterministic validation properties of the source candidate. Commit-specific hosted CI evidence is intentionally maintained by GitHub Actions and tagged release metadata rather than embedded here. See [`docs/RELEASE_EVIDENCE_LIFECYCLE.md`](docs/RELEASE_EVIDENCE_LIFECYCLE.md).

## Functional V&V

- Python compilation: **PASS required**
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
- Scientific Discovery Assurance schema + synthetic cross-record validation: **PASS required**
- Local-time priority guard: **PASS required**
- Research-boundary declaration-only guard: **PASS required**
- Formal-proof / specification-equivalence separation: **PASS required**
- Replication-state guard: **PASS required**
- CLI version contract: **0.3.3 required**
- Runtime no-network-client import regression: **PASS required**
- Public-safe environment-fingerprint regression: **PASS required**
- JSON / YAML / CFF parse checks: **PASS required**
- Local Markdown-link integrity: **PASS required**
- GitHub Actions immutable-SHA check: **PASS required**
- GitHub Actions Node 24 runtime migration: **required**
- Pull-request dependency vulnerability review: **PASS required on pull requests**
- Protected-main CodeQL analysis: **PASS required on main pushes**
- Checkout credential persistence disabled: **required**
- Hosted-job timeout / artifact-retention controls declared: **required**

## Dependency V&V

- Development test runner: **pytest 9.1.1 required**
- Project optional dev range: **pytest >=9.1.1,<10 required**
- The pytest security remediation must pass the complete supported Python and cross-platform matrix before release.

## Packaging V&V

- Wheel and source-distribution build: **PASS required**
- Build backend/tooling pins: **setuptools 84.0.0, wheel 0.48.0, build 1.6.1 required**
- Package build runs without isolated dependency re-resolution in hosted package smoke: **required**
- PEP 639 license metadata: **`LicenseRef-Proprietary` required**
- License file included in wheel metadata: **required**
- Public package-index upload guard: **`Private :: Do Not Upload` required**
- Clean wheel install and CLI smoke: **PASS required**

## Public-boundary / OPSEC V&V

- Automated OPSEC scanner: **PASS required**
- Unapproved external URLs: **must fail scanner**
- High-risk binary/log artifact types: **must fail scanner**
- Worked examples: **synthetic only**
- Scientific Discovery Assurance worked example: **explicitly synthetic and intentionally unresolved**
- No personal email addresses, credentials, private keys, local home paths, or private URLs in the public candidate
- Public reference boundary, threat model, interoperability boundary, security-reporting policy, and scientific-discovery limitations present
- No private operating playbook, private deployment details, proprietary prioritization logic, or real research-session evidence in the public candidate
- Contribution/IP boundary explicit

## Expected core synthetic example behavior

The core fixture intentionally contains three critical mission/claim nodes, two with direct evidence support:

- critical nodes: **3**
- directly covered: **2**
- direct coverage ratio: **66.7%**
- visible critical evidence gap: `CLAIM-CYCLE-TARGET`
- unresolved assumptions: **3**, listed without automated priority scoring

## Expected Scientific Discovery Assurance behavior

The synthetic discovery fixture intentionally preserves unresolved assurance state:

- proof checker: **PASS**
- specification equivalence: **PARTIAL**
- replication: **PARTIAL**
- priority state: **UNANCHORED**
- research-boundary independent verification: **NOT_ASSESSED**
- Discovery Passport disposition: **REVIEW_REQUIRED**

The profile validator must pass because the records are structurally and semantically consistent with those bounded states. It must not elevate them into scientific truth, trusted priority, proven boundary enforcement, complete specification equivalence, or completed replication.

These are fixture behaviors, not claims about any external program or discovery.

## Hosted acceptance

The exact pushed commit must independently pass the declared hosted Python matrix, Ubuntu/macOS/Windows smoke tests, Ruff, OPSEC, deterministic reproduction, Scientific Discovery Assurance validation, dependency review where applicable, protected-main CodeQL, and fresh wheel installation. The Actions run attached to that commit is the authoritative hosted evidence.

## Disposition rule

**SOURCE PASS** means this candidate satisfies the deterministic source-level contract. It is not equivalent to scientific truth, mission readiness, legal priority, or publication/deployment authorization. Stable release additionally requires the GitHub administration, hosted V&V, licensing, release-provenance, and public-UAT gates in [`docs/RELEASE_CHECKLIST.md`](docs/RELEASE_CHECKLIST.md).
