# QBI IV&V Fit Review

**Status:** public-source capability review  
**As of:** 2026-09-17

This document compares the public Frontier Mission Assurance / FTQC Assurance surface with public DARPA Quantum Benchmarking Initiative (QBI) IV&V needs.

It is **not** a proposal, eligibility determination, affiliation claim, QBI-readiness score, or representation of evaluator-internal methods.

## Public QBI reference

DARPA states that QBI is designed to determine whether quantum-computing approaches can achieve utility-scale operation by 2033. Publicly described stages are:

- **Stage A** — describe a utility-scale quantum computer concept with a plausible near-term path;
- **Stage B** — develop the R&D plan, identify risks, describe mitigation and risk-reduction prototypes;
- **Stage C** — work with the Government to verify and validate that the system can be constructed as designed and operated as intended.

DARPA also maintains a separate QBI IV&V opportunity seeking innovative infrastructure, equipment, and expertise for independent verification and validation.

Primary public references:

- https://www.darpa.mil/research/programs/quantum-benchmarking-initiative
- https://www.darpa.mil/work-with-us/opportunities/darpa-pa-26-02-01
- https://www.darpa.mil/research/programs/quantum-benchmarking-initiative/stage-b-selection
- https://www.darpa.mil/sites/default/files/attachment/2026-03/darpa-qbi-q-a-2026.pdf

The current DARPA program page lists the IV&V opportunity deadline as **December 30, 2026**. Solicitation amendments and the applicable submission package remain authoritative for any real proposal.

## What the current public FMA / FTQC surface can credibly contribute

The repository demonstrates reusable infrastructure for:

- explicit claim, assumption, evidence, dependency, and decision linkage;
- change-sensitive decision-basis continuity;
- evidence applicability envelopes;
- separation of reported evidence, fresh reproduction, independent replication, expert adjudication, and system applicability;
- explicit expert-review gates;
- bounded Decision Receipts / Mission Decision Packets;
- source-neutral synthetic FTQC reference behavior;
- public/private evidence separation;
- reproducible software-contract validation and release evidence;
- institutional independence and conflict-role discipline.

Those are potentially useful **assurance orchestration and evidence-architecture** capabilities.

## What the current public repository does not establish

The repository does not establish capability to independently perform or certify:

- QEC theory, decoder validity, thresholds, or mathematical closure;
- quantum-physics performance;
- system-specific FTQC resource-estimator correctness;
- hardware fidelity, loss, calibration, or metrology;
- laboratory test execution;
- utility-scale benchmark execution;
- supplier or manufacturing qualification for a real quantum system;
- government eligibility or OCI acceptability;
- independent evaluator authority.

Those remain qualified technical, laboratory, contractual, legal, and government determinations.

## Current-fit conclusion

The strongest defensible near-term role is:

> **evidence architecture + decision-basis continuity + verification-readiness support + expert-orchestration interfaces**

The current public surface should **not** be represented as a complete QBI IV&V capability.

A credible QBI-facing team would likely need additional qualified capability across several areas, potentially including:

- quantum error correction;
- modality-specific physics and hardware;
- controls and systems integration;
- metrology and experimental test;
- resource estimation and architecture modeling;
- independent laboratory or test infrastructure;
- government contracting and OCI review.

The exact mix depends on the solicitation and proposed contribution.

## Partner-before-pretend rule

When a required capability is outside the demonstrated BN7/FMA scope:

1. mark the boundary explicitly;
2. identify the competency required;
3. retain or team with a qualified party where appropriate;
4. preserve that party's scope and evidence;
5. do not relabel orchestration as domain validation.

## Conflict and independence implications

DARPA's public Stage A FAQ states that an entity receiving QBI IV&V support may face exclusions from performer awards because of potential organizational conflicts of interest, and that disclosure may be required in other U.S. Government quantum procurements.

Therefore:

- independence has strategic value;
- performer-side work is not automatically disqualifying from every future role;
- actual eligibility and OCI treatment are program-specific;
- proposed work should be screened before acceptance;
- qualified government-contracting / OCI counsel should review consequential cases.

See the repository-wide [Independence and Conflict Policy](../../../docs/INDEPENDENCE_AND_CONFLICT_POLICY.md).

## Go / no-go criteria for a real QBI IV&V submission

Do not submit merely because the opportunity exists.

A proposal should proceed only when the team can clearly state:

- the **distinctive infrastructure, equipment, or expertise** being offered;
- why that contribution adds value beyond existing QBI IV&V capability;
- the qualified personnel and facilities that support the claim;
- the exact verification or validation problem being addressed;
- the independence / OCI posture;
- the data, security, contracting, and technical boundaries;
- the evidence that the proposed capability works.

If those conditions are not yet met, the correct action is to continue building demonstrable capability and relationships rather than overclaim.

## Strategic use inside FMA

QBI is an external rigor reference, not the identity of FTQC Assurance.

The durable FMA product remains:

> **preserve what must be true, what evidence supports it, what remains uncertain, what changed, which qualified judgment is required, and what decision should reopen.**
