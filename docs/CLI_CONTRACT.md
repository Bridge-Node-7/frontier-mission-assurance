# CLI Contract

FMA is a local command-line reference implementation. Runtime commands make no remote API calls, emit no telemetry, and perform no default uploads.

## Exit codes

- `0` — the requested check completed successfully.
- `2` — invalid input, failed validation, failed receipt/decision check, or controlled command error.

## Commands

- `fma validate GRAPH` — structural/semantic graph validation.
- `fma assumptions GRAPH` — deterministic listing of unresolved assumptions; no priority score.
- `fma coverage GRAPH` — JSON direct-evidence coverage for critical mission/claim/requirement nodes.
- `fma impact GRAPH NODE_ID` — transitive declared dependency impact.
- `fma receipt RECEIPT` — non-executing hash/numerical verification.
- `fma reproduce RECEIPT` — explicit trusted-code execution followed by receipt verification.
- `fma decision GRAPH DECISION_RECEIPT` — decision-basis reference verification.
- `fma report GRAPH --out PATH` — human-readable Markdown assurance report.
- `fma --version` — installed package version.

## Trust rule

Machine PASS states are scoped to the exact control that ran. They do not establish scientific truth, authorization, qualification, compliance, safety, security, or mission readiness.
