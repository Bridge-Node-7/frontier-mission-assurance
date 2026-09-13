# Architecture

FMA is intentionally thin. It uses ordinary YAML/JSON and small command-line checks so the public reference remains inspectable and portable.

## Logical architecture

```text
Sources / Experiments / Simulations
              │
              ▼
  declared code + inputs
              │
              ▼
    Research Receipt v2
              │
      ┌───────┴────────┐
      ▼                ▼
non-executing      explicit trusted
 verification       reproduction
                       │
                       ▼
                fresh workspace
                outputs absent
                       │
                       ▼
                  new outputs
                       │
                       ▼
                hash + numeric V&V
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

- **Graph validation** checks declared IDs, kinds, statuses, relations, and references and surfaces duplicate edges plus `depends_on` self-loops/cycles as warnings.
- **Evidence coverage** reports whether critical mission/claim/requirement nodes have direct evidence edges.
- **Assumption visibility** lists unresolved assumptions without calculating an automated priority score.
- **Dependency impact** traverses declared `depends_on` / `requires` relations to show what may need review after change.
- **Research receipts** bind declared code, inputs, outputs, and numerical checks to a versioned verification contract.
- **Fresh reproduction** stages only declared code and inputs into a temporary workspace, requires the declared entrypoint to run, and verifies newly created outputs.
- **Decision receipts** verify that cited basis nodes exist in a valid graph.

These are bounded reference mechanics rather than a claim that all program operations belong in FMA.

## Verification versus reproduction

`fma receipt` is intentionally non-executing. For a version-2 receipt it verifies the declared code, input, and output hashes plus numerical acceptance criteria and reports how many controls actually ran.

`fma reproduce` is explicit and opt-in. It requires a version-2 receipt, verifies code and inputs before execution, creates a fresh temporary workspace containing the receipt plus declared code and inputs, leaves declared outputs absent before execution, executes the trusted declared command with `shell=False`, and then verifies the outputs and numerical criteria.

That workspace prevents a stale result in the caller's working tree from satisfying a fresh reproduction. It is an integrity boundary, not a sandbox, container, or hermetic execution environment. Legacy version-1 receipts remain non-executingly verifiable for historical continuity but are not eligible for the current fresh-reproduction PASS.

## What the graph does not prove

Graph validity is not scientific truth. A structurally valid edge can still be based on weak or incorrect source material. Source credibility, independence, applicability, calibration validity, and domain-specific sufficiency remain review responsibilities unless separately encoded and validated.

See [`../PUBLIC_BOUNDARY.md`](../PUBLIC_BOUNDARY.md) for the public-data and claim boundary.

## Runtime boundary

The public runtime operates on local files and has no remote API client or telemetry path. Network/package infrastructure may be used during installation and hosted CI, but validation itself is local. See [`THREAT_MODEL.md`](THREAT_MODEL.md) and [`INTEROPERABILITY.md`](INTEROPERABILITY.md).
