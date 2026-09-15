# BN7 Interoperability

Orbital Recovery Assurance is intentionally a profile, not a new institutional system.

## Ownership boundaries

```text
Governed evidence / intelligence
        ↓ references only
Mission Graph
  dependency relations
  failure domains
  ProofRequests
  strategic options
        ↓ bounded context
Orbital Recovery Assurance profile
  evidence/eligibility/requalification checks
  synthetic reference assessment
        ↓ assessment context
Frontier Decision Engine
  human-facing decision preparation
        ↓
Accountable human
  consequential decision
```

## Interoperability rules

1. The profile must not become a second canonical evidence store.
2. Recovery options represented here do not replace Mission Graph strategic-option ownership.
3. The reference option-assessment policy is not a generic BN7 decision standard.
4. A profile assessment may inform downstream decision preparation, but never records
   the consequential decision.
5. A later domain system may replace the profile's rich orbital semantics without
   changing FMA core contracts.
6. Cross-system adapters must preserve provenance and fail visibly on ambiguity.
7. No current change to Mission Graph or Frontier Decision Engine is required merely
   to admit this profile.

This keeps the integration additive, reversible, and low-coupling.
