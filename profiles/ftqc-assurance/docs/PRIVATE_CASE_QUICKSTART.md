# Private FTQC Case Quickstart

Use this path when you want to evaluate one real FTQC decision in a governed private workspace.

The public repository remains source-neutral. Do **not** place customer, partner, supplier, laboratory, architecture, schedule, credential, controlled, or otherwise protected evidence in the public repository or a public fork.

The operating rule is:

> **Reference the evidence. Do not relocate the evidence.**

## What this gives you

A private FTQC case connects one consequential decision to:

- the system concept and architecture revision under review;
- the workload and controlling assumptions;
- one decision-relevant resource estimate;
- evidence-validity envelopes;
- qualified expert-review gates;
- an FMA assurance graph;
- the current human disposition and explicit reopen conditions.

The validator checks the declared contracts and their cross-record references. It does not establish quantum truth, QEC or decoder correctness, resource-estimator correctness, hardware performance, independent V&V, government readiness, or decision authority.

## 1. Start from the source-neutral shape

Create a private working directory **outside this public repository**. The bundled synthetic baseline shows the required file shape:

```text
system-concept.json
resource-estimate-receipt.json
evidence-envelopes.json
expert-adjudications.json
assurance-graph.yaml
decision-receipt.yaml
```

For evaluation, you can copy the bundled baseline into an access-controlled workspace:

```bash
cp -R profiles/ftqc-assurance/examples/synthetic-neutral-atom/baseline ../my-ftqc-case
```

On Windows PowerShell:

```powershell
Copy-Item -Recurse .\profiles\ftqc-assurance\examples\synthetic-neutral-atom\baseline ..\my-ftqc-case
```

The copied files are still synthetic reference data. They are only a structural starting point.

## 2. Convert the case to governed private records

Before treating the workspace as a real case:

1. change each FTQC profile record from `record_class: synthetic` to `record_class: private`;
2. change `assurance-graph.yaml -> metadata.record_class` to `private`;
3. replace all synthetic identifiers, titles, assumptions, evidence references, estimator identity, result values, expert questions, and decision rationale with governed case values;
4. for a real resource estimate, set `result.synthetic_only` to `false`;
5. keep raw evidence in its authoritative system and use only governed references in the case;
6. keep the decision on `HOLD` or `REVISE` while mandatory applicability or expert-review gates remain unresolved.

The validator can confirm contract consistency. It cannot prove that every placeholder or synthetic value was replaced correctly; accountable review remains required.

## 3. Validate the case

From the FMA source root:

```bash
python scripts/validate_ftqc_case.py ../my-ftqc-case
```

A passing private case ends with:

```text
FTQC CASE PASS
PROFILE: 0.2
RECORD CLASS: private
...
```

A PASS means the declared profile records, graph, decision receipt, references, and bounded gates are structurally coherent. It does not mean the technical conclusion is correct.

## 4. Render the decision basis

```bash
python scripts/validate_ftqc_case.py ../my-ftqc-case \
  --report ../my-ftqc-case/decision-basis.md
```

The report surfaces:

- current human disposition;
- mission objective and architecture revision;
- resource-estimate state and provenance;
- assumptions;
- evidence applicability and authority state;
- expert-review gates;
- explicit reopen conditions;
- unresolved decision gates.

The report is a review surface, not a substitute for the authoritative evidence systems it references.

## 5. Compare two governed states

When the decision basis changes, keep the previous governed case state and produce a current case state. Then compare them:

```bash
python scripts/compare_ftqc_cases.py \
  ../my-ftqc-case-previous \
  ../my-ftqc-case-current \
  --report ../my-ftqc-case-current/change-impact.md
```

The comparison surfaces declared:

- changed assumptions and context;
- reused resource estimates that are now stale;
- evidence that falls outside its current applicability envelope;
- expert reviews whose declared reopen triggers were crossed;
- downstream graph impact;
- whether the declared decision node is impacted.

The comparison does not modify either case and does not infer the replacement quantum-engineering answer.

You can still use the core graph tool for a direct dependency query:

```bash
fma impact ../my-ftqc-case-current/assurance-graph.yaml <CHANGED-NODE-ID>
```

The operational question is:

> **What became stale, what fell outside its evidence envelope, what expert judgment must reopen, and which decision basis now deserves reconsideration?**

## Suggested first case

Choose one decision that can materially delay, redirect, or de-risk the program. Keep the first case small:

```text
1 decision
1 architecture revision
1 workload
1 decision-relevant resource estimate
1–3 controlling claims
only the critical assumptions
only the evidence references that matter
1–2 expert gates
explicit reopen conditions
```

If the case becomes large before it is useful, reduce it.

## Operational-use boundary

The public repository is available for evaluation and review under its license posture. Internal operational use, private deployment, integration, modification, or other rights not granted by the public release require the applicable written permission or agreement from Bridge Node 7. See the repository-level `docs/USE_AND_EVALUATION.md`.
