# Stable Release Acceptance

A stable Frontier Mission Assurance release binds one exact source state to one verified public artifact set. Promotion occurs only after the source, hosted verification, release metadata, and clean-user checks agree on the same identity.

## Hosted verification

The required hosted verification surface includes:

- Python 3.11, 3.12, and 3.13 validation on Ubuntu;
- Ubuntu, macOS, and Windows smoke validation;
- wheel build and fresh installation;
- lint, unit, regression, schema, tamper, and public-release tests;
- adversarial rejection-path tests for assurance-graph and decision validation;
- code-binding and fresh-output reproduction-integrity regressions;
- controlled malformed-input CLI behavior with exit code `2` and no traceback;
- deterministic report regression under `SOURCE_DATE_EPOCH`;
- dependency review where applicable;
- static analysis where configured;
- Scientific Discovery Assurance validation when present;
- Orbital Recovery Assurance validation when present;
- tracked-file public release verification.

Any required check that is red, unexpectedly skipped, or materially different from the source revision blocks stable promotion.

## Reproduction-integrity release gate

The stable candidate demonstrates that:

- declared code and input hashes are verified before trusted execution;
- the receipt command is bound to the declared entrypoint;
- the reproduction workspace begins without declared outputs;
- a successful no-output execution cannot reuse a stale source-tree result;
- newly generated outputs satisfy declared hashes and acceptance checks;
- legacy receipt formats retain their documented verification semantics;
- reproduction is described accurately as a trusted-code integrity workflow.

## Public experience

The release surface makes the following immediately clear:

- what FMA validates and the scope of a PASS;
- how to run the reference evaluation;
- the recommended documentation path;
- how assumptions, evidence gaps, reproducibility, dependencies, and decision basis are represented;
- how Mission Decision Packets connect evidence to accountable decisions and explicit reopen conditions;
- how specialized assurance profiles integrate without replacing governed systems;
- how to report a security issue privately;
- what licensing and distribution rights apply.

Public examples remain source-neutral and limited to material appropriate for unrestricted evaluation.

## Release evidence

The stable release record binds:

- the exact accepted commit;
- the stable tag;
- source archive;
- wheel;
- SHA-256 artifact manifest;
- tracked-source manifest generated from the release commit;
- software bill of materials;
- available provenance attestations;
- successful clean-user verification of the published artifacts.

Hosted validation evidence is recorded in GitHub Actions and release metadata.

## Acceptance rule

A stable release is promoted only when the source, hosted verification, public artifact set, and clean-user verification agree on the same release identity and all required controls pass.
