# Interoperability

FMA exposes small public contracts intended for interchange without requiring disclosure of implementation details beyond the contract boundary.

## Contract versions

Current public contract versions:

- assurance graph: `graph_version: "1.0"`;
- research receipt: `receipt_version: "1.0"`;
- decision receipt: `decision_version: "1.0"`.

The JSON Schemas under `schemas/` are the portable structural contracts. Runtime validation intentionally aligns with their supported graph values.

## Compatibility rules

- Producers must preserve declared version fields.
- Consumers must fail visibly on unsupported contract versions.
- Public identifiers should be stable within a record and must not encode sensitive organization/program context.
- Implementations may map richer local state into these public contracts; interoperability does not require the contract to describe that implementation.
- A future incompatible contract change requires a new contract version and migration notes.

## Evidence semantics

Interoperability establishes structure and declared relationships, not source credibility or scientific truth. A consumer must retain the distinction between evidence bytes, provenance declarations, acceptance checks, and authorized human judgment.
