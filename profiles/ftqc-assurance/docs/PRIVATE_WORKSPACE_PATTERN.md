# Private Workspace Pattern

The public FTQC profile is not a customer data store.

Use this pattern for governed work:

```text
Authoritative systems of record
lab / source control / models / documents / supplier systems
                 │
                 │ governed references
                 ↓
          private FMA-Q workspace
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

FMA-Q should retain only the minimum information needed to preserve identity, provenance reference, applicability, relationship to claims, review state, and decision relevance.

The authoritative source remains the system that owns the evidence.

## Public boundary

Do not place customer identities, proprietary architecture records, raw experiment data, supplier-sensitive records, controlled technical data, credentials, or nonpublic program information in this public repository.
