# Frontier Mission Assurance

**Know whether a consequential technical decision is still supported when the evidence changes.**

*Evidence-native verification and validation for high-consequence frontier systems.*

Frontier Mission Assurance (FMA) connects claims, assumptions, experiments, estimates, interfaces, dependencies, and evidence to the technical decisions that rely on them—so teams can see what is supported, what remains uncertain, and what must be reconsidered when reality changes.

**Start with one consequential decision. Keep the existing work where it is.**

FMA is a local-first assurance layer for technical, scientific, and engineering decision bases. It does not replace laboratories, source control, test infrastructure, research notebooks, supplier systems, domain experts, or accountable decision authorities. Those systems remain authoritative; FMA carries the minimum reviewable decision basis across them.

**Local-first:** the installed FMA runtime makes no remote API calls, emits no telemetry, and performs no default uploads.

**Public-example boundary:** checked-in examples and profile fixtures are synthetic or source-neutral evaluation material. They are not customer cases, real-system validation, mission readiness evidence, or proof of operational use.

FMA does **not** manufacture the scientific or engineering answer that replaces a decision basis that has become stale.

**Mission → Claim → Assumption → Experiment → Evidence → Decision**

> **Design principle:** automate what machines can prove; preserve accountable human authority where judgment matters.

## What FMA tells you

- **What is supported.** Which claims have declared evidence behind them.
- **What is still assumed.** Which mission-critical dependencies remain unresolved.
- **What changed.** Which estimates, supporting evidence, claims, or interfaces are affected by a changed dependency.
- **What must be reconsidered.** Which human decision basis is stale or should reopen.

FMA does **not** infer a new scientific or engineering answer merely because an old basis became invalid.

## See FMA in 90 seconds

Imagine your team is deciding whether to commit more time, money, or integration effort to a technical architecture.

The decision looked supportable because a resource estimate, supporting evidence, and expert review all relied on one important assumption.

Then new evidence changes that assumption.

### Without a clear assurance trail

Someone has to reconstruct the reasoning across models, test results, documents, tickets, experiment folders, and conversations to answer:

- Does the old estimate still apply?
- Which supporting evidence needs another look?
- Does the prior expert review still hold?
- Is the decision basis still supportable?
- What should we verify before committing further?

### With FMA

Once the changed assumption is reflected in the decision basis, FMA surfaces the consequence:

**The basis for the previous decision has changed.**

The resource estimate that depended on the old assumption is now stale. Some supporting evidence may no longer apply under the new conditions. The prior expert review should be revisited.

That does **not** mean the architecture is automatically good or bad. It means the reason for treating the previous decision as settled has changed.

FMA helps the team see **what changed, why it matters, and what deserves review before committing further**. The accountable human still decides what happens next.

<details>
<summary><strong>See the precise references FMA keeps under the hood</strong></summary>

The identifiers below are machine-readable references used to keep the decision basis precise and traceable. A decision-maker does not need to memorize them to understand the result.

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

