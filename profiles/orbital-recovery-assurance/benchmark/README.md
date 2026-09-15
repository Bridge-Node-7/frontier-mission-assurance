# Synthetic Known-Truth Benchmark

This benchmark tests the bounded recovery-assessment policy under a declared synthetic generator with hidden latent truth.

## Current protocol

`protocol.json` is protocol 1.3. It generates a posterior first and samples the latent truth from that posterior so the probability semantics are coherent inside the synthetic experiment. The policy receives the posterior and declared gate state; it does not receive the sampled truth.

The generator uses only the stable `random()` stream plus explicit deterministic transforms and cumulative truth sampling rather than distribution helper algorithms whose exact sequences are not a portable release contract. Discrete case generation, choices, acceptance flags, and safety counts are expected to reproduce exactly. Aggregate floating-point metrics are compared to the checked-in snapshots with a `1e-12` absolute/relative tolerance because interpreter versions may legitimately differ in the final bits of floating reductions.

The deterministic primary run uses 5,000 cases. A separate stress matrix perturbs the random seed and the stable/uncertain case mix.

## Metrics

- unsafe-action rate;
- mean decision regret against a synthetic oracle constrained by true-state safety and gate state;
- Brier score for the state-conditioned augmentation-success forecast;
- log loss for the same forecast;
- 10-bin expected calibration error as a diagnostic only.

The fixed safe baselines are:

- always hold;
- controlled retirement whenever its declared gates are clear.

A gate-only fixed-base-rate ranker is retained as a contrast baseline. It intentionally omits the robust-action safety filter, so its regret is not treated as compensating for an unsafe-action violation.

## Protocol history

Earlier benchmark protocols are preserved as invalidated-method evidence. Their results do not support the current PASS claim. See `PROTOCOL_HISTORY.md`.

## Claim boundary

A PASS demonstrates only behavior under the declared synthetic generator. It does not establish real-world calibration, operational safety, recoverability, demand, mission readiness, or external validation.
