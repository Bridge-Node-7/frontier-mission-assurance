# Interoperability

FMA exposes small public contracts intended for interchange without disclosing private implementation.

## Contract versions

Current public contract versions:

- assurance graph: `graph_version: "1.0"`;
- research receipt: `receipt_version: "1.0"`;
- decision receipt: `decision_version: "1.0"`.

The JSON Schemas under `schemas/` are the portable structural contracts. Runtime validation intentionally aligns with their supported graph values.

## Compatibility rules

- Producers must preserve declared version fields.
- Consumers must fail visibly on unsupported contract versions.
- Public identifiers should be stable within a record and must not encode private organization/program context.
- Private systems may map richer internal state into these public contracts, but the public contract does not define or reveal the private internal model.
- A future incompatible contract change requires a new contract version and migration notes.

## Evidence semantics

Interoperability establishes structure and declared relationships, not source credibility or scientific truth. A consumer must retain the distinction between evidence bytes, provenance declarations, acceptance checks, and authorized human judgment.
