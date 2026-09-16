# Standards Positioning

Frontier Mission Assurance composes established assurance primitives into a compact, portable decision-evidence layer for frontier engineering teams.

Its contribution is the system-level integration of traceability, artifact identity, reproducibility, evidence-state separation, dependency impact, explicit decision basis, and human-owned authority into a workflow that remains inspectable in ordinary version-controlled artifacts.

## Product contribution

FMA combines:

- a mission assurance graph connecting missions, claims, assumptions, evidence, dependencies, risks, and decisions;
- content-addressed research receipts with explicit acceptance semantics;
- fresh code-bound reproduction for trusted receipt-declared code;
- decision receipts tied to graph-valid basis nodes;
- Mission Decision Packets with explicit reopen conditions;
- profile contracts for specialized assurance domains;
- precise PASS semantics that keep machine verification distinct from scientific or institutional authority.

The product value is in **composition, precision, portability, verification discipline, and operator experience**.

## Assurance-case interoperability

Structured assurance cases are an established field. FMA uses a compact portable projection optimized for evidence traceability and decision preparation while allowing richer assurance-case models to remain authoritative in the systems that own them.

Teams that require dedicated strategy, context, justification, defeater, or domain-specific constructs can retain those semantics locally and map the portable subset into FMA through explicit adapters.

## Provenance and attestations

Research receipts bind declared code, inputs, outputs, execution identity, and acceptance checks using SHA-256 and versioned semantics.

Core receipt integrity establishes exact artifact relationships relative to the receipt. Authorship, signer identity, external timestamping, and trust-root policy can be layered through external attestations when the mission requires them.

Scientific Discovery Assurance additionally records external anchor and signature evidence for research-priority claims while keeping those functions distinct from the core receipt model.

## Reproducibility

FMA keeps exact artifact identity and semantic acceptance separate:

- SHA-256 identifies exact bytes;
- numerical checks express declared acceptance criteria;
- fresh reproduction verifies that required outputs were created after execution in a fresh declared-artifact workspace;
- profile-specific controls can add domain acceptance semantics without weakening artifact identity.

For stochastic or nondeterministic workloads, FMA preserves exact hashes for each run and supports separately declared statistical acceptance semantics.

## Portfolio interoperability

Bridge Node 7 systems converge through explicit adapters, stable contract identifiers, and clear ownership boundaries.

Domain systems keep their richer records. FMA carries the portable assurance projection. Cross-system adapters are deterministic, provenance-preserving, source-neutral in public examples, and independently validated.
