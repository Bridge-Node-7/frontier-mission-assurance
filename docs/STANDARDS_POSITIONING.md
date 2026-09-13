# Standards positioning

Frontier Mission Assurance is a deliberately small public reference layer. It does not claim that assurance cases, provenance records, artifact hashing, reproducible workflows, numerical regression checks, or signed attestations are new inventions.

## What FMA is

FMA combines a small set of established engineering ideas into a bounded workflow for frontier teams:

- a graph of missions, claims, assumptions, evidence, dependencies, risks, and decisions;
- content-addressed research receipts with explicit acceptance checks;
- fresh code-bound reproduction for trusted receipt-declared code;
- thin decision receipts tied to graph-valid basis nodes;
- explicit PASS semantics that refuse to convert machine checks into scientific truth or decision authority.

The product claim is therefore about **composition, restraint, portability, and user experience**, not novelty of the underlying primitives.

## Assurance-case relationship

Structured assurance cases are an established field. FMA's assurance graph is intentionally less expressive than full assurance-case metamodels: it does not currently require dedicated strategy, context, justification, or defeater node classes.

That is a deliberate minimum-sufficient-assurance choice, not a claim that richer assurance-case formalisms are unnecessary. Teams that require those constructs should keep them in the owning domain model or use a richer assurance-case tool and map the portable subset into FMA.

## Provenance and supply-chain relationship

Research Receipt v2 binds declared code, inputs, outputs, and numerical checks with SHA-256 and records the command/entrypoint needed for trusted fresh reproduction.

Core FMA receipts are **not signed attestations**. Hash consistency can establish artifact integrity relative to the receipt; it does not establish who authored, approved, or witnessed the receipt. Authorship, signer identity, external timestamping, and trust-root policy require separate evidence.

Scientific Discovery Assurance can record external anchor and signature evidence for research-priority claims, but that is distinct from signing every core FMA receipt.

## Reproducibility relationship

FMA keeps exact artifact identity and semantic acceptance as separate concepts.

- SHA-256 identifies exact bytes.
- Numerical checks express declared acceptance criteria.
- Fresh reproduction verifies that required outputs were created after execution in a fresh declared-artifact workspace.
- A PASS still does not prove scientific truth, independent replication, or adequacy of the declared acceptance criteria.

For stochastic or nondeterministic workloads, future profiles should preserve exact hashes for each run while allowing separately declared statistical acceptance semantics rather than weakening hash identity.

## Portfolio rule

Bridge Node 7 repositories should converge through explicit adapters and stable contract identifiers, not by forcing one giant evidence or decision ontology.

The owning domain system keeps the richer record. FMA carries the portable assurance projection. Cross-repository adapters must be deterministic, provenance-preserving, synthetic in public examples, and independently validated.
