# Validation

Orbital Recovery Assurance is verified in layers so structural integrity, arithmetic behavior, cross-record consistency, benchmark behavior, and release portability can be evaluated independently.

## Structural and arithmetic controls

The profile validator checks schemas, reference record classes, evidence references, provenance-correlation behavior, executable fixture binding, option-assessment consistency, requalification evidence resolution, timeline metrics, benchmark regeneration, stress-matrix regeneration, and the source-neutral public release policy.

The unit suite exercises fail-closed gates, robust-option coverage, observation value over admissible options, finite/probability hardening, provenance correlation, evidence reference resolution, event-derived Time-to-Trust metrics, and the synthetic benchmark acceptance contract.

## Synthetic known-truth benchmark

The current protocol generates a posterior first, samples the hidden latent truth from that posterior, and evaluates the reference policy on 5,000 deterministic pseudo-random cases. Decision regret is compared against safety-respecting baselines. A gate-only base-rate ranker is reported separately as a contrast baseline because it can violate the robust-option safety envelope.

The benchmark also reports Brier score, log loss, and a calibration diagnostic for the synthetic augmentation-success forecast. These metrics characterize the declared synthetic generator and policy.

A stress matrix reruns the same acceptance contract across multiple seeds and stable/uncertain case mixes.

## Verification scope

A PASS confirms that the declared software, schemas, fixtures, benchmark protocol, and cross-record invariants behaved as specified under the tested conditions.

Mission recoverability, operational safety, authority, mission-specific probability calibration, and approval to act remain tied to the governed evidence and approval processes for the actual system.
