# CLI Contract

FMA is a local command-line reference implementation. Runtime commands make no remote API calls, emit no telemetry, and perform no default uploads.

## Trust rule

> **Machine PASS states are scoped to the exact control that ran. They do not establish scientific truth, authorization, qualification, compliance, safety, security, or mission readiness.**

## Exit codes

- `0` — the requested check completed successfully.
- `2` — invalid input, failed validation, failed receipt/decision check, or controlled command error.

Malformed YAML/JSON, directory paths supplied where files are required, missing files, invalid arguments, and other controlled input failures are presented as bounded one-line `FAIL:`/`ERROR:` messages with exit code `2`; they should not expose a Python traceback.

## Commands

- `fma validate GRAPH` — structural/semantic graph validation.
- `fma assumptions GRAPH` — deterministic listing of unresolved assumptions; no priority score.
- `fma coverage GRAPH` — JSON direct-evidence coverage for critical mission/claim/requirement nodes.
- `fma impact GRAPH NODE_ID` — transitive declared dependency impact.
- `fma receipt RECEIPT` — non-executing receipt verification. Version-2 receipts bind declared code, inputs, outputs, and numerical checks; the PASS line reports the number of controls that actually ran.
- `fma reproduce RECEIPT` — explicit trusted-code execution for a version-2 receipt in a fresh declared-artifact workspace, followed by code/input/output/hash and numerical verification.
- `fma decision GRAPH DECISION_RECEIPT` — decision-basis reference verification.
- `fma report GRAPH --out PATH` — human-readable Markdown assurance report. Set `SOURCE_DATE_EPOCH` when byte-reproducible report output is required.
- `fma --version` — installed package version.

Run `fma <command> --help` for positional descriptions and a concrete usage example. Running `fma` with no subcommand exits `2` and points first-time users to [`FIVE_MINUTE_EVALUATION.md`](FIVE_MINUTE_EVALUATION.md).

## Receipt versions

### Version 2.0 — current executable contract

Version-2 receipts require non-empty `code`, `inputs`, `outputs`, and `checks` arrays plus `experiment.entrypoint`. The entrypoint must be one of the declared code artifacts, and the declared command must reference that entrypoint.

`fma reproduce` verifies code and input hashes before execution, creates a temporary workspace containing only the receipt plus declared code and inputs, does **not** copy declared outputs into that workspace, executes the trusted command with `shell=False`, and then verifies the newly present outputs and numerical checks. This prevents a stale output in the caller's working directory from satisfying a fresh reproduction.

The temporary workspace is an integrity control, not a security sandbox or proof of hermetic execution. Trusted code retains the ambient permissions and capabilities of the host process.

### Version 1.0 — legacy verification compatibility

The runtime can still non-executingly verify legacy version-1 receipts for historical continuity. `fma reproduce` refuses version-1 receipts because they do not carry the code-binding and fresh-output semantics required for a current reproduction PASS.
