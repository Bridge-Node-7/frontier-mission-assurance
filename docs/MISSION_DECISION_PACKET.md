# Mission Decision Packet

A Mission Decision Packet is the minimum reviewable bundle needed to connect a consequential technical decision to its evidence, assumptions, reproduction state, dependencies, and explicit conditions for reopening the decision.

It is designed for fast frontier programs where research, software, experiments, interfaces, and external contributors move at different speeds.

The packet is not a replacement for notebooks, source control, laboratory systems, test infrastructure, or private program management. It is the thin evidence-to-decision layer across them.

## The core idea

A static design review answers:

> Why did we decide this?

A Mission Decision Packet should also answer:

> What would make us revisit it?

That second question matters because high-consequence engineering decisions are rarely permanent. They remain justified only while their declared evidence, assumptions, interfaces, and mission requirements remain inside the reviewed boundary.

```text
MISSION
  ↓
DECISION QUESTION
  ↓
CLAIMS / REQUIREMENTS
  ↓
ASSUMPTIONS + INTERFACES
  ↓
EVIDENCE / EXPERIMENT / REPRODUCTION
  ↓
DECISION BASIS
  ↓
HUMAN DISPOSITION
  ↓
REOPEN CONDITIONS
  └────────────→ reassess when the evidence boundary changes
```

This turns a one-time review into a bounded, inspectable decision contract without automating the accountable human judgment.

## Packet contents

A useful packet normally contains only what the decision actually needs:

1. **Mission objective** — the outcome the decision serves.
2. **Decision question** — the consequential choice being made.
3. **Claims or requirements** — what must be true for the decision to remain justified.
4. **Open assumptions** — what the team is relying on without direct establishment.
5. **Direct evidence** — experiment, analysis, simulation, proof, test, or other evidence supporting the claims.
6. **Reproduction evidence** — where a result important enough to influence the decision has been rerun or independently challenged.
7. **Interfaces and dependencies** — what upstream or external changes may invalidate the basis.
8. **Decision receipt** — the current human disposition and cited basis.
9. **Reopen conditions** — explicit triggers that require the decision to be reconsidered.
10. **Human-readable report** — a compact review surface for the people who own the decision.

The packet should stay small. Its quality is measured by decision usefulness, not record count.

## Why the reopen contract matters

A decision receipt is more valuable when it records the conditions under which the decision no longer deserves to be treated as settled.

Examples of reopen triggers include:

- a critical assumption is contradicted by new evidence;
- a representative experiment produces materially different behavior;
- a dependency or external interface changes;
- a model is shown not to apply to the physical configuration being built;
- a reproduced result falls outside its declared tolerance;
- an AI-generated result fails specification or applicability review;
- a mission requirement or operating envelope changes.

FMA does not monitor those conditions autonomously in this public reference. It makes them explicit so that private program policy, CI, review practice, or another system can decide how to watch them.

## 90-second inspection path

The bundled synthetic frontier-program fixture already demonstrates the pattern.

```bash
fma validate examples/frontier_program/graph.yaml
fma assumptions examples/frontier_program/graph.yaml
fma coverage examples/frontier_program/graph.yaml
fma impact examples/frontier_program/graph.yaml CLAIM-CYCLE-TARGET
fma receipt examples/research_receipt/receipt.yaml
fma decision examples/frontier_program/graph.yaml examples/frontier_program/decision-receipt.yaml
fma report examples/frontier_program/graph.yaml --out mission-decision-report.md
```

The intended interpretation is more important than the commands:

- the graph is structurally valid;
- unresolved assumptions remain visible;
- critical direct-evidence gaps remain visible;
- dependency impact can be inspected before downstream work silently inherits a changed premise;
- reproducibility can be verified separately from scientific truth;
- the decision basis can cite the exact graph nodes it depends on;
- the synthetic decision remains `HOLD` because the integrated-cycle claim lacks direct experimental evidence.

See [`../examples/frontier_program/README.md`](../examples/frontier_program/README.md) for the worked decision story.

## Research-to-decision flow

Many frontier teams already have reproducible research code. FMA adds a layer above that code without changing the research workflow:

```text
PAPER / THEORY / MODEL / AI OUTPUT
              ↓
      REPRODUCIBLE CODE + DATA
              ↓
       RESEARCH RECEIPT
              ↓
          CLAIM / ASSUMPTION
              ↓
       SYSTEM / INTERFACE IMPACT
              ↓
        DECISION RECEIPT
```

The point is not to turn research into paperwork. The point is to preserve the chain from a result to the decision that depends on it.

A result can be reproducible and still be inapplicable to the system being built. A proof can be formally valid and still formalize the wrong requirement. A subsystem can pass locally and still fail when composed with another subsystem. The Mission Decision Packet keeps those distinctions visible.

## Cross-organization use

For a partner or supplier boundary, the packet can expose only the shareable contract:

```text
PRIVATE INTERNAL STATE
        │
        │ bounded export
        ▼
CLAIM + REQUIREMENT + EVIDENCE + RECEIPT
        │
        ▼
INTERFACE REVIEW
        │
        ▼
DEPENDENT DECISION
```

The private reasoning, sensitive evidence, customer context, and prioritization model do not belong in the public FMA repository.

## AI-assisted work

If AI contributes to a result, the packet should not collapse machine output directly into evidence.

A useful path is:

```text
AI OUTPUT
   ↓
PROVENANCE
   ↓
CLAIM + LIMITATIONS
   ↓
SPECIFICATION / APPLICABILITY REVIEW
   ↓
EXPERIMENT / REPRODUCTION / CHALLENGE
   ↓
DECISION BASIS
```

The Scientific Discovery Assurance profile provides additional bounded contracts for this class of work. See [`../profiles/scientific-discovery/README.md`](../profiles/scientific-discovery/README.md).

## Pilot acceptance criteria

A Mission Decision Packet earns continued use only if it improves the engineering decision.

Useful acceptance questions are:

- Can a new reviewer reconstruct the decision basis faster?
- Did the packet surface an important assumption that was previously implicit?
- Did it expose missing direct evidence before a downstream commitment?
- Can a reproduced result be traced to the decision it influences?
- Can the team identify which decisions need review after an upstream change?
- Are the reasons for `APPROVE`, `HOLD`, `REVISE`, or `REJECT` understandable without reconstructing the entire program history?
- Are the conditions that would reopen the decision explicit?

If the packet does not improve those outcomes, reduce it.

## Public-boundary rule

This repository contains only public-safe software, documentation, and synthetic fixtures. Do not place real mission evidence, proprietary architecture details, customer identifiers, private partner information, credentials, or internal decision intelligence in this public repository.

Operational use belongs in an appropriately access-controlled environment.
