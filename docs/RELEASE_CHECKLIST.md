# GitHub Release Checklist

This checklist is the acceptance path for staging and potentially publishing FMA under `Bridge-Node-7/frontier-mission-assurance`.

## Public-boundary / IP gate

- [ ] The candidate is intentionally limited to the public reference layer.
- [ ] No private operational repository names, architecture, customer/program context, or private decision logic are disclosed.
- [ ] Licensing is selected intentionally before any public visibility change.
- [ ] A separate private proper-noun/context review passes without embedding the private denylist in this repository.

## Repository creation

- [ ] Repository name is exactly `frontier-mission-assurance`.
- [ ] Initial visibility is **private**.
- [ ] Default branch is `main`.
- [ ] `PUBLIC_BOUNDARY.md`, `OPSEC.md`, `DISCLAIMER.md`, `SECURITY.md`, `docs/PUBLIC_REFERENCE_BOUNDARY.md`, and `VALIDATION_REPORT.md` are present.

## First push / hosted CI

- [ ] Push only the reviewed release-candidate commit.
- [ ] Confirm `V&V CI` starts successfully.
- [ ] Python 3.11 / Ubuntu passes.
- [ ] Python 3.12 / Ubuntu passes.
- [ ] Python 3.13 / Ubuntu passes.
- [ ] Ubuntu/macOS/Windows smoke jobs pass.
- [ ] Wheel build + fresh dependency-resolving install passes.
- [ ] Ruff passes.
- [ ] Public-release OPSEC scan passes.
- [ ] Synthetic assurance-report artifacts upload successfully.

## Governance

- [ ] Protect `main` with required hosted checks.
- [ ] Block force-push and deletion of protected `main`.
- [ ] Review security/secret-scanning controls available to the account/repository.
- [ ] Review dependency-update behavior.
- [ ] Confirm workflow permissions remain least-privilege.

## Public UX

- [ ] README renders correctly.
- [ ] Five-minute evaluation is easy to find.
- [ ] macOS/Linux and Windows PowerShell paths are correct.
- [ ] Local documentation links resolve.
- [ ] No external person, customer, supplier, partner, or program identity appears.
- [ ] The repository does not imply a graphical UI, hosted site, or private operational platform exists.

## Release

- [ ] Hosted CI passes on the exact release commit.
- [ ] Regenerate `REPO_FILE_MANIFEST.sha256`.
- [ ] Generate source ZIP and wheel from the exact release commit.
- [ ] Generate external SHA-256 manifest.
- [ ] Create the GitHub tag/pre-release from the exact passing commit.
- [ ] Record exact commit SHA and Actions run in the release receipt.

## Profile integration

- [ ] Add FMA to the existing Bridge Node 7 profile only after the repository is publicly reachable.
- [ ] Make a surgical profile edit; do not overwrite newer profile positioning.

## Final acceptance rule

Do not make the repository public or promote a final release when any required gate is red, skipped unexpectedly, unresolved, or materially different from the reviewed candidate.
