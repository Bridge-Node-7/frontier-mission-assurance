# Frontier Mission Assurance

**Mission assurance for frontier teams moving faster than their evidence can naturally stay organized.**

Frontier Mission Assurance (FMA) is a deliberately small public reference layer for connecting:

**Mission → claim → assumption → experiment → evidence → decision**

in ordinary version-controlled files. It is designed for small, interdisciplinary teams building difficult systems under uncertainty. The goal is not more process; the goal is to make the decision basis inspectable: what must be true, what is directly supported, what is still assumed, what has been reproduced, what changed, and what an accountable human can justify doing next.

> **Trust rule:** Machine PASS states are scoped to the exact control that ran. They do not establish scientific truth, authorization, qualification, compliance, safety, security, or mission readiness.

> **Public boundary:** this repository contains software, public documentation, and synthetic fixtures. It is not a repository for real mission evidence or sensitive program data. See [`PUBLIC_BOUNDARY.md`](PUBLIC_BOUNDARY.md) and [`SECURITY.md`](SECURITY.md).

> **Use boundary:** this is a public evaluation/reference implementation. Copyright © 2026 Bridge Node 7. All rights reserved; this release grants no reuse license. See [`LICENSE`](LICENSE).

## Start here

For the shortest useful evaluation path, read in this order:

1. **This README** — purpose, boundaries, and capabilities.
2. [`docs/FIVE_MINUTE_EVALUATION.md`](docs/FIVE_MINUTE_EVALUATION.md) — run the bounded synthetic example.
3. [`docs/CLI_CONTRACT.md`](docs/CLI_CONTRACT.md) — commands, exit codes, receipt versions, and PASS semantics.
4. [`docs/VV_DOCTRINE.md`](docs/VV_DOCTRINE.md) and [`docs/THREAT_MODEL.md`](docs/THREAT_MODEL.md) — what the controls prove and what remains outside the boundary.
5. [`docs/MISSION_ORIENTED_ADOPTION.md`](docs/MISSION_ORIENTED_ADOPTION.md) and [`docs/MISSION_DECISION_PACKET.md`](docs/MISSION_DECISION_PACKET.md) — adopt FMA around one consequential decision rather than migrating an entire program.

## The mission-oriented question

A technical leader should be able to answer five questions without reconstructing the program from notebooks, tickets, slide decks, chat threads, experiment folders, and tribal knowledge:

1. **What must be true for the mission to succeed?**
2. **Which claims are supported by direct evidence, and which still depend on assumptions?**
3. **Which important results have been freshly reproduced or independently challenged?**
4. **What decisions or interfaces are affected when a dependency changes?**
5. **What decision can an accountable human justify now—and what would make us revisit it?**

FMA provides thin connective tissue across the tools a team already uses. It does not require a central data migration or attempt to replace laboratory systems, source control, test infrastructure, issue trackers, research notebooks, or engineering tools.

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

FMA makes that loop inspectable without pretending that machine-readable structure makes the underlying science true.

## Five-minute evaluation

Requires Python 3.11 or newer. The bounded evaluation is local-only, non-executing with respect to research receipt commands, and uses synthetic fixtures. The clean-adopter path installs the exact pinned build backend inside the isolated environment before the editable install.

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

The synthetic fixture intentionally retains a visible critical evidence gap. A PASS means the reference mechanics behaved as declared; it does **not** establish mission readiness. See [`docs/FIVE_MINUTE_EVALUATION.md`](docs/FIVE_MINUTE_EVALUATION.md) for the complete bounded path.

## Public capabilities

- **Assurance-graph validation** — detect malformed nodes, invalid relations, duplicate identifiers, dangling references, and surface duplicate edges plus dependency cycles/self-loops as warnings.
- **Open-assumption visibility** — list unresolved assumptions without assigning an automated priority score.
- **Evidence coverage** — identify critical mission/claim/requirement nodes without direct supporting evidence.
- **Dependency impact** — show which declared nodes depend transitively on a changed dependency.
- **Research receipts** — SHA-256-bind declared code and inputs, record an observed hash for every output, and apply versioned exact or semantic acceptance without collapsing those meanings.
- **Fresh code-bound reproduction** — version-2 and local version-3 receipts verify code and inputs, require direct execution of the declared entrypoint, run in a fresh temporary workspace where declared outputs are absent, then evaluate the declared output assurance.
- **External execution evidence** — version-3.1 receipts can bind submission/collection identity, execution chronology, environment identity, output hashes, and calibration coverage without claiming that FMA itself launched the scheduler job.
- **Tracked-file public-boundary scanning** — public release checks examine every Git-tracked file regardless of directory name; local untracked caches are not treated as release content.
- **Decision receipts** — verify that a declared decision basis references nodes in a valid assurance graph.
- **Mission Decision Packets** — connect a consequential human decision to evidence, assumptions, reproduction state, dependencies, and explicit reopen conditions.
- **Scientific Discovery Assurance** — portable contracts for discovery provenance, priority evidence, research-boundary declarations, formal-proof/specification separation, replication, and attribution chronology.
- **Orbital Recovery Assurance** — bounded source contracts and tools for Mission Recovery Chain mapping, physical/trust/authority separation, provenance-aware evidence handling, robust option eligibility, next-best evidence, requalification, Time-to-Trust metrics, and synthetic known-truth evaluation under uncertainty.
- **CI-native V&V** — exercise graph, receipt, decision, schema, package, bounded profiles, adversarial rejection, and public-boundary controls on supported environments.

