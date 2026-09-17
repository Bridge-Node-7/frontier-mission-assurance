# FTQC Verification-Readiness Baseline

The FTQC Verification-Readiness Baseline is a bounded engagement pattern for making one consequential fault-tolerant quantum computing decision easier to review, challenge, and revisit as evidence changes.

It is **not** a quantum-hardware certification, a substitute for qualified scientific judgment, or a claim of readiness for any government program.

## Mission question

Start with one decision:

> **What must be true for this decision to remain defensible, what evidence supports those conditions, what remains unresolved, and what should be verified next?**

The baseline is intentionally narrower than an enterprise-wide assurance program.

## Minimum decision basis

A useful baseline should contain only the smallest set of records needed to make the decision basis reviewable:

1. **Decision statement** — the consequential decision, accountable owner, date, and scope.
2. **Critical claims** — only claims that materially control the decision.
3. **Evidence references** — authoritative source identity, evidence class, provenance reference, and current review state.
4. **Assumptions** — unresolved propositions that the decision still depends on.
5. **Applicability envelopes** — where each evidence item applies and what establishes that applicability.
6. **Dependencies** — technical, interface, partner, supplier, manufacturing, schedule, or external dependencies that can change the decision basis.
7. **Expert gates** — questions that require qualified QEC, physics, photonics, controls, metrology, systems, manufacturing, security, or other domain judgment.
8. **Risk-retirement actions** — the next experiment, prototype, review, measurement, analysis, or evidence acquisition that could reduce important uncertainty.
9. **Reopen conditions** — the exact changes that force reconsideration.
10. **Decision Receipt / Mission Decision Packet** — the bounded human-owned disposition and its declared basis.

## Suggested output set

A governed engagement can produce:

| Output | Purpose |
| --- | --- |
| Critical Claims Register | Identifies propositions the decision materially depends on |
| Evidence Map | Connects claims to authoritative evidence references and review state |
| Assumption Register | Preserves unresolved propositions instead of laundering them into facts |
| Dependency Map | Exposes technical, interface, industrial, and external dependencies |
| Evidence Validity Envelopes | States where decision-relevant evidence applies |
| Expert Review Gates | Marks the boundary between machine-checkable structure and qualified judgment |
| Risk-Retirement Plan | Identifies the next evidence-producing action |
| Decision Receipt / Mission Decision Packet | Preserves the current disposition and explicit reopen conditions |

These are views over the same governed decision basis, not separate sources of truth.

## Decision states

The baseline should fail closed when a decision-gating condition is unresolved.

Typical dispositions include:

- **APPROVE WITHIN DECLARED SCOPE** — only when every mandatory gate is satisfied under the governing process.
- **HOLD** — important evidence or expert review remains unresolved.
- **REVIEW REQUIRED** — the basis exists but qualified adjudication is still required.
- **RECONSIDER** — a changed dependency invalidated or weakened the prior basis.

A software or contract-validation PASS must never be translated into scientific, engineering, mission, or program approval.

## Expert-review boundary

When the baseline reaches a question whose answer requires specialized scientific or engineering competence, record:

> **DOMAIN EXPERT REVIEW REQUIRED**

Then identify the required competency and evidence set.

For FTQC work, possible expert domains include quantum error correction, atomic or solid-state physics, photonics, controls, cryogenics where applicable, metrology, resource estimation, systems engineering, manufacturing, and supply-chain qualification.

The profile records the review boundary. It does not manufacture the missing judgment.

## Verification-readiness test

A decision basis is becoming verification-ready when an authorized reviewer can determine, without reconstructing the entire program from tribal knowledge:

- what claim is being made;
- what evidence supports it;
- which assumptions remain open;
- where the evidence applies;
- which dependencies control validity;
- which expert judgments are still required;
- what would falsify, weaken, or reopen the basis;
- who owns the consequential decision.

Verification-readiness is not a binary certification. It is a reduction in hidden uncertainty and reconstruction cost.

## Public/private boundary

The public FMA repository contains only reusable contracts, synthetic fixtures, and source-neutral guidance.

Real customer, architecture, experiment, supplier, partner, schedule, controlled, export-sensitive, or proprietary information belongs in a governed private workspace. Follow the repository-wide public boundary and the FTQC private-workspace pattern.

## Independence boundary

Performer-side verification-readiness support is not automatically independent V&V. The role must be declared accurately, and any future evaluator role must be screened under the applicable independence and conflict process.

See:

- [Independence and Conflict Policy](../../../docs/INDEPENDENCE_AND_CONFLICT_POLICY.md)
- [Expert Review Gates](EXPERT_REVIEW_GATES.md)
- [Private Workspace Pattern](PRIVATE_WORKSPACE_PATTERN.md)
- [QBI Public Crosswalk](QBI_PUBLIC_CROSSWALK.md)

## Success criterion

The baseline succeeds when the organization can answer one consequential question faster and with less hidden uncertainty:

> **What does this decision depend on, what is still unproven, and what evidence should we obtain next?**
