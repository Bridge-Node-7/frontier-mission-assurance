# Source Validation Report — v0.4.0

**Date:** 2026-09-12  
**Role:** bounded public reference for evidence-native verification, validation, reproducibility, traceability, and mission assurance

This report records deterministic validation properties of the source candidate. Commit-specific hosted CI evidence is maintained by GitHub Actions and tagged release metadata rather than embedded here. See [`docs/RELEASE_EVIDENCE_LIFECYCLE.md`](docs/RELEASE_EVIDENCE_LIFECYCLE.md).

## Functional V&V

- Python compilation: **PASS required**
- Automated tests: **PASS required**
- Assurance-graph validation: **PASS required**
- Runtime/schema contract alignment regressions: **PASS required**
- Open-assumption visibility: **PASS required**
- Direct evidence-coverage analysis: **PASS required**
- Dependency-impact traversal: **PASS required**
- Warning-level detection of `depends_on` self-loops and cycles: **PASS required**
- Research-receipt code/input/output SHA-256 verification: **PASS required**
- Research-receipt numerical acceptance: **PASS required**
- Version-2 fresh reproduction from a workspace that does not contain pre-existing declared outputs: **PASS required**
- Version-2 entrypoint code binding before execution: **PASS required**
- Stale-output/no-output regression: **must fail closed**
- Legacy version-1 receipt non-executing verification compatibility: **PASS required**
- Legacy version-1 fresh reproduction: **must fail closed**
- Empty version-2 code/input/output/check sections: **must fail closed**
- Malformed YAML, directory paths, and controlled input errors: **exit 2 without traceback required**
- Decision-basis receipt verification: **PASS required**
- Decision and graph rejection branches: **adversarial regression coverage required**
- Mission Decision Packet documentation and worked synthetic example: **present required**
- Bounded public-reference evaluation: **PASS required**
- Markdown assurance-report generation: **PASS required**
- `SOURCE_DATE_EPOCH` deterministic report generation: **PASS required**
- Scientific Discovery Assurance schema + synthetic cross-record validation: **PASS required**
- Local-time priority guard: **PASS required**
- Research-boundary declaration-only guard: **PASS required**
- Formal-proof / specification-equivalence separation: **PASS required**
- Replication-state guard: **PASS required**
- CLI version contract: **0.4.0 required**
- Runtime no-network-client import regression: **PASS required**
- Public-safe environment-fingerprint regression: **PASS required**
- JSON / YAML / CFF parse checks: **PASS required**
- Local Markdown-link integrity: **PASS required**
- GitHub Actions immutable-SHA check: **PASS required**
- Pull-request dependency vulnerability review: **PASS required on pull requests**
- Protected-main CodeQL analysis: **PASS required on main pushes**
- Checkout credential persistence disabled: **required**
- Hosted-job timeout / artifact-retention controls declared: **required**

## Reproduction integrity contract

`fma receipt` is non-executing. For the current version-2 receipt contract it verifies declared code, input, and output artifacts plus numerical acceptance checks and reports the number of controls that actually passed.

`fma reproduce` accepts only version-2 receipts. It verifies declared code and inputs before execution, requires the declared command to reference the declared entrypoint, stages only the receipt, declared code, and declared inputs into a fresh temporary workspace, executes the trusted command with `shell=False`, and then verifies that declared outputs now exist with the expected hashes and numerical values. Pre-existing outputs from the source working directory are not staged into the reproduction workspace.

This strengthens causal reproduction evidence but does not provide a sandbox or hermetic environment. Trusted reproduction code still executes with the permissions and ambient capabilities of the invoking host.

## Dependency V&V

- Development test runner: **pytest 9.1.1 required**
- Project optional dev range: **pytest >=9.1.1,<10 required**
- Supported Python and cross-platform verification: **PASS required**

## Packaging V&V

- Wheel and source-distribution build: **PASS required**
- Build backend/tooling pins: **setuptools 84.0.0, wheel 0.48.0, build 1.6.1 required**
- Package build runs without isolated dependency re-resolution in hosted package smoke: **required**
- PEP 639 license metadata: **`LicenseRef-Proprietary` required**
- License file included in wheel metadata: **required**
- Public package-index upload guard: **`Private :: Do Not Upload` required**
- Clean wheel install and CLI smoke: **PASS required**

## Public-boundary V&V

- Automated public-boundary scanner: **PASS required**
- Unapproved external URLs: **must fail scanner**
- High-risk binary/log artifact types: **must fail scanner**
- Worked examples: **synthetic only**
- Scientific Discovery Assurance worked example: **explicitly synthetic and intentionally unresolved**
- No personal email addresses, credentials, private keys, local home paths, private URLs, real program identities, or nonpublic evidence in the public candidate
- Security-reporting policy, threat model, interoperability contract, acceptance criteria, release acceptance, and scientific-discovery limitations present
- Public-facing artifacts and regression names use product-facing boundary and acceptance terminology
- Contribution/IP boundary explicit

## Expected core synthetic example behavior

The core fixture intentionally contains three critical mission/claim nodes, two with direct evidence support:

- critical nodes: **3**
- directly covered: **2**
- direct coverage ratio: **66.7%**
- visible critical evidence gap: `CLAIM-CYCLE-TARGET`
- unresolved assumptions: **3**, listed without automated priority scoring
- decision disposition: **HOLD** until the declared evidence gap is resolved or the dependency basis changes

The version-2 research receipt additionally binds its analysis entrypoint, input data, output result, and numerical expectation. A reproduction PASS requires fresh output generation in the isolated declared-artifact workspace.

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

The exact pushed commit must independently pass the declared hosted Python matrix, Ubuntu/macOS/Windows smoke tests, Ruff, public-boundary validation, version-2 fresh reproduction, adversarial rejection regressions, deterministic report behavior, Scientific Discovery Assurance validation, dependency review where applicable, protected-main CodeQL, and fresh wheel installation. The Actions run attached to that commit is the authoritative hosted evidence.

## Disposition rule

**SOURCE PASS** means this candidate satisfies the deterministic source-level contract. It is not equivalent to scientific truth, mission readiness, legal priority, or publication/deployment authorization. Stable release additionally requires the source, hosted verification, published artifact set, and clean-user verification to agree under [`docs/RELEASE_ACCEPTANCE.md`](docs/RELEASE_ACCEPTANCE.md).
