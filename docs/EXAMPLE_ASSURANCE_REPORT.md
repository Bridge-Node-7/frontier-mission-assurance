# Example Mission Assurance Report

This is an illustrative output shape for `examples/frontier_program/graph.yaml`.

## Evidence coverage

- Critical nodes: **3**
- Directly covered: **2**
- Coverage ratio: **66.7%**

### Critical nodes without direct evidence

- `CLAIM-CYCLE-TARGET`

## Open assumptions

| Assumption | Status | Title |
|---|---|---|
| `ASSUMP-CONTROL-INTERFACE` | open | The control interface can satisfy calibration, reliability, and manufacturability needs simultaneously |
| `ASSUMP-CYCLE-COMPOSITION` | open | Sensing, control, actuation, and scheduling compose within the target cycle budget |
| `ASSUMP-SCALE-PERFORMANCE` | open | Subsystem performance does not degrade beyond architecture margin at deployment scale |

## Decision receipt

The synthetic example decision is **HOLD** because the graph deliberately contains a critical claim without direct evidence.

The public reference exposes that gap; it does not calculate an automatic engineering priority or make the consequential decision.
