# Architecture

FMA is intentionally thin. It uses ordinary YAML/JSON and small command-line checks so the public reference remains inspectable and portable.

## Logical architecture

```text
Sources / Experiments / Simulations
              │
              ▼
       declared artifacts
              │
              ▼
       Research Receipt
              │
              ▼
       Assurance Graph
              │
      ┌───────┼────────┐
      ▼       ▼        ▼
  validate  coverage  impact
      │       │        │
      └───────┼────────┘
              ▼
       Decision Receipt
```

## Assurance path

A useful generic path is:

```text
MISSION
  ↓ depends_on
CLAIM / REQUIREMENT
  ↓ depends_on
ASSUMPTION
  ↓ verified_by / validated_by
EXPERIMENT / EVIDENCE
  ↓ supports
DECISION BASIS
```

The graph is a portable public structure. It is not a requirement to centralize every operational detail or sensitive artifact in one repository.

## Separation of responsibilities

- **Graph validation** checks declared IDs, kinds, statuses, relations, and references.
- **Evidence coverage** reports whether critical mission/claim/requirement nodes have direct evidence edges.
- **Assumption visibility** lists unresolved assumptions without calculating an automated priority score.
- **Dependency impact** traverses declared `depends_on` / `requires` relations to show what may need review after change.
- **Research receipts** bind declared inputs/outputs to hashes and numerical checks.
- **Decision receipts** verify that cited basis nodes exist in a valid graph.

These are bounded reference mechanics rather than a claim that all program operations belong in FMA.

## Verification versus reproduction

`fma receipt` is intentionally non-executing: it validates the checked-in artifact hashes and numerical acceptance criteria.

`fma reproduce` is explicit and opt-in: it verifies receipt inputs first, executes the declared command with `shell=False` inside the receipt directory, and then verifies the resulting output hashes and numerical criteria.

## What the graph does not prove

Graph validity is not scientific truth. A structurally valid edge can still be based on weak or incorrect source material. Source credibility, independence, applicability, calibration validity, and domain-specific sufficiency remain review responsibilities unless separately encoded and validated.

See [`../PUBLIC_BOUNDARY.md`](../PUBLIC_BOUNDARY.md) for the public-data and claim boundary.

## Runtime boundary

The public runtime operates on local files and has no remote API client or telemetry path. Network/package infrastructure may be used during installation and hosted CI, but validation itself is local. See [`THREAT_MODEL.md`](THREAT_MODEL.md) and [`INTEROPERABILITY.md`](INTEROPERABILITY.md).
