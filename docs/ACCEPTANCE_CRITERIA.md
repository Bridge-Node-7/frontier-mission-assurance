# Acceptance Criteria

These criteria define the expected behavior of the public Frontier Mission Assurance reference implementation and its stable release surface.

## AC-01 — Five-minute orientation

A technical user should understand within five minutes:

- what FMA validates;
- what it does not prove;
- how public/synthetic data is separated from real program data;
- how to run the example validation path.

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

Receipt verification shall remain non-executing. Fresh reproduction shall execute only when explicitly invoked on a version-2 receipt, shall verify declared code and inputs before execution, shall require the declared command to reference the declared entrypoint, and shall use `shell=False`. Reproduction is not a sandbox.

## AC-08 — Decision-basis verification

A decision receipt shall fail if its declared basis references nodes absent from the validated graph.

## AC-09 — Public boundary

Automated and human review shall reject credentials, personal paths, private URLs, real program identities, and nonpublic evidence from the public source and release surface.

## AC-10 — Clean package consumer

A wheel built from the exact release commit shall install into a clean environment and run the documented public example commands.

## AC-11 — Bounded one-command evaluation

After installation, `python scripts/evaluate_public_reference.py` shall complete the non-executing public-reference journey and end with `RESULT - PUBLIC REFERENCE EVALUATION PASS`.

## AC-12 — Runtime privacy

The runtime package shall contain no network-client imports and shall emit no telemetry or default uploads.

## AC-13 — Contract alignment

Published schema constraints for contract versions and graph statuses shall align with runtime validation behavior. Runtime-only cross-artifact invariants that are not expressible in the published JSON Schema shall be documented and regression-tested.

## AC-14 — Public GitHub presentation

A visitor shall be able to identify the repository purpose, maturity, licensing posture, public-data boundary, five-minute evaluation path, reading order, and non-claims without relying on private context.

## AC-15 — Clean-user evaluation

An independent user starting from a clean supported environment shall be able to follow only documented commands and reach the declared bounded evaluation result without author-machine assumptions.

## AC-16 — Release provenance

The public release record shall bind the accepted tag to the exact passing commit, successful hosted V&V run, source archive, wheel, and external SHA-256 manifest. The frozen source archive shall reconstruct to the exact accepted Git tree.

## AC-17 — Scientific Discovery Assurance

The bundled synthetic scientific-discovery records shall validate as a linked contract set while preserving unresolved assurance state: local time alone shall not establish trusted priority, a research-boundary attestation shall remain declaration-only, proof-checker `PASS` shall remain separate from specification-equivalence review, partial replication shall remain visible, and the synthetic Discovery Passport shall remain `REVIEW_REQUIRED` until those evidence gates are satisfied.

## AC-18 — Fresh reproduction integrity

A pre-existing valid output shall never be sufficient for `fma reproduce` to pass. Version-2 reproduction shall run in a fresh temporary workspace that contains the receipt, declared code, and declared inputs but no declared outputs before execution. A command that exits successfully without producing a required output shall fail closed. Modified declared code without a matching receipt hash shall fail before command execution.

## AC-19 — Controlled CLI errors and deterministic reports

Malformed YAML/JSON, directory paths supplied where files are required, invalid arguments, and other controlled input failures shall exit `2` without a Python traceback. `fma report` shall support byte-reproducible output when `SOURCE_DATE_EPOCH` is set to the same valid value.
