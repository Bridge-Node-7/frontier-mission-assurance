# Profile Contract

## Contract version

**FTQC Assurance profile contract:** `0.1`  
**Minimum compatible FMA source baseline:** `0.7.2`

The profile contract version is independent from the containing FMA release version. Consumers should pin both the FMA release and the `profile_version` carried by profile records. Breaking profile-contract changes require a profile-version change.

## Purpose

Provide source-neutral contracts and deterministic reference behavior for preserving the decision basis of a fault-tolerant quantum program as assumptions, evidence, resource estimates, interfaces, and expert judgments change.

## Architectural class

**Frontier Mission Assurance profile.** The profile extends FMA through bounded domain records and references. It does not modify the universal FMA graph ontology.

## Profile ownership

The profile owns:

- the public schemas under this directory;
- synthetic neutral-atom reference fixtures;
- applicability-envelope semantics;
- expert-review-class semantics;
- FTQC-specific reference validation and change-impact demonstration;
- the Workload-to-System Assurance Chain as a non-canonical view.

## Retained system ownership

The surrounding program retains ownership of:

- canonical laboratory, modeling, code, test, document, and supplier records;
- quantum theory and hardware-performance judgments;
- generic FMA graph and Decision Receipt semantics;
- operational and program authority;
- the final consequential decision;
- institutional learning outside the declared profile contracts.

## Inputs

- a declared FTQC system concept and architecture revision;
- resource-estimate records and their assumptions;
- evidence references with bounded applicability;
- declared interface, component, and dependency relationships;
- qualified expert adjudication where required;
- an FMA assurance graph and Decision Receipt.

## Outputs

- profile validation findings;
- a human-readable synthetic Decision Basis report;
- changed-assumption impact over declared dependencies;
- stale-resource-estimate identification;
- evidence applicability changes;
- expert-review reopen conditions;
- decision-reopen indication.

## Decision authority

Machine outputs surface declared structure, change impact, and review conditions. Qualified experts and accountable human owners retain scientific judgment and consequential decision authority.

## Public release policy

Examples are synthetic and contain no real customer, partner, supplier, program, architecture, or operator identity. Nonpublic evidence stays in governed systems and is referenced rather than copied into this profile.
