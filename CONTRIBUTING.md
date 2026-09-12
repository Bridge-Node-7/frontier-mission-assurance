# Contributing

## Release-candidate contribution policy

This release candidate is **All Rights Reserved** while the public license and inbound-contribution terms are still being decided.

Until those terms are intentionally selected, **external code contributions are not accepted**. Public-safe bug reports, reproducibility reports, and documentation feedback are welcome through the repository's issue forms. Maintainer changes must continue to satisfy the complete V&V and OPSEC gates.

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
