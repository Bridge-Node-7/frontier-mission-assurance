# Current UX Simulation

FMA v0.3.1 is intentionally a Git/CLI reference implementation rather than a graphical product.

## Current surfaces

1. **CLI** — validation, assumption visibility, evidence coverage, dependency impact, receipt verification, explicit reproduction, decision-basis checks, and report generation.
2. **GitHub-native workflow** — pull-request checklist, issue forms, CI, validation evidence, dependency vulnerability review, protected-main CodeQL, and release records.
3. **Markdown report** — human-readable summary of direct evidence coverage and unresolved assumptions.
4. **Research Reproducibility Contract** — human-facing environment/execution/result expectations paired with machine-readable receipts.
5. **Scientific Discovery Assurance profile** — portable schemas, synthetic linked records, and a deterministic profile validator for discovery provenance, priority evidence, research-boundary declarations, formal-proof/specification separation, replication, and attribution chronology.

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
validate synthetic scientific-discovery profile
  ↓
generate / inspect bounded evidence outputs
```

## Simulated personas

### First-time technical reviewer

Expected: understand purpose, public/private boundary, non-claims, and evaluation path without reading implementation code.

### Clean-machine developer

Expected: follow documented install/evaluation commands and receive bounded, fail-visible results.

### Research/reproducibility user

Expected: distinguish non-executing receipt verification from explicit trusted reproduction and inspect declared hashes/tolerances.

### Scientific-discovery reviewer

Expected: distinguish structural validity from scientific truth, local chronology from trusted priority, a declared privacy boundary from proof of enforcement, formal proof checking from specification validation, and partial replication from completed reproduction.

### Security / OPSEC reviewer

Expected: identify the public-data boundary, scanner behavior, prohibited artifact types, runtime privacy posture, vulnerability-reporting path, dependency-review gate, and main-line static analysis quickly.

### Release engineer

Expected: distinguish source validation from hosted commit evidence and tagged release evidence without recursive or stale receipts.

### Logged-out public visitor

Expected: understand purpose, maturity, licensing, non-claims, five-minute evaluation, scientific-discovery profile, and public/private boundary without authentication or private context.

### External clean-user evaluator

Expected: start from a clean environment, follow only documented commands, reach the declared bounded results, and distinguish successful mechanics from mission readiness or scientific acceptance.

## Trust boundary

`fma receipt` reviews declared evidence without executing code.

`fma reproduce` is a separate, explicit trusted-code operation.

The Scientific Discovery Assurance profile validates declared contracts and selected cross-record invariants; it does not certify a discovery.

## Non-goal

This release does not claim to provide a hosted application, graphical dashboard, customer portal, private operational case-management system, scientific certification authority, provider-enforcement audit system, or proof that every software vulnerability has been eliminated.
