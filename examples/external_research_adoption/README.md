# External Research Adoption — Starter Sidecar

This source-neutral example demonstrates the smallest useful FMA wrapper around technical work that already exists somewhere else.

The external work is deliberately **not copied into this directory**.

```text
AUTHORITATIVE EXTERNAL WORK
paper / repository / model / experiment
             │
             │ exact identity + governed references
             ▼
THIS FMA SIDECAR
assurance graph + Decision Receipt
             │
             ▼
ACCOUNTABLE REVIEW
```

## What the example establishes

The synthetic sidecar records:

- a reported paper/result identity;
- a frozen synthetic source revision;
- the relationship that still needs review between the reported result and implementation;
- an unresolved reproduction-environment assumption;
- an unresolved applicability assumption;
- a planned fresh reproduction;
- a `HOLD` Decision Receipt that prevents the external result from silently becoming established decision evidence.

It does **not** claim that the external result is scientifically true, freshly reproduced, independently replicated, or applicable to a real system.

## Validate the sidecar

```bash
fma validate examples/external_research_adoption/graph.yaml
fma decision \
  examples/external_research_adoption/graph.yaml \
  examples/external_research_adoption/decision-receipt.yaml
```

## Use this as a starter

For a real governed evaluation, copy the *shape* of this sidecar into a private workspace rather than modifying the source repository merely to satisfy FMA.

Replace the synthetic identities with governed references to the exact artifacts your reviewers are authorized to use. Add a Research Receipt only when a bounded reproduction is justified and the code is trusted for execution in the selected environment.

Keep the source system authoritative. Keep protected evidence out of the public repository. Keep the decision disposition proportional to what the evidence actually establishes.

See [`../../docs/EXTERNAL_RESEARCH_ADOPTION.md`](../../docs/EXTERNAL_RESEARCH_ADOPTION.md) for repository, paper, model, experiment, and external-execution paths.
