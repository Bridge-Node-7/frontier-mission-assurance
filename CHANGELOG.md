# Changelog

## 0.7.0 — Orbital Recovery Assurance

- Added a bounded Orbital Recovery Assurance profile under `profiles/orbital-recovery-assurance/` rather than creating a new institutional repository.
- Added the Mission Recovery Chain view `Power → Contact → Telemetry → Command → Capability` with trust and authority as cross-cutting overlays.
- Added physical/trust/authority state separation, provenance-aware evidence handling, validity envelopes, robust-action filtering, option-specific fail-closed gates, and next-best-evidence evaluation over admissible options.
- Added explicit HOLD/no-consequential-action utility, per-option unsafe hypotheses, gate failures, eligibility, and utility advantage versus HOLD so blocked options remain explainable.
- Added post-intervention requalification and event-derived TTC/TTE/TTMC/TTT/TTV recovery metrics.
- Added a source-neutral synthetic known-truth benchmark with preregistered safe baselines, deterministic checked-in results, protocol-history preservation, and stress-matrix validation.
- Added a local-only validator for governed private cases with lifecycle gates for mapped, assessed, post-intervention, and requalification-review stages; public CI never receives real mission evidence.
- Added evaluation/adoption, private-workspace, Recovery Assurance Package, Epistemic Firewall, evidence-quorum, evidence-degradation exercise, recovery-pathway, real-case, and bounded intervention-experiment guidance.
- Added Orbital profile validation to the existing Python matrix, cross-platform smoke, Makefile gate, and deliberate stable-release source verification without creating a parallel workflow.
- Preserved governed evidence/dependency ownership, downstream human decision preparation, and accountable human consequential authority.
- Preserved the public/synthetic repository boundary and made the source-vs-wheel distribution boundary explicit.

## 0.6.0 — resilience and trust semantics

- Made the authoritative public release-boundary scan operate on every Git-tracked file regardless of directory name, closing force-tracked build/cache disclosure bypasses while allowing untracked ephemeral caches to remain outside release scope.
- Added Research Receipt 3.1 with explicit per-output `EXACT`, `SEMANTICALLY_CHECKED`, and `RECORD_ONLY` assurance semantics while preserving an observed SHA-256 for every output.
- Required semantic outputs to name the exact same-output checks that define their bounded equivalence claim; record-only outputs make no equivalence claim.
- Added external execution chronology checks for `submitted_at <= started_at <= completed_at <= collected_at` and bound required calibration validity to the declared execution interval.
- Preserved Research Receipt 3.0 compatibility while making the strengthened 3.1 semantics explicit rather than silently redefining the existing contract.
- Hardened generated Mission Assurance Reports against decision laundering by carrying the PASS non-claims in the portable artifact, labeling evidence coverage as declared/unverified, surfacing validation-warning counts, and distinguishing undeclared assumptions from proof that no assumptions exist.
- Added a deterministic CycloneDX release SBOM plus GitHub build-provenance and SBOM attestations, including clean-user attestation verification before release closeout.
- Updated CLI summaries and public documentation so declared acceptance, scientific truth, and authenticated authorship remain visibly distinct.
- Updated current maturity, source validation, release receipt, package metadata, and citation metadata to the v0.6 line.

## 0.5.0 — research receipt v3

- Added Research Receipt v3 with explicit `EXACT_SHA256`, `NUMERIC_CHECKS`, and `HYBRID` output-acceptance modes while keeping declared code and inputs SHA-256 exact.
- Preserved every observed v3 output SHA-256 as provenance even when stochastic/numerical acceptance does not require byte identity.
- Added calibration/instrument-state provenance with explicit policy, identity, configuration hash, lineage, observation time, and validity-window checks.
- Added a bounded external/cluster contract that separates submission/environment evidence from result collection and verifies scheduler/job continuity, code/input manifests, environment identity, timeout/cancellation semantics, terminal state, and collected-output hashes without running a real cluster in public CI.
- Kept version-2 exact local reproduction semantics backward compatible.
- Improved reproduction diagnostics for undeclared Python helpers while retaining raw child stderr, and made invalid graph-status errors list the sorted allowed set.
- Added synthetic-only regression coverage for stochastic acceptance, calibration freshness, external collection provenance, exact-hash tampering, external execution refusal, and bounded diagnostics.
- Preserved the public/synthetic boundary, local-only runtime behavior for FMA itself, All Rights Reserved licensing, protected release gates, and human consequential decision authority.

## 0.4.2 — reproduction entrypoint binding

- Tightened version-2 reproduction so a Python command must execute the declared entrypoint as its first script argument; merely mentioning the entrypoint later in `argv` no longer satisfies the binding control.
- Reject interpreter execution modes such as `python -c`, `python -m`, stdin execution, and other decoy-token shapes from satisfying declared-entrypoint binding.
- Added adversarial regression coverage for interpreter-mode and decoy-entrypoint command shapes while preserving successful `python <entrypoint> ...` reproduction.
- Made the clean-adopter evaluation path install the exact pinned build backend inside its isolated environment and use that reviewed backend without build-isolation drift.
- Preserved fresh-output verification, SHA-256 code/input/output binding, cross-platform V&V, Scientific Discovery Assurance, Mission Decision Packets, local-only runtime, synthetic-only public fixtures, All Rights Reserved licensing, and human consequential decision authority.

## 0.4.1 — portable contract identity

