# Governed Workspace

Orbital Recovery Assurance separates **public assurance infrastructure** from
**governed mission evidence**.

## Reference repository

The repository publishes the schemas, validators, methods, synthetic examples,
benchmark material, and documentation needed to inspect the profile.

Public examples should be authored from the public contract and public sources
rather than derived by copying an operational case.

## Governed assessment environment

Real assessments should remain in the partner's existing governed environment or a
purpose-built governed workspace.

A local assessment may reference:

```text
LOCAL-EVIDENCE-001
LOCAL-AUTHORITY-001
LOCAL-CONFIG-001
LOCAL-RECOVERY-CHAIN-001
LOCAL-OPTION-001
```

The Mission Recovery Chain view should remain a projection over these governed records,
not a second canonical store.

The local environment resolves those identifiers to real records. The public repository
does not need to know what they represent.

## Ownership rule

Use one authoritative owner per real record.

If another system already owns evidence, configuration, authority, or a strategic option,
the assessment should reference it rather than silently cloning it into a second canonical
store.

## Public example rule

When proposing a public example:

1. start from the published profile contract;
2. use synthetic identifiers and values;
3. cite only sources suitable for public reference;
4. run the repository release checks;
5. complete human review of the resulting public surface.

Treat publication as a separate review decision; passing the profile validator
does not authorize release.

## No default data path back to BN7

The profile can be evaluated locally and does not require a remote service.

That separation keeps the reference method inspectable while authoritative
records remain governed by the systems that own them.

## Governed record class

Portable schemas support governed case records as well as synthetic reference
examples. Checked-in worked examples are required to remain `synthetic`.
