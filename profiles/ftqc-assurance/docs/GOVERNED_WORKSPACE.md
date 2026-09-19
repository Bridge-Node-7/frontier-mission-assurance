# Governed Workspace

Use this pattern when applying the FTQC profile around real work:

```text
Authoritative systems of record
lab / source control / models / documents / supplier systems
                 │
                 │ governed references
                 ↓
    governed FTQC Assurance workspace
                 │
                 │ bounded profile contracts
                 ↓
              FMA runtime
                 │
                 ↓
        Decision Basis / Packet
```

## Doctrine

> **Reference the evidence. Do not relocate the evidence.**

FTQC Assurance should retain only the minimum information needed to preserve identity, provenance reference, applicability, relationship to claims, review state, and decision relevance.

The authoritative source remains the system that owns the evidence.

## Operational use

Keep authoritative evidence in the environment that owns it. Carry only the
bounded references and review context needed for the assurance case.

Contribute material to this repository only when it is appropriate for the
repository's published evaluation scope.