- Added stable `$id` identifiers to the core Research Receipt v2 and Decision Receipt v1 schemas, completing consistent identifiers across the three core FMA contracts.
- Clarified that interoperability preserves richer local evidence and decision semantics through explicit adapters rather than forcing one universal ontology.
- Added public standards positioning that distinguishes FMA's bounded composition and UX from established assurance-case, provenance, hashing, reproducibility, and attestation primitives.
- Clarified that unsigned core receipts establish declared integrity and consistency, not authorship or signer identity.
- Added regression coverage for stable, unique core schema identifiers.
- Preserved v0.4.0 reproduction integrity, cross-platform V&V, Scientific Discovery Assurance, Mission Decision Packets, local-only runtime, synthetic-only public fixtures, and human consequential decision authority.

## 0.4.0 — reproduction integrity

- Upgraded executable research receipts to version 2.0 with explicit code artifacts and a declared execution entrypoint.
- Changed `fma reproduce` to run from a fresh temporary workspace containing only the receipt, declared code, and declared inputs; declared outputs must be created by that run before hashes and numerical checks can pass.
- Bound declared execution code by SHA-256 and reject reproduction when the declared command does not reference the receipt entrypoint.
- Retained non-executing verification compatibility for legacy version-1 receipts while requiring version 2.0 for fresh reproduction.
- Made receipt success messages report the controls that actually ran and reject empty code/input/output/check sections for version-2 receipts.
- Converted malformed YAML, directory paths, and other controlled input failures into one-line exit-2 CLI failures without Python tracebacks.
- Added positional CLI help, command examples, and a first-run pointer to the five-minute evaluation.
- Added warning-level detection for `depends_on` self-loops and cycles while preserving finite dependency traversal.
- Added deterministic report generation through `SOURCE_DATE_EPOCH` and expanded adversarial rejection-path regression coverage.
- Preserved the public/synthetic boundary, one-runtime-dependency design, cross-platform V&V, immutable Action pins, protected-main release gate, Scientific Discovery Assurance, Mission Decision Packets, and human consequential decision authority.

## 0.3.5 — durable public-release polish

- Refined release evidence and regression naming so the current source reads as a finished product rather than a maintenance narrative.
- Preserved the Mission Decision Packet, explicit reopen conditions, Scientific Discovery Assurance, and bounded public-data model introduced in the v0.3 line.
- Preserved cross-platform V&V, dependency review, CodeQL, immutable Action pins, local-only runtime, synthetic-only fixtures, All Rights Reserved licensing, and human consequential decision authority.
- No assurance-graph, schema, CLI, runtime, or workflow semantics changed from v0.3.4.

## 0.3.4 — mission decision UX and public-surface finalization

- Added the Mission Decision Packet as a bounded evidence-to-decision pattern with explicit reopen conditions.
- Upgraded the synthetic frontier-program example into a worked technical decision walkthrough.
- Simplified the README around mission, evidence, reproducibility, decision basis, and bounded evaluation.
- Standardized public-boundary terminology across source, tests, CI, release automation, and contribution surfaces.
- Consolidated acceptance and release documentation into user-facing contracts.
- Preserved runtime semantics, Scientific Discovery Assurance, cross-platform V&V, dependency review, CodeQL, immutable Action pins, local-only runtime, synthetic-only fixtures, All Rights Reserved licensing, and human consequential decision authority.

## 0.3.3 — development test-runner security remediation

- Updated the pinned development test runner to pytest 9.1.1.
- Raised the optional development dependency floor to `pytest>=9.1.1,<10`.
- Added a release-surface regression that keeps the supported pytest baseline aligned between `requirements-dev.txt` and package metadata.
- Preserved the v0.3.2 security, scientific-discovery, release, and runtime behavior.

## 0.3.2 — build-tool dependency security closure

- Updated pinned setuptools to 84.0.0.
- Updated pinned wheel to 0.48.0, incorporating upstream security fixes including path-traversal protections.
- Kept package metadata, hosted package smoke, release construction, release-surface tests, and validation documentation aligned on the same build-tool versions.

## 0.3.1 — security and release hardening

- Moved first-party GitHub Actions to current Node 24 runtimes while retaining immutable commit-SHA pins.
- Added high-severity dependency vulnerability review to the required pull-request V&V path.
- Added CodeQL Python analysis to protected-main V&V before stable release eligibility.
- Pinned build-backend/tooling requirements and made hosted package construction non-isolated to reduce release-time dependency drift.
- Added supported-version and private vulnerability-reporting guidance.

## 0.3.0 — Scientific Discovery Assurance

- Added six portable contracts: Discovery Passport, Research Priority Receipt, Research Boundary Attestation, Formal Proof Record, Replication Receipt, and bounded Agent Provenance Reference.
- Added a fully synthetic linked discovery case that remains visibly `REVIEW_REQUIRED` while specification equivalence and replication are incomplete.
- Added deterministic cross-record validation and negative tests for false priority, research-boundary overclaiming, proof/specification collapse, and incomplete replication.
- Added profile-specific documentation for attribution, specification equivalence, and limitations.
- Extended hosted cross-platform V&V and stable-release clean-user verification to exercise the scientific-discovery profile.

## 0.2.0 — initial public reference

- Established the portable assurance graph, assumption visibility, evidence coverage, dependency impact, research receipts, explicit trusted reproduction, decision receipts, synthetic examples, and cross-platform verification baseline.
- Established the bounded public-data and claim boundary.
- Established deterministic release provenance and clean-user artifact verification.
- Retained the All Rights Reserved posture and public package-index upload guard.

## Pre-0.2.0 development history

Earlier tagged release candidates remain available in Git history for exact reproducibility. The stable changelog focuses on supported public product evolution rather than intermediate staging iterations.
