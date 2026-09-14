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
- **CI-native V&V** — exercise graph, receipt, decision, schema, package, scientific-discovery, adversarial rejection, and public-boundary controls on supported environments.

## Mission Decision Packet

A **Mission Decision Packet** is the smallest reviewable bundle that connects one consequential technical decision to its evidence, assumptions, reproduction state, dependencies, and explicit conditions for reopening the decision.

The key question is not only:

> Why did we decide this?

It is also:

> **What would make us revisit it?**

That turns a one-time review into a change-sensitive decision record without automating accountable human judgment. Start with the worked synthetic example in [`examples/frontier_program/`](examples/frontier_program/) and the pattern in [`docs/MISSION_DECISION_PACKET.md`](docs/MISSION_DECISION_PACKET.md).

## Research receipt v2

Version 2 binds the code entrypoint as well as input/output artifacts and requires exact output hashes:

```yaml
receipt_version: "2.0"
experiment:
  id: DEMO-Z-EXPECTATION
  command: python analysis.py
  entrypoint: analysis.py
  seed: 1111
code:
  - path: analysis.py
    sha256: "..."
inputs:
  - path: data/measurements.csv
    sha256: "..."
outputs:
  - path: outputs/result.json
    sha256: "..."
checks:
  - name: z_expectation
    path: outputs/result.json
    json_path: estimate_z
    expected: 0.6
    atol: 1.0e-12
```

`fma receipt ...` is non-executing. It verifies the declared artifacts and checks and reports how many controls actually passed.

`fma reproduce ...` is an explicit trusted-code operation. It verifies declared code and inputs first, requires the command to execute the declared entrypoint directly or as the first Python script argument, creates a fresh temporary workspace containing the receipt plus declared code and inputs, intentionally does **not** stage declared outputs, executes with `shell=False`, and then verifies the outputs and numerical criteria. Interpreter modes such as `python -c`, `python -m`, or stdin execution cannot satisfy entrypoint binding merely by mentioning the declared entrypoint later in the command. A successful command that produces no required output fails closed rather than reusing a stale result from the caller's working directory.

The reproduction workspace is an integrity boundary, **not a sandbox or hermetic environment**. Trusted code still runs with the permissions and ambient capabilities of the host. Legacy version-1 receipts remain available for non-executing historical verification but do not receive the current fresh-reproduction PASS.

## Research receipt v3.1

Version 3.1 makes the output claim explicit instead of treating every successful check as the same kind of reproduction:

- `EXACT` — an observed output hash must match the declared reference hash.
- `SEMANTICALLY_CHECKED` — the newly produced output receives its own observed SHA-256, and explicitly named numerical checks define the bounded equivalence claim.
- `RECORD_ONLY` — the fresh output is cryptographically recorded, but FMA makes no equivalence claim for it.

For external execution evidence, version 3.1 also binds `submitted_at`, `started_at`, `completed_at`, and `collected_at` chronology. When calibration evidence is required, the declared calibration validity window must cover the execution interval. A syntactically valid scheduler/job record is still an assertion unless an external trust mechanism authenticates its issuer.

Example output interpretation:

```text
Exact outputs:        declared exact comparisons only
Semantic outputs:     declared check scope only
Record-only outputs:  identity recorded, no equivalence claim
Scientific truth:     NOT ESTABLISHED
```

See [`docs/RESEARCH_REPRODUCIBILITY_CONTRACT.md`](docs/RESEARCH_REPRODUCIBILITY_CONTRACT.md) and [`docs/THREAT_MODEL.md`](docs/THREAT_MODEL.md).

## Scientific Discovery Assurance

[`profiles/scientific-discovery/`](profiles/scientific-discovery/) adds a bounded contract set for machine-assisted or computational discovery:

