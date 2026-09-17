# Source Validation Report — v0.8.0

**Date:** 2026-09-17  
**Role:** public reference implementation for evidence-native verification, validation, reproducibility, traceability, and mission assurance

This report defines the deterministic validation contract for the source candidate. Commit-specific hosted CI evidence belongs in GitHub Actions and tagged release metadata rather than being copied into source. See [`docs/RELEASE_EVIDENCE_LIFECYCLE.md`](docs/RELEASE_EVIDENCE_LIFECYCLE.md).

## Core functional V&V

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
- External v3.1 chronology and calibration-interval coverage: **PASS required**
- Malformed input failures: **exit 2 without traceback required**
- Decision-basis receipt verification: **PASS required**
- Mission Decision Packet reference example: **present required**
- Deterministic Markdown report under `SOURCE_DATE_EPOCH`: **PASS required**
- Scientific Discovery Assurance linked reference profile: **PASS required**
- Runtime no-network-client import regression: **PASS required**
- JSON / YAML / CFF parse checks: **PASS required**
- Local Markdown-link integrity: **PASS required**
- GitHub Actions immutable-SHA pins: **PASS required**
- Pull-request dependency vulnerability review: **PASS required on pull requests**
- Protected-main CodeQL analysis: **PASS required on main pushes**

## Orbital Recovery Assurance V&V

Release eligibility requires the accepted Orbital Recovery Assurance profile contract and regression surface to remain green, including source-neutral records, physical/trust/authority separation, Mission Recovery Chain invariants, provenance correlation, fail-closed robust-option eligibility, next-best-evidence behavior, requalification, event-derived recovery metrics, governed local-case validation, deterministic benchmarks, and cross-platform smoke paths.

These controls establish behavior under the declared contracts and synthetic generator. Mission recoverability, flight safety, ownership, authority, mission-specific probability calibration, and mission readiness remain governed externally.

## FTQC Assurance V&V

The v0.8.0 source candidate adds FTQC Assurance profile contract `0.1`. Release eligibility requires:

- FTQC profile schemas and public reference records agree on profile contract `0.1`;
- public FTQC examples remain synthetic and source-neutral;
- the universal FMA graph ontology remains unchanged by the domain profile;
- system-concept assumption references resolve to FMA assumption nodes;
- resource-estimate assumption references resolve and remain distinct from estimator correctness;
- evidence envelopes name an evidence class, explicit applicability conditions, applicability basis, authority state, and decision-gate state;
- `ESTABLISHED` applicability cannot rest only on a declared-assumption basis;
- internal, external, and independent-review classes remain explicit and non-equivalent;
- mandatory expert gates cannot coexist with an `APPROVE` synthetic Decision Receipt unless supported within scope;
- the public baseline remains `HOLD` while a decision-gating applicability envelope is only declared;
- the changed-assumption scenario modifies exactly one declared physical-model assumption;
- that change makes the dependent synthetic resource estimate stale;
- evidence outside its declared applicability envelope is surfaced without inferring architecture failure;
- the QEC expert review reopens when its declared physical-model dependency changes;
- affected claims and the dependent decision are surfaced through declared dependency/support relationships;
- the human-readable Decision Basis report clearly separates software/contract PASS from technical-decision HOLD;
- the evaluator is deterministic across repeated runs;
- the QBI crosswalk remains documentation-only and makes no readiness, affiliation, or evaluator-internal claim;
- profile validation and evaluation pass on the supported Python matrix and Ubuntu/macOS/Windows smoke paths.

These controls establish declared profile behavior only. They do not establish quantum-physics validity, QEC correctness, resource-estimator correctness, hardware performance, supplier qualification, independent V&V, government-program readiness, or consequential decision authority.

## Public release V&V

The authoritative release surface is the Git-tracked file set. Required behavior:

- every Git-tracked candidate file is scanned regardless of directory name;
- prohibited credential/private-key/local-path/private-IP patterns fail closed;
- unapproved external URLs fail closed;
- high-risk binary/archive/document extensions fail closed unless the public contract intentionally changes;
- public examples remain source-neutral;
- proper nouns, sensitive technical values, and relationship context receive human public-surface review.

A current-tree release-policy PASS attests to the tracked source state under review; historical Git objects remain separate durable history.

## Reproduction integrity contract

`fma receipt` verifies receipt structure and declared integrity without executing the receipt command. `fma reproduce` is the explicit trusted-code operation for local code-bound receipts. The fresh workspace prevents stale declared outputs from satisfying reproduction; trusted code still executes with host permissions and ambient capabilities.

## Dependency and packaging V&V

- Development test runner: **pytest 9.1.1 required**
- Project optional dev range: **pytest >=9.1.1,<10 required**
- Supported Python and cross-platform verification: **PASS required**
- Wheel and source build: **PASS required**
- Build tooling: **setuptools 84.0.0, wheel 0.48.0, build 1.6.1 required**
- PEP 639 license metadata and license file: **required**
- Public package-index upload guard: **required**
- Clean wheel install and CLI smoke: **PASS required**

Assurance profiles are distributed through the repository/source archive. The core wheel remains the `frontier_assurance` package and CLI surface.

## Hosted acceptance

The exact pushed commit must pass the declared Python matrix, Ubuntu/macOS/Windows smoke tests, Ruff, tracked-file public-release validation, adversarial regressions, all assurance profile validators, dependency review where applicable, protected-main CodeQL on main, and clean wheel installation. The Actions run attached to that exact commit is the authoritative hosted evidence.

## Disposition rule

**SOURCE PASS** means the candidate satisfies this deterministic source contract. Scientific, regulatory, safety, mission-qualification, quantum-performance, independent-evaluator, and consequential-authority determinations remain with the governing processes responsible for them. Stable release additionally requires the source, hosted verification, published artifact set, and clean-user verification to agree under [`docs/RELEASE_ACCEPTANCE.md`](docs/RELEASE_ACCEPTANCE.md).
