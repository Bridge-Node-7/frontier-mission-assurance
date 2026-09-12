# GitHub Release Checklist Template

This is the reusable acceptance template for staging and potentially publishing FMA under `Bridge-Node-7/frontier-mission-assurance`. **It is not a live status board.** Commit-specific status belongs in GitHub Actions and the tagged release record.

See [`RELEASE_EVIDENCE_LIFECYCLE.md`](RELEASE_EVIDENCE_LIFECYCLE.md) for the evidence model.

## Public-boundary / IP gate

- [ ] The candidate is intentionally limited to the public reference layer.
- [ ] No private operational repository names, architecture, customer/program context, or private decision logic are disclosed.
- [ ] Licensing is selected intentionally before any public visibility or release change.
- [ ] A separate private proper-noun/context review passes without embedding the private denylist in this repository.

## Repository identity

- [ ] Repository name is exactly `frontier-mission-assurance`.
- [ ] Default branch is `main`.
- [ ] `PUBLIC_BOUNDARY.md`, `OPSEC.md`, `DISCLAIMER.md`, `SECURITY.md`, `docs/PUBLIC_REFERENCE_BOUNDARY.md`, and `VALIDATION_REPORT.md` are present.

## Hosted V&V

- [ ] Push only the reviewed candidate commit.
- [ ] Confirm `V&V CI` starts successfully.
- [ ] Python 3.11 / Ubuntu passes.
- [ ] Python 3.12 / Ubuntu passes.
- [ ] Python 3.13 / Ubuntu passes.
- [ ] Ubuntu/macOS/Windows smoke jobs pass.
- [ ] Wheel build + fresh dependency-resolving install passes.
- [ ] Ruff passes.
- [ ] Public-release OPSEC scan passes.
- [ ] Pull-request dependency vulnerability review passes when applicable.
- [ ] Protected-main CodeQL analysis passes before stable release eligibility.
- [ ] Scientific Discovery Assurance synthetic profile validation passes when present.
- [ ] Synthetic assurance-report artifacts upload successfully.

## Governance

- [ ] Protect `main` with required hosted checks.
- [ ] Block force-push and deletion of protected `main`.
- [ ] Review security/secret-scanning controls available to the account/repository.
- [ ] Confirm the vulnerability-reporting policy remains accurate for the repository's available private-reporting controls.
- [ ] Review dependency-update behavior.
- [ ] Confirm workflow permissions remain least-privilege.
- [ ] Confirm only intended long-lived branches remain.
- [ ] Confirm no stale/open PR or issue blocks release.

## Public UX

- [ ] README renders correctly.
- [ ] Five-minute evaluation is easy to find.
- [ ] macOS/Linux and Windows PowerShell paths are correct.
- [ ] Local documentation links resolve.
- [ ] Scientific Discovery Assurance documentation and synthetic example are discoverable when included.
- [ ] No external person, customer, supplier, partner, program, or real research identity appears in public examples.
- [ ] The repository does not imply a graphical UI, hosted site, or private operational platform exists.
- [ ] Issue forms render and remain usable without custom repository-label setup.
- [ ] Logged-out public GitHub UAT passes after public-surface changes.
- [ ] External clean-user evaluation passes before a stable release.

## Release

- [ ] Hosted CI passes on the exact release commit.
- [ ] Generate a complete tracked-source SHA-256 manifest from the exact release commit as a release artifact rather than embedding commit-specific hashes back into source.
- [ ] Generate source ZIP and wheel from the exact release commit.
- [ ] Generate the external release-artifact SHA-256 manifest.
- [ ] Confirm the frozen source archive reconstructs to the exact accepted Git tree and verifies against the tracked-source manifest.
- [ ] Create the GitHub tag/release from the exact passing commit.
- [ ] Bind exact commit SHA and Actions run in the release record.

## Profile integration

- [ ] Keep the Bridge Node 7 public profile link accurate after public release changes.
- [ ] Make surgical profile edits only when public positioning actually changes.

## Final acceptance rule

Do not promote a stable release when any required gate is red, skipped unexpectedly, unresolved, or materially different from the reviewed candidate.