## Mission Decision Packet

A **Mission Decision Packet** is the smallest reviewable bundle that connects one consequential technical decision to its evidence, assumptions, reproduction state, dependencies, and explicit conditions for reopening the decision.

The key question is not only:

> Why did we decide this?

It is also:

> **What would make us revisit it?**

That turns a one-time review into a change-sensitive decision record without automating accountable human judgment. Start with the worked synthetic example in [`examples/frontier_program/`](examples/frontier_program/) and the pattern in [`docs/MISSION_DECISION_PACKET.md`](docs/MISSION_DECISION_PACKET.md).

## Research receipt v2

Version 2 binds the code entrypoint as well as input/output artifacts and requires exact output hashes. `fma receipt ...` is non-executing. `fma reproduce ...` is an explicit trusted-code operation. The reproduction workspace is an integrity boundary, **not a sandbox or hermetic environment**. Trusted code still runs with the permissions and ambient capabilities of the host.

See [`docs/RESEARCH_REPRODUCIBILITY_CONTRACT.md`](docs/RESEARCH_REPRODUCIBILITY_CONTRACT.md) and [`docs/THREAT_MODEL.md`](docs/THREAT_MODEL.md).

## Research receipt v3.1

Version 3.1 makes the output claim explicit instead of treating every successful check as the same kind of reproduction:

- `EXACT` — an observed output hash must match the declared reference hash.
- `SEMANTICALLY_CHECKED` — the newly produced output receives its own observed SHA-256, and explicitly named numerical checks define the bounded equivalence claim.
- `RECORD_ONLY` — the fresh output is cryptographically recorded, but FMA makes no equivalence claim for it.

For external execution evidence, version 3.1 also binds `submitted_at`, `started_at`, `completed_at`, and `collected_at` chronology. When calibration evidence is required, the declared calibration validity window must cover the execution interval. A syntactically valid scheduler/job record is still an assertion unless an external trust mechanism authenticates its issuer.

## Scientific Discovery Assurance

[`profiles/scientific-discovery/`](profiles/scientific-discovery/) adds a bounded contract set for machine-assisted or computational discovery. The bundled synthetic case intentionally remains `REVIEW_REQUIRED`: proof checking passes, but specification equivalence and replication are incomplete.

```bash
python scripts/validate_scientific_discovery.py .
```

Expected result:

```text
SCIENTIFIC DISCOVERY PROFILE PASS
```

That PASS establishes only the declared contracts and synthetic cross-record invariants; it does not certify the discovery.

## Orbital Recovery Assurance

[`profiles/orbital-recovery-assurance/`](profiles/orbital-recovery-assurance/) is a bounded assurance profile for degraded or uncertain orbital mission capability. It does not control orbital assets, authorize operations, establish ownership, or certify recoverability or mission readiness.

Its operator-facing Mission Recovery Chain is:

```text
Power → Contact → Telemetry → Command → Capability
```

Trust and authority remain cross-cutting overlays rather than a sixth serial link. The doctrine is **count independent recovery paths, not merely assets**.

The real-user flow is:

```text
Map → Count → Exercise → Assess → Acquire Evidence → Human Decision
    → Intervene → Requalify → Measure Time to Trust → Reassess
```

Public examples are synthetic and source-neutral. Real mission evidence remains partner-governed outside this public repository. Machine outputs stop at eligibility for downstream human decision preparation.

Evaluate the source-distributed profile with:

```bash
python -m pip install "jsonschema==4.26.0"
python scripts/validate_orbital_recovery_assurance.py .
python -m unittest tests.test_orbital_recovery_assurance -v
python scripts/run_orbital_recovery_synthetic_benchmark.py .
```

For a partner-controlled private case:

```bash
python scripts/validate_orbital_recovery_case.py /path/to/private-case --require-stage mapped
```

The private-case validator is local-only and structural. Later lifecycle gates can require `assessed`, `post-intervention`, or `requalification-review`.

