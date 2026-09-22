# FTQC Golden Path

This is the shortest public path for evaluating how Frontier Mission Assurance (FMA) carries one fault-tolerant quantum-computing decision from evidence to explicit reconsideration.

The path uses existing FMA contracts and the existing FTQC Assurance profile. It does **not** introduce a second assurance engine, a new decision authority, or a replacement quantum-engineering answer.

## The behavior

```text
FTQC technical evidence
        ↓
FTQC Assurance case
        ↓
claims + assumptions + applicability + expert review
        ↓
decision receipt + reopen conditions
        ↓
one controlling assumption changes
        ↓
resource estimate / evidence envelope / expert review become affected
        ↓
decision basis deserves reconsideration
```

FMA identifies what became stale or left its reviewed envelope. Qualified domain experts determine the replacement scientific or engineering answer. Accountable humans retain consequential decision authority.

## 1. Evaluate the bundled reference

From the repository root:

```bash
python scripts/evaluate_ftqc_reference.py .
```

Expected final line:

```text
RESULT - FTQC REFERENCE EVALUATION PASS
```

The reference deliberately keeps software/contract validation separate from technical readiness.

## 2. Inspect one governed case

For an authorized real case, use a separate governed workspace and keep authoritative evidence at its source.

Start with:

- [FTQC Assurance](../profiles/ftqc-assurance/README.md)
- [Governed FTQC Case Quickstart](../profiles/ftqc-assurance/docs/GOVERNED_CASE_QUICKSTART.md)
- [FTQC Evidence / Mission-Risk Baseline](../profiles/ftqc-assurance/docs/FTQC_EVIDENCE_MISSION_RISK_BASELINE.md)

A minimal case should contain one consequential decision, one architecture revision, one workload, one decision-relevant estimate, only the controlling claims and assumptions, the evidence references that matter, the necessary expert gates, and explicit reopen conditions.

## 3. Compare the reviewed state with a changed state

Keep the previous governed state and create a current state. Then run:

```bash
python scripts/compare_ftqc_cases.py \
  ../my-ftqc-case-previous \
  ../my-ftqc-case-current \
  --report ../my-ftqc-case-current/change-impact.md
```

The comparison may surface:

- changed assumptions and context;
- reused estimates that are now stale;
- evidence outside its declared applicability envelope;
- expert reviews whose reopen triggers were crossed;
- downstream graph impact;
- whether the declared decision node is impacted.

The comparison does **not** infer the replacement quantum-engineering answer.

## 4. Preserve the human-facing decision basis

Use the existing [Mission Decision Packet](MISSION_DECISION_PACKET.md) pattern to keep the smallest reviewable bundle around the consequential decision.

A packet should make visible:

- the mission objective;
- the decision question;
- claims and requirements;
- open assumptions;
- direct and reproduction evidence;
- interfaces and dependencies;
- the current human disposition;
- explicit reopen conditions.

The key question is not only *why did we decide this?* It is also *what would make us revisit it?*

## 5. Use the existing portable assurance boundary

FMA owns the portable:

`bn7.frontier-mission-assurance.assurance-context/0.1.0`

contract. It carries bounded change impact and review state for downstream decision preparation while excluding raw evidence and avoiding any increase in epistemic or decision authority.

See:

- [Interoperability](INTEROPERABILITY.md)
- [Portable interface manifest](../INTERFACES.json)
- [Synthetic changed-assumption assurance context](../examples/assurance_context/synthetic-changed-assumption.json)

## 6. Downstream decision preparation remains bounded

A downstream consumer may use the assurance-context projection to prepare a decision view, but transport is not approval.

The invariants are:

```text
integrity        ≠ authenticated origin
schema validity  ≠ factual truth
reproduction     ≠ scientific validity
evidence         ≠ universal applicability
decision context ≠ consequential authority
```

## Golden-path acceptance questions

A first-time technical reviewer should be able to answer:

1. What decision is under review?
2. What evidence and assumptions support it?
3. What changed?
4. Which estimate, evidence envelope, claim, or expert review became affected?
5. Why does the prior basis deserve reconsideration?
6. What remains for a qualified human/domain expert to determine?

If the path does not make those answers easier, reduce the case rather than adding more records.

## Scope boundary

This public path demonstrates source-neutral contracts, synthetic examples, local validation, change-impact behavior, and decision-basis continuity. It does not establish quantum truth, hardware performance, government readiness, mission qualification, independent V&V, customer acceptance, or authority to deploy.
