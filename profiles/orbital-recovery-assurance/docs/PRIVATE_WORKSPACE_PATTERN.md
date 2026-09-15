# Private Workspace Pattern

Orbital Recovery Assurance separates **public assurance infrastructure** from
**private mission evidence**.

## Public repository

The public repository may contain:

- schemas;
- validators;
- methods;
- synthetic examples;
- synthetic benchmark protocols and results;
- source-neutral documentation.

It should not contain real program or relationship identifiers, telemetry,
customer evidence, mission-sensitive configuration, private economics, or operational
authority records.

## Private assessment environment

Real assessments should remain in the partner's existing governed environment or a
purpose-built private workspace.

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

## Sanitization rule

If an assessment artifact is ever proposed for public contribution:

1. remove real identities and relationship context;
2. replace program-specific identifiers with synthetic identifiers;
3. remove mission-sensitive values;
4. ensure every remaining example is safe to publish;
5. run the repository public-boundary gate;
6. perform human public-surface review.

Sanitization does not make a real assessment automatically suitable for release.

## No default data path back to BN7

The public profile has no requirement for telemetry upload, remote API access, or customer
data storage. A partner can evaluate and use the architecture locally.

That separation is intentional: the public method can be inspectable while the real
evidence remains under the partner's governance.

## Private record class

Real partner-controlled case records use `record_class: private`. That class is supported by the portable schemas but must never be committed as a worked case to the public repository. The public profile validator separately requires every checked-in worked example to remain `synthetic`.
