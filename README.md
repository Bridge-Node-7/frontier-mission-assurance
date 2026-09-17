# Frontier Mission Assurance

**Evidence-native verification and validation for high-consequence frontier systems.**

Frontier Mission Assurance (FMA) turns fragmented technical evidence into an inspectable decision basis. It connects mission intent to claims, assumptions, experiments, evidence, dependencies, and decisions in ordinary version-controlled artifacts.

**Mission → Claim → Assumption → Experiment → Evidence → Decision**

FMA is built for teams working at the edge of science and engineering, where the system is complex, the evidence changes quickly, and consequential decisions must remain explainable after the fact.

> **Design principle:** automate what machines can prove; preserve accountable human authority where judgment matters.

> **Public release policy:** this repository contains the reusable public product surface—software, schemas, synthetic examples, documentation, and release evidence. Mission-specific and protected evidence remains in governed environments. See [`PUBLIC_BOUNDARY.md`](PUBLIC_BOUNDARY.md).

> **Release status:** [`VERSION`](VERSION) identifies the current source. A version is stable only when the matching tag and GitHub Release have been published by the Stable Release workflow; otherwise use the latest published release for stable artifacts.

> **Rights:** Copyright © 2026 Bridge Node 7. All rights reserved. See [`LICENSE`](LICENSE).

## Start here

### Start

1. [`docs/FIVE_MINUTE_EVALUATION.md`](docs/FIVE_MINUTE_EVALUATION.md) — evaluate the source-neutral reference locally.
2. [`docs/MISSION_ORIENTED_ADOPTION.md`](docs/MISSION_ORIENTED_ADOPTION.md) — apply FMA around one consequential technical decision.
3. [`docs/MISSION_DECISION_PACKET.md`](docs/MISSION_DECISION_PACKET.md) — build the smallest reviewable decision basis.

### Choose a profile when relevant

- [`profiles/scientific-discovery/README.md`](profiles/scientific-discovery/README.md) — Scientific Discovery Assurance.
- [`profiles/ftqc-assurance/README.md`](profiles/ftqc-assurance/README.md) — FTQC Assurance and decision-basis continuity.
- [`profiles/orbital-recovery-assurance/README.md`](profiles/orbital-recovery-assurance/README.md) — Orbital Recovery Assurance.

### Reference

- [`docs/CLI_CONTRACT.md`](docs/CLI_CONTRACT.md) — commands, exit codes, receipt versions, and PASS semantics.
- [`docs/VV_DOCTRINE.md`](docs/VV_DOCTRINE.md) — verification and validation doctrine.
- [`docs/PROFILE_ARCHITECTURE.md`](docs/PROFILE_ARCHITECTURE.md) — core/profile ownership, compatibility, and separation rules.
- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) — core architecture.
- [`docs/INTEROPERABILITY.md`](docs/INTEROPERABILITY.md) — portable contracts and compatibility.
- [`docs/THREAT_MODEL.md`](docs/THREAT_MODEL.md) — trust and execution boundaries.
- [`docs/STANDARDS_POSITIONING.md`](docs/STANDARDS_POSITIONING.md) — standards and non-claim positioning.

## The mission question

A technical leader should be able to answer five questions without reconstructing the program from notebooks, tickets, slide decks, chat threads, experiment folders, and tribal knowledge:

1. **What must be true for the mission to succeed?**
2. **Which claims are supported by direct evidence, and which still depend on assumptions?**
3. **Which important results have been freshly reproduced or independently challenged?**
4. **What decisions or interfaces are affected when a dependency changes?**
5. **What decision can an accountable human justify now—and what would make that decision reopen?**

FMA provides a portable assurance layer across the tools a team already uses. Existing laboratory systems, source control, test infrastructure, issue trackers, research notebooks, evidence stores, and operational systems remain authoritative in their own domains.

```text
MISSION OBJECTIVE
      ↓
AI / THEORY / ENGINEERING RESULT
      ↓
CLAIM + ASSUMPTIONS
      ↓
SIMULATION / EXPERIMENT / EVIDENCE
      ↓
REPRODUCTION + CHALLENGE
      ↓
HUMAN DECISION
      ↓
CHANGE / NEW EVIDENCE
      └───────────────→ reassess affected claims and decisions
```