- `DiscoveryPassport` records the claimed result, contributors, execution context, provenance, verification state, attribution chronology, limitations, and accountable decision authority.
- `ResearchPriorityReceipt` binds an artifact hash to declared priority evidence; a local runtime clock alone remains untrusted.
- `ResearchBoundaryAttestation` records a declared research-data boundary; the declaration is not proof that the boundary was enforced.
- `FormalProofRecord` keeps proof-checker state separate from specification-equivalence review.
- `ReplicationReceipt` preserves independent reproduction state and unresolved discrepancies.
- `AgentProvenanceRef` provides bounded machine-run references without requiring a remote telemetry service.

The bundled synthetic case intentionally remains `REVIEW_REQUIRED`: proof checking passes, but specification equivalence and replication are incomplete.

```bash
python scripts/validate_scientific_discovery.py .
```

Expected result:

```text
SCIENTIFIC DISCOVERY PROFILE PASS
```

That PASS establishes only the declared contracts and synthetic cross-record invariants; it does not certify the discovery.

## Runtime privacy

The installed FMA runtime makes no remote API calls, emits no telemetry, and performs no default uploads. Package installation and hosted CI may use their configured package/repository networks; runtime assurance checks operate on local files.

## Repository map

```text
frontier-mission-assurance/
├── src/frontier_assurance/      # reference implementation
├── schemas/                     # portable JSON Schemas
├── profiles/                    # bounded assurance profiles
│   └── scientific-discovery/    # scientific-discovery contracts
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

A minimal assumption:

```yaml
- id: ASSUMP-001
  kind: assumption
  title: Integrated behavior remains inside the declared envelope
  status: open
```

FMA intentionally does **not** calculate an engineering priority score from assumption fields. It exposes assumptions, gaps, and dependency impact; consequence, urgency, resource allocation, and final priority remain human-owned.

## Status semantics

Recommended node statuses:

- `proposed` — not yet accepted into the baseline
- `open` — unresolved assumption/risk/evidence gap
- `active` — accepted current baseline
- `verified` — declared verification evidence meets its stated acceptance criteria
- `validated` — declared physical/operational evidence supports intended use
- `planned` — planned activity or experiment
- `complete` — completed activity where `verified`/`validated` is not the correct semantic
- `retired` — intentionally no longer active
- `superseded` — replaced by a newer node

## What a PASS means

A passing FMA validator means the checked artifact met this repository's declared machine-checkable rules. It does **not** establish scientific truth, certify a supplier or subsystem, approve acquisition, establish regulatory compliance, prove mission readiness, authenticate an unsigned artifact's author, establish legal priority, or replace authorized human review.

See [`DISCLAIMER.md`](DISCLAIMER.md), [`PUBLIC_BOUNDARY.md`](PUBLIC_BOUNDARY.md), and [`SECURITY.md`](SECURITY.md).

## Development

```bash
python -m pip install -r requirements-dev.txt
python -m pip install --no-deps -e .
make check
```

Hosted CI additionally rehearses supported Python versions, multiple operating systems, fresh wheel installation, the tracked-file public release boundary, adversarial rejection behavior, fresh reproduction integrity, and the Scientific Discovery Assurance synthetic profile.

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

The current source identity is defined by [`VERSION`](VERSION). The v0.6 line strengthens tracked-file public-boundary enforcement, explicit output-assurance scope, external execution chronology, and calibration-to-execution validity while preserving FMA's deliberately small public scope, Mission Decision Packets, Scientific Discovery Assurance, cross-platform verification, and stable-release automation.

Current deterministic validation expectations and residual limitations are recorded in [`VALIDATION_REPORT.md`](VALIDATION_REPORT.md).

## Copyright and citation

Copyright © 2026 Bridge Node 7. All rights reserved. No reuse license is granted by this release. See [`LICENSE`](LICENSE).

External code contributions are not accepted unless and until Bridge Node 7 intentionally adopts separate inbound-contribution terms; public-safe feedback and bug reports are welcome.

The package metadata intentionally blocks public package-index upload; evaluation artifacts are distributed through the repository release workflow.

Use [`CITATION.cff`](CITATION.cff) and cite the exact tagged release if the public reference materially informs published work.
