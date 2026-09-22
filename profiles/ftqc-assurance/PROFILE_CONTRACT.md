# Profile Contract

## Contract version

**FTQC Assurance profile contract:** `0.2`  
**Profile introduced in FMA:** `0.8.0`  
**Contract 0.2 first supported by FMA:** `0.10.0`

The profile contract version is independent from the FMA release version. Consumers should pin both the FMA release and the `profile_version` carried by profile records. Contract 0.2 preserves the original record types and permits a non-synthetic resource-estimate result to declare `synthetic_only: false`; public synthetic references must still declare `synthetic_only: true`. Breaking profile-contract changes require a profile-version change.

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

## Authority boundary

The profile does not replace authoritative technical records, domain judgment,
the FMA core contracts, or consequential decision authority. Those remain with
the processes responsible for the underlying system and decision.

## Inputs

- a declared FTQC system concept and architecture revision;
- resource-estimate records and their assumptions;
- evidence references with bounded applicability;
- reviewed serialized technical-evidence artifacts may be adopted through an explicit fail-closed adapter without importing the producer implementation;
- declared interface, component, and dependency relationships;
- qualified expert adjudication where required;
- an FMA assurance graph and Decision Receipt.

## Case validation

Contract 0.2 supports case directories using the same six-file shape as the public reference. `scripts/validate_ftqc_case.py` validates the declared profile records, cross-record references, assurance graph, decision receipt, applicability gates, and expert-review gates without relocating authoritative evidence or granting new technical authority.

## External technical-evidence adoption

FMA 0.11.1 keeps the 0.11.0 adapter semantics unchanged but moves reviewed producer-release compatibility into `compatibility/reviewed-producers.json`. Contract identity and exact schema SHA-256 remain code-enforced; the registry only records which producer releases have completed explicit review. A future producer release remains rejected until the registry is deliberately reviewed and updated.

FMA 0.11.0 adds a bounded adapter for reviewed FTQC ExperimentResult and
ProcessorEvidenceReceipt artifacts. The producer-owned schemas remain external;
FMA verifies exact reviewed schema digests plus trusted artifact SHA-256 values
before mapping only the minimum semantics required by profile contract 0.2.

This is an adoption boundary, not a new profile contract. Processor technical
status remains distinct from FMA applicability, authority, reproduction state,
expert review, and decision disposition.

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

## Public evaluation scope

The public contract is evaluated with source-neutral synthetic examples. Applied
cases reference authoritative evidence rather than copying it into the profile.
