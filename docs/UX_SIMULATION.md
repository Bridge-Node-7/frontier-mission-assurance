# Current UX Simulation

FMA v0.2.0-rc10 is intentionally a Git/CLI reference implementation rather than a graphical product.

## Current surfaces

1. **CLI** — validation, assumption visibility, evidence coverage, dependency impact, receipt verification, explicit reproduction, decision-basis checks, and report generation.
2. **GitHub-native workflow** — pull-request checklist, issue forms, CI, validation evidence, and release records.
3. **Markdown report** — human-readable summary of direct evidence coverage and unresolved assumptions.
4. **Research Reproducibility Contract** — human-facing environment/execution/result expectations paired with machine-readable receipts.

## Primary technical journey

```text
clone / unpack
  ↓
create isolated Python environment
  ↓
install package
  ↓
run bounded five-minute evaluation
  ↓
validate synthetic graph
  ↓
list unresolved assumptions
  ↓
inspect direct evidence gaps
  ↓
verify research receipt
  ↓
optionally reproduce trusted code
  ↓
verify decision basis
  ↓
generate report
```

## Simulated personas

### First-time technical reviewer

Expected: understand purpose, public/private boundary, non-claims, and evaluation path without reading implementation code.

### Clean-machine developer

Expected: follow documented install/evaluation commands and receive bounded, fail-visible results.

### Research/reproducibility user

Expected: distinguish non-executing receipt verification from explicit trusted reproduction and inspect declared hashes/tolerances.

### Security / OPSEC reviewer

Expected: identify the public-data boundary, scanner behavior, prohibited artifact types, and runtime privacy posture quickly.

### Release engineer

Expected: distinguish source validation from hosted commit evidence and tagged release evidence without recursive or stale receipts.

### Logged-out public visitor

Expected after publication: understand purpose, maturity, licensing, non-claims, five-minute evaluation, and public/private boundary without authentication or private context.

### External clean-user evaluator

Expected after publication: start from a clean environment, follow only documented commands, reach the declared bounded result, and distinguish successful mechanics from mission readiness.

## Trust boundary

`fma receipt` reviews declared evidence without executing code.

`fma reproduce` is a separate, explicit trusted-code operation.

## Non-goal

This release does not claim to provide a hosted application, graphical dashboard, customer portal, or private operational case-management system.
