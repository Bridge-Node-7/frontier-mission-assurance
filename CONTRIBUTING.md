# Contributing

## Contribution policy

This public reference is **All Rights Reserved**. No reuse license is granted by this release.

**External code contributions are not accepted** unless and until Bridge Node 7 intentionally adopts separate inbound-contribution terms. Public-safe bug reports, reproducibility reports, and documentation feedback are welcome through the repository's issue forms. Maintainer changes must continue to satisfy the complete V&V and public-boundary gates.

## Principle

Prefer small changes that improve one claim-to-evidence-to-decision path.

## Before a maintainer PR

```bash
python -m pip install -e '.[dev]'
make check
```

## Evidence quality

When adding evidence, record:

- source/provenance;
- what exact claim it supports;
- conditions under which it is valid;
- limitations;
- independence level when material;
- whether the evidence is analytical, computational, simulated, experimental, or operational.

Do not convert inference into fact. If evidence is only suggestive, encode uncertainty explicitly.
