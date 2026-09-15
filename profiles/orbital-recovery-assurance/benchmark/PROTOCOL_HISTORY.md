# Benchmark Protocol History

## Protocol 1.0 — INVALIDATED BEFORE ACCEPTANCE

The first synthetic benchmark protocol incorrectly required the bounded policy to have lower mean decision regret than a gate-only base-rate baseline even when that baseline selected actions outside the true-state safety envelope.

That comparison violated the profile's non-compensatory assurance doctrine: an unsafe baseline is not an admissible decision policy, regardless of its compensated utility/regret score.

Protocol 1.0 and its deterministic result are preserved as failed-method evidence. They are not used to support a PASS claim.

## Protocol 1.1 — CURRENT

Protocol 1.1 uses lexicographic acceptance:

1. the bounded policy must have zero unsafe-action rate under the declared synthetic generator;
2. decision regret is compared only against baselines that do not intentionally bypass the robust-action safety constraint;
3. the gate-only base-rate ranker is reported as a contrast baseline, including its unsafe-action rate, but cannot defeat a safe policy merely by taking unsafe actions;
4. state-conditioned success forecasts must outperform the preregistered fixed base-rate forecast on Brier score and log loss.

This change is a methodology correction, not a reinterpretation of a failed acceptance result.

## Protocol 1.1 — INVALIDATED FOR CALIBRATION-GENERATOR COHERENCE

Protocol 1.1 fixed the non-compensatory safety comparison, but adding a calibration diagnostic exposed a deeper issue: the generator selected a latent truth first and then constructed a noisy posterior around that truth. Those numbers are useful uncertainty scores, but they are not guaranteed to be calibrated posterior probabilities.

Because the benchmark explicitly evaluates probabilistic forecast quality, the generator must make the posterior semantics coherent. Protocol 1.2 therefore generates the posterior first and samples the latent truth from that posterior. This is the current protocol.
