# Research Reproducibility Contract

The Research Reproducibility Contract is the human-facing companion to an executable research receipt. It answers the questions a new technical user needs before attempting reproduction.

## Recommended contract

A reproducible research artifact should state:

```text
STATUS
Active Research Artifact | Historical Research Artifact | Reference Only

PAPER / CLAIM
Publication, DOI, archive identifier, or claim being reproduced

TESTED
Operating system, Python/runtime, compiler/toolchain

TIME TO FIRST VERIFIED RESULT
Approximate bounded evaluation time

TIME TO FULL REPRODUCTION
Approximate full-run time when materially different

HARDWARE
CPU/GPU/memory requirements

QUICK VERIFY
One bounded command

FULL REPRODUCTION
One explicit trusted command or documented workflow

EXPECTED RESULT
Artifact path, numerical expectation, tolerance, or hash

LAST VERIFIED
Date plus release/tag identity
```

## Machine-readable mapping

The executable receipt supplies the machine-checkable portion:

`Code → Input → Environment → Experiment → Result → Acceptance → Receipt`

### Version 3.1 — current v3 contract

Version 3.1 is the current version-3 contract. It preserves exact code/input provenance and an observed SHA-256 for every output while making each output's assurance meaning explicit:

- `EXACT` — the output is required to satisfy its declared exact identity;
- `SEMANTICALLY_CHECKED` — the output is assessed by declared same-output checks that define the bounded equivalence claim;
- `RECORD_ONLY` — the output is retained as provenance without an equivalence claim.

This prevents one receipt-wide acceptance label from overstating what was established for every output. A semantically checked output must name the checks that govern that output. A record-only output remains evidence of what was observed, not evidence that it matched a reference result.

Version 3.1 retains the version-3 execution and provenance model:

- declared code and inputs remain exact SHA-256 identities;
- every observed output receives an observed SHA-256 provenance record;
- calibration/instrument state can record identity, configuration hash, lineage, observation time, and validity window;
- `REQUIRED` calibration fails when missing or outside its declared validity window;
- `REVIEW_IF_MISSING` keeps missing or stale calibration visible for human review;
- `LOCAL` execution retains fresh-workspace reproduction;
- `EXTERNAL` execution separates submission/environment evidence from result-collection evidence and binds job identity, scheduler reference, code/input manifests, environment identity, chronology, timeout/cancellation semantics, terminal state, and collected-output hashes;
- public CI verifies a synthetic external receipt; it does not pretend to run a real cluster.

For external receipts, `fma receipt` verifies the collected evidence. `fma reproduce` deliberately refuses to launch the external scheduler workflow; submission remains an explicit operator/system responsibility.

### Version 3.0 — retained v3 compatibility

Version 3.0 remains supported under its original version-3 receipt-wide acceptance model. It uses `output_acceptance.mode` values such as `EXACT_SHA256`, `NUMERIC_CHECKS`, or `HYBRID` while retaining exact code/input identity and observed-output provenance.

Version 3.1 strengthens the expression of assurance; it does not redefine historical 3.0 records. Consumers must preserve a 3.0 receipt's declared semantics rather than silently interpreting it as a 3.1 per-output record.

### Version 2.0 — exact local reproduction

Version 2 remains supported and unchanged:

- declared code, inputs, and expected outputs are SHA-256-bound;
- `experiment.entrypoint` must be a declared code artifact and the command must execute it directly or as the first Python script argument;
- numerical checks supplement exact output identity;
- `fma reproduce` runs in a fresh temporary workspace containing the receipt, declared code, and declared inputs, with declared outputs absent before execution;
- a successful reproduction must create outputs whose hashes and numerical checks match the receipt.

### Version 1.0 — historical verification compatibility

Version-1 receipts remain readable for non-executing historical verification. They do not carry code-binding and fresh-output guarantees, so `fma reproduce` does not issue a current reproduction PASS for a version-1 receipt.

The fresh workspace is an integrity control, not a sandbox or hermetic environment. Trusted code can still access resources allowed by the host, so environment equivalence and undeclared ambient dependencies remain separate assurance questions.

## Compatibility rule

Receipt versions retain their original assurance meaning. Version 2 exact-output semantics, version 3.0 receipt-wide acceptance semantics, and version 3.1 per-output assurance semantics must not be silently collapsed into one another.

## Deterministic reports

`fma report` normally records the current UTC generation time. When a byte-reproducible report is needed for receipt binding or deterministic release evidence, set `SOURCE_DATE_EPOCH` to the intended Unix timestamp before generating the report.

## Minimum sufficient assurance

Not every research artifact needs a full production platform. The contract should capture only enough environment, execution, result, calibration, and acceptance information to let an independent user determine whether the declared computational result is still reproducible or whether review is required.

## Non-claim

A reproducible computation, matching tolerance, valid calibration record, or successful external job receipt does not by itself establish scientific truth, operational validity, mission readiness, regulatory acceptance, or authorization for consequential action.
