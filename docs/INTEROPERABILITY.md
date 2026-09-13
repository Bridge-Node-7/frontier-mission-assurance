# Interoperability

FMA exposes small public contracts intended for interchange without requiring disclosure of implementation details beyond the contract boundary.

## Contract versions

Current public contract versions:

- assurance graph: `graph_version: "1.0"`;
- executable research receipt: `receipt_version: "2.0"`;
- decision receipt: `decision_version: "1.0"`.

The JSON Schemas under `schemas/` are the portable structural contracts. Runtime validation intentionally aligns with their supported values and additionally enforces cross-artifact invariants that JSON Schema alone does not conveniently express, such as the version-2 entrypoint being a declared code artifact and check paths referring to declared outputs.

The runtime retains non-executing verification compatibility for historical version-1 research receipts. Fresh reproduction requires the version-2 contract because version 1 does not carry the current code-binding and fresh-output semantics.

## Compatibility rules

- Producers must preserve declared version fields.
- Consumers must fail visibly on unsupported contract versions.
- Public identifiers should be stable within a record and must not encode sensitive organization/program context.
- Implementations may map richer local state into these public contracts; interoperability does not require the contract to describe that implementation.
- A future incompatible contract change requires a new contract version and migration notes.
- A consumer must not silently upgrade a legacy receipt's assurance meaning; version-1 verification remains historically useful but is not equivalent to a version-2 fresh reproduction PASS.

## Evidence semantics

Interoperability establishes structure and declared relationships, not source credibility or scientific truth. A consumer must retain the distinction between code bytes, evidence bytes, provenance declarations, acceptance checks, reproduction state, and authorized human judgment.
