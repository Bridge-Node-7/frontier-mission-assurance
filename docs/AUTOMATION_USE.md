# Automation Use

This guide defines a bounded operating contract for automated assistance working with Frontier Mission Assurance.

It is a product-use contract, not a transfer of scientific, engineering, security, legal, regulatory, or consequential decision authority.

## Default posture

Automated assistance should be **read-only toward authoritative external work unless explicitly authorized otherwise**.

The safe default sequence is:

```text
identify exact source state
        ↓
read authoritative artifacts
        ↓
separate reported from verified evidence
        ↓
create or update an FMA sidecar
        ↓
validate machine-checkable structure
        ↓
surface assumptions, gaps, and impact
        ↓
request human review for judgment-bearing semantics
```

## Required rules

1. Preserve authoritative sources. Do not rewrite an external repository, paper, experiment, or governed record merely to fit FMA.
2. Record exact source identity before drawing conclusions from an artifact that can change.
3. Distinguish **reported**, **verified**, **reproduced**, **replicated**, and **applicable** states. Do not collapse them into one confidence label.
4. Use the narrowest relevant profile. Core FMA remains valid without a profile.
5. Never equate successful reproduction with scientific truth.
6. Never equate scientific truth with applicability to a different system or decision.
7. Never use the trusted-code reproduction path for unknown or unauthorized code. The FMA fresh workspace is not a security sandbox.
8. Preserve unresolved assumptions and contradictory evidence. Do not hide them to obtain a green machine state.
9. Use only material authorized for the current workflow. Keep authoritative evidence in its system of record and pass only bounded references or approved projections into FMA.
10. Preserve accountable human authority for consequential judgments and actions.

## Profile discovery

Each bounded profile exposes a machine-readable `profile.yaml` manifest that identifies its public profile contract and validator.

Automation may use the manifest to discover the profile surface. Profile presence does not establish domain fitness for a specific decision.

## Existing work

For a repository, paper, model, simulation, experiment, or external execution that was not authored for FMA, follow [`EXTERNAL_RESEARCH_ADOPTION.md`](EXTERNAL_RESEARCH_ADOPTION.md).

Prefer a separate sidecar over source modification. A useful first sidecar can be as small as one assurance graph plus one Decision Receipt.

## Command safety

Non-executing commands such as structural validation and receipt verification are appropriate when the referenced artifacts are authorized for review.

`fma reproduce` is an explicit execution operation. Before invoking it, the operator or governing system must establish that:

- the code is trusted and authorized for execution;
- the host environment is appropriate;
- required inputs are permitted in that environment;
- the expected side effects and resource use are acceptable.

If those conditions are not established, stop at non-executing verification and report the unresolved reproduction requirement.

## Output discipline

Automated output should make evidence state visible. Prefer statements such as:

```text
SOURCE IDENTITY        ESTABLISHED
REPORTED RESULT        IDENTIFIED
FRESH REPRODUCTION     NOT ESTABLISHED
APPLICABILITY          REVIEW REQUIRED
DECISION BASIS         HOLD
```

over narrative language that implies more certainty than the evidence supports.

## Human handoff

Require qualified human review when the next step depends on scientific validity, specification equivalence, evidence applicability, safety, security, supplier qualification, legal/regulatory interpretation, program authority, or another consequential judgment.

Automation may organize the basis and identify what changed. It must not manufacture the authority that closes the decision.
