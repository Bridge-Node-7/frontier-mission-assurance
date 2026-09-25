# Scientific Discovery Assurance

**Evidence architecture for machine-assisted and computational discovery.**

Scientific Discovery Assurance keeps provenance, specification, priority, proof state, replication, attribution, and accountable decision ownership explicit from candidate discovery through institutional review.

The profile is designed for work where computational speed can exceed the natural pace of evidence organization. Its role is to preserve a reviewable chain from the originating problem and source material to proof, replication, attribution, and the final governed decision.

See [`PROFILE_CONTRACT.md`](PROFILE_CONTRACT.md) for the profile boundary, ownership model, and decision-authority contract.

## Contract set

- `DiscoveryPassport` — discovery claim, contributors, provenance, verification state, attribution chronology, scope, and decision authority.
- `ResearchPriorityReceipt` — artifact hash with declared priority evidence.
- `ResearchBoundaryAttestation` — declared research-data handling boundary and supporting evidence references.
- `FormalProofRecord` — proof-system result kept distinct from specification-equivalence review.
- `ReplicationReceipt` — independent reproduction state and unresolved discrepancies.
- `AgentProvenanceRef` — portable references to machine runs without exposing an internal telemetry graph.

## Assurance path

```text
Problem specification
        ↓
Candidate discovery
        ↓
Source + trigger provenance
        ↓
Priority evidence
        ↓
Research-boundary evidence
        ↓
Formal proof when applicable
        ↓
Adversarial review
        ↓
Independent replication
        ↓
Discovery Passport
        ↓
Accountable institutional decision
```

## Decision semantics

The profile keeps distinct evidence states distinct:

- artifact identity is separate from scientific validity;
- a research-boundary declaration is separate from evidence of enforcement;
- proof-checker success is separate from specification equivalence;
- replication is a separate evidence object;
- attribution events can coexist without forcing an automated single-winner conclusion;
- consequential publication, deployment, and mission decisions remain with accountable authorities.

This separation is a strength of the profile: machine-verifiable evidence can accelerate review without collapsing scientific judgment into a single automated state.

See [`ASSURANCE_SCOPE.md`](ASSURANCE_SCOPE.md), [`SPECIFICATION_EQUIVALENCE.md`](SPECIFICATION_EQUIVALENCE.md), and [`ATTRIBUTION.md`](ATTRIBUTION.md).

## Public evaluation scope

Public worked examples are source-neutral and suitable for unrestricted
evaluation. They demonstrate the profile contracts without implying a stronger
scientific conclusion.

## Verify

```bash
python -m pip install "jsonschema==4.26.0"
python scripts/validate_scientific_discovery.py .
```

Expected result:

```text
SCIENTIFIC DISCOVERY PROFILE PASS
```

## Verification scope

The bundled reference case remains `REVIEW_REQUIRED` by design because specification-equivalence review and independent replication are incomplete. That state demonstrates that the profile preserves unresolved scientific obligations rather than converting partial evidence into a stronger claim.

A PASS confirms the declared profile contracts and cross-record invariants exercised by the validation set. Scientific conclusions remain tied to the evidence and review processes responsible for the underlying discovery.
