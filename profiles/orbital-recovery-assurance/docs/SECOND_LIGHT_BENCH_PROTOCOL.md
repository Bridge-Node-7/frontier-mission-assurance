# SECOND LIGHT Bench Protocol

**Status:** bounded research protocol / synthetic-and-bench guidance only.

SECOND LIGHT explores whether a legacy reflector or other passive RF aperture could support a new mission use through external characterization, independently supplied feed/receiver-transmitter hardware, controlled positioning, and closed-loop RF calibration.

It is **not** an operational spacecraft procedure, a claim of novelty, a flight-qualification plan, or evidence that a particular asset is recoverable.

## Governing rule

Acceptance must flow:

`Mission requirement → link budget → antenna/RF requirements → measured configuration → requalification`

Do not begin with an arbitrary fraction of theoretical antenna gain and declare success from that number alone.

## Gate 0 — Intended mission use

Declare the bounded service to be supported and the required RF performance envelope. Depending on transmit/receive role, this may include:

- required realized gain or `G/T`;
- required `EIRP` or receive sensitivity contribution;
- frequency/bandwidth;
- pointing tolerance;
- cross-polarization limit;
- sidelobe constraints;
- stability over time/temperature;
- allowable calibration overhead.

If the mission-level requirement is unknown, the bench cannot establish mission fitness.

## Gate 1 — Geometry and structural observability

Establish whether the aperture geometry can be measured with sufficient fidelity to support an RF model.

Record:

- observable aperture region;
- missing/occluded regions;
- gross deformation;
- local surface-error estimate where measurable;
- reference coordinate frame;
- repeatability of the geometry solution.

A geometry model is evidence, not truth; uncertainty should propagate into later RF predictions.

## Gate 2 — Passive RF characterization

Characterize the aperture/feed system without adaptive compensation first.

Measure or estimate, as applicable:

- boresight response;
- beam shape;
- pointing offset;
- bandwidth behavior;
- polarization behavior;
- repeatability and drift.

Where a random small-scale surface-error approximation is justified, a Ruze-type screen may be used as a first-order loss estimate:

`η_surface ≈ exp[-(4πσ/λ)^2]`

This is a screening relationship, not a universal acceptance test. Large-scale or spatially correlated deformation requires a more appropriate physical-optics or measured-field treatment.

## Gate 3 — External feed viability

Demonstrate that an independently supplied feed or feed array can be positioned within the required capture volume and controlled repeatably.

Record:

- feed location/orientation uncertainty;
- positioning repeatability;
- thermal/mechanical drift;
- power and data independence assumptions;
- safe operating bounds for the bench article.

## Gate 4 — Closed-loop calibration

Use measured RF response, not geometry alone, to adjust allowed feed parameters.

The closed loop may compensate for effects such as:

- feed displacement;
- pointing bias;
- illumination error;
- some low-order reflector deformation.

It should **not** claim recovery of arbitrary high-spatial-frequency damage or missing aperture area.

The optimization target must be derived from the mission-level RF requirements rather than an unconstrained maximum-gain objective.

## Gate 5 — Requalification

After calibration, evaluate the resulting configuration against the declared mission requirements.

A successful bench result should record:

- configuration identity;
- measurement conditions;
- measured RF metrics;
- uncertainty;
- requirement-by-requirement disposition;
- unresolved evidence gaps;
- conditions that would require retest.

The output is a bounded requalification evidence package, not a flight authorization.

## Failure is useful evidence

A negative result is valuable if it establishes why the aperture cannot support the intended mission envelope, which assumptions failed, and what evidence would change that conclusion. The protocol therefore treats `HOLD`, `NOT_SUPPORTED`, and `RETIRE_PATHWAY` outcomes as valid results rather than forcing a recovery narrative.
