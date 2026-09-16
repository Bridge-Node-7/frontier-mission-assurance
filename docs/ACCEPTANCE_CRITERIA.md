# Acceptance Criteria

These criteria define the expected behavior of the public Frontier Mission Assurance reference implementation and its stable release surface.

## AC-01 — Five-minute orientation

A technical user should understand within five minutes:

- what FMA validates;
- the verification scope of a PASS;
- how public reference data is separated from mission-specific evidence;
- how to run the reference validation path.

## AC-02 — Graph validation

A valid synthetic graph shall pass. Duplicate identifiers, dangling edges, unsupported kinds/relations/statuses, and malformed required fields shall fail visibly. Duplicate edges, `depends_on` self-loops, and `depends_on` cycles shall remain visible as warnings rather than being silently accepted.

## AC-03 — Evidence gap visibility

Critical mission/claim/requirement nodes without direct supporting evidence shall be returned explicitly rather than hidden.

## AC-04 — Assumption visibility without automated prioritization

Open assumptions shall be listed deterministically. The public reference shall not calculate a hidden or composite engineering priority score.

## AC-05 — Dependency impact

Changing a declared dependency shall expose transitively dependent nodes for review. Cycles shall not cause unbounded traversal.

## AC-06 — Research receipt verification

Version-2 research receipts shall require non-empty declared code, inputs, outputs, and numerical checks. Code, input, or output hash tampering and numerical-check failures shall fail deterministically. The PASS summary shall report the controls that actually ran rather than claiming an unexecuted verification class.

## AC-07 — Trusted reproduction boundary

Receipt verification shall remain non-executing. Fresh reproduction shall execute only when explicitly invoked on a version-2 receipt, shall verify declared code and inputs before execution, shall require the declared entrypoint to be executed directly or as the first Python script argument, and shall use `shell=False`. Interpreter modes or later decoy tokens shall not satisfy entrypoint binding. Reproduction is an integrity workflow and trusted code runs with host permissions.

## AC-08 — Decision-basis verification

A decision receipt shall fail if its declared basis references nodes absent from the validated graph.

## AC-09 — Public release policy

Automated and human review shall reject credentials, personal paths, private URLs, mission-specific identities, and nonpublic evidence from the public source and release surface.

## AC-10 — Clean package consumer

A wheel built from the exact release commit shall install into a clean environment and run the documented public example commands.

## AC-11 — One-command evaluation

After installation, `python scripts/evaluate_public_reference.py` shall complete the public-reference journey and end with `RESULT - PUBLIC REFERENCE EVALUATION PASS`.

## AC-12 — Runtime privacy

The runtime package shall contain no network-client imports and shall emit no telemetry or default uploads.

## AC-13 — Contract alignment

Published schema constraints for contract versions and graph statuses shall align with runtime validation behavior. Runtime-only cross-artifact invariants that are not expressible in the published JSON Schema shall be documented and regression-tested.

## AC-14 — Public GitHub presentation

A visitor shall be able to identify the repository purpose, maturity, licensing posture, public release policy, five-minute evaluation path, reading order, core capabilities, and verification scope without relying on private context.

## AC-15 — Clean-user evaluation

An independent user starting from a clean supported environment shall be able to follow only documented commands and reach the declared reference evaluation result without author-machine assumptions.

## AC-16 — Release provenance

The public release record shall bind the accepted tag to the exact passing commit, successful hosted V&V run, source archive, wheel, and external SHA-256 manifest. The frozen source archive shall reconstruct to the exact accepted Git tree.

## AC-17 — Scientific Discovery Assurance

The bundled synthetic scientific-discovery records shall validate as a linked contract set while preserving unresolved assurance state: local time alone shall not establish trusted priority, a research-boundary attestation shall remain declaration-only, proof-checker `PASS` shall remain separate from specification-equivalence review, partial replication shall remain visible, and the synthetic Discovery Passport shall remain `REVIEW_REQUIRED` until those evidence gates are satisfied.

## AC-18 — Fresh reproduction integrity

A pre-existing valid output shall never be sufficient for `fma reproduce` to pass. Version-2 reproduction shall run in a fresh temporary workspace that contains the receipt, declared code, and declared inputs but no declared outputs before execution. A command that exits successfully without producing a required output shall fail closed. Modified declared code without a matching receipt hash shall fail before command execution.

## AC-19 — Controlled CLI errors and deterministic reports

Malformed YAML/JSON, directory paths supplied where files are required, invalid arguments, and other controlled input failures shall exit `2` without a Python traceback. `fma report` shall support byte-reproducible output when `SOURCE_DATE_EPOCH` is set to the same valid value.

## AC-20 — Version-3 stochastic output acceptance

Version-3 receipts shall keep declared code and input artifacts exact while making output acceptance explicit. `NUMERIC_CHECKS` may accept non-byte-identical output only when every declared numerical tolerance passes. The observed output SHA-256 remains visible provenance. `EXACT_SHA256` and `HYBRID` require reference output hashes and shall fail on a mismatch.

## AC-21 — Calibration/instrument-state provenance

Version-3 receipts shall record an `as_of` time and an explicit calibration policy. `REQUIRED` calibration shall fail when evidence is missing or outside its declared validity window. Instrument state shall carry identity, configuration hash, observation time, validity window, and lineage. A review-required policy shall not silently become an unconditional PASS claim.

## AC-22 — External long-running reproduction evidence

A version-3 `EXTERNAL` receipt shall separate submission/environment evidence from collection evidence, preserve scheduler/job identity, exact code/input manifests, environment identity, timeout and cancellation semantics, terminal state, and collected-output hashes. Public CI shall validate a synthetic reference contract without claiming to execute a real cluster. `fma reproduce` shall not launch an external scheduler job.

## AC-23 — Actionable diagnostics

When local reproduction fails on a Python import error, raw child stderr shall remain visible and FMA may add a concise hint that a declared code artifact or runtime dependency could be missing. Unsupported graph statuses shall report the rejected value and the sorted allowed set without changing graph-validation semantics.
