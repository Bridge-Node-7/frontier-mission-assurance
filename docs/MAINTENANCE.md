# Maintenance and Repository Hygiene

This repository is designed to remain small, inspectable, and release-oriented. Maintenance should preserve that property.

## Branch model

- `main` is the only long-lived branch.
- Feature, maintenance, and dependency branches are temporary.
- Closed or merged work should not leave stale branches.
- Force-push and deletion of protected `main` should be blocked through repository administration.

## Dependency updates

Dependabot checks Python and GitHub Actions dependencies on a bounded schedule. Dependency changes are proposals, not automatic release inputs.

- Patch/minor updates may be evaluated together when risk is low.
- Major-version updates are isolated from a frozen release candidate.
- Security-critical updates may interrupt the normal cadence, but still require the relevant V&V gates.
- GitHub Actions remain pinned to immutable commit SHAs after any update is accepted.
- No dependency PR is auto-merged solely because its upstream release is newer.

## Release-candidate discipline

Once a candidate is frozen, unrelated dependency churn does not enter that candidate. A material source change creates a new candidate identity and requires V&V again.

## Evidence lifecycle

Source validation, hosted commit evidence, and tagged release evidence are separate layers. See [`RELEASE_EVIDENCE_LIFECYCLE.md`](RELEASE_EVIDENCE_LIFECYCLE.md).

## Public-surface hygiene

Before public release, verify the repository tree, branches, pull requests, issues, Actions artifacts, release assets, and commit metadata. Public history is durable disclosure.
