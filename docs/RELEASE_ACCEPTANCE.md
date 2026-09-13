# Stable Release Acceptance

A stable Frontier Mission Assurance release is acceptable only when the published artifact set is bound to an exact passing commit and the public reference remains inside its declared boundary.

## Repository state

A stable release requires:

- `main` as the protected default branch;
- the intended release commit to be the exact accepted source state;
- only intentional long-lived branches and collaboration state;
- public documentation, schemas, software, and synthetic fixtures only.

## Hosted verification

The required hosted verification surface includes:

- Python 3.11, 3.12, and 3.13 validation on Ubuntu;
- Ubuntu, macOS, and Windows smoke validation;
- wheel build and fresh installation;
- lint, unit, regression, schema, tamper, and boundary tests;
- adversarial rejection-path tests for assurance-graph and decision validation;
- version-2 code-binding and fresh-output reproduction-integrity regressions;
- controlled malformed-input CLI behavior with exit code `2` and no traceback;
- deterministic report regression under `SOURCE_DATE_EPOCH`;
- dependency review where applicable;
- protected-main static analysis before stable release eligibility;
- Scientific Discovery Assurance validation when present;
- public-boundary validation.

A required check that is red, unexpectedly skipped, or materially different from the reviewed candidate blocks stable promotion.

## Reproduction-integrity release gate

The stable candidate must demonstrate that:

- declared version-2 code and input hashes are verified before trusted execution;
- the receipt command references the declared entrypoint;
- the reproduction workspace begins without declared outputs;
- a successful no-output execution fails receipt verification rather than reusing a stale source-tree result;
- newly generated outputs match declared hashes and numerical acceptance checks;
- legacy version-1 receipts remain non-executingly verifiable but do not receive a current fresh-reproduction PASS;
- reproduction is described accurately as a trusted-code integrity workflow rather than a sandbox or hermetic execution environment.

## Public experience

The release surface must make the following easy to establish:

- what FMA does and does not prove;
- how to run the bounded evaluation path;
- the recommended documentation reading order;
- how assumptions, evidence gaps, reproducibility, dependencies, and decision basis are represented;
- how the Mission Decision Packet connects evidence to a human decision and explicit reopen conditions;
- how to report a security issue privately;
- what licensing applies.

Examples remain synthetic and generic. Real program evidence does not belong in this public repository.

## Release evidence

The stable release record must bind:

- the exact accepted commit;
- the stable tag;
- source archive;
- wheel;
- SHA-256 artifact manifest;
- tracked-source manifest generated from the release commit;
- successful clean-user verification of the published artifacts.

Commit-specific hosted evidence belongs in GitHub Actions and release metadata rather than being recursively embedded back into the source tree.

## Acceptance rule

A stable release is promoted only when the source, hosted verification, public artifact set, and clean-user verification agree on the same release identity and all required controls pass.
