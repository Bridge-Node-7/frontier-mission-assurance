# Interoperability

Orbital Recovery Assurance is a bounded assurance profile designed to compose with governed evidence systems and downstream human-governed decision workflows without becoming a second source of truth.

## Public interface boundary

```text
Governed evidence references
        ↓
Orbital Recovery Assurance profile
  evidence / eligibility / requalification checks
  synthetic reference assessment
        ↓
Bounded assessment context
        ↓
Human-governed decision workflow
```

## Interoperability rules

1. The profile must not become a second canonical evidence store.
2. Richer systems retain ownership of their native evidence, dependency, and option semantics.
3. The reference option-assessment policy is bounded to this profile and is not a universal decision standard.
4. A profile assessment may inform downstream decision preparation, but never records the consequential decision.
5. Domain-specific systems may provide richer semantics through explicit adapters without changing FMA core contracts.
6. Adapters must preserve provenance and fail visibly on ambiguity.
7. Integration should remain additive, reversible, and low-coupling.

The public contract exposes only the information needed for interoperable assurance. Internal system topology and implementation ownership are outside this repository's public boundary.
