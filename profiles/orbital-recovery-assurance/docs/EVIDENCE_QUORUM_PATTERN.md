# Evidence Quorum Pattern

Multiple records are not automatically multiple independent witnesses.

The profile groups evidence into provenance-correlation components when records share any declared root such as sensor source, clock source, identity source, or software pipeline. Shared-root relationships propagate transitively.

## Structural quorum

If a local mission policy requires corroboration, it should reason over independent provenance components rather than raw evidence-item count.

Example:

```text
EVIDENCE-A -- shared clock --> EVIDENCE-B
EVIDENCE-B -- shared identity --> EVIDENCE-C
```

The public reference treats these three records as one correlation component for structural-independence purposes.

## Non-claim

A separate provenance component is **not proof of statistical independence**. Missing lineage is not evidence of independence. The profile therefore does not publish a universal numerical "independence score."

A real user may declare a local quorum policy such as:

- minimum number of independently rooted components;
- required evidence classes;
- maximum age / validity envelope;
- mandatory source diversity;
- contradiction handling.

That policy remains local to the mission and accountable human governance.
