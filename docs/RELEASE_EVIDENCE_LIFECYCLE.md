# Release Evidence

FMA distinguishes three verification layers:

## Source validation

Versioned source files define the supported schemas, CLI behavior, tests, and validation requirements. `VALIDATION_REPORT.md` records deterministic source-level checks.

## Hosted validation

GitHub Actions records validation results for the source revision under the declared operating-system and Python matrix.

## Published release evidence

A published release binds the supported tag to its source archive, wheel, SHA-256 artifact manifest, and other released verification artifacts.

A source-level PASS does not by itself establish scientific validity, mission readiness, certification, independent V&V, or consequential decision authority.
