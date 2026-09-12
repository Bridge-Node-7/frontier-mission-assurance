# Synthetic Mission Decision Packet

This directory contains **only synthetic fixture data**.

It does not represent any real company, customer, supplier, employer, partner, mission, facility, architecture, schedule, requirement, performance value, experiment, or decision.

Use it to learn the data model and CLI behavior. Do not replace these files with real sensitive program data in a public fork or public repository.

## Decision story

The synthetic mission is to deliver a high-consequence frontier system inside a declared performance envelope.

The architecture has analytical evidence supporting resource feasibility, but one critical integration claim remains unresolved:

> Can the integrated control cycle meet the target budget when sensing, control, actuation, scheduling, and interface behavior are composed?

The example therefore keeps three assumptions visible:

- cycle composition remains inside the target budget;
- subsystem performance transfers to deployment scale with adequate margin;
- the control interface can satisfy calibration, reliability, and manufacturability needs together.

A synthetic integrated timing experiment is planned, but the timing claim does not yet have direct experimental evidence.

The decision receipt therefore records:

```text
DISPOSITION: HOLD
```

That is intentional. FMA is behaving correctly when it preserves an unresolved critical evidence gap instead of converting analytical confidence into a false verification state.

## Packet map

- [`graph.yaml`](graph.yaml) — mission, claims, assumptions, evidence, experiment, interface, risk, and decision relationships.
- [`decision-receipt.yaml`](decision-receipt.yaml) — current disposition, rationale, cited basis, and explicit reopen conditions.
- [`sources/mission-brief.md`](sources/mission-brief.md) — synthetic mission evidence.
- [`sources/architecture-note.md`](sources/architecture-note.md) — synthetic analytical evidence.
- [`../research_receipt/`](../research_receipt/) — separate deterministic reproduction example used to demonstrate research-receipt mechanics.

For the broader pattern, see [`../../docs/MISSION_DECISION_PACKET.md`](../../docs/MISSION_DECISION_PACKET.md).

## Quick start

From an installed development environment:

```bash
fma validate examples/frontier_program/graph.yaml
fma assumptions examples/frontier_program/graph.yaml
fma coverage examples/frontier_program/graph.yaml
fma impact examples/frontier_program/graph.yaml CLAIM-CYCLE-TARGET
fma decision examples/frontier_program/graph.yaml examples/frontier_program/decision-receipt.yaml
fma report examples/frontier_program/graph.yaml --out mission-decision-report.md
```

To inspect separate reproducibility mechanics:

```bash
fma receipt examples/research_receipt/receipt.yaml
```

Use `fma reproduce` only when you intentionally trust and want to execute the receipt-declared command.

## What a technical reviewer should notice

### 1. Evidence is not inferred

The resource-feasibility claim has direct synthetic analytical evidence. The cycle-target claim does not. FMA reports that distinction instead of assuming that evidence for one claim automatically supports another.

### 2. Assumptions are first-class

The system does not hide unresolved composition, scale-transfer, or interface assumptions inside prose. They remain inspectable nodes.

### 3. Integration risk crosses disciplines

The graph includes a cross-domain composition risk because individually acceptable subsystems can still fail when timing, interfaces, calibration, or scale are combined.

### 4. The decision has a basis

The decision receipt cites the exact claim, assumption, evidence, and planned experiment on which the `HOLD` disposition depends.

### 5. The decision knows when it must be revisited

The receipt explicitly reopens when:

- a representative integrated-cycle experiment produces verified reproducibility evidence; or
- the timing target or architecture dependency is materially revised.

That makes the decision change-sensitive rather than a static approval record.

## How to adapt the pattern privately

For a real program, replace the synthetic identifiers with access-controlled program records and keep sensitive evidence outside this public repository.

A first private pilot should stay small:

```text
1 mission objective
1 consequential decision
1–3 claims or requirements
only the assumptions that matter
existing direct evidence
one reproducibility receipt where justified
one decision receipt with reopen conditions
```

The goal is not to maximize structure. The goal is to reduce hidden uncertainty and make the next justified decision easier to see.
