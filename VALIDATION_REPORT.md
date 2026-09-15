# Source Validation Report — v0.7.0

**Date:** 2026-09-15  
**Role:** bounded public reference for evidence-native verification, validation, reproducibility, traceability, and mission assurance

This report records deterministic validation requirements for the source candidate. Commit-specific hosted CI evidence belongs in GitHub Actions and tagged release metadata rather than being copied into source. See [`docs/RELEASE_EVIDENCE_LIFECYCLE.md`](docs/RELEASE_EVIDENCE_LIFECYCLE.md).

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
- Mission Decision Packet synthetic example: **present required**
- Deterministic Markdown report under `SOURCE_DATE_EPOCH`: **PASS required**
- Scientific Discovery Assurance linked synthetic profile: **PASS required**
- Runtime no-network-client import regression: **PASS required**
- JSON / YAML / CFF parse checks: **PASS required**
- Local Markdown-link integrity: **PASS required**
- GitHub Actions immutable-SHA pins: **PASS required**
- Pull-request dependency vulnerability review: **PASS required on pull requests**
- Protected-main CodeQL analysis: **PASS required on main pushes**

## Orbital Recovery Assurance V&V

The v0.7 source candidate adds a bounded source-distributed Orbital Recovery Assurance profile. Release eligibility requires:

- profile schemas and synthetic records agree on profile contract `0.5`;
- public synthetic examples remain source-neutral;
- physical, trust, and authority semantics remain distinct;
- the Mission Recovery Chain contains exactly power/contact/telemetry/command/capability, with trust and authority as overlays;
- recovery-chain evidence references resolve;
- evidence validity and provenance-correlation controls remain explicit;
- robust-option filtering is non-vacuous and fail-closed;
- unsafe credible hypotheses and gate failures remain visible per option;
- HOLD/no-consequential-action remains an explicit utility baseline;
- next-best evidence is evaluated over the admissible policy and is surfaced only when positive-value;
- machine output stops at eligibility for downstream human decision preparation;
- post-intervention requalification evidence references resolve and fail closed when incomplete;
- TTC/TTE/TTMC/TTT/TTV metrics remain event-derived;
- the checked-in synthetic benchmark is deterministic and matches current protocol/code;
- the primary known-truth benchmark uses 5,000 cases and must PASS its declared protocol;
- the declared stress matrix must PASS;
- the synthetic bounded policy unsafe-action rate must remain 0.0 under the declared generator;
- private-case structural validation remains local-only and supports mapped, assessed, post-intervention, and requalification-review lifecycle gates;
- private-case quiet failures must not echo unresolved private identifiers;
- JSON object serialization order must not become part of the recovery-chain contract;
- Orbital profile validation must pass on the supported Python matrix and explicit Ubuntu/macOS/Windows smoke path.

These controls demonstrate only behavior under the declared contracts and synthetic generator. They do not establish real-world spacecraft recoverability, flight safety, ownership, authority, probability calibration, commercial demand, or mission readiness.

## Public-boundary V&V

The authoritative release boundary is the Git-tracked file set. Required behavior:

- every Git-tracked candidate file is scanned regardless of directory name;
- prohibited credential/private-key/local-path/private-IP patterns fail closed;
- unapproved external URLs fail closed;
- high-risk binary/archive/document extensions fail closed unless the public contract intentionally changes;
- public examples remain synthetic;
- proper nouns, sensitive technical values, and relationship context still require human public-surface review.

A current-tree boundary PASS does not prove that historical Git objects never contained sensitive material.

## Reproduction integrity contract

`fma receipt` is non-executing. `fma reproduce` is an explicit trusted-code operation for local code-bound receipts. The workspace is an integrity boundary, **not a sandbox or hermetic environment**. Trusted code still executes with host permissions and ambient capabilities.

## Dependency / packaging V&V

- Development test runner: **pytest 9.1.1 required**
- Project optional dev range: **pytest >=9.1.1,<10 required**
- Supported Python and cross-platform verification: **PASS required**
- Wheel and source build: **PASS required**
- Build tooling: **setuptools 84.0.0, wheel 0.48.0, build 1.6.1 required**
- PEP 639 license metadata and license file: **required**
- Public package-index upload guard: **required**
- Clean wheel install and CLI smoke: **PASS required**

Bounded profiles are distributed through the repository/source archive. The core wheel remains the `frontier_assurance` package and CLI surface.

## Hosted acceptance

The exact pushed commit must pass the declared Python matrix, Ubuntu/macOS/Windows smoke tests, Ruff, tracked-file public-boundary validation, adversarial regressions, both bounded profile validators, dependency review where applicable, protected-main CodeQL on main, and clean wheel installation. The Actions run attached to that exact commit is authoritative hosted evidence.

## Disposition rule

**SOURCE PASS** means the candidate satisfies this deterministic source contract. It is not scientific truth, authenticated authorship, mission readiness, certification, or deployment authorization. Stable release additionally requires the source, hosted verification, published artifact set, and clean-user verification to agree under [`docs/RELEASE_ACCEPTANCE.md`](docs/RELEASE_ACCEPTANCE.md).
