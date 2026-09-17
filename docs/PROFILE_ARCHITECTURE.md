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
- public/private release boundaries;
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

## Validation

Profiles use the repository's existing assurance machinery rather than creating parallel release systems.

A maintained profile should have a bounded validator and source-neutral validation fixtures. Its required validator belongs in the canonical local maintainer gate, hosted CI, and stable-release verification surface when the profile is part of the published release.

A profile PASS means its declared machine-checkable controls passed. It does not establish the truth, readiness, safety, qualification, or authorization of a real domain system.

## Public/private boundary

Public profile material may include schemas, generic documentation, synthetic or sanitized fixtures, validation logic, and release evidence.

Customer, partner, supplier, program, proprietary architecture, controlled technical data, credentials, private links, protected logs, and other nonpublic evidence remain in governed environments.

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

This architecture is contract-first. A profile manifest or plugin runtime is not required for a profile to be valid. Additional machinery should be introduced only when repeated operational use demonstrates a need for it.
