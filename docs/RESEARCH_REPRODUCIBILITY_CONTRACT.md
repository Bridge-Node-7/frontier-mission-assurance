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

`Source → Environment → Experiment → Result → Validation → Receipt`

- input/output SHA-256 hashes preserve artifact identity;
- declared numerical checks preserve acceptance expectations;
- explicit reproduction separates trusted code execution from non-executing receipt verification;
- environment fingerprints capture public-safe execution context;
- hosted CI demonstrates the contract on clean infrastructure.

## Minimum sufficient assurance

Not every research artifact needs a full production platform. The contract should capture only enough environment, execution, result, and acceptance information to let an independent user determine whether the declared computational result is still reproducible.

## Non-claim

A reproducible computation does not by itself establish scientific truth, operational validity, mission readiness, or regulatory acceptance.
