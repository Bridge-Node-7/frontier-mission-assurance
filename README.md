# Frontier Mission Assurance

**Mission assurance for frontier teams moving faster than their evidence can naturally stay organized.**

Frontier Mission Assurance (FMA) is a deliberately small public reference layer for connecting:

**Mission → claim → assumption → experiment → evidence → decision**

in ordinary version-controlled files.

It is designed for small, interdisciplinary teams building difficult systems under uncertainty. The goal is not more process. The goal is to make the decision basis inspectable: what must be true, what is directly supported, what is still assumed, what has been reproduced, what changed, and what a human can justify doing next.

> **Public boundary:** this repository contains software, public documentation, and synthetic fixtures. It is not a repository for real mission evidence or sensitive program data. See [`PUBLIC_BOUNDARY.md`](PUBLIC_BOUNDARY.md) and [`SECURITY.md`](SECURITY.md).

## The mission-oriented question

A technical leader should be able to answer five questions without reconstructing the program from notebooks, tickets, slide decks, chat threads, experiment folders, and tribal knowledge:

1. **What must be true for the mission to succeed?**
2. **Which claims are supported by direct evidence, and which still depend on assumptions?**
3. **Which important results have been reproduced or independently challenged?**
4. **What decisions or interfaces are affected when a dependency changes?**
5. **What decision can an accountable human justify now—and what would change that decision?**

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

## Mission Decision Packet

A **Mission Decision Packet** is the smallest reviewable bundle that connects one consequential technical decision to its evidence, assumptions, reproduction state, dependencies, and explicit conditions for reopening the decision.

The key question is not only:

> Why did we decide this?

It is also:

> **What would make us revisit it?**

That turns a one-time review into a change-sensitive decision record without automating accountable human judgment.

Start with the worked synthetic example in [`examples/frontier_program/`](examples/frontier_program/) and the pattern in [`docs/MISSION_DECISION_PACKET.md`](docs/MISSION_DECISION_PACKET.md).

## Where FMA creates leverage

- **AI-assisted research** — preserve provenance and require evidence gates instead of treating generated output as established fact.
- **Cross-disciplinary integration** — connect theory, software, controls, experimental hardware, interfaces, and system evidence without forcing them into one tool.
- **Design and readiness reviews** — make direct evidence, open assumptions, unresolved gaps, and decision basis visible in a repeatable form.
- **Partner and supplier interfaces** — represent what is claimed, required, evidenced, and still uncertain at an interface while keeping sensitive details outside the public repository.
- **Change impact** — show which declared claims, requirements, risks, and decisions may need review when an upstream dependency changes.
- **Small-team velocity** — start with one consequential decision and add only the assurance structure that earns its keep.

For a bounded adoption pattern, see [`docs/MISSION_ORIENTED_ADOPTION.md`](docs/MISSION_ORIENTED_ADOPTION.md).

## Public capabilities

- **Assurance-graph validation** — detect malformed nodes, invalid relations, duplicate identifiers, and dangling references.
- **Open-assumption visibility** — list unresolved assumptions without assigning an automated priority score.
- **Evidence coverage** — identify critical mission/claim/requirement nodes without direct supporting evidence.
- **Dependency impact** — show which declared nodes depend transitively on a changed dependency.
- **Research receipts** — SHA-256-bind declared input/output artifacts to numerical acceptance checks.
- **Explicit reproduction** — `fma reproduce` verifies declared inputs, executes a trusted receipt command, then verifies outputs and tolerances.
- **Decision receipts** — verify that a declared decision basis references nodes in a valid assurance graph.
- **Scientific Discovery Assurance** — portable contracts for discovery provenance, priority evidence, research-boundary declarations, formal-proof/specification separation, replication, and attribution chronology.
- **CI-native V&V** — exercise graph, receipt, decision, schema, package, scientific-discovery, and public-boundary checks on pull requests.

## Five-minute evaluation

Requires Python 3.11 or newer. The bounded evaluation is local-only, non-executing with respect to research receipt commands, and uses synthetic fixtures.

### macOS / Linux

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -e .
.venv/bin/python scripts/evaluate_public_reference.py
```

### Windows PowerShell

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e .
.\.venv\Scripts\python.exe scripts/evaluate_public_reference.py
```

Expected final line:

```text
RESULT - PUBLIC REFERENCE EVALUATION PASS
```

