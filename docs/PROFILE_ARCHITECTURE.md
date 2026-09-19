# Profile Architecture

Frontier Mission Assurance uses one core assurance language with bounded domain profiles.

```text
FMA core
   ↓
profile contract
   ↓
domain-specific assurance
```

A profile extends FMA for a domain without turning the core graph into a domain ontology and without replacing the systems that own the underlying technical evidence.

## Core ownership

FMA core owns cross-domain contracts and release machinery, including:

- the universal assurance graph and its generic node/relationship semantics;
- research and decision receipt semantics;
- dependency impact, evidence coverage, assumption visibility, and reporting;
- CLI behavior and common verification semantics;
- release scope and distribution controls;
- common CI, packaging, and stable-release controls.

The core must not depend on profile-specific science, mission logic, or specialist terminology.

## Profile ownership

A bounded profile may own:

- domain-specific schemas and record semantics;
- source-neutral examples and reference cases;
- profile-specific validation invariants;
- domain views that project onto the FMA core graph;
- adoption and assurance-scope guidance.

Profiles may depend on the FMA core. The FMA core must remain usable without any one profile.

## Retained domain ownership

The authoritative domain environment retains ownership of the underlying truth and operational record. Depending on the domain, that can include laboratories, source repositories, models, papers, notebooks, test systems, supplier systems, mission systems, or other governed records.

FMA references those records where appropriate. It does not require them to become public or to move into an FMA repository.

Qualified experts and accountable authorities retain scientific, technical, safety, security, regulatory, operational, and consequential decision authority.

## Versioning and compatibility

Three identities can matter at the same time:

1. **FMA release version** — the containing software/reference release.
2. **Profile contract version** — the bounded behavioral contract for a profile.
3. **Record/schema version** — the version declared by an individual portable record when applicable.

Breaking changes to a profile-level behavioral contract require a profile-contract version change. Breaking changes to a portable record require an explicit record/schema version change and migration guidance. Core contract changes follow the same explicit-version principle.

Consumers must not infer stronger compatibility than the declared versions provide.

## Profile discovery manifest

Each maintained profile exposes a small `profile.yaml` discovery manifest. The manifest identifies:

- the profile ID and human-readable name;
- the profile contract version;
- the FMA release in which the profile was introduced;
- the path to the authoritative public `PROFILE_CONTRACT.md`;
- the deterministic profile validator.

The manifest is validated against [`../schemas/profile-manifest.schema.json`](../schemas/profile-manifest.schema.json).

This is intentionally a **discovery contract, not a plugin framework**. It does not load arbitrary code, grant domain authority, or imply that a profile is appropriate for a specific decision.

## Validation

Profiles use the repository's existing assurance machinery rather than creating parallel release systems.

A maintained profile has a bounded validator and source-neutral validation fixtures. Its required validator belongs in the canonical local maintainer gate, hosted CI, and stable-release verification surface when the profile is part of the published release.

`python scripts/validate_profile_manifests.py .` verifies the common profile-discovery surface before profile-specific validators run.

A profile PASS means its declared machine-checkable controls passed. It does not establish the truth, readiness, safety, qualification, or authorization of a real domain system.

## Publication surface

Published profiles contain the schemas, documentation, source-neutral fixtures,
validation logic, and release evidence required to understand and verify the
profile.

Case evidence remains referenced at its authoritative source rather than copied
into the profile repository.

> **Reference authoritative evidence where possible; do not create a second system of record.**

## When a profile stays in this repository

A profile should remain inside Frontier Mission Assurance while it can share the same core contracts, dependencies, release cadence, CI surface, maintainers, and distribution model without materially burdening unrelated users.

Current bounded profiles are:

- Scientific Discovery Assurance;
- Orbital Recovery Assurance;
- FTQC Assurance.

## When separation may be justified

Consider a separate repository only when operational evidence shows one or more durable boundaries such as:

- an independent release cadence;
- specialized or heavy dependencies;
- a materially different runtime or distribution model;
- distinct maintainers and ownership;
- a large independent CI burden;
- profile changes routinely blocking core releases.

Separation is an operational decision, not a cosmetic modularity goal.

## No plugin framework implied

The architecture remains contract-first. The manifest makes bounded profiles easier for humans and automation to discover; it does not create a dynamic plugin runtime. Additional machinery should be introduced only when repeated operational use demonstrates a need for it.
