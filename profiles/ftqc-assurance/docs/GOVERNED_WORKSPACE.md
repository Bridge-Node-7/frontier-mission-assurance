# Governed Workspace

The public FTQC profile is a portable contract and reference implementation, not a system of record.

Use this pattern for governed work:

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

## Workspace use

Keep authoritative evidence in the system that owns it. Use governed references
and only the profile fields required for provenance, applicability, review, and
decision traceability.
