# Real Case Protocol

This protocol describes how to apply Orbital Recovery Assurance to a real mission case
without turning the public repository into a mission-data store or operational authority.

## 1. Declare the decision scope

Record privately:

- required mission capability;
- current operating/recovery question;
- accountable human decision authority;
- consequence level;
- local evidence-admissibility policy;
- explicit stop/hold conditions.

The profile does not supply legal authority or a universal evidence-sufficiency rule.

## 2. Keep real evidence under partner governance

Use local identifiers and references. Do not commit real telemetry, identities, command
records, source mappings, economics, credentials, or protected program information to the
public repository.

The public profile is the method. The partner's governed environment remains the evidence
source of record.

## 3. Map the Mission Recovery Chain

For each essential mission capability, build the local projection:

`Power → Contact → Telemetry → Command → Capability`

Add trust and authority overlays. Record alternate paths and bypass/replacement options.
The chain is a view; it does not replace the underlying evidence/dependency systems.

## 4. Count independent recovery paths

Do not count raw assets. Identify whether recovery alternatives share material roots such
as identity, timing, software/update, ground capacity, cloud, communications, supplier,
authority, or configuration dependencies.

Separate structural roots do not by themselves prove statistical independence.

## 5. Classify and validate evidence

Keep evidence classes distinct:

- observed;
- calculated;
- inferred;
- simulated;
- reported.

Apply the Epistemic Firewall. Analysis can propose hypotheses and tests, but cannot promote
itself into observed or verified evidence.

For each item, record provenance and its validity envelope: configuration/version,
environment, intended use, review time, and invalidation triggers where available.

## 6. Find the binding constraint

Ask which current chain stage, trust condition, authority condition, or shared dependency
actually prevents restoration of the required capability.

Do not begin with a favored solution. The response follows the bottleneck.

## 7. Define recovery options and gates

For each option, declare privately:

- modeled hypothesis/state set and the provenance of that model;
- posterior or uncertainty representation and who/what produced it;
- credible-coverage policy used by the robust envelope;
- modeled success basis;
- safety predicate across credible states;
- option-specific trust/authority/safety gates;
- one declared utility space with terms reviewed for overlap/double counting;
- post-intervention requalification obligations.

The public profile does **not** infer the real posterior, learn a safety predicate, calibrate real-world success probabilities, or decide which hypotheses are credible. Those are governed local inputs and should be reviewable evidence in their own right.

Optimization may rank. It does not authorize. For every option, preserve why it is blocked: unsafe credible hypotheses, unsatisfied gates, or both. Keep the HOLD utility baseline explicit so eligibility is never mistaken for a recommendation to act.

## 8. Acquire next-best evidence

Use observation-value analysis only within the admissible policy. A measurement is useful
when it can improve the human decision basis after safety and gate constraints—not merely
because it improves an option that remains inadmissible.

If no observation has positive decision value, preserve HOLD rather than inventing one.

## 9. Prepare the human review package

Use `RECOVERY_ASSURANCE_PACKAGE.md` to summarize:

- current chain view;
- evidence and provenance state;
- unresolved contradictions/unknowns;
- robust options;
- gate eligibility;
- next-best evidence;
- expected requalification obligations;
- reopen conditions.

The package is evidence for an accountable decision process, not a decision authorization.

## 10. Intervene only under external authority

Any real observation, commanding, servicing, or recovery action is governed by the
operator's own technical, legal, safety, security, and mission-authority processes.

Orbital Recovery Assurance stops at decision preparation.

## 11. Requalify the changed system

After intervention, treat the resulting configuration as changed. Verify the intended
capability against declared requirements and the new configuration/dependencies before
calling the mission capability trusted for resumed use.

A technical success is not automatically mission requalification.

## 12. Measure recovery and trust separately

Record applicable timeline events and compute:

- TTC — Time to Contain;
- TTE — Time to Establish Evidence;
- TTMC — Time to Minimum Credible Capability;
- TTT — Time to Trust;
- TTV — Time to Verify Recovery.

Use the difference between technical restoration and trustworthy restoration to identify
process bottlenecks.

## 13. Reassess on material change

Reopen the assessment when configuration, software, evidence validity, authority, mission
requirements, interface state, dependency state, or post-intervention results materially
change.

## 14. Promote learning cautiously

A single real case does not automatically become BN7 institutional truth. Generalize only
through governed comparison across multiple cases and preserve contrary evidence and
scope limits.

## Real-case success criteria

The method is creating value when a real team can demonstrate at least one of the following:

- a material evidence gap was discovered before consequential action;
- a shared dependency invalidated an assumed recovery path;
- new evidence changed option eligibility;
- HOLD prevented unsupported escalation;
- requalification prevented premature mission-restoration claims;
- Time-to-Trust identified a recoverability bottleneck not visible in ordinary MTTR;
- the entire assessment was performed without moving sensitive mission evidence into the
  public repository.

## Local case validation

Use `record_class: private` for real records retained in the partner-controlled workspace. From a matching FMA source checkout or verified source archive:

```bash
python scripts/validate_orbital_recovery_case.py /path/to/private-case
```

The validator checks declared schemas and cross-record references for the files present in the case directory. It is intentionally non-networked and does not make a real-world truth, safety, authorization, ownership, recoverability, or calibration claim. Missing lifecycle artifacts are allowed until that stage exists; when an artifact is present, its references must resolve.

Use `--require-stage mapped|assessed|post-intervention|requalification-review` when the workflow requires a minimum artifact stage. A structural PASS at an earlier stage is not a claim that later recovery or requalification work is complete.

## Logging boundary

The private-case validator may echo local file names and unresolved local identifiers when it reports failures. Do not run a private-case validation in public CI, paste its detailed output into public issues, or place the private workspace under the public repository checkout. Keep logs inside the same governed boundary as the case evidence.
