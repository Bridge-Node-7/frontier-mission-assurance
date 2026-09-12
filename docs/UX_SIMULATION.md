# Current UX Simulation

FMA v0.2.0-rc8 is intentionally a Git/CLI reference implementation rather than a graphical product.

## Current surfaces

1. **CLI** — validation, assumption visibility, evidence coverage, dependency impact, receipt verification, explicit reproduction, decision-basis checks, and report generation.
2. **GitHub-native workflow** — pull-request checklist, issue forms, CI, validation evidence, and release receipts.
3. **Markdown report** — human-readable summary of direct evidence coverage and unresolved assumptions.

## Primary technical journey

```text
clone / unpack
  ↓
create isolated Python environment
  ↓
install package
  ↓
validate synthetic graph
  ↓
list unresolved assumptions
  ↓
inspect direct evidence gaps
  ↓
verify research receipt
  ↓
verify decision basis
  ↓
generate report
```

## Trust boundary

`fma receipt` reviews declared evidence without executing code.

`fma reproduce` is a separate, explicit trusted-code operation.

## Non-goal

This release does not claim to provide a hosted application, graphical dashboard, customer portal, or private operational case-management system.
