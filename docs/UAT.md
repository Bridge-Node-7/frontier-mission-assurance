# User Acceptance Tests

These UAT cases define the intended behavior of the public reference implementation.

## UAT-01 — Five-minute orientation

A technical user should understand within five minutes:

- what FMA validates;
- what it does not prove;
- how public/synthetic data is separated from real program data;
- how to run the example validation path.

## UAT-02 — Graph validation

A valid synthetic graph shall pass. Duplicate identifiers, dangling edges, unsupported kinds/relations/statuses, and malformed required fields shall fail visibly.

## UAT-03 — Evidence gap visibility

Critical mission/claim/requirement nodes without direct supporting evidence shall be returned explicitly rather than hidden.

## UAT-04 — Assumption visibility without automated prioritization

Open assumptions shall be listed deterministically. The public reference shall not calculate a hidden or composite engineering priority score.

## UAT-05 — Dependency impact

Changing a declared dependency shall expose transitively dependent nodes for review.

## UAT-06 — Research receipt verification

Hash or numerical-check tampering shall fail deterministically.

## UAT-07 — Trusted reproduction boundary

Receipt verification shall remain non-executing. Reproduction shall execute only when explicitly invoked and shall use `shell=False`.

## UAT-08 — Decision-basis verification

A decision receipt shall fail if its declared basis references nodes absent from the validated graph.

## UAT-09 — OPSEC

The public-release scanner and manual review shall find no credentials, personal paths, private URLs, real program identities, or nonpublic evidence.

## UAT-10 — Clean package consumer

A wheel built from the exact release commit shall install into a clean environment and run the documented public example commands.

## UAT-10 — Bounded one-command evaluation

After installation, `python scripts/evaluate_public_reference.py` shall complete the non-executing public-reference journey and end with `RESULT - PUBLIC REFERENCE EVALUATION PASS`.

## UAT-11 — Runtime privacy

The runtime package shall contain no network-client imports and shall emit no telemetry or default uploads.

## UAT-12 — Contract alignment

Published schema constraints for contract versions and graph statuses shall align with runtime validation behavior.
