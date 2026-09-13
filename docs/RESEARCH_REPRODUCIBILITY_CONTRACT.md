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

`Code → Input → Environment → Experiment → Fresh Result → Validation → Receipt`

For the current version-2 executable contract:

- declared code artifacts are SHA-256-bound before execution;
- `experiment.entrypoint` identifies the declared code artifact the command must reference;
- input and output SHA-256 hashes preserve artifact identity;
- declared numerical checks preserve acceptance expectations;
- explicit reproduction separates trusted code execution from non-executing receipt verification;
- reproduction runs from a fresh temporary workspace containing the receipt, declared code, and declared inputs, while declared outputs are absent before execution;
- successful reproduction therefore requires the command to create the declared outputs in that fresh workspace before hashes and numerical checks can pass;
- environment fingerprints capture public-safe execution context;
- hosted CI demonstrates the contract on clean infrastructure.

The fresh workspace is an integrity control, not a sandbox or hermetic environment. Trusted code can still access resources allowed by the host, so environment equivalence and undeclared ambient dependencies remain separate assurance questions.

## Legacy receipt compatibility

Version-1 receipts remain readable for non-executing historical verification. They do not carry the version-2 code-binding and fresh-output guarantees, so `fma reproduce` does not issue a current reproduction PASS for a version-1 receipt.

## Deterministic reports

`fma report` normally records the current UTC generation time. When a byte-reproducible report is needed for receipt binding or deterministic release evidence, set `SOURCE_DATE_EPOCH` to the intended Unix timestamp before generating the report.

## Minimum sufficient assurance

Not every research artifact needs a full production platform. The contract should capture only enough environment, execution, result, and acceptance information to let an independent user determine whether the declared computational result is still reproducible.

## Non-claim

A reproducible computation does not by itself establish scientific truth, operational validity, mission readiness, regulatory acceptance, or authorization for consequential action.
