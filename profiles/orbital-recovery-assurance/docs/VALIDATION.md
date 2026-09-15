# Validation

Orbital Recovery Assurance is validated in layers.

## Structural and arithmetic controls

The profile validator checks schemas, synthetic record classes, evidence references, provenance-correlation behavior, executable fixture binding, option-assessment consistency, requalification evidence resolution, timeline metrics, benchmark regeneration, stress-matrix regeneration, and the source-neutral profile boundary.

The unit suite exercises fail-closed gates, robust-action coverage, observation value over admissible options, finite/probability hardening, provenance correlation, evidence reference resolution, event-derived Time-to-Trust metrics, and the synthetic benchmark acceptance contract.

## Synthetic known-truth benchmark

The current protocol generates a posterior first, samples the hidden latent truth from that posterior, and evaluates the bounded policy on 5,000 deterministic pseudo-random cases. It compares decision regret only against safety-respecting baselines. A gate-only base-rate ranker is reported separately as a contrast baseline because it can violate the robust-action safety envelope.

The benchmark also reports Brier score, log loss, and a calibration diagnostic for the synthetic augmentation-success forecast. The benchmark does not establish real-world probability calibration.

A stress matrix reruns the same acceptance contract across multiple seeds and stable/uncertain case mixes.

## PASS meaning

A PASS proves only that the declared software, schemas, fixtures, benchmark protocol, and bounded cross-record invariants behaved as specified. It does not prove a real asset is recoverable, that an intervention is safe, that authority exists, that any operation should occur, or that the synthetic probabilities transfer to the real world.
