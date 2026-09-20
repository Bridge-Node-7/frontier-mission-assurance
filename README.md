# Frontier Mission Assurance

**Evidence-native verification and validation for high-consequence frontier systems.**

Frontier Mission Assurance (FMA) preserves the evidence behind consequential technical decisions as assumptions, experiments, estimates, interfaces, and dependencies change.

**Mission → Claim → Assumption → Experiment → Evidence → Decision**

FMA is a local-first assurance layer for teams working at the edge of science and engineering. It does not replace laboratories, source control, test infrastructure, research notebooks, supplier systems, or operational tools. Those systems remain authoritative; FMA carries the minimum reviewable decision basis across them.

> **Design principle:** automate what machines can prove; preserve accountable human authority where judgment matters.

## What FMA tells you

- **What is supported.** Which claims have declared evidence behind them.
- **What is still assumed.** Which mission-critical dependencies remain unresolved.
- **What changed.** Which estimates, evidence envelopes, claims, or interfaces are affected by a changed dependency.
- **What must be reconsidered.** Which human decision basis is stale or should reopen.

FMA does **not** infer a new scientific or engineering answer merely because an old basis became invalid.

## See the behavior in 90 seconds

A source-neutral example:

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

That distinction is the product: **expose what became invalid without manufacturing the domain judgment that replaces it.**

## Start

1. **Evaluate the public reference** — [`docs/FIVE_MINUTE_EVALUATION.md`](docs/FIVE_MINUTE_EVALUATION.md)
2. **Apply FMA around one consequential decision** — [`docs/MISSION_ORIENTED_ADOPTION.md`](docs/MISSION_ORIENTED_ADOPTION.md)
3. **Wrap work you already own** — [`docs/EXTERNAL_RESEARCH_ADOPTION.md`](docs/EXTERNAL_RESEARCH_ADOPTION.md)
4. **Build the smallest reviewable decision basis** — [`docs/MISSION_DECISION_PACKET.md`](docs/MISSION_DECISION_PACKET.md)
5. **Install a published stable release** — [`docs/INSTALL_STABLE_RELEASE.md`](docs/INSTALL_STABLE_RELEASE.md)
6. **Understand evaluation and governed-use boundaries** — [`docs/USE_AND_EVALUATION.md`](docs/USE_AND_EVALUATION.md)

For bounded automation use, see [`docs/AUTOMATION_USE.md`](docs/AUTOMATION_USE.md).

## Choose a profile only when it helps

FMA has one assurance core. Profiles are bounded domain projections; they do not redefine the core product.

- [`profiles/scientific-discovery/README.md`](profiles/scientific-discovery/README.md) — Scientific Discovery Assurance
- [`profiles/ftqc-assurance/README.md`](profiles/ftqc-assurance/README.md) — FTQC Assurance
  - governed case: [`profiles/ftqc-assurance/docs/GOVERNED_CASE_QUICKSTART.md`](profiles/ftqc-assurance/docs/GOVERNED_CASE_QUICKSTART.md)
- [`profiles/orbital-recovery-assurance/README.md`](profiles/orbital-recovery-assurance/README.md) — Orbital Recovery Assurance

Each profile exposes a `PROFILE_CONTRACT.md` and a small machine-readable `profile.yaml` manifest. See [`docs/PROFILE_ARCHITECTURE.md`](docs/PROFILE_ARCHITECTURE.md).

## The mission question

A technical leader should be able to answer five questions without reconstructing the program from notebooks, tickets, slide decks, chat threads, experiment folders, and tribal knowledge:

1. **What must be true for the mission to succeed?**
2. **Which claims are supported by direct evidence, and which still depend on assumptions?**
3. **Which important results have been freshly reproduced or independently challenged?**
4. **What decisions or interfaces are affected when a dependency changes?**
5. **What decision can an accountable human justify now—and what would make that decision reopen?**

The useful output is not a bigger graph. It is less hidden uncertainty around a consequential decision.

## Existing work stays where it is

For an existing repository, paper, model, simulation, experiment, or external execution:

```text
existing work
    ↓
freeze exact source state
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
