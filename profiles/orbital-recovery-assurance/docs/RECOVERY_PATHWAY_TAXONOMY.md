# Recovery Pathway Taxonomy

This document provides a **non-canonical, source-neutral classification aid** for the Orbital Recovery Assurance profile. It helps structure synthetic assessments without turning Frontier Mission Assurance into a spacecraft ontology.

## 1. Target responsiveness

A degraded orbital asset is not simply "alive" or "dead." A useful assessment distinguishes at least:

- `RESPONSIVE` — command/telemetry paths are available within the declared trust boundary.
- `INTERMITTENT` — evidence of activity exists, but availability or commandability is incomplete or unstable.
- `NONRESPONSIVE` — no supported command/telemetry path is currently established.
- `UNKNOWN` — available evidence is insufficient to classify responsiveness.

Responsiveness is not the same as recoverability. A nonresponsive asset may still retain valuable structure, aperture, mass, power-generation surfaces, or other residual capability.

## 2. Physical-control state

Keep physical dynamics separate from communications state:

- `CONTROLLED`
- `DEGRADED_CONTROL`
- `UNCONTROLLED_OR_TUMBLING`
- `UNKNOWN`

This distinction matters because an intervention that is acceptable for a controlled host may be outside the robust action envelope for an uncontrolled target.

## 3. Interface preparedness

The profile distinguishes whether a recovery pathway relies on interfaces deliberately designed for future servicing:

- `PREPARED` — a declared compatible servicing interface exists.
- `PARTIALLY_PREPARED` — a usable structural or functional interface may exist but was not designed for the intended intervention.
- `UNPREPARED` — intervention depends on characterization or adaptation to legacy geometry/interfaces.
- `UNKNOWN` — interface suitability is not established.

Preparedness affects evidence burden; it does not itself establish safety or permission.

## 4. Recovery capability layers

A recovery concept can be decomposed into three generic layers:

1. **Observe** — detect, characterize, localize, estimate state, and reduce uncertainty.
2. **Contact** — establish a mechanically and dynamically acceptable physical relationship when physical intervention is required.
3. **Interface** — exchange force, power, data, fluid, thermal capacity, payload function, or another mission-relevant resource.

An intervention does not need all three layers. Observation-only recovery analysis may never progress to physical contact.

## 5. Recovery pathways

The profile can assess pathways such as:

- `OBSERVE_ONLY` — acquire evidence without changing the asset.
- `REMOTE_RECOVERY` — attempt restoration through an already-supported remote command/control path.
- `EXTERNAL_AUGMENTATION` — add independent capability rather than requiring restoration of every original subsystem.
- `COMPONENT_OR_RESOURCE_REUSE` — recover bounded residual value from surviving structure or subsystems for a new configuration.
- `CONTROLLED_RETIREMENT` — place the system into a bounded end state when useful recovery is not justified.
- `NO_CONSEQUENTIAL_ACTION_YET` — preserve optionality while acquiring evidence.

These labels are assessment aids, not universal industry categories and not instructions for live operations.

## 6. Assurance principle

The key question is not whether a pathway is technically imaginable. It is whether the declared evidence supports enough physical state, trust, authority, interface compatibility, and post-intervention mission fitness for that pathway to enter accountable decision preparation.