The result is a decision loop that stays inspectable as the system changes.

## Five-minute evaluation

Requires Python 3.11 or newer. The evaluation is local and uses source-neutral reference fixtures.

### macOS / Linux

```bash
python3 -m venv .venv
.venv/bin/python -m pip install "setuptools==84.0.0" "wheel==0.48.0"
.venv/bin/python -m pip install --no-build-isolation -e .
.venv/bin/python scripts/evaluate_public_reference.py
```

### Windows PowerShell

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install "setuptools==84.0.0" "wheel==0.48.0"
.\.venv\Scripts\python.exe -m pip install --no-build-isolation -e .
.\.venv\Scripts\python.exe scripts/evaluate_public_reference.py
```

Expected final line:

```text
RESULT - PUBLIC REFERENCE EVALUATION PASS
```

The reference fixture includes a deliberate critical evidence gap so evaluators can see how FMA surfaces unresolved mission-critical assumptions rather than hiding them behind a green status.

Next, use [`docs/MISSION_ORIENTED_ADOPTION.md`](docs/MISSION_ORIENTED_ADOPTION.md) to apply the same pattern around one consequential decision in work your team already owns.

## Core capabilities

- **Assurance-graph validation** — validate nodes, relations, references, dependencies, and graph integrity.
- **Assumption visibility** — surface unresolved assumptions without inventing an automated priority score.
- **Evidence coverage** — identify critical mission, claim, and requirement nodes without direct supporting evidence.
- **Dependency impact** — trace which declared nodes depend on a changed dependency.
- **Research receipts** — SHA-256-bind declared code, inputs, and observed outputs with versioned acceptance semantics.
- **Fresh code-bound reproduction** — execute trusted receipt-declared code in a fresh declared-artifact workspace and evaluate newly produced outputs.
- **External execution evidence** — bind submission, execution chronology, environment identity, output hashes, and calibration coverage for externally executed work.
- **Decision receipts** — verify that a declared decision basis references valid assurance-graph nodes.
- **Mission Decision Packets** — connect a consequential technical decision to evidence, assumptions, reproduction state, dependencies, and explicit reopen conditions.
- **Public release controls** — scan tracked files, verify structured artifacts, pin Actions, exercise tamper paths, and preserve deterministic release evidence.
- **Scientific Discovery Assurance** — portable contracts for discovery provenance, priority evidence, specification, proof state, replication, and attribution chronology.
- **Orbital Recovery Assurance** — evidence-driven recovery assurance for mission-state assessment, recovery-path diversity, robust option eligibility, next-best evidence, requalification, and Time-to-Trust.
- **FTQC Assurance** — preserve the decision basis of fault-tolerant quantum programs as assumptions, evidence, estimates, interfaces, and expert reviews change.
- **CI-native V&V** — run the complete assurance surface across supported Python versions and operating systems.

## Mission Decision Packet

A **Mission Decision Packet** is the smallest reviewable bundle that connects one consequential technical decision to its evidence, assumptions, reproduction state, dependencies, and explicit reopen conditions.

The key question is not only:

> Why did we decide this?

It is also:

> **What would make us revisit it?**

That turns a one-time review into a change-sensitive decision record while preserving accountable human judgment. Start with [`examples/frontier_program/`](examples/frontier_program/) and [`docs/MISSION_DECISION_PACKET.md`](docs/MISSION_DECISION_PACKET.md).

## Research receipts

FMA research receipts separate exact artifact identity from declared acceptance semantics.

- **Exact identity** — SHA-256 binds the declared bytes.
- **Fresh reproduction** — trusted code and inputs are staged into a fresh workspace and required outputs are created after execution.
- **Semantic checks** — numerical or domain checks can establish a declared equivalence claim without weakening exact artifact identity.
- **External execution evidence** — versioned records can bind scheduler/job identity, chronology, environment, calibration coverage, and collected outputs.

The reproduction workspace is an integrity boundary. Trusted code runs with the permissions and ambient capabilities of the host. See [`docs/RESEARCH_REPRODUCIBILITY_CONTRACT.md`](docs/RESEARCH_REPRODUCIBILITY_CONTRACT.md) and [`docs/THREAT_MODEL.md`](docs/THREAT_MODEL.md).

## Scientific Discovery Assurance

[`profiles/scientific-discovery/`](profiles/scientific-discovery/) provides evidence architecture for machine-assisted and computational discovery.

Its assurance path preserves source and trigger provenance, priority evidence, research-boundary evidence, formal proof state, specification-equivalence review, independent replication, attribution chronology, and accountable institutional decision ownership.

```bash
python scripts/validate_scientific_discovery.py .
```

Expected result:

```text
SCIENTIFIC DISCOVERY PROFILE PASS
```

See [`profiles/scientific-discovery/README.md`](profiles/scientific-discovery/README.md) and [`profiles/scientific-discovery/PROFILE_CONTRACT.md`](profiles/scientific-discovery/PROFILE_CONTRACT.md).

## Orbital Recovery Assurance

[`profiles/orbital-recovery-assurance/`](profiles/orbital-recovery-assurance/) structures the path from uncertain orbital system state to trusted mission capability.

Its operator-facing Mission Recovery Chain is:

```text
Power → Contact → Telemetry → Command → Capability
```

Trust and authority are cross-cutting overlays. Recovery resilience is measured by **independent recovery paths**, not raw asset count.

The working sequence is:

```text
Map → Count → Exercise → Assess → Acquire Evidence → Decide
    → Requalify → Measure Time to Trust → Reassess
