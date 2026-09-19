# Source Validation Report — v0.11.0

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
- Assurance-context export `0.1.0` schema and source-neutral example: **PASS required**
- Unsupported assurance-context identity, missing release identity, and raw-evidence fields: **fail closed required**
- HOLD, REVIEW_REQUIRED, DECLARED, EXTERNAL_REPORTED, and RE-EVALUATION_OPPORTUNITY states: **preserved required**
- Mission Decision Packet reference example: **present required**
- External-research adoption sidecar graph and Decision Receipt: **PASS required**
- Profile manifests and manifest schema: **PASS required**
- Deterministic Markdown report under `SOURCE_DATE_EPOCH`: **PASS required**
- Scientific Discovery Assurance linked reference profile: **PASS required**
- Runtime no-network-client import regression: **PASS required**
- JSON / YAML / CFF parse checks: **PASS required**
- Local Markdown-link integrity: **PASS required**
- GitHub Actions immutable-SHA pins: **PASS required**
- Pull-request dependency vulnerability review: **PASS required on pull requests**
- Protected-main CodeQL analysis: **PASS required on main pushes**

## Existing-work adoption V&V

The public adoption surface must demonstrate that FMA can wrap work that was not authored for FMA without modifying the authoritative source repository.

Release eligibility requires:

- the source-neutral external-research sidecar graph validates under the core assurance-graph contract;
- its Decision Receipt resolves against the sidecar graph;
- the example remains explicitly synthetic/source-neutral and suitable for unrestricted public evaluation;
- the public documentation keeps artifact identity, reproduction, scientific validity, applicability, and consequential authority distinct;
- trusted-code reproduction guidance does not describe the FMA fresh workspace as a security sandbox;
- stable-install guidance preserves the source-vs-wheel distribution boundary and does not expand license rights;
- evaluation/use guidance remains subordinate to the repository `LICENSE` and grants no new rights by documentation alone.

These controls establish an adoption contract and worked public example. They do not establish customer fit, production deployment, or external validation.

## Profile-manifest V&V

Every directory under `profiles/` must expose a `profile.yaml` that:

- validates against `schemas/profile-manifest.schema.json`;
- uses a `profile_id` matching its directory name;
- declares a unique profile identity and semantic profile version;
- names the FMA release in which the profile was introduced;
- references a profile contract contained inside the same profile directory;
- references an existing Python validator;
- does not declare an introduction release newer than the current FMA source version.

The manifest is a discovery contract only. It is not a plugin runtime and does not establish domain fitness for a particular decision.

## Orbital Recovery Assurance V&V

Release eligibility requires the accepted Orbital Recovery Assurance profile contract and regression surface to remain green, including source-neutral records, physical/trust/authority separation, Mission Recovery Chain invariants, provenance correlation, fail-closed robust-option eligibility, next-best-evidence behavior, requalification, event-derived recovery metrics, governed local-case validation, deterministic benchmarks, and cross-platform smoke paths.

These controls establish behavior under the declared contracts and synthetic generator. Mission recoverability, flight safety, ownership, authority, mission-specific probability calibration, and mission readiness remain governed externally.

## FTQC Assurance V&V

The v0.11.0 source candidate retains FTQC Assurance profile contract `0.2` and adds bounded external technical-evidence adoption. Release eligibility requires:

- reviewed ExperimentResult and ProcessorEvidenceReceipt artifacts fail closed on wrong trusted artifact SHA-256;
- externally supplied producer schemas must match the exact reviewed schema SHA-256 values before JSON Schema validation;
- ExperimentResult internal integrity and ProcessorEvidenceReceipt payload integrity must verify independently;
- the processor receipt must bind exactly one input artifact and that linkage must match the supplied ExperimentResult identity and SHA-256;
- unreviewed future producer releases fail closed even when contract identity is unchanged;
- current generated decoder-backlog model evidence maps to `SIMULATED / NOT_ASSESSED / DECLARED`;
- reproduced evidence may map to `REPRODUCED` without promoting authority;
- cross-architecture technical evidence maps to applicability `REVIEW_REQUIRED`;
- positive processor technical status maps only to `RE-EVALUATION_OPPORTUNITY`, never automatic approval;
- unfavorable processor technical status remains a bounded technical result and must not be promoted into a mission/company-level conclusion;
- the adapter emits an existing profile-0.2 evidence-validity envelope rather than a new ontology;
- assurance-context remains `0.1.0` unless a future wire-semantic requirement is proven;

