# FTQC Assurance

**Know when a fault-tolerant quantum design decision is still supported—and when new evidence means it must be revisited.**

FTQC Assurance is a bounded Frontier Mission Assurance profile for decision-basis continuity in fault-tolerant quantum computing programs.

It connects:

```text
design assumptions
↓
resource estimates
↓
QEC / physical-model evidence
↓
experimental results
↓
interfaces and dependencies
↓
expert review
↓
technical decisions
```

When one changes, FTQC Assurance identifies what must be reconsidered.

The profile does **not** determine quantum truth, certify hardware, validate QEC performance, reproduce a government evaluation process, or replace qualified scientific and engineering judgment.

## Five-minute evaluation

From the repository root:

```bash
python scripts/evaluate_ftqc_reference.py .
```

Expected final line:

```text
RESULT - FTQC REFERENCE EVALUATION PASS
```

The evaluation deliberately separates:

```text
SOFTWARE / CONTRACT VALIDATION
PASS

TECHNICAL DECISION READINESS
HOLD
```

A passing software check means the declared synthetic contracts behaved as specified. It does not mean the synthetic quantum architecture is validated.

The reference case contains a baseline and a changed-assumption scenario. The changed case modifies one physical-model assumption and demonstrates which resource estimate, evidence envelope, expert review, claims, and decision must be reconsidered.

## Use one governed private case

The bundled reference teaches profile behavior. For an access-controlled real evaluation, use the private-case validator rather than modifying the synthetic fixture in place:

```bash
python scripts/validate_ftqc_case.py ../my-ftqc-case \
  --report ../my-ftqc-case/decision-basis.md
```

Start with one decision and the six-file case shape documented in [`docs/PRIVATE_CASE_QUICKSTART.md`](docs/PRIVATE_CASE_QUICKSTART.md). Real evidence stays in its authoritative system; the private case carries only the bounded references and decision context required for review.

When you have a previous and current governed case state, `scripts/compare_ftqc_cases.py` surfaces stale estimates, evidence outside its envelope, expert-review reopen triggers, downstream impact, and decision reconsideration without manufacturing the replacement technical answer.

## Decision-basis continuity

The product question is not only:

> Why did we make this decision?

It is also:

> **Which assumptions and evidence keep the decision defensible, and what change would reopen it?**

That creates a change-sensitive decision basis rather than a static review package.

## Workload-to-System Assurance Chain

The profile-wide chain is architecture-neutral:

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

The synthetic neutral-atom reference is an **Algorithm-to-Atom view** of this more general chain. Other FTQC modalities can map into the same profile without changing the FMA core ontology.

## Profile contracts

Profile contract `0.2` uses four bounded contracts:

- **FTQC System Concept** — freezes the architecture revision, mission question, workload, and declared assumptions under review.
- **Resource Estimate Receipt** — records the meaning, assumptions, result, and applicability of a resource-estimation output without replacing computational provenance.
- **Evidence Validity Envelope** — records where evidence applies, what establishes that applicability, and whether it is decision-gating.
- **Expert Adjudication Record** — records the scope, class, evidence, uncertainties, exclusions, and reopen triggers of qualified domain judgment.

See [`PROFILE_CONTRACT.md`](PROFILE_CONTRACT.md) and [`ASSURANCE_SCOPE.md`](ASSURANCE_SCOPE.md).

## Verification-readiness baseline

[`docs/FTQC_EVIDENCE_MISSION_RISK_BASELINE.md`](docs/FTQC_EVIDENCE_MISSION_RISK_BASELINE.md) defines the smallest bounded engagement pattern for connecting one consequential FTQC decision to its critical claims, assumptions, evidence, dependencies, expert gates, risk-retirement actions, and explicit reopen conditions.

The intended outcome is **verification readiness**, not certification or a favorable technical verdict.

## Public reference boundary

The public profile contains only source-neutral contracts, documentation, validation logic, and synthetic reference data. Real customer, partner, supplier, architecture, experiment, program, or controlled evidence belongs in governed systems outside this public repository.

The operating doctrine is:

> **Reference the evidence. Do not relocate the evidence.**

See [`docs/PRIVATE_WORKSPACE_PATTERN.md`](docs/PRIVATE_WORKSPACE_PATTERN.md).

## QBI crosswalk

[`docs/QBI_PUBLIC_CROSSWALK.md`](docs/QBI_PUBLIC_CROSSWALK.md) is a bounded public-source crosswalk for learning and interoperability. It is not a QBI implementation, readiness determination, or representation of any internal evaluation process.

[`docs/QBI_IVV_FIT_REVIEW.md`](docs/QBI_IVV_FIT_REVIEW.md) records the current public-source fit assessment: BN7 can credibly contribute verification-readiness and evidence-to-decision infrastructure, while deep quantum adjudication, test infrastructure, evaluator eligibility, and independence determinations remain governed by qualified experts and the applicable process.

## Adoption

Start with one consequential decision, not an enterprise rollout. See [`docs/ADOPTION_PATH.md`](docs/ADOPTION_PATH.md).

Before accepting work that could later intersect with an independent-review role, apply the repository-level [`../../docs/INDEPENDENCE_AND_CONFLICT_POLICY.md`](../../docs/INDEPENDENCE_AND_CONFLICT_POLICY.md).
