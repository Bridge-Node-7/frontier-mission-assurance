# Bottleneck Shift Reference — FTQC research experiment

**STATUS: EXPERIMENTAL / SYNTHETIC ONLY — NO QUANTUM COMPUTING PERFORMANCE CLAIM**  
**Case:** `SYN-FTQC-BOTTLENECK-SHIFT-001`  
**Evidence owner:** external researchers retain authority over their work; this folder contains no imported ORNL code or user/customer data.

## Why this exists

A quantum optimization can make a local metric much better without improving the **whole workload**. It may move the dominant time contribution to state preparation, conversion, readout, hardware control, or another dependency. This narrowly bounded experiment makes that *constraint migration* visible before treating a gate-count reduction as a mission result.

It follows the June 2026 Materials-to-Mission capstone principle: **fund the verified lifecycle bottleneck, not the technology label**. It also follows the [FTQC Assurance workload-to-system chain](../../README.md), the [resource-estimate assurance boundary](../../docs/RESOURCE_ESTIMATE_ASSURANCE.md), and the repository [research reproducibility contract](../../../../docs/RESEARCH_REPRODUCIBILITY_CONTRACT.md).

**External inspiration, not experimental input or endorsement:**

- ORNL, *Breaking a quantum computing bottleneck*, October 12, 2026 (official ORNL news article; source locator maintained in authorized research records).
- Chao Lu et al., *LuGo: An enhanced quantum phase estimation implementation*, *Future Generation Computer Systems*, vol. 178 (2026), DOI `10.1016/j.future.2025.108270`; preprint `arXiv:2503.15439v2`.
- ORNL paper Table 1 reports a 64×64 Toeplitz case with **2,876,007** conventional gates versus **91,054** LuGo gates and circuit-generation times **1,908.18 s** versus **37.65 s**. Those are author-reported results and **not values or observations produced by this experiment**. No claim is made here about actual quantum advantage, reproduced LuGo implementation, real hardware performance, licensing, or a customer's platform.

## Minimal reproducible run

Requires Python 3.11+ and only its standard library. From this folder:

```bash
python analyze.py case.json --output result.json
python -m unittest -v test_analyze.py
```

From repository root (including in the existing `pytest` CI):

```bash
python -m pytest -q tests/test_ftqc_bottleneck_shift_reference.py
```

Expected illustrative result:

| Input scenario | Baseline total | Circuit restructure | Hybrid restructure | Dominant baseline stage |
| --- | ---: | ---: | ---: | --- |
| Nominal synthetic | 1,400 | 540 | 510 | Circuit generation |
| Preparation-cost stress synthetic | 1,500 | 1,190 | 710 | Circuit generation |

All values are **unitless synthetic latency units**, not seconds, gates, quantum runtimes, or measurements. The target of ≥1.5× speedup across both scenarios is a synthetic illustrative rule established in `case.json`. The simple circuit restructure **fails** that target under preparation-cost stress (worst-case ~1.26×), even though it improves the nominal case (~2.59×). The synthetic hybrid meets it (worst-case ~2.11×). In both cases the dominant modeled stage shifts to preparation. **No option is qualified or recommended for use.**

## What the code actually does

`analyze.py` accepts a single explicitly labeled SYNTHETIC case and four declared **sequential** time-contribution stages: preparation, circuit generation, quantum execution, readout. It computes the sum and the largest modeled contributor for each option and scenario, compares with the same-scenario baseline, and displays whether the declared numerical ratio target holds across every scenario. It retains a list of unresolved scientific and mission gates and always outputs `HOLD_PENDING_REAL_WORKLOAD_AND_EXPERT_REVIEW`.

This is **not** a quantum algorithm, quantum simulator, quantum compiler, project scheduling engine, reliable physical cost model, quantum resource estimator, new FTQC profile/contract, or an autonomous decision maker. Dominant time contribution in a sequential sum is **not proof of causal or binding bottleneck** in a real system. Sequential summation ignores concurrency, shared-failure correlations, queueing, fidelity, error-correction overhead, statistical uncertainty, and the full effects of architecture changes. Numeric ratios are not a substitute for workload-equivalent, error-matched comparisons against competitive classical and quantum alternatives.

The input parser rejects unlabelled/non-synthetic cases, unknown stages, missing alternatives, negative/nonfinite durations, zero totals, duplicate scenario IDs, missing proof gates, and undeclared schema fields. It does not access network resources, write outside the explicitly requested output location, ingest secrets, or call external systems.

## Next evidence, not automatic escalation

To turn this illustration into a legitimate mission decision:

1. Define one authorized mission, actual workload, numerical accuracy target, constrained architecture, and accountable reviewer.
2. Pin primary paper and authorized code/data/revision; inspect external code and rights **before** execution in an appropriate environment.
3. Measure end-to-end workload-equivalent alternatives (including a strong classical baseline), with a declared environment, units, uncertainty and reproducible research receipt.
4. Compare the observed bottleneck and counterexamples across plausible scenarios. Re-open the decision when the workload, estimator, hardware basis, compilation target, physical model, or evidence validity changes.
5. Use existing FTQC Assurance Resource Estimate Receipts and expert adjudication for relevant actual estimates; use the FMA graph to preserve dependencies and decision continuity. Do not put customer, protected, or unpublished evidence into this public fixture.

No scheduled scraping, monitoring, customer contact, provider integration, new top-level product or public performance claim is created here. Later experiments should be opened only in response to an actual evidence gap or authorized mission question.