FMA DOES NOT CLAIM
That the new architecture is good or bad.
```

</details>

**The takeaway:** when important evidence changes, FMA helps the team see what changed, why it matters, and what deserves review before the previous decision is treated as settled.

## Choose your path

- **Technical evaluator** — run the [Five-Minute Evaluation](docs/FIVE_MINUTE_EVALUATION.md).
- **Technical leader or prospective adopter** — start with [one consequential decision](docs/MISSION_ORIENTED_ADOPTION.md).
- **Existing research or engineering work** — [wrap the work without reorganizing it around FMA](docs/EXTERNAL_RESEARCH_ADOPTION.md).
- **FTQC program** — follow the [FTQC decision-to-reassessment golden path](docs/FTQC_GOLDEN_PATH.md).
- **Need the smallest reviewable decision basis** — use the [Mission Decision Packet](docs/MISSION_DECISION_PACKET.md).
- **Need stable artifacts** — use the [latest published GitHub Release](docs/INSTALL_STABLE_RELEASE.md); `main` may be newer than the latest stable release.
- **Governed or operational evaluation** — review [use and evaluation boundaries](docs/USE_AND_EVALUATION.md).
- **Independent or evaluator-side work** — review the [Independence & Conflict Policy](docs/INDEPENDENCE_AND_CONFLICT_POLICY.md) before representing a review as independent.

For bounded automation use, see [`docs/AUTOMATION_USE.md`](docs/AUTOMATION_USE.md).

The public repository is provided for evaluation and review. Operational use, integration, modification, or deployment beyond the public rights requires separate written permission. See [`LICENSE`](LICENSE) and [`docs/USE_AND_EVALUATION.md`](docs/USE_AND_EVALUATION.md). For governed or operational engagement, use [Partner](https://bridgenode7.com/partner/).

## Choose a profile only when it helps

FMA has one assurance core. Profiles are bounded domain projections; they do not redefine the core product.

- [**Scientific Discovery Assurance**](profiles/scientific-discovery/README.md) — use this when a computational, AI-generated, or research result could influence an important decision and you need proof state, replication, provenance, and unresolved scientific obligations kept distinct.
- [**FTQC Assurance**](profiles/ftqc-assurance/README.md) — use this when a fault-tolerant quantum architecture decision depends on changing resource estimates, physical assumptions, experimental evidence, interfaces, or expert review.
  - governed case: [`profiles/ftqc-assurance/docs/GOVERNED_CASE_QUICKSTART.md`](profiles/ftqc-assurance/docs/GOVERNED_CASE_QUICKSTART.md)
- [**Orbital Recovery Assurance**](profiles/orbital-recovery-assurance/README.md) — use this when a degraded or uncertain orbital capability may be recoverable, but physical state, trust, authority, recovery options, or requalification remain unresolved.
  - bounded cross-system service evaluation: [Orbital Logistics Assurance Harness](profiles/orbital-recovery-assurance/experiments/orbital-logistics-assurance-harness/README.md)

Each profile exposes a `PROFILE_CONTRACT.md` and a small machine-readable `profile.yaml` manifest. See [`docs/PROFILE_ARCHITECTURE.md`](docs/PROFILE_ARCHITECTURE.md).

## The mission question

A technical leader should be able to answer five questions without reconstructing the program from notebooks, tickets, slide decks, chat threads, experiment folders, and tribal knowledge:

1. **What must be true for the mission to succeed?**
2. **Which claims are supported by direct evidence, and which still depend on assumptions?**
3. **Which important results have been freshly reproduced or independently challenged?**
4. **What decisions or interfaces are affected when a dependency changes?**
5. **What decision does the evidence justify now—and what would make that decision reopen?**

The useful output is not a bigger graph. It is less hidden uncertainty around a consequential decision.

## Existing work stays where it is

For an existing repository, paper, model, simulation, experiment, or external execution:

```text
existing work
    ↓
capture exact source state
    ↓
identify the claim or result that matters
    ↓
create a bounded FMA sidecar
    ↓
reference authoritative evidence
    ↓
reproduce only where appropriate and trusted
    ↓
surface assumptions and applicability limits
    ↓
connect the basis to one decision
    ↓
