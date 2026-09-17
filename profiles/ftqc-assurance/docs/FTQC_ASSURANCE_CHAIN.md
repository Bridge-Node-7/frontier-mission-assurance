# Workload-to-System Assurance Chain

FTQC Assurance uses an architecture-neutral view of the evidence path from intended utility to a consequential technical decision:

```text
Utility / mission objective
→ Workload
→ Algorithm
→ Logical resource requirement
→ QEC assumptions
→ Resource estimate
→ Physical error / loss assumptions
→ Control / movement / scheduling
→ Physical architecture
→ Subsystem and interface dependencies
→ Industrial dependencies
→ Risk-retirement evidence
→ Expert adjudication
→ Mission decision
```

The chain is a decision-oriented projection, not a claim that every FTQC architecture uses the same implementation.

## Neutral-atom view

The synthetic reference case renders the same pattern as an **Algorithm-to-Atom view**. This keeps the public example relevant to neutral-atom systems without hard-coding the entire FTQC profile to one modality.

## Change sensitivity

A material change should not silently preserve downstream confidence. When a declared dependency changes, FMA-Q surfaces affected graph nodes, evidence envelopes, expert reviews, resource estimates, and decisions for reconsideration.

The profile does not infer the new scientific answer. It identifies where the prior decision basis no longer composes cleanly.
