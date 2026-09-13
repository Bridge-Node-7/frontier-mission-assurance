# Interoperability

FMA exposes small public contracts intended for interchange without requiring disclosure of implementation details beyond the contract boundary.

## Contract versions

Current public contract versions:

- assurance graph: `graph_version: "1.0"`;
- executable research receipt: `receipt_version: "3.0"`;
- exact local research receipt compatibility: `receipt_version: "2.0"`;
- decision receipt: `decision_version: "1.0"`.

The versioned JSON Schemas publish stable identifiers:

- `https://bridge-node-7.github.io/frontier-mission-assurance/assurance-graph.schema.json`
- `https://bridge-node-7.github.io/frontier-mission-assurance/research-receipt.schema.json`
- `https://bridge-node-7.github.io/frontier-mission-assurance/research-receipt-v3.schema.json`
- `https://bridge-node-7.github.io/frontier-mission-assurance/decision-receipt.schema.json`

Those identifiers name contracts; they do not imply that every producer must use the same internal data model.

The JSON Schemas under `schemas/` are the portable structural contracts. Runtime validation additionally enforces cross-artifact invariants that JSON Schema alone does not conveniently express: declared entrypoint binding, check-to-output binding, calibration validity at the receipt `as_of` time, external job identity continuity, code/input manifest integrity, collection-output provenance, and the selected output-acceptance mode.

Version 2 remains the exact local-reproduction contract. Version 3 is additive: code and input hashes remain exact, output acceptance becomes explicit, calibration state can be governed, and external scheduler submission/collection evidence can be verified without pretending public CI ran a real cluster.

The runtime retains non-executing verification compatibility for historical version-1 receipts. Fresh local reproduction requires version 2 or a version-3 receipt whose execution mode is `LOCAL`. Version-3 `EXTERNAL` receipts are collection-verification contracts and are not launched by `fma reproduce`.

## Mapping richer domain models

FMA is a thin assurance envelope, not a universal ontology.

A domain system may own richer evidence or decision semantics and map only the portable subset required by FMA. For example, a domain evidence record may retain source basis, contradictory evidence, AI involvement, reviewer identity, applicability, and classification while projecting a stable evidence node and references into an FMA graph.

Likewise, a domain decision object may retain objectives, alternatives, scores, constraints, approvals, or outcome lineage while projecting a bounded FMA Decision Receipt for basis verification and reopen conditions.

Interoperability therefore means **preserve local meaning, map explicit fields, and fail visibly on loss or ambiguity**. It does not mean flattening every Bridge Node 7 repository into one schema.

## Compatibility rules

- Producers must preserve declared version fields.
- Consumers must fail visibly on unsupported contract versions.
- Public identifiers should be stable within a record and must not encode sensitive organization/program context.
- Implementations may map richer local state into these public contracts; interoperability does not require the contract to describe that implementation.
- A future incompatible contract change requires a new contract version and migration notes.
- A consumer must not silently upgrade a legacy receipt's assurance meaning.
- Version-2 exact-output semantics must not be weakened by version-3 stochastic acceptance.
- Adapters must preserve provenance to the source record and must not invent evidence, confidence, authority, calibration state, or outcome state that the source did not contain.

## Evidence semantics

Interoperability establishes structure and declared relationships, not source credibility or scientific truth. A consumer must retain the distinction between code bytes, evidence bytes, provenance declarations, acceptance checks, calibration state, reproduction state, and authorized human judgment.

See [`STANDARDS_POSITIONING.md`](STANDARDS_POSITIONING.md) for the non-claim boundary relative to established assurance and provenance standards.