define what would reopen that decision
```

FMA does not require a source repository to be reorganized around FMA. See [`examples/external_research_adoption/`](examples/external_research_adoption/) for a source-neutral sidecar.

## Mission Decision Packet

A **Mission Decision Packet** is the smallest reviewable bundle that connects one consequential technical decision to its evidence, assumptions, reproduction state, dependencies, and explicit reopen conditions.

The key question is not only:

> Why did we decide this?

It is also:

> **What would make us revisit it?**

Start with [`docs/MISSION_DECISION_PACKET.md`](docs/MISSION_DECISION_PACKET.md) and [`examples/frontier_program/`](examples/frontier_program/).

## Core capabilities

- **Assurance-graph validation** — validate nodes, relations, references, dependencies, and graph integrity.
- **Assumption visibility** — surface unresolved assumptions without inventing an automated priority score.
- **Evidence coverage** — identify critical nodes without direct supporting evidence.
- **Dependency impact** — trace which declared nodes depend on a changed dependency.
- **Research receipts** — bind declared code, inputs, outputs, and acceptance semantics to exact artifact identity.
- **Fresh code-bound reproduction** — execute trusted receipt-declared code in a fresh workspace and verify newly produced outputs.
- **External execution evidence** — bind submission, chronology, environment identity, output hashes, and calibration coverage for externally executed work.
- **Decision receipts** — verify that a declared decision basis resolves against the assurance graph.
- **Assurance-context exports** — project bounded change impact and review state for downstream decision preparation without copying raw evidence or increasing authority.
- **Mission Decision Packets** — preserve evidence, assumptions, dependencies, human disposition, and reopen conditions together.
- **Profile manifests** — expose bounded profile identity, contract version, containing release, and validator without creating a plugin framework.
- **Release integrity** — scan tracked files, pin Actions, exercise tamper paths, build deterministic release evidence, and verify clean installation.
- **CI-native V&V** — exercise the public assurance surface across supported Python versions and Ubuntu/macOS/Windows smoke paths.

## Research and reproduction semantics

FMA separates artifact identity, reproduction, scientific truth, and applicability.

```text
SOURCE IDENTITY        may be established
REPORTED RESULT        may be identified
FRESH REPRODUCTION     may or may not be established
SCIENTIFIC VALIDITY    remains a qualified judgment
APPLICABILITY          remains bounded to declared conditions
DECISION AUTHORITY     remains human-owned
```

A successful reproduction is not automatically scientific truth. Scientific truth is not automatically applicability to another configuration, scale, system, or decision.

See [`docs/RESEARCH_REPRODUCIBILITY_CONTRACT.md`](docs/RESEARCH_REPRODUCIBILITY_CONTRACT.md), [`docs/INTEROPERABILITY.md`](docs/INTEROPERABILITY.md), and [`docs/THREAT_MODEL.md`](docs/THREAT_MODEL.md).

## Verification semantics

A machine PASS means only that the checked artifact satisfied the machine-checkable controls exercised by that command or workflow.

Scientific validity, regulatory approval, safety acceptance, mission qualification, security authorization, supplier qualification, independent V&V, and consequential decision authority remain with the qualified processes responsible for those determinations.

The exact source validation contract is [`VALIDATION_REPORT.md`](VALIDATION_REPORT.md). Commit-specific hosted proof belongs in GitHub Actions. Stable release proof belongs to the matching tag, release artifacts, checksums, SBOM, and provenance attestations.

## Runtime behavior and repository scope

The installed FMA runtime makes no remote API calls, emits no telemetry, and performs no default uploads. Runtime assurance checks operate on local files.

This repository provides the public reference implementation, source-neutral examples, portable contracts, validation tooling, and release evidence used to evaluate FMA behavior. See [`SCOPE.md`](SCOPE.md) and [`SECURITY.md`](SECURITY.md).

## Repository map

```text
frontier-mission-assurance/
├── src/frontier_assurance/          # core reference implementation
├── schemas/                         # core + profile-manifest schemas
├── profiles/                        # bounded domain profiles
├── examples/                        # source-neutral worked examples and sidecars
├── tests/                           # regression, tamper, adversarial, and boundary tests
├── scripts/                         # deterministic validators and evaluators
├── docs/                            # adoption, architecture, contracts, and doctrine
├── .github/                         # CI, dependency maintenance, and release workflows
├── SCOPE.md                         # repository purpose and verification scope
├── SECURITY.md                      # security guidance
├── VALIDATION_REPORT.md             # deterministic source validation contract
└── PROJECT_FACTS.json               # machine-readable public scope
```

## Reference

- [`docs/CLI_CONTRACT.md`](docs/CLI_CONTRACT.md) — commands, exit codes, receipt versions, and PASS semantics
- [`docs/VV_DOCTRINE.md`](docs/VV_DOCTRINE.md) — verification and validation doctrine
- [`docs/PROFILE_ARCHITECTURE.md`](docs/PROFILE_ARCHITECTURE.md) — core/profile ownership and separation rules
- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) — core architecture
- [`docs/INTEROPERABILITY.md`](docs/INTEROPERABILITY.md) — portable contracts and compatibility
- [`docs/THREAT_MODEL.md`](docs/THREAT_MODEL.md) — trust and execution boundaries
- [`docs/STANDARDS_POSITIONING.md`](docs/STANDARDS_POSITIONING.md) — standards and non-claim positioning
- [`docs/INDEPENDENCE_AND_CONFLICT_POLICY.md`](docs/INDEPENDENCE_AND_CONFLICT_POLICY.md) — conditions for representing a review as independent

## Development

```bash
python -m pip install -r requirements-dev.txt
python -m pip install --no-deps -e .
make check
```

The canonical local gate validates the core reference, existing-work sidecar, profile manifests, all bounded profiles, deterministic reports, release-integrity controls, and regression suite. Hosted CI adds the supported Python matrix, cross-platform smoke paths, dependency review, CodeQL on protected `main`, and clean wheel installation.

## Release status and rights

[`VERSION`](VERSION) identifies the current source. A version is stable only when the matching tag and GitHub Release have been published by the explicit Stable Release workflow. Use the latest published GitHub Release when you need stable artifacts.

Copyright © 2026 Bridge Node 7. All rights reserved. The public release is provided for evaluation and review only; it does not itself grant operational-use rights. See [`LICENSE`](LICENSE) and [`docs/USE_AND_EVALUATION.md`](docs/USE_AND_EVALUATION.md).

For current Bridge Node 7 information, see <https://bridgenode7.com/>.

Use [`CITATION.cff`](CITATION.cff) and cite the exact tagged release when the public reference materially informs published work.
