# Synthetic Known-Truth Benchmark

This benchmark evaluates the Orbital Recovery Assurance reference policy against hidden latent truth generated under a declared synthetic model.

## Current protocol

`protocol.json` is protocol 1.3. It generates a posterior first and samples the latent truth from that posterior so probability semantics remain coherent inside the experiment. The policy receives the posterior and declared gate state; the sampled truth remains hidden until scoring.

The generator uses the stable `random()` stream with explicit deterministic transforms and cumulative truth sampling. Discrete case generation, choices, acceptance flags, and safety counts reproduce exactly across supported environments. Aggregate floating-point metrics are compared to checked-in snapshots with a `1e-12` absolute/relative tolerance to accommodate legitimate final-bit differences in floating reductions.

The deterministic primary run uses 5,000 cases. A separate stress matrix varies the random seed and stable/uncertain case mix.

## Metrics

- unsafe-action rate;
- mean decision regret against a synthetic oracle constrained by true-state safety and gate state;
- Brier score for the state-conditioned augmentation-success forecast;
- log loss for the same forecast;
- 10-bin expected calibration error as a diagnostic.

The fixed safe baselines are:

- always hold;
- controlled retirement whenever its declared gates are clear.

A gate-only fixed-base-rate ranker is retained as a contrast baseline. Because it omits the robust-option safety filter, its regret is reported separately from the safety-respecting acceptance comparison.

## Protocol history

Earlier benchmark protocols are preserved as invalidated-method evidence with explicit reasons. The current PASS claim is tied only to protocol 1.3 and its checked-in acceptance contract. See [`PROTOCOL_HISTORY.md`](PROTOCOL_HISTORY.md).

## Verification scope

A PASS demonstrates the declared policy behavior under the synthetic generator, including the non-compensatory safety requirement and the stated forecasting diagnostics.

Operational calibration, mission recoverability, safety qualification, and mission readiness require evidence from the applicable mission context and remain separate from this synthetic benchmark.
