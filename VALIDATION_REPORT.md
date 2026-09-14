# Source Validation Report — v0.6.0

**Date:** 2026-09-13  
**Role:** bounded public reference for evidence-native verification, validation, reproducibility, traceability, and mission assurance

This report records deterministic validation properties of the source candidate. Commit-specific hosted CI evidence belongs in GitHub Actions and tagged release metadata rather than being copied into source. See [`docs/RELEASE_EVIDENCE_LIFECYCLE.md`](docs/RELEASE_EVIDENCE_LIFECYCLE.md).

## Functional V&V

- Python compilation: **PASS required**
- Automated tests: **PASS required**
- Assurance-graph validation and rejection branches: **PASS required**
- Stable, unique core schema identifiers: **PASS required**
- Open-assumption visibility without automated priority scoring: **PASS required**
- Evidence coverage and dependency-impact traversal: **PASS required**
- Warning-level dependency self-loop/cycle detection: **PASS required**
- Version-2 exact fresh reproduction with code/input binding and stale-output rejection: **PASS required**
- Research Receipt v3.0 backward compatibility: **PASS required**
- Research Receipt v3.1 exact / semantic / record-only output assurance: **PASS required**
- Every v3.1 output: **observed SHA-256 required**
- `SEMANTICALLY_CHECKED` outputs: **explicit same-output check identifiers required**
- `RECORD_ONLY` outputs: **no equivalence claim permitted**
- External v3.1 chronology `submitted <= started <= completed <= collected`: **PASS required**
- Required calibration state covers declared execution interval: **PASS required**
- External job identity, manifests, terminal state, and collected output hashes: **PASS required**
- External scheduler execution itself: **not claimed**
- Malformed YAML, directory paths, and controlled input errors: **exit 2 without traceback required**
- Decision-basis receipt verification: **PASS required**
- Mission Decision Packet synthetic example: **present required**
- Deterministic Markdown report under `SOURCE_DATE_EPOCH`: **PASS required**
- Scientific Discovery Assurance linked synthetic profile: **PASS required**
- Formal proof / specification-equivalence separation: **PASS required**
- Replication and priority guards: **PASS required**
- Runtime no-network-client import regression: **PASS required**
- JSON / YAML / CFF parse checks: **PASS required**
- Local Markdown-link integrity: **PASS required**
- GitHub Actions immutable-SHA pins: **PASS required**
- Pull-request dependency vulnerability review: **PASS required on pull requests**
- Protected-main CodeQL analysis: **PASS required on main pushes**

## Public-boundary V&V

The authoritative release boundary is the Git-tracked file set. Directory names such as `build/`, `dist/`, `.pytest_cache/`, or `__pycache__/` do not exempt a force-tracked file from inspection.

Required behavior:

- every Git-tracked candidate file is scanned regardless of directory name;
- untracked ephemeral caches do not become release content and may be ignored by the release-boundary control;
- prohibited credential/private-key/local-path/private-IP patterns fail closed;
- unapproved external URLs fail closed;
- high-risk binary/archive/document extensions fail closed unless the public contract intentionally changes;
- non-text tracked files outside the prohibited set require visible manual review;
- public examples remain synthetic;
- proper nouns, sensitive technical values, and relationship context still require human public-surface review.

A current-tree boundary PASS does not prove that historical Git objects never contained sensitive material.

## Research Receipt v3.1 assurance contract

Version 3.1 preserves an observed hash for every output and separates three output meanings:

- `EXACT`: observed hash must equal the declared reference hash;
- `SEMANTICALLY_CHECKED`: bounded equivalence is defined only by the explicitly referenced numerical checks for that output;
- `RECORD_ONLY`: output identity is recorded without an equivalence claim.

Aggregate output-acceptance modes remain `EXACT_SHA256`, `NUMERIC_CHECKS`, and `HYBRID`, but v3.1 requires per-output scope so a small passing numerical subset cannot silently imply total output equivalence.

For external evidence, v3.1 requires submission and collection job identity plus `submitted_at`, `started_at`, `completed_at`, and `collected_at` chronology. When calibration is required, its declared validity window must cover the execution interval. These records remain assertions unless a separate trust mechanism authenticates their issuer.

## Reproduction integrity contract

`fma receipt` is non-executing. `fma reproduce` is an explicit trusted-code operation for local code-bound receipts. It verifies declared code and inputs, stages only declared source artifacts into a fresh temporary workspace, leaves declared outputs absent, executes with `shell=False`, and verifies the newly created outputs according to the declared versioned assurance semantics.

The workspace is an integrity boundary, **not a sandbox or hermetic environment**. Trusted code still executes with host permissions and ambient capabilities.

## Dependency / packaging V&V

- Development test runner: **pytest 9.1.1 required**
- Project optional dev range: **pytest >=9.1.1,<10 required**
- Supported Python and cross-platform verification: **PASS required**
- Wheel and source build: **PASS required**
- Build tooling: **setuptools 84.0.0, wheel 0.48.0, build 1.6.1 required**
- PEP 639 license metadata and license file: **required**
- Public package-index upload guard: **required**
- Clean wheel install and CLI smoke: **PASS required**

## Expected core synthetic behavior

- critical mission/claim/requirement nodes: **3**
- directly covered: **2**
- direct coverage ratio: **66.7%**
- visible critical evidence gap: `CLAIM-CYCLE-TARGET`
- unresolved assumptions: **3**, listed without automated priority scoring
- decision disposition: **HOLD** until the declared evidence gap is resolved or the dependency basis changes

## Scientific Discovery Assurance

The synthetic discovery case intentionally remains bounded:

- proof checker: **PASS**
- specification equivalence: **PARTIAL**
- replication: **PARTIAL**
- priority state: **UNANCHORED**
- research-boundary independent verification: **NOT_ASSESSED**
- Discovery Passport disposition: **REVIEW_REQUIRED**

The validator must preserve those unresolved states rather than elevate them into scientific truth, trusted priority, proven boundary enforcement, complete specification equivalence, or completed replication.

## Hosted acceptance

The exact pushed commit must pass the declared Python matrix, Ubuntu/macOS/Windows smoke tests, Ruff, tracked-file public-boundary validation, adversarial receipt regressions, Scientific Discovery Assurance validation, protected-main CodeQL, dependency review where applicable, and clean wheel installation. The Actions run attached to that exact commit is authoritative hosted evidence.

## Disposition rule

**SOURCE PASS** means the candidate satisfies this deterministic source contract. It is not scientific truth, authenticated authorship, mission readiness, legal priority, certification, or deployment authorization. Stable release additionally requires the source, hosted verification, published artifact set, and clean-user verification to agree under [`docs/RELEASE_ACCEPTANCE.md`](docs/RELEASE_ACCEPTANCE.md).
