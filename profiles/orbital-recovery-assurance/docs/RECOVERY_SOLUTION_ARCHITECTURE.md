# Recovery Assurance Architecture

The profile focuses on seven bounded assurance functions.

1. **Residual Capability Assessment** — represent what physical capability may remain.
2. **Trust and Authority State** — keep command trust and legitimate authority separate
   from hardware state.
3. **Decision-Relevant Observation** — choose evidence acquisition by expected decision
   improvement, not raw data volume.
4. **Robust Action Envelope** — exclude interventions unsafe across the declared credible
   hypothesis set before economic ranking.
5. **Option-Specific Assurance Gates** — different actions require different proof.
6. **Requalification** — after an intervention, evaluate the resulting configuration
   against the requirements of the intended mission capability.
7. **Time to Trust** — distinguish technical restoration from the later point at which
   evidence supports resuming a defined capability.

The intended lifecycle is:

`Recover → Requalify → Repurpose or Retire`

The profile does not assume recovery is always the preferred outcome. A defensible
retirement or additional-observation decision is a valid result.

## Target and pathway dimensions

The assurance functions operate over a source-neutral target classification rather than a single "defunct" state. Assessments may distinguish responsiveness, physical-control state, interface preparedness, and whether a pathway is observation-only, remote recovery, external augmentation, bounded reuse, retirement, or no consequential action yet.

The reusable capability stack is **Observe → Contact → Interface**. These are not mandatory sequential steps: some assessments remain observation-only, while physical recovery concepts must justify both contact and interface evidence before they can enter decision preparation.

See `RECOVERY_PATHWAY_TAXONOMY.md`.

## Experimental intervention pattern

The profile may carry bounded experiment protocols that test a recovery-enabling hypothesis without elevating the hypothesis into operational capability. `SECOND_LIGHT_BENCH_PROTOCOL.md` is one example: it treats passive-aperture reuse as a mission-requirement-driven bench question and closes the loop through requalification evidence rather than an arbitrary performance percentage.