The Orbital profile is distributed in the repository/source archive, not the core Python wheel. Public visibility is not a grant of operational or commercial reuse beyond the repository's stated license; such use requires rights explicitly granted by Bridge Node 7 or a separate agreement.

## Runtime privacy

The installed FMA runtime makes no remote API calls, emits no telemetry, and performs no default uploads. Package installation and hosted CI may use their configured package/repository networks; runtime assurance checks operate on local files.

## Repository map

```text
frontier-mission-assurance/
├── src/frontier_assurance/      # reference implementation
├── schemas/                     # portable JSON Schemas
├── profiles/                    # bounded assurance profiles
│   ├── scientific-discovery/    # scientific-discovery contracts
│   └── orbital-recovery-assurance/ # orbital-recovery contracts and source tools
├── examples/                    # synthetic worked examples
├── tests/                       # regression, tamper, adversarial, and boundary tests
├── docs/                        # architecture, acceptance, and adoption guidance
├── .github/                     # CI and public issue/PR workflows
├── PUBLIC_BOUNDARY.md           # public-data and claim boundary
├── SECURITY.md                  # security and vulnerability-reporting guidance
├── VALIDATION_REPORT.md         # deterministic source validation contract
└── PROJECT_FACTS.json           # machine-readable public scope
```

## Core data model

Node kinds:

`mission`, `claim`, `requirement`, `assumption`, `model`, `simulation`, `experiment`, `evidence`, `component`, `interface`, `failure_mode`, `risk`, `decision`.

Core relations:

`supports`, `depends_on`, `contradicts`, `verifies`, `validates`, `implements`, `requires`, `generated_by`, `supersedes`, `mitigates`.

FMA intentionally does **not** calculate an engineering priority score from assumption fields. It exposes assumptions, gaps, and dependency impact; consequence, urgency, resource allocation, and final priority remain human-owned.

## What a PASS means

A passing FMA validator means the checked artifact met this repository's declared machine-checkable rules. It does **not** establish scientific truth, certify a supplier or subsystem, approve acquisition, establish regulatory compliance, prove mission readiness, authenticate an unsigned artifact's author, establish legal priority, or replace authorized human review.

See [`DISCLAIMER.md`](DISCLAIMER.md), [`PUBLIC_BOUNDARY.md`](PUBLIC_BOUNDARY.md), and [`SECURITY.md`](SECURITY.md).

## Development

```bash
python -m pip install -r requirements-dev.txt
python -m pip install --no-deps -e .
make check
```

Hosted CI additionally rehearses supported Python versions, multiple operating systems, fresh wheel installation, the tracked-file public release boundary, adversarial rejection behavior, fresh reproduction integrity, and both bounded assurance profiles.

## Design principles

1. Mission first.
2. Minimum sufficient assurance.
3. Assumptions remain visible.
4. Evidence is preserved by construction.
5. Traceability crosses analysis, software, experiment, and system boundaries.
6. Verification rigor scales with consequence.
7. AI-generated work requires explicit evidence gates.
8. Failures remain evidence rather than being erased from history.
9. Human judgment owns prioritization and consequential decisions.
10. The purpose of V&V is faster justified decisions, not paperwork.

See [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md), [`docs/INTEROPERABILITY.md`](docs/INTEROPERABILITY.md), [`docs/ACCEPTANCE_CRITERIA.md`](docs/ACCEPTANCE_CRITERIA.md), [`docs/RELEASE_ACCEPTANCE.md`](docs/RELEASE_ACCEPTANCE.md), [`docs/RELEASE_EVIDENCE_LIFECYCLE.md`](docs/RELEASE_EVIDENCE_LIFECYCLE.md), and [`docs/MAINTENANCE.md`](docs/MAINTENANCE.md).

## Current maturity

The current source identity is defined by [`VERSION`](VERSION). The v0.7 line adds bounded Orbital Recovery Assurance with source-neutral Mission Recovery Chain mapping, robust option eligibility, private local case validation, synthetic known-truth benchmarking, post-intervention requalification, and Time-to-Trust while preserving FMA's deliberately small public scope, Mission Decision Packets, Scientific Discovery Assurance, cross-platform verification, and deliberate stable-release automation.

Current deterministic validation expectations and residual limitations are recorded in [`VALIDATION_REPORT.md`](VALIDATION_REPORT.md).

## Copyright and citation

Copyright © 2026 Bridge Node 7. All rights reserved. No reuse license is granted by this release. See [`LICENSE`](LICENSE).

External code contributions are not accepted unless and until Bridge Node 7 intentionally adopts separate inbound-contribution terms; public-safe feedback and bug reports are welcome.

The package metadata intentionally blocks public package-index upload; evaluation artifacts are distributed through the repository release workflow.

Use [`CITATION.cff`](CITATION.cff) and cite the exact tagged release if the public reference materially informs published work.
