# Mission Recovery Chain View

The Mission Recovery Chain is a **user-facing projection**, not a new system of record,
canonical BN7 object, decision engine, or spacecraft ontology.

Its purpose is to help an operator answer one practical question quickly:

> **Where is the current path back to the required mission capability blocked?**

## Default chain

For a declared mission thread, start with:

`Power → Contact → Telemetry → Command → Capability`

- **Power** — sufficient energy/state persistence exists for recovery activity.
- **Contact** — a usable or predictable communications path exists.
- **Telemetry** — sufficient state information is available to characterize the system.
- **Command** — legitimate, technically usable control can be established.
- **Capability** — the required mission service can be delivered at the declared level.

The chain is a **logical recovery view**, not a universal assertion that every mission has
one strictly serial path. Alternate ground paths, external observation, service vehicles,
replacement assets, or other recovery options may bypass a failed asset or create a new
path. Model the chain for each essential mission capability and preserve those alternate
paths explicitly.

## Trust and authority are overlays, not a sixth serial link

Trust and authority apply across the chain:

```text
                 TRUST / AUTHORITY
                 ↓   ↓   ↓   ↓
POWER → CONTACT → TELEMETRY → COMMAND → CAPABILITY
```

Examples:

- Is the power-state observation trustworthy?
- Is the contact path authentic and uncompromised?
- Is the telemetry-producing software/configuration trusted?
- Is command authority legitimate and current?
- Is the resulting capability supported by sufficient requalification evidence?

This preserves the profile's three-plane architecture instead of collapsing trust,
authority, and physical state into one serial state machine.

## Count recovery paths, not assets

**Asset redundancy is not functional redundancy. Functional redundancy is not recovery
redundancy.**

A recovery path counts only when it can perform the required function under the failure
condition being assessed and does not silently collapse onto the same material dependency
as another path.

Examples of common-mode dependencies include shared identity, timing, software/update,
cloud, ground-capacity, supplier, communications, or authority roots.

The profile does not emit a synthetic "independence score." Preserve the dependency
structure and provenance roots explicitly. Separate structural roots also do not prove
statistical independence.

## Map → Count → Exercise

### 1. MAP

For each essential capability, identify:

- what must remain available;
- what must remain trustworthy;
- what must remain recoverable;
- which evidence establishes each state;
- which alternate paths can restore or bypass a failed stage.

### 2. COUNT

Count functionally capable **independent recovery paths**, not merely assets:

- alternate communications/command paths;
- usable ground capacity;
- trusted software/configuration baselines;
- cryptographic/identity recovery mechanisms;
- service/augmentation options;
- replacement capability;
- people and authorities able to activate those options.

### 3. EXERCISE

Use synthetic or controlled exercises to combine:

- technical failure;
- ambiguous diagnosis;
- lost/degraded communications;
- evidence disagreement;
- trust degradation;
- authority uncertainty;
- post-intervention evidence gaps.

Measure which dependency becomes binding and what evidence is required to reopen the
path.

## Relationship to the assurance loop

```text
MAP THE RECOVERY CHAIN
        ↓
FIND THE CURRENT BINDING CONSTRAINT
        ↓
ESTABLISH WHAT IS OBSERVED / INFERRED / UNKNOWN
        ↓
ACQUIRE DECISION-RELEVANT EVIDENCE
        ↓
FILTER TO ROBUST OPTIONS
        ↓
PREPARE ELIGIBLE OPTIONS FOR HUMAN DECISION
        ↓
INTERVENE
        ↓
REQUALIFY
        ↓
MEASURE TIME TO TRUST
        ↓
REASSESS
```

The solution follows the bottleneck. The profile must not assume that cybersecurity,
hardware, ground infrastructure, servicing, logistics, or capacity is always the binding
constraint.

## Machine-readable view

`schemas/recovery-chain-view.schema.json` and the synthetic example
`examples/synthetic-recovery-case/recovery-chain-view.json` provide an optional portable
projection for this lens.

The view references governed evidence. It does not become the canonical evidence source.
