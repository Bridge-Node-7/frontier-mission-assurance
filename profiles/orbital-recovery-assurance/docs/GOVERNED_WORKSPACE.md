# Governed Workspace

Orbital Recovery Assurance is designed to work with authoritative evidence
systems without becoming a second source of truth.

## Operating pattern

Use the public profile for its schemas, validators, methods, reference cases,
and review semantics. Perform real assessments in the environment approved for
that work, and connect the profile through bounded identifiers and references.

A local assessment may reference:

```text
LOCAL-EVIDENCE-001
LOCAL-AUTHORITY-001
LOCAL-CONFIG-001
LOCAL-RECOVERY-CHAIN-001
LOCAL-OPTION-001
```

The local environment resolves those identifiers to authoritative records. The
Mission Recovery Chain remains a projection over those records rather than a
second canonical store.

## Ownership rule

Use one authoritative owner per real record.

If another system already owns evidence, configuration, authority, or a
strategic option, reference it rather than silently cloning it into a second
canonical store.

## Contribution rule

Worked examples in this repository are synthetic and reviewable on their own.
Contribute additional examples only when they are appropriate for the
repository's published evaluation scope and pass the repository validation
gates.

## Local operation

The public profile does not require telemetry upload or remote API access. It
can be evaluated and used locally with the operator's own governed evidence
references.

## Governed record class

Partner-controlled case records may use `record_class: private` in governed
workspaces. Checked-in worked examples remain `synthetic` and are validated as
such.