The existing FTQC case controls remain required:

- FTQC profile schemas, manifests, public reference records, evaluator, and private-case validator agree on profile contract `0.2`;
- public synthetic FTQC reference records remain source-neutral and require `resource-estimate-receipt.result.synthetic_only = true`;
- non-synthetic FTQC cases may truthfully use `record_class = private` and `synthetic_only = false`;
- the generic FTQC case validator accepts a user-supplied six-file case directory outside the public repository;
- all four FTQC profile records in one case use a consistent record class;
- case validation preserves the universal FMA graph ontology and core Decision Receipt semantics;
- system-concept assumption references resolve to FMA assumption nodes;
- resource-estimate system/workload/assumption/applicability references resolve explicitly;
- evidence envelopes name evidence class, applicability conditions, applicability basis, authority state, and decision-gate state;
- `ESTABLISHED` applicability cannot rest only on a declared-assumption basis;
- internal, external, and independent-review classes remain explicit and non-equivalent;
- mandatory expert gates or unresolved decision-gating applicability cannot coexist with an `APPROVE` Decision Receipt;
- the generic FTQC case report surfaces disposition, assumptions, resource-estimate state/provenance, applicability envelopes, expert gates, and reopen conditions;
- previous/current FTQC case comparison deterministically surfaces changed assumptions/context, stale reused resource estimates, out-of-envelope evidence, declared expert-review reopen triggers, downstream graph impact, and decision-node reconsideration;
- the public baseline remains `HOLD` while a decision-gating applicability envelope is only declared;
- the public changed-assumption scenario modifies exactly one declared physical-model assumption and preserves stale-estimate, outside-envelope, expert-review reopen, impacted-claim, and decision-reconsideration behavior;
- the public evaluator remains deterministic;
- case regression coverage rejects mixed record classes, synthetic cases claiming non-synthetic results, unresolved-gate approval, and missing applicability references;
- the case validation and case-comparison workflows are exercised in local `make check`, supported Python CI, cross-platform smoke paths, and the explicit Stable Release workflow;
- the QBI crosswalk remains documentation-only and makes no readiness, affiliation, or evaluator-internal claim.

These controls establish declared profile and private-case contract behavior only. They do not establish quantum-physics validity, QEC correctness, decoder correctness, resource-estimator correctness, hardware performance, supplier qualification, independent V&V, government-program readiness, or consequential decision authority.

## Public release V&V

The authoritative release surface is the Git-tracked file set. Required behavior:

- every Git-tracked candidate file is scanned regardless of directory name;
- prohibited credential/private-key/local-path/private-IP patterns fail closed;
- unapproved external URLs fail closed;
- high-risk binary/archive/document extensions fail closed unless the public contract intentionally changes;
- public examples remain source-neutral;
- candidate content receives human public-surface review for contextual publication suitability.

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
- Bounded dependency-update proposals remain enabled; acceptance still requires review and the relevant V&V gates.

Assurance profiles are distributed through the repository/source archive. The core wheel remains the `frontier_assurance` package and CLI surface.

## Hosted acceptance

The exact pushed commit must pass the declared Python matrix, Ubuntu/macOS/Windows smoke tests, Ruff, tracked-file public-release validation, adversarial regressions, profile-manifest validation, external-research sidecar validation, all assurance profile validators, dependency review where applicable, protected-main CodeQL on main, and clean wheel installation. The Actions run attached to that exact commit is the authoritative hosted evidence.

## Disposition rule

**SOURCE PASS** means the candidate satisfies this deterministic source contract. Scientific, regulatory, safety, mission-qualification, quantum-performance, independent-evaluator, external-adoption, and consequential-authority determinations remain with the governing processes responsible for them. Stable release additionally requires the source, hosted verification, published artifact set, and clean-user verification to agree under [`docs/RELEASE_ACCEPTANCE.md`](docs/RELEASE_ACCEPTANCE.md).