The synthetic fixture intentionally retains a visible critical evidence gap. A PASS means the reference mechanics behaved as declared; it does **not** establish mission readiness. See [`docs/FIVE_MINUTE_EVALUATION.md`](docs/FIVE_MINUTE_EVALUATION.md) for the complete bounded path.

For deeper inspection, use the individual CLI commands described in [`docs/CLI_CONTRACT.md`](docs/CLI_CONTRACT.md). `fma reproduce` is separate because it executes trusted receipt-declared code.

### Runtime privacy

The installed FMA runtime makes no remote API calls, emits no telemetry, and performs no default uploads. Package installation and hosted CI may use their configured package/repository networks; runtime assurance checks operate on local files.

## Repository map

```text
frontier-mission-assurance/
├── src/frontier_assurance/      # reference implementation
├── schemas/                     # portable JSON Schemas
├── profiles/                    # bounded assurance profiles
│   └── scientific-discovery/    # scientific-discovery contracts
├── examples/                    # synthetic worked examples
├── tests/                       # regression, tamper, and boundary tests
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

## Research receipt

A research receipt records provenance and acceptance expectations:

```yaml
receipt_version: "1.0"
experiment:
  id: DEMO-Z-EXPECTATION
  command: python analysis.py
  seed: 1111
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

`fma receipt ...` verifies declared artifact hashes and numerical checks without executing code.

`fma reproduce ...` is an explicit trusted-code operation: it verifies input hashes first, runs the declared command with `shell=False`, then verifies outputs and numerical criteria.

The receipt is a reproducibility record, not a digital signature or scientific certification.

For a human-facing environment/execution/result contract that can accompany research code, see [`docs/RESEARCH_REPRODUCIBILITY_CONTRACT.md`](docs/RESEARCH_REPRODUCIBILITY_CONTRACT.md).

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

A passing FMA validator means the checked artifact met this repository's declared machine-checkable rules. It does **not** establish scientific truth, certify a supplier or subsystem, approve acquisition, establish regulatory compliance, prove mission readiness, establish legal priority, or replace authorized human review.

See [`DISCLAIMER.md`](DISCLAIMER.md), [`PUBLIC_BOUNDARY.md`](PUBLIC_BOUNDARY.md), and [`SECURITY.md`](SECURITY.md).

## Development

```bash
python -m pip install -r requirements-dev.txt
python -m pip install --no-deps -e .
make check
```

Hosted CI additionally rehearses supported Python versions, multiple operating systems, fresh wheel installation, the public release boundary, and the Scientific Discovery Assurance synthetic profile.

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

See [`docs/VV_DOCTRINE.md`](docs/VV_DOCTRINE.md), [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md), [`docs/THREAT_MODEL.md`](docs/THREAT_MODEL.md), [`docs/INTEROPERABILITY.md`](docs/INTEROPERABILITY.md), [`docs/RESEARCH_REPRODUCIBILITY_CONTRACT.md`](docs/RESEARCH_REPRODUCIBILITY_CONTRACT.md), [`docs/RELEASE_EVIDENCE_LIFECYCLE.md`](docs/RELEASE_EVIDENCE_LIFECYCLE.md), [`docs/ACCEPTANCE_CRITERIA.md`](docs/ACCEPTANCE_CRITERIA.md), and [`docs/RELEASE_ACCEPTANCE.md`](docs/RELEASE_ACCEPTANCE.md).

## Current maturity

The current source identity is defined by [`VERSION`](VERSION). The v0.3 line includes Scientific Discovery Assurance, Mission Decision Packets, cross-platform verification, and stable-release automation while preserving a deliberately small public scope.

Current deterministic validation expectations and residual limitations are recorded in [`VALIDATION_REPORT.md`](VALIDATION_REPORT.md).

## Copyright and citation

Copyright © 2026 Bridge Node 7. All rights reserved. No reuse license is granted by this release. See [`LICENSE`](LICENSE).

External code contributions are not accepted unless and until Bridge Node 7 intentionally adopts separate inbound-contribution terms; public-safe feedback and bug reports are welcome.

The package metadata intentionally blocks public package-index upload; evaluation artifacts are distributed through the repository release workflow.

Use [`CITATION.cff`](CITATION.cff) and cite the exact tagged release if the public reference materially informs published work.
