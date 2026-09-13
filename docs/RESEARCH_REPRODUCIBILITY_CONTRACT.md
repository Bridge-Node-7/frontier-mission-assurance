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

### Version 2 — exact local reproduction

Version 2 remains supported and unchanged:

- declared code, inputs, and expected outputs are SHA-256-bound;
- `experiment.entrypoint` must be a declared code artifact and the command must execute it directly or as the first Python script argument;
- numerical checks supplement exact output identity;
- `fma reproduce` runs in a fresh temporary workspace containing the receipt, declared code, and declared inputs, with declared outputs absent before execution;
- a successful reproduction must create outputs whose hashes and numerical checks match the receipt.

### Version 3 — explicit acceptance and long-running provenance

Version 3 extends the contract without weakening version-2 integrity:

- declared code and inputs remain exact SHA-256 identities;
- every observed output receives an observed SHA-256 provenance record;
- `output_acceptance.mode` explicitly selects `EXACT_SHA256`, `NUMERIC_CHECKS`, or `HYBRID`;
- stochastic or numerically equivalent output may pass only when declared numerical tolerances pass under `NUMERIC_CHECKS` or `HYBRID`;
- exact and hybrid modes require a declared reference SHA-256 for each output;
- calibration/instrument state records identity, configuration hash, lineage, observation time, and validity window;
- `REQUIRED` calibration fails when missing or outside its declared validity window;
- `REVIEW_IF_MISSING` keeps missing or stale calibration visible for human review;
- `LOCAL` execution retains fresh-workspace reproduction;
- `EXTERNAL` execution separates a submission/environment receipt from a result-collection receipt and binds job identity, scheduler reference, code/input manifests, environment identity, timeout/cancellation semantics, terminal state, and collected-output hashes;
- public CI verifies a synthetic external receipt; it does not pretend to run a real cluster.

For external receipts, `fma receipt` verifies the collected evidence. `fma reproduce` deliberately refuses to launch the external scheduler workflow; submission remains an explicit operator/system responsibility.

The fresh workspace is an integrity control, not a sandbox or hermetic environment. Trusted code can still access resources allowed by the host, so environment equivalence and undeclared ambient dependencies remain separate assurance questions.

## Legacy receipt compatibility

Version-1 receipts remain readable for non-executing historical verification. They do not carry code-binding and fresh-output guarantees, so `fma reproduce` does not issue a current reproduction PASS for a version-1 receipt.

Version-2 receipts retain their original exact-output semantics. Version 3 is additive; consumers must not silently reinterpret a version-2 receipt as stochastic or external execution.

## Deterministic reports

`fma report` normally records the current UTC generation time. When a byte-reproducible report is needed for receipt binding or deterministic release evidence, set `SOURCE_DATE_EPOCH` to the intended Unix timestamp before generating the report.

## Minimum sufficient assurance

Not every research artifact needs a full production platform. The contract should capture only enough environment, execution, result, calibration, and acceptance information to let an independent user determine whether the declared computational result is still reproducible or whether review is required.

## Non-claim

A reproducible computation, matching tolerance, valid calibration record, or successful external job receipt does not by itself establish scientific truth, operational validity, mission readiness, regulatory acceptance, or authorization for consequential action.
