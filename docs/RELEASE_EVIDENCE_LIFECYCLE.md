# Release Evidence Lifecycle

FMA separates durable source evidence from live GitHub execution evidence so release documentation cannot become stale, recursive, or self-referential.

## Four evidence layers

### 1. Source contract

Versioned files define the public boundary, schemas, CLI behavior, tests, and release acceptance criteria. These files must be reproducible from the source tree alone.

### 2. Source validation

`VALIDATION_REPORT.md` records deterministic source-level checks that can be rerun from the candidate tree. It does not embed a future commit SHA or claim the current state of hosted CI.

### 3. Hosted commit evidence

GitHub Actions proves the exact pushed commit on the declared Python and operating-system matrix. Commit-specific hosted evidence belongs in the Actions run attached to that commit, not in a source file that existed before the commit did.

### 4. Tagged release evidence

A release record binds the accepted tag to the exact commit, successful hosted run, source archive, wheel, and external SHA-256 manifest. The tagged release is the durable public handoff.

## Why this separation matters

Embedding live CI status or the current commit hash inside the source tree creates a recursion problem: changing the receipt creates a new commit, which invalidates the receipt. Keeping commit-specific proof outside the source tree prevents that failure mode.

## Release rule

A green source report is necessary but not sufficient. Public release requires source validation **and** successful hosted evidence on the exact candidate commit **and** the configured human/governance gates.
