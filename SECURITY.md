# Security and Data Handling

This public repository contains only public-safe software, documentation, and synthetic fixtures.

It must not contain credentials, secrets, private keys, personally identifying information, real external program identities in worked examples, proprietary data, private system details, restricted technical data, nonpublic performance values, internal URLs, private repository links, screenshots, or raw logs that reveal private context.

See [`PUBLIC_BOUNDARY.md`](PUBLIC_BOUNDARY.md).

## Supported versions

Only the latest tagged stable release is supported for security fixes. Earlier tags remain reproducible release records, but they are not maintained security branches.

## Reporting a vulnerability

Do **not** disclose suspected vulnerabilities, exploit details, credentials, or sensitive reproduction data in a public issue, pull request, Discussion, commit, branch name, or Actions artifact.

Use this repository's GitHub Security page and private vulnerability-reporting flow when that control is available. Include the affected release or commit, a concise impact description, the smallest public-safe reproduction sufficient for triage, and any proposed mitigation. Do not include real mission/program data or unrelated secrets.

If private reporting is not available in the viewer's GitHub session, do not publish exploit details as a workaround; use an already authorized private Bridge Node 7 contact channel.

## Automated security controls

The repository uses bounded, fail-visible controls as defense in depth:

- Dependabot monitors Python and GitHub Actions dependencies.
- Pull-request V&V performs dependency vulnerability review for high-severity findings.
- Protected-main V&V performs CodeQL analysis for Python before a stable release can be triggered.
- GitHub Actions are pinned to immutable commit SHAs.
- Runtime regression tests prohibit common network-client imports in the installed FMA package.
- Version-2 receipt tests verify code/input binding and fresh-output reproduction behavior.
- The public release boundary check rejects several high-risk disclosure patterns and artifact types.

These controls reduce risk; they do not prove the absence of vulnerabilities, malicious dependencies, sensitive proper nouns, or unsafe operational use.

## Public GitHub is a disclosure surface

Treat public issues, pull requests, Actions logs, uploaded artifacts, Discussions, release notes, commit history, branch names, and filenames as publicly observable. Deleting a file later does not guarantee removal from forks, caches, clones, logs, or history.

## Executing research receipts

`fma receipt` is verification-only and does not execute the declared experiment command.

`fma reproduce` **does execute trusted repository code** and accepts only the current version-2 executable receipt contract. It verifies declared code and input hashes before execution, requires the command to reference the declared entrypoint, creates a fresh temporary workspace that does not contain declared outputs, runs the command with `shell=False`, and then verifies the resulting output hashes and numerical checks.

The fresh workspace prevents a stale checked-in result from satisfying a current reproduction PASS, but it is **not a sandbox or hermetic execution environment**. Trusted code can still use permissions, interpreters, libraries, environment variables, devices, files, and other capabilities available from the host.

Do not run `fma reproduce` on an untrusted receipt, checkout, fork, pull request, or artifact. Review the command and bound code first and use an appropriately isolated execution environment when the consequence warrants it.

Legacy version-1 research receipts remain usable for non-executing historical verification. They are not eligible for the current fresh-reproduction PASS because they do not carry the version-2 code-binding and fresh-output semantics.

## Operational use

Use an access-controlled environment with appropriate identity, authorization, retention, audit, backup, and incident-response controls for real program data. Do not mirror real evidence into this public repository.

If sensitive information or credentials are committed, assume exposure occurred. Rotate affected credentials immediately and follow the relevant incident-response process. History rewriting alone is not sufficient remediation.
