# External Research and Existing-Work Adoption

Frontier Mission Assurance should meet technical work where it already exists.

The default rule is:

> **Wrap the work. Do not reorganize the work around FMA.**

Keep the authoritative repository, paper, model, experiment, test system, laboratory record, or external execution environment unchanged unless its owner separately authorizes a change. Create a bounded FMA sidecar that identifies the exact source state, records what is claimed and assumed, references the evidence, and connects that basis to one consequential decision.

## Existing Git repository

Use this path when the important artifact already lives in source control.

```text
existing repository
        ↓
freeze exact revision
        ↓
identify the result or claim that matters
        ↓
create a separate FMA sidecar
        ↓
reference authoritative artifacts
        ↓
reproduce only where appropriate and trusted
        ↓
record assumptions and evidence gaps
        ↓
connect the basis to one decision
        ↓
define what would reopen that decision
```

The source repository remains authoritative. FMA does not require a new branch, new folder, changed build process, or copied source tree inside the original repository.

For a source-neutral worked sidecar, see [`../examples/external_research_adoption/`](../examples/external_research_adoption/).

## Research paper

A paper can enter FMA before every supporting artifact is available. The assurance state must stay proportional to the evidence actually present.

```text
PAPER ONLY
→ paper identity + claim + provenance + assumptions
→ no fresh-reproduction claim

PAPER + CODE
→ exact code revision + implementation relationship
→ reproduction may still be unestablished

PAPER + CODE + DATA
→ bounded reproduction candidate
→ environment and execution assumptions remain explicit

PAPER + CODE + DATA + ENVIRONMENT
→ stronger reproduction candidate
→ scientific validity and applicability still require separate judgment
```

A verified artifact identity does not establish the truth of the paper's scientific claim. A successful reproduction does not establish that the claim applies to a different system, scale, configuration, or decision.

Use Scientific Discovery Assurance when proof state, specification equivalence, replication, provenance, attribution, or machine-assisted discovery semantics matter.

### External reported resource estimates

When an external paper reports a resource estimate, preserve the estimate as external evidence unless a separate authorized process establishes a stronger assurance state. Under FTQC Assurance profile contract `0.1`, Resource Estimate Receipts remain synthetic/reference-only.

Do not convert a published number into a fresh-reproduction, independent-validation, or system-applicability claim merely by copying it into an FMA record. Keep these states distinct:

```text
author reported
≠
freshly reproduced
≠
independently replicated
≠
expert adjudicated
≠
applicable to another architecture or system revision
```

A bounded sidecar can still record the exact paper/version, reported estimate, controlling assumptions, evidence references, applicability limits, reproduction state, and decision reopen conditions without changing the authoritative source.


## Paper plus repository

Treat the paper and repository as related but distinct evidence objects.

Record:

- the exact paper identity or archival reference;
- the exact repository revision used for evaluation;
- which paper claim the implementation is intended to support;
- the declared input and environment requirements;
- whether the reported output was merely identified, freshly reproduced, semantically checked, or independently replicated;
- unresolved discrepancies;
- applicability limits relevant to the decision.

Do not infer that a repository reproduces every claim in a paper simply because the repository accompanies the paper.

## Model or simulation

Freeze the model identity and configuration that produced the result under review. Keep model correctness separate from execution integrity.

A useful sidecar records:

- model/version identity;
- configuration and material assumptions;
- input provenance;
- result identity;
- numerical or semantic acceptance criteria where appropriate;
- applicability envelope;
- downstream claims and decisions that depend on the result.

If a model assumption changes, use dependency impact to identify what requires reconsideration. FMA identifies affected basis; qualified domain reviewers determine the new technical answer.

## Experiment or test result

Reference the governed experimental record rather than copying protected raw data into a public FMA workspace.

Record only the minimum decision-relevant projection, such as:

- evidence identity and governed locator;
- hardware or test-article revision;
- calibration/configuration state;
- operating conditions;
- result state;
- applicability conditions;
- affected claim or requirement;
- required expert review.

Evidence that was valid for one configuration should not silently remain valid after the configuration changes.

## External execution

FMA can verify a declared external-execution evidence record without launching the external scheduler or computing environment itself.

For externally executed research:

1. bind the submitted code and input identities;
2. retain the external job/scheduler identity and chronology;
3. bind environment and calibration evidence where applicable;
4. collect output provenance;
5. apply the declared output-assurance semantics;
6. keep submission authority and external execution under the system that owns them.

`fma reproduce` is not an arbitrary-code execution service and does not launch version-3 `EXTERNAL` receipts.

## Safe reproduction boundary

Only use the trusted-code reproduction path when the code is authorized and the execution environment is appropriate for that code.

Unknown or untrusted external code should be reviewed and isolated under the controls of the environment responsible for executing it. FMA's fresh workspace is an integrity control, not a security sandbox.

## Minimum sidecar

For many existing-work evaluations, the first useful sidecar is only:

```text
assurance-graph.yaml
one Decision Receipt
optional Research Receipt when reproduction is justified
supporting notes that point back to authoritative evidence
```

Start smaller than the source system. Add structure only when it improves the consequential decision.

## Success test

The adoption path is working when an independent reviewer can answer, without restructuring the source work:

- what exact artifact or revision was evaluated;
- what claim matters to the decision;
- what evidence directly supports it;
- what is reported versus freshly verified or reproduced;
- what remains assumed;
- where the evidence applies;
- what change would make the current decision basis stale.

That is the intended boundary between an existing technical artifact and a usable assurance record.
