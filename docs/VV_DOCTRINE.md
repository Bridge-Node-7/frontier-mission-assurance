# V&V Doctrine: Minimum Sufficient Assurance

## Objective

The objective of V&V is **not maximum documentation**. It is the fastest defensible path from uncertainty to a justified engineering decision.

## Operating equation

Conceptually:

```text
Assurance Value = (Decision Confidence × Mission Consequence)
                  / (Verification Cost + Schedule Burden)
```

This is not a calibrated physical equation. It is a decision heuristic: verification effort should scale with consequence, uncertainty, and reversibility.

## Ten principles

1. **Mission first.** A test is valuable because of the mission decision it informs.
2. **Minimum sufficient assurance.** Stop when evidence is sufficient for the current decision; reopen when the context changes.
3. **Assumption visibility.** Hidden assumptions are untracked engineering debt.
4. **Sensitivity-driven verification.** Verify high-sensitivity assumptions before low-consequence details.
5. **Evidence by construction.** Experiments should emit provenance and acceptance results automatically.
6. **Cross-domain traceability.** Preserve links across math, code, simulation, hardware, suppliers, and mission claims.
7. **Graduated independence.** Higher-consequence claims receive greater verification independence.
8. **AI requires evidence gates.** Faster design generation must be matched by faster falsification and validation.
9. **Failures become institutional knowledge.** Failed experiments and contradicted assumptions remain searchable evidence.
10. **The product is a decision.** Reports are useful only when they improve a decision.

## Graduated verification independence

- **Tier 0 — Self-check:** creator executes automated checks.
- **Tier 1 — Independent implementation:** reference and production calculations cross-check.
- **Tier 2 — Peer reproduction:** another engineer/scientist independently reproduces.
- **Tier 3 — Mission V&V:** evidence is evaluated against system/mission consequence.
- **Tier 4 — External replication:** reserved for the highest-consequence claims.

## Evidence ladder

Keep these distinct:

1. **Analytical support** — theorem, derivation, resource model.
2. **Computational verification** — implementation matches intended mathematics.
3. **Simulation evidence** — model behavior under declared assumptions.
4. **Subsystem validation** — physical behavior in representative conditions.
5. **Integration validation** — composed behavior across interfaces.
6. **Mission validation** — end capability satisfies intended use.

Never silently promote evidence from a lower rung into a stronger claim.