```

Mission-specific evidence remains in the governed systems that own it. The profile provides portable contracts, local validation, deterministic reference cases, and decision-review artifacts without creating a second source of truth.

Evaluate the profile with:

```bash
python -m pip install "jsonschema==4.26.0"
python scripts/validate_orbital_recovery_assurance.py .
python -m unittest tests.test_orbital_recovery_assurance -v
python scripts/run_orbital_recovery_synthetic_benchmark.py .
```

For a governed mission case:

```bash
python scripts/validate_orbital_recovery_case.py /path/to/private-case --require-stage mapped
```

See [`profiles/orbital-recovery-assurance/README.md`](profiles/orbital-recovery-assurance/README.md) and [`profiles/orbital-recovery-assurance/docs/PARTNER_QUICKSTART.md`](profiles/orbital-recovery-assurance/docs/PARTNER_QUICKSTART.md).

## FTQC Assurance

[`profiles/ftqc-assurance/`](profiles/ftqc-assurance/) preserves **decision-basis continuity** for fault-tolerant quantum programs.

It connects system concepts, resource-estimation assumptions, bounded evidence applicability, interface and component dependencies, expert review, and human decisions without turning FMA into a quantum simulator or certification authority.

Its architecture-neutral Workload-to-System Assurance Chain is:

```text
Utility / mission objective
→ Workload
→ Algorithm
→ Logical resource requirement
→ QEC assumptions
→ Resource estimate
→ Physical error / loss assumptions
→ Control / movement / scheduling
→ Physical architecture
→ Subsystem and interface dependencies
→ Industrial dependencies
→ Risk-retirement evidence
→ Expert adjudication
→ Mission decision
```

The public neutral-atom reference case changes one physical-model assumption and demonstrates which estimate, evidence envelope, expert review, claims, and decision must be reconsidered.

Evaluate it with:

```bash
python scripts/evaluate_ftqc_reference.py .
```

Expected final line:

```text
RESULT - FTQC REFERENCE EVALUATION PASS
```

The output deliberately distinguishes **software / contract validation** from **technical decision readiness**. A profile PASS does not establish quantum performance, QEC validity, hardware readiness, independent V&V, or mission approval.

See [`profiles/ftqc-assurance/README.md`](profiles/ftqc-assurance/README.md).

## Runtime privacy

The installed FMA runtime makes no remote API calls, emits no telemetry, and performs no default uploads. Runtime assurance checks operate on local files. Package installation and hosted CI use only the networks configured for those environments.

## Repository map

```text
frontier-mission-assurance/
├── src/frontier_assurance/          # core reference implementation
├── schemas/                         # portable JSON Schemas
├── profiles/                        # specialized assurance profiles
│   ├── scientific-discovery/        # discovery assurance contracts
│   ├── orbital-recovery-assurance/  # orbital recovery assurance contracts
│   └── ftqc-assurance/              # FTQC decision-basis continuity contracts
├── examples/                        # source-neutral worked examples
├── tests/                           # regression, tamper, adversarial, and boundary tests
├── docs/                            # architecture, contracts, doctrine, and adoption guidance
├── .github/                         # CI and release workflows
├── ASSURANCE_SCOPE.md               # verification and authority scope
├── PUBLIC_BOUNDARY.md               # public release policy
├── SECURITY.md                      # security guidance
├── VALIDATION_REPORT.md             # deterministic validation contract
└── PROJECT_FACTS.json               # machine-readable public scope
```

## Core data model

Node kinds:

`mission`, `claim`, `requirement`, `assumption`, `model`, `simulation`, `experiment`, `evidence`, `component`, `interface`, `failure_mode`, `risk`, `decision`.

Core relations:

`supports`, `depends_on`, `contradicts`, `verifies`, `validates`, `implements`, `requires`, `generated_by`, `supersedes`, `mitigates`.

FMA exposes assumptions, evidence gaps, and dependency impact while leaving consequence, urgency, resource allocation, and final priority with accountable human owners.

## Verification semantics

A machine PASS means the checked artifact satisfied the declared machine-checkable controls exercised by that command or workflow.

Scientific validation, regulatory approval, safety acceptance, mission qualification, security authorization, and consequential decision authority remain governed by the qualified processes responsible for those determinations. See [`ASSURANCE_SCOPE.md`](ASSURANCE_SCOPE.md), [`PUBLIC_BOUNDARY.md`](PUBLIC_BOUNDARY.md), and [`SECURITY.md`](SECURITY.md).

## Development

```bash
python -m pip install -r requirements-dev.txt
python -m pip install --no-deps -e .
make check
```

Hosted CI exercises supported Python versions, Ubuntu/macOS/Windows smoke paths, fresh wheel installation, dependency review, CodeQL, public release controls, adversarial rejection behavior, fresh reproduction integrity, and all assurance profiles.

## Design principles

1. Mission first.
2. Minimum sufficient assurance.
3. Assumptions remain visible.
4. Evidence is preserved by construction.
5. Traceability crosses analysis, software, experiment, and system boundaries.
6. Verification rigor scales with consequence.
7. AI-generated work passes through explicit evidence gates.
8. Failures remain evidence rather than disappearing from history.
9. Human judgment owns prioritization and consequential decisions.
10. V&V should accelerate justified decisions, not add paperwork.

See [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md), [`docs/PROFILE_ARCHITECTURE.md`](docs/PROFILE_ARCHITECTURE.md), [`docs/INTEROPERABILITY.md`](docs/INTEROPERABILITY.md), [`docs/ACCEPTANCE_CRITERIA.md`](docs/ACCEPTANCE_CRITERIA.md), [`docs/RELEASE_ACCEPTANCE.md`](docs/RELEASE_ACCEPTANCE.md), [`docs/RELEASE_EVIDENCE_LIFECYCLE.md`](docs/RELEASE_EVIDENCE_LIFECYCLE.md), and [`docs/MAINTENANCE.md`](docs/MAINTENANCE.md).

## Release and citation

The current source identity is defined by [`VERSION`](VERSION). Deterministic validation expectations are recorded in [`VALIDATION_REPORT.md`](VALIDATION_REPORT.md), and stable releases are published through the repository's explicit release workflow with source archives, wheel artifacts, checksums, SBOM, and provenance attestations.

Copyright © 2026 Bridge Node 7. All rights reserved. No reuse license is granted by this release. See [`LICENSE`](LICENSE).

External code contributions are accepted only under terms explicitly adopted by Bridge Node 7. Public-safe feedback and bug reports are welcome.

Use [`CITATION.cff`](CITATION.cff) and cite the exact tagged release when the public reference materially informs published work.
