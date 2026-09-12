# Maintenance and Repository Hygiene

This repository is designed to remain small, inspectable, and release-oriented. Maintenance should preserve that property.

## Branch model

- `main` is the only long-lived branch.
- Feature, maintenance, and dependency branches are temporary.
- Closed or merged work should not leave stale branches.
- Force-push and deletion of protected `main` should be blocked through repository administration.

## Dependency and security updates

Dependabot checks Python and GitHub Actions dependencies on a bounded schedule. Dependency changes are proposals, not automatic release inputs.

- Pull requests are subject to high-severity dependency vulnerability review inside the existing required V&V path.
- Protected-main pushes run CodeQL for Python inside the existing required Python 3.12 V&V path.
- Patch/minor updates may be evaluated together when risk is low.
- Major-version updates are isolated from a frozen release candidate.
- Security-critical updates may interrupt the normal cadence, but still require the relevant V&V gates.
- GitHub Actions remain pinned to immutable commit SHAs after any update is accepted.
- First-party Actions should remain on supported Node runtimes; runtime-major migrations are treated as reviewed maintenance changes.
- Build-backend/tooling versions are pinned for release candidates to reduce environment drift.
- No dependency PR is auto-merged solely because its upstream release is newer.

## Release-candidate discipline

Once a candidate is frozen, unrelated dependency churn does not enter that candidate. A material source change creates a new candidate identity and requires V&V again.

## Evidence lifecycle

Source validation, hosted commit evidence, and tagged release evidence are separate layers. See [`RELEASE_EVIDENCE_LIFECYCLE.md`](RELEASE_EVIDENCE_LIFECYCLE.md).

## Issue intake

Issue forms are intentionally self-describing and do not require custom repository labels to render or accept a public-safe report. Classification may be added later through repository administration, but issue intake must not depend on hidden setup.

Security vulnerabilities are different: suspected exploit details must not be posted through public issue intake. Follow [`../SECURITY.md`](../SECURITY.md).

## Public-surface hygiene

Before public release, verify the repository tree, branches, pull requests, issues, Actions artifacts, release assets, and commit metadata. Public history is durable disclosure.
