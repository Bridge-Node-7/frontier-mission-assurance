# Recovery Assurance Package

This is a bounded human-review template for presenting the basis of an orbital recovery
assessment. It is not an authorization, certification, ownership record, or operational
command.

## 1. Assessment identity

- Assessment ID:
- Configuration ID:
- As-of time:
- Intended capability:
- Accountable review owner:
- Handling boundary:

## 2. Mission outcome

State the capability that matters and the minimum useful service level to be restored,
requalified, repurposed, or retired.

## 3. Mission Recovery Chain

For each essential mission capability, summarize the current recovery projection:

`Power → Contact → Telemetry → Command → Capability`

For every stage record:

- current state;
- evidence references;
- recovery/bypass options;
- current blocking condition if any.

Record trust and authority as overlays across the chain rather than serial stages.
State the currently binding constraint or candidate constraints without implying that a
view is itself a source of truth. Count independent recovery paths, not raw assets.

## 4. Current state

### Physical
Summarize supported, degraded, failed, contested, or unknown physical capability.

### Trust
Summarize telemetry, command-path, software, identity, and data-integrity trust state.

### Authority
Summarize whether the relevant authority is verified, declared, disputed, unknown, or
otherwise bounded by the local governance model.

## 5. Evidence basis

For each material claim record:

- evidence reference;
- evidence class;
- provenance roots;
- validity envelope;
- as-of time;
- unresolved contradiction;
- applicability to the current configuration.

Do not count correlated evidence as independent merely because it appears in multiple
documents.

## 6. Recovery pathways considered

For each pathway:

- pathway ID;
- objective;
- required evidence;
- credible-state safety predicate;
- option-specific gates;
- intervention-success model;
- utility space;
- HOLD utility baseline;
- per-option unsafe hypotheses, required gates, gate failures, eligibility, and utility advantage relative to HOLD;
- unresolved assumptions.

## 7. Robust-action result

Record which pathways remain acceptable across the declared credible state set and which
are excluded.

A robust-action result is not an authorization.

## 8. Decision-relevant evidence

Record any positive-value next observation:

- observation ID;
- cost/risk basis;
- possible outcomes;
- expected change to admissible options;
- net expected value of information.

If no observation has positive expected value, say so explicitly.

## 9. Eligibility for decision preparation

For each pathway state:

- robust / not robust;
- gate clear / gate blocked;
- evidence gaps;
- reason for HOLD where applicable.

Machine output may make an option eligible for downstream decision preparation. It does
not select or authorize the option.

## 10. Human decision reference

If a consequential decision is made, reference the downstream governed decision record.
Do not silently convert this package into the decision authority.

## 11. Post-intervention requalification

For the resulting configuration record:

- new configuration identity;
- intended capability;
- requirements;
- evidence supporting each requirement;
- unresolved requirement;
- operating envelope;
- requalification disposition.

A technically successful intervention is not the same as a requalified mission
capability.

## 12. Recovery timeline

Where available, record:

- time to containment;
- time to evidence;
- time to minimum credible capability;
- time to trust;
- time to verification.

These are descriptive measures derived from declared timeline events.

## 13. Reopen conditions

List the changes that invalidate or require reassessment of this package, including
configuration, evidence validity, authority, software, interface state, mission
requirement, or new contradictory evidence.

## 14. Non-claims

This package does not by itself establish:

- ownership;
- legal authority;
- operational authorization;
- flight safety;
- mission readiness;
- real-world probability calibration;
- certification;
- scientific truth.
