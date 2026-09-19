# Security and Data Handling

This repository is a public reference implementation. Security guidance here covers the published software, examples, workflows, and release artifacts.

See [`SCOPE.md`](SCOPE.md) for the repository's evaluation and verification scope.

## Supported versions

Only the latest tagged stable release is supported for security fixes. Earlier tags remain reproducible release records, but they are not maintained security branches.

## Reporting a vulnerability

Do **not** disclose suspected vulnerabilities, exploit details, credentials, or sensitive reproduction data in a public issue, pull request, Discussion, commit, branch name, or Actions artifact.

Use this repository's GitHub Security page and private vulnerability-reporting flow when that control is available. Include the affected release or commit, a concise impact description, the smallest reproduction sufficient for triage, and any proposed mitigation. Do not include unrelated sensitive material.

If private reporting is not available in the viewer's GitHub session, do not publish exploit details as a workaround; use an established non-public reporting channel.

## Automated security controls

The repository uses bounded, fail-visible controls as defense in depth:

- Dependabot monitors Python and GitHub Actions dependencies.
- Pull-request V&V performs dependency vulnerability review for high-severity findings.
- Protected-main V&V performs CodeQL analysis for Python before a stable release can be triggered.
- GitHub Actions are pinned to immutable commit SHAs.
- Runtime regression tests prohibit common network-client imports in the installed FMA package.
- Version-2 receipt tests verify code/input binding and fresh-output reproduction behavior.
- The release-hygiene check rejects unsupported artifact types and obvious secret-like material.

These controls reduce risk; they do not prove the absence of vulnerabilities, malicious dependencies, sensitive proper nouns, or unsafe operational use.

## Reporting surface

Issues, pull requests, Actions logs, uploaded artifacts, Discussions, release notes, commit history, branch names, and filenames are part of the repository's observable surface. Use the private vulnerability-reporting path for sensitive security reports.

## Executing research receipts

`fma receipt` is verification-only and does not execute the declared experiment command.

`fma reproduce` **does execute trusted repository code** and accepts only the current version-2 executable receipt contract. It verifies declared code and input hashes before execution, requires the command to reference the declared entrypoint, creates a fresh temporary workspace that does not contain declared outputs, runs the command with `shell=False`, and then verifies the resulting output hashes and numerical checks.

The fresh workspace prevents a stale checked-in result from satisfying a current reproduction PASS, but it is **not a sandbox or hermetic execution environment**. Trusted code can still use permissions, interpreters, libraries, environment variables, devices, files, and other capabilities available from the host.

Do not run `fma reproduce` on an untrusted receipt, checkout, fork, pull request, or artifact. Review the command and bound code first and use an appropriately isolated execution environment when the consequence warrants it.

Legacy version-1 research receipts remain usable for non-executing historical verification. They are not eligible for the current fresh-reproduction PASS because they do not carry the version-2 code-binding and fresh-output semantics.

## Operational use

Use an access-controlled environment with appropriate identity, authorization, retention, audit, backup, and incident-response controls for real program data. Do not mirror real evidence into this public repository.

If sensitive information or credentials are committed, assume exposure occurred. Rotate affected credentials immediately and follow the relevant incident-response process. History rewriting alone is not sufficient remediation.
