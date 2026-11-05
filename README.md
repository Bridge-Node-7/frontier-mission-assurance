# Frontier Mission Assurance

**Know whether a consequential technical decision is still supported when the evidence changes.**

*Evidence-native verification and validation for high-consequence frontier systems.*

Frontier Mission Assurance (FMA) connects claims, assumptions, experiments, estimates, interfaces, dependencies, and evidence to the technical decisions that rely on them—so teams can see what is supported, what remains uncertain, and what must be reconsidered when reality changes.

**Start with one consequential decision. Keep the existing work where it is.**

[Latest release](https://github.com/Bridge-Node-7/frontier-mission-assurance/releases/latest) · [Five-minute evaluation](docs/FIVE_MINUTE_EVALUATION.md) · [Partner](https://bridgenode7.com/partner/)

**Local-first:** the installed FMA runtime makes no remote API calls, emits no telemetry, and performs no default uploads.

**Mission → Claim → Assumption → Experiment → Evidence → Decision**

> **Design principle:** automate what machines can prove; preserve accountable human authority where judgment matters.

## What FMA tells you

- **What is supported.** Which claims have declared evidence behind them.
- **What is still assumed.** Which mission-critical dependencies remain unresolved.
- **What changed.** Which estimates, supporting evidence, claims, or interfaces are affected by a changed dependency.
- **What must be reconsidered.** Which human decision basis is stale or should reopen.

## See FMA in 90 seconds

A team decides whether to commit more time, money, or integration effort to a technical architecture. The decision looked supportable because a resource estimate, supporting evidence, and expert review all relied on one important assumption. Then new evidence changes that assumption.

Without a clear assurance trail, someone reconstructs the reasoning across models, tests, documents, tickets, and conversations: Does the old estimate still apply? Which evidence needs another look? Does the prior review still hold? Is the decision basis still supportable?

With FMA, once the changed assumption is reflected in the decision basis, the consequence is surfaced: **the basis for the previous decision has changed.** The dependent estimate is stale. Some supporting evidence may no longer apply. The prior expert review should be revisited. It shows why treating the previous decision as settled no longer holds. The accountable human decides what happens next.

<details>
<summary><strong>Machine-readable references under the hood</strong></summary>

```text
DECISION
Proceed with Architecture Revision A.

SUPPORTED BY
Resource estimate R-14
Evidence envelopes E-2 and E-5
Expert review X-3

CRITICAL ASSUMPTION
A-7

CHANGE
A-7 changes.

FMA RESPONSE
R-14                  → STALE
E-2 / E-5             → OUTSIDE DECLARED APPLICABILITY
X-3                    → REOPEN
Dependent claims       → IMPACTED
Prior decision basis   → RECONSIDER
```

</details>

## Choose your path

- **Technical evaluator** — [Five-Minute Evaluation](docs/FIVE_MINUTE_EVALUATION.md)
- **Technical leader or prospective adopter** — [one consequential decision](docs/MISSION_ORIENTED_ADOPTION.md)
- **Existing research or engineering work** — [wrap without reorganizing around FMA](docs/EXTERNAL_RESEARCH_ADOPTION.md)
- **FTQC program** — [FTQC decision-to-reassessment golden path](docs/FTQC_GOLDEN_PATH.md)
- **Smallest reviewable decision basis** — [Mission Decision Packet](docs/MISSION_DECISION_PACKET.md)
- **Stable artifacts** — [latest published GitHub Release](docs/INSTALL_STABLE_RELEASE.md)
- **Governed or operational evaluation** — [use and evaluation](docs/USE_AND_EVALUATION.md)
- **Independent or evaluator-side work** — [Independence & Conflict Policy](docs/INDEPENDENCE_AND_CONFLICT_POLICY.md)

Bounded automation: [`docs/AUTOMATION_USE.md`](docs/AUTOMATION_USE.md). Governed engagement: [Partner](https://bridgenode7.com/partner/).

## Profiles

FMA has one assurance core. Profiles are bounded domain projections.

- [**Scientific Discovery Assurance**](profiles/scientific-discovery/README.md) — computational, AI-generated, or research results that could influence an important decision
- [**FTQC Assurance**](profiles/ftqc-assurance/README.md) — fault-tolerant quantum architecture decisions under changing estimates, assumptions, evidence, or review ([governed case](profiles/ftqc-assurance/docs/GOVERNED_CASE_QUICKSTART.md))
- [**Orbital Recovery Assurance**](profiles/orbital-recovery-assurance/README.md) — degraded or uncertain orbital capability where physical state, trust, authority, or requalification remain unresolved

Each profile exposes `PROFILE_CONTRACT.md` and `profile.yaml`. See [`docs/PROFILE_ARCHITECTURE.md`](docs/PROFILE_ARCHITECTURE.md).

## The mission question

A technical leader should answer without reconstructing the program from notebooks, tickets, decks, and tribal knowledge:

1. What must be true for the mission to succeed?
2. Which claims are supported by direct evidence, and which still depend on assumptions?
3. Which important results have been freshly reproduced or independently challenged?
4. What decisions or interfaces are affected when a dependency changes?
5. What decision does the evidence justify now—and what would make that decision reopen?

The useful output is less hidden uncertainty around a consequential decision.

## Existing work stays where it is

```text
existing work → capture exact source state → identify the claim that matters
→ create a bounded FMA sidecar → reference authoritative evidence
→ reproduce only where appropriate → surface assumptions and applicability limits
→ connect the basis to one decision → define what would reopen that decision
```

See [`examples/external_research_adoption/`](examples/external_research_adoption/).

## Mission Decision Packet

The smallest reviewable bundle connecting one consequential technical decision to its evidence, assumptions, reproduction state, dependencies, and explicit reopen conditions.

> Why did we decide this? **What would make us revisit it?**

Start with [`docs/MISSION_DECISION_PACKET.md`](docs/MISSION_DECISION_PACKET.md) and [`examples/frontier_program/`](examples/frontier_program/).

## Core capabilities

- Assurance-graph validation; assumption visibility; evidence coverage; dependency impact
- Research receipts; fresh code-bound reproduction; external execution evidence
- Decision receipts; assurance-context exports; Mission Decision Packets
- Profile manifests; release integrity; CI-native V&V across supported platforms

## Research and verification

FMA separates source identity, reported result, fresh reproduction, scientific validity, applicability, and decision authority. See [`docs/EPISTEMIC_ASSURANCE.md`](docs/EPISTEMIC_ASSURANCE.md), [`docs/RESEARCH_REPRODUCIBILITY_CONTRACT.md`](docs/RESEARCH_REPRODUCIBILITY_CONTRACT.md), [`docs/THREAT_MODEL.md`](docs/THREAT_MODEL.md).

A machine PASS means the checked artifact satisfied the machine-checkable controls exercised by that command or workflow. Scientific validity, regulatory approval, safety acceptance, mission qualification, security authorization, supplier qualification, independent V&V, and consequential decision authority remain with the qualified processes responsible for those determinations.

Exact source validation contract: [`VALIDATION_REPORT.md`](VALIDATION_REPORT.md). Stable release proof belongs to the matching tag, release artifacts, checksums, SBOM, and provenance attestations.

## Repository map

```text
frontier-mission-assurance/
├── src/frontier_assurance/   # core reference implementation
├── schemas/                  # core + profile-manifest schemas
├── profiles/                 # bounded domain profiles
├── examples/                 # source-neutral worked examples and sidecars
├── tests/                    # regression, tamper, adversarial, and boundary tests
├── scripts/                  # deterministic validators and evaluators
├── docs/                     # adoption, architecture, contracts, and doctrine
├── SCOPE.md · SECURITY.md · VALIDATION_REPORT.md · PROJECT_FACTS.json
```

## Reference

- [`docs/CLI_CONTRACT.md`](docs/CLI_CONTRACT.md) · [`docs/VV_DOCTRINE.md`](docs/VV_DOCTRINE.md) · [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md)
- [`docs/PROFILE_ARCHITECTURE.md`](docs/PROFILE_ARCHITECTURE.md) · [`docs/INTEROPERABILITY.md`](docs/INTEROPERABILITY.md)
- [`docs/STANDARDS_POSITIONING.md`](docs/STANDARDS_POSITIONING.md) · [`docs/INDEPENDENCE_AND_CONFLICT_POLICY.md`](docs/INDEPENDENCE_AND_CONFLICT_POLICY.md)

## Development

```bash
python -m pip install -r requirements-dev.txt
python -m pip install --no-deps -e .
make check
```

## Assurance boundary

FMA is a local-first assurance layer for technical, scientific, and engineering decision bases. Laboratories, source control, test infrastructure, research notebooks, supplier systems, domain experts, and accountable decision authorities remain authoritative; FMA carries the minimum reviewable decision basis across them.

Checked-in examples and profile fixtures are synthetic or source-neutral evaluation material. The public repository is provided for evaluation and review; operational use beyond public rights requires separate written permission. See [`LICENSE`](LICENSE) and [`docs/USE_AND_EVALUATION.md`](docs/USE_AND_EVALUATION.md).

## Release and rights

[`VERSION`](VERSION) identifies current source. Stable distribution identity lives on the matching tag and GitHub Release. Copyright © 2026 Bridge Node 7. All rights reserved. See [`LICENSE`](LICENSE). Cite with [`CITATION.cff`](CITATION.cff) and the exact tagged release when the public reference materially informs published work.

https://bridgenode7.com/
