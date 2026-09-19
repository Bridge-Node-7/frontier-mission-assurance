# Adoption Path

Adopt FTQC Assurance around **one consequential technical decision**.

Do not begin with an enterprise-wide assurance rollout.

## Operator path

For a governed evaluation, first create the six-file case described in [`GOVERNED_CASE_QUICKSTART.md`](GOVERNED_CASE_QUICKSTART.md), then validate it with:

```bash
python scripts/validate_ftqc_case.py ../my-ftqc-case \
  --report ../my-ftqc-case/decision-basis.md
```

This is the supported profile-level path for a real private case. The public synthetic evaluator remains a reference test, not a substitute for the private-case validator.

## Step 1 — Name the decision

Write the exact decision and accountable human owner.

## Step 2 — Identify the critical claims

Select only the claims that materially control the decision.

## Step 3 — Reference existing evidence

Keep laboratory, code, model, test, document, and supplier systems authoritative. Add governed references rather than copying entire evidence stores.

## Step 4 — Bound applicability

Record where each decision-relevant evidence item applies and what establishes that applicability.

## Step 5 — Add expert gates

Identify questions that require QEC, physics, photonics, controls, metrology, systems, manufacturing, or other qualified judgment.

## Step 6 — Record reopen conditions

State which changed assumptions, evidence, interfaces, or reviews would force reconsideration.

## Step 7 — Test one change

Deliberately modify one synthetic or governed assumption and verify that the affected decision basis becomes visible.

## Success criterion

The profile is useful when it reduces the effort required to answer:

> **What does this decision depend on, and what changed enough that we should revisit it?**
