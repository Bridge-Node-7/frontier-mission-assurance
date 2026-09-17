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
- `fma receipt RECEIPT` — non-executing receipt verification for supported receipt versions. Version 2 binds exact local code/input/output identity. Version 3 preserves exact code/input identity while adding explicit output-assurance, calibration, and local/external execution evidence.
- `fma reproduce RECEIPT` — explicit trusted-code execution for version-2 receipts and version-3 receipts whose execution mode is `LOCAL`, in a fresh declared-artifact workspace. Version-3 `EXTERNAL` receipts are verified as collected execution evidence and are not launched by this command.
- `fma decision GRAPH DECISION_RECEIPT` — decision-basis reference verification.
- `fma report GRAPH --out PATH` — human-readable Markdown assurance report. Set `SOURCE_DATE_EPOCH` when byte-reproducible report output is required.
- `fma --version` — installed package version.

Run `fma <command> --help` for positional descriptions and a concrete usage example. Running `fma` with no subcommand exits `2` and points first-time users to [`FIVE_MINUTE_EVALUATION.md`](FIVE_MINUTE_EVALUATION.md).

## Receipt versions

### Version 3.1 — current v3 contract

Version 3.1 is the current version-3 contract. It preserves exact SHA-256 identity for declared code and inputs and preserves an observed SHA-256 for every output. Each output also declares its assurance semantics explicitly as `EXACT`, `SEMANTICALLY_CHECKED`, or `RECORD_ONLY`.

- `EXACT` requires the declared exact-output identity.
- `SEMANTICALLY_CHECKED` binds the output to declared checks for that same output and treats those checks as the bounded equivalence claim.
- `RECORD_ONLY` records output provenance without making an equivalence claim.

Version 3 also supports calibration/instrument-state evidence and `LOCAL` or `EXTERNAL` execution records. `LOCAL` receipts can be reproduced through the fresh-workspace path. `EXTERNAL` receipts are evidence-verification contracts; `fma reproduce` does not submit or launch the external scheduler workflow.

### Version 3.0 — retained v3 compatibility

Version 3.0 remains supported for backward compatibility with the original version-3 receipt-wide acceptance model. Consumers must preserve its declared semantics and must not silently reinterpret a 3.0 record as a 3.1 per-output assurance record.

### Version 2.0 — exact local reproduction

Version-2 receipts require non-empty `code`, `inputs`, `outputs`, and `checks` arrays plus `experiment.entrypoint`. The entrypoint must be one of the declared code artifacts, and the declared command must reference that entrypoint.

`fma reproduce` verifies code and input hashes before execution, creates a temporary workspace containing only the receipt plus declared code and inputs, does **not** copy declared outputs into that workspace, executes the trusted command with `shell=False`, and then verifies the newly present outputs and numerical checks. This prevents a stale output in the caller's working directory from satisfying a fresh reproduction.

The temporary workspace is an integrity control, not a security sandbox or proof of hermetic execution. Trusted code retains the ambient permissions and capabilities of the host process.

### Version 1.0 — historical verification compatibility

The runtime can still non-executingly verify version-1 receipts for historical continuity. `fma reproduce` refuses version-1 receipts because they do not carry the code-binding and fresh-output semantics required for a current reproduction PASS.
