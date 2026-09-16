# Mission Case Protocol

This protocol applies Orbital Recovery Assurance to a governed mission case while preserving source-of-record ownership, operational authority, and data-handling controls.

## 1. Declare the decision scope

Record within the governed mission workspace:

- required mission capability;
- current operating or recovery question;
- accountable human decision authority;
- consequence level;
- local evidence-admissibility policy;
- explicit stop and HOLD conditions.

Legal authority and evidence-sufficiency rules come from the governing mission process.

## 2. Preserve source-of-record ownership

Use local identifiers and references to mission evidence. Telemetry, identities, command records, source mappings, economics, credentials, and protected program information remain in the systems authorized to hold them.

The public profile provides the assurance method. The governed mission environment remains the evidence source of record.

## 3. Map the Mission Recovery Chain

For each essential mission capability, build the local projection:

`Power → Contact → Telemetry → Command → Capability`

Add trust and authority overlays. Record alternate paths, bypasses, and replacement options. The chain is a portable view over governed evidence and dependency records.

## 4. Assess independent recovery paths

Distinguish raw asset count from functionally capable recovery diversity. Identify material shared roots such as identity, timing, software/update infrastructure, ground capacity, cloud, communications, suppliers, authority, or configuration dependencies.

Treat statistical independence as an evidence question rather than an assumption derived from structural separation alone.

## 5. Classify and validate evidence

Keep evidence classes distinct:

- observed;
- calculated;
- inferred;
- simulated;
- reported.

Apply the Epistemic Firewall: analysis can generate hypotheses and next tests; evidence-state promotion requires admissible evidence under the declared local policy.

For each material item, record provenance and its validity envelope: configuration/version, environment, intended use, review time, and invalidation triggers where available.

## 6. Identify the binding constraint

Determine which current chain stage, trust condition, authority condition, or shared dependency prevents restoration of the required capability.

Recovery planning follows the binding constraint rather than a favored intervention.

## 7. Define recovery options and gates

For each option, declare within the governed mission workspace:

- modeled hypothesis/state set and provenance;
- posterior or uncertainty representation and producer;
- credible-coverage policy used by the robust envelope;
- modeled success basis;
- safety predicate across credible states;
- option-specific trust, authority, safety, and evidence gates;
- one declared utility space with terms reviewed for overlap and double counting;
- post-intervention requalification obligations.

Posterior construction, safety predicates, mission-specific success calibration, and the credible hypothesis set are governed local inputs. They should be reviewable evidence in their own right.

Optimization supports comparison. Accountable authority decides. For each option, preserve the exact blocking basis: unsafe credible hypotheses, unsatisfied gates, evidence gaps, or combinations of those conditions. Keep the HOLD utility baseline explicit so eligibility remains distinct from a decision to act.

## 8. Acquire decision-relevant evidence

Use observation-value analysis inside the admissible policy. A measurement is valuable when it can improve the governed decision basis after safety and gate constraints are applied.

When no observation has positive decision value, preserve the current state rather than manufacture a measurement objective.

## 9. Prepare the decision-review package

Use [`RECOVERY_ASSURANCE_PACKAGE.md`](RECOVERY_ASSURANCE_PACKAGE.md) to summarize:

- current Mission Recovery Chain;
- evidence and provenance state;
- unresolved contradictions and unknowns;
- robust options;
- gate eligibility;
- next-best evidence;
- expected requalification obligations;
- reopen conditions.

The package provides the assurance basis for the governing decision process.

## 10. Execute under mission authority

Observation, commanding, servicing, recovery, or retirement actions follow the operator's established technical, legal, safety, security, and mission-authority processes.

Orbital Recovery Assurance feeds that process with evidence, verification, and decision-preparation artifacts.

## 11. Requalify the changed system

After intervention, treat the resulting configuration as changed. Verify the intended capability against declared requirements, configuration, interfaces, and dependencies before accepting the new mission state.

Intervention success and mission requalification are separate evidence states.

## 12. Measure recovery and trust separately

Record applicable timeline events and compute:

- TTC — Time to Contain;
- TTE — Time to Establish Evidence;
- TTMC — Time to Minimum Credible Capability;
- TTT — Time to Trust;
- TTV — Time to Verify Recovery.

The difference between technical restoration and trusted restoration exposes process bottlenecks that ordinary repair metrics can miss.

## 13. Reassess on material change

Reopen the assessment when configuration, software, evidence validity, authority, mission requirements, interface state, dependency state, or post-intervention results materially change.

## 14. Promote learning through governed comparison

Generalize lessons across comparable cases only when the evidence supports the transfer. Preserve contrary evidence, configuration dependence, and validity limits so local results remain correctly scoped.

## Outcome indicators

The method is creating value when a mission team can demonstrate one or more of the following:

- a material evidence gap was discovered before consequential action;
- a shared dependency invalidated an assumed recovery path;
- new evidence changed option eligibility;
- HOLD prevented unsupported escalation;
- requalification prevented premature restoration claims;
- Time-to-Trust exposed a recovery bottleneck not visible in ordinary repair metrics;
- the assessment was completed without moving mission-sensitive evidence into the public repository.

## Local case validation

Use `record_class: private` for records retained in the governed mission workspace. From a matching FMA source checkout or verified source archive:

```bash
python scripts/validate_orbital_recovery_case.py /path/to/private-case
```

The validator checks the declared schemas and cross-record references for the files present in the case directory. It runs locally without network calls. Mission truth, evidence authenticity, calibration, authority, ownership, safety, and operational approval remain governed inputs.

Use `--require-stage mapped|assessed|post-intervention|requalification-review` when the workflow requires a minimum artifact stage. Each stage proves only the artifacts required at that point in the lifecycle.

## Logging policy

The local validator may echo file names and unresolved local identifiers when reporting failures. Keep validation output inside the same governed boundary as the case evidence, and run mission cases outside public CI and public repository workspaces.
