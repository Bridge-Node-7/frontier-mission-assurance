# Frontier Mission Assurance

**Public reference implementation for evidence-native verification, validation, and mission assurance.**

Frontier Mission Assurance (FMA) is a deliberately small public reference layer for representing:

**Mission → claim → assumption → experiment → evidence → decision**

in ordinary version-controlled files.

Its purpose is to make traceability, evidence gaps, reproducibility, and decision basis easier to inspect without turning fast technical work into process-heavy bureaucracy.

> **Public boundary:** this repository contains only software, public-safe documentation, and synthetic fixtures. It is **not** a live program workspace, customer system, canonical operational kernel, or repository for real mission evidence. Do not place personal names, external organization names, private URLs, screenshots, raw logs, credentials, customer/program identifiers, or nonpublic technical evidence in public issues, pull requests, CI artifacts, examples, branches, releases, or commit history. See [`OPSEC.md`](OPSEC.md), [`PUBLIC_BOUNDARY.md`](PUBLIC_BOUNDARY.md), and [`docs/PUBLIC_REFERENCE_BOUNDARY.md`](docs/PUBLIC_REFERENCE_BOUNDARY.md).

## Why this exists

High-consequence engineering decisions often depend on evidence that is scattered across analysis, simulation, experiments, interfaces, and test artifacts. FMA provides a portable reference contract for connecting those artifacts while keeping consequential prioritization and final decisions human-owned.

The public implementation intentionally provides only a bounded set of capabilities:

- **Assurance-graph validation** — detect malformed nodes, invalid relations, duplicate identifiers, and dangling references.
- **Open-assumption visibility** — list unresolved assumptions without assigning an automated priority score.
- **Evidence coverage** — identify critical mission/claim/requirement nodes without direct supporting evidence.
- **Dependency impact** — show which declared nodes depend transitively on a changed dependency.
- **Research receipts** — SHA-256-bind declared input/output artifacts to numerical acceptance checks.
- **Explicit reproduction** — `fma reproduce` verifies declared inputs, executes a trusted receipt command, then verifies outputs and tolerances.
- **Decision receipts** — verify that a declared decision basis references nodes in a valid assurance graph.
- **CI-native V&V** — exercise graph, receipt, decision, schema, package, and public-boundary checks on pull requests.

FMA does **not** expose private operational reasoning, proprietary prioritization, private relationship semantics, customer/program workflows, real evidence, or internal decision systems.

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
├── src/frontier_assurance/      # minimal public reference implementation
├── schemas/                     # portable JSON Schemas
├── examples/                    # synthetic-only worked fixtures
├── tests/                       # positive, regression, tamper, and boundary tests
├── docs/                        # public architecture, V&V doctrine, UAT, release boundary
├── .github/                     # CI + issue/PR public-safety workflows
├── PUBLIC_BOUNDARY.md           # public-data and claim boundary
├── OPSEC.md                     # public-release handling rules
├── scripts/opsec_scan.py        # automated disclosure-pattern scan
├── VALIDATION_REPORT.md         # current release-candidate evidence
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

FMA intentionally does **not** calculate an engineering priority score from assumption fields. It exposes assumptions, gaps, and dependency impact; consequence, urgency, resource allocation, and final priority remain human-owned or belong to private program policy.

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

## GitHub operating model

Every meaningful change should answer at least one of these:

1. What claim changes?
2. What evidence changed?
3. What assumption changed?
4. What decision basis changes?
5. What test prevents regression?

The PR template and issue forms encode that behavior without requiring a separate process system.

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

A passing FMA validator means the checked artifact met this repository's declared machine-checkable rules. It does **not** establish scientific truth, certify a supplier or subsystem, approve acquisition, establish regulatory compliance, prove mission readiness, or replace independent engineering review.

This distinction is intentional: assurance requires explicit evidence and human judgment, not a generic green badge.

## Quickstart: individual commands

```bash
fma validate examples/frontier_program/graph.yaml
fma assumptions examples/frontier_program/graph.yaml
fma coverage examples/frontier_program/graph.yaml
fma impact examples/frontier_program/graph.yaml ASSUMP-CYCLE-COMPOSITION
fma receipt examples/research_receipt/receipt.yaml
fma decision examples/frontier_program/graph.yaml examples/frontier_program/decision-receipt.yaml
fma report examples/frontier_program/graph.yaml --out build/assurance-report.md
```

Explicit trusted reproduction:

```bash
fma reproduce examples/research_receipt/receipt.yaml
```

`fma receipt` does **not** execute code. `fma reproduce` does; run reproduction only on trusted code after reviewing the declared command.

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

See [`docs/VV_DOCTRINE.md`](docs/VV_DOCTRINE.md), [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md), [`docs/THREAT_MODEL.md`](docs/THREAT_MODEL.md), [`docs/INTEROPERABILITY.md`](docs/INTEROPERABILITY.md), [`docs/UAT.md`](docs/UAT.md), and [`docs/RELEASE_CHECKLIST.md`](docs/RELEASE_CHECKLIST.md).

## Current maturity

**v0.2.0-rc8 — public-reference release candidate.**

The repository is intentionally fail-visible: unsupported claims and unresolved assumptions are outputs, not defects to hide. Current verification evidence and residual limitations are recorded in [`VALIDATION_REPORT.md`](VALIDATION_REPORT.md).

## Copyright and citation

Copyright © 2026 Bridge Node 7. All rights reserved. No reuse license is granted by this release candidate. See [`LICENSE`](LICENSE).

External code contributions are not accepted while release-candidate licensing and inbound contribution terms remain unresolved; public-safe feedback and bug reports are welcome.

The release-candidate package metadata intentionally blocks public package-index upload; evaluation artifacts are distributed only through the controlled repository/release workflow.

Use [`CITATION.cff`](CITATION.cff) and cite the exact tagged release if the public reference materially informs published work.
