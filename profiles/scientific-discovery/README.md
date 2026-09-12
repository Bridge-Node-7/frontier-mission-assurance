# Scientific Discovery Assurance

Scientific Discovery Assurance is a bounded FMA profile for machine-assisted or computational discovery where provenance, specification, priority, reproduction, and human decision authority must remain explicit.

It is not a scientific certification system and it does not determine truth.

## Contract set

- `DiscoveryPassport` — discovery claim, contributors, provenance, verification state, attribution chronology, limitations, and decision authority.
- `ResearchPriorityReceipt` — artifact hash plus declared priority evidence. Local runtime time alone remains untrusted.
- `ResearchBoundaryAttestation` — declared research-data handling boundary. A declaration is not proof of enforcement.
- `FormalProofRecord` — proof-system result kept separate from specification-equivalence review.
- `ReplicationReceipt` — independent reproduction state and unresolved discrepancies.
- `AgentProvenanceRef` — bounded references to machine runs without publishing a full internal telemetry graph.

## Assurance path

```text
problem specification
        ↓
candidate discovery
        ↓
source + trigger provenance
        ↓
priority receipt
        ↓
research-boundary declaration
        ↓
formal proof record when applicable
        ↓
adversarial review
        ↓
independent replication
        ↓
Discovery Passport
        ↓
accountable human / institutional decision
```

## Deliberate boundaries

- A valid schema does not establish a scientifically valid result.
- A local timestamp does not establish trusted priority.
- A research-boundary attestation records a declaration; independent evidence is required to establish enforcement.
- A proof checker can establish that a formal statement follows under its declared assumptions, but that does not by itself establish that the formal statement matches the intended scientific or mathematical claim.
- Replication remains a separate evidence object.
- Attribution events can coexist; the profile does not collapse credit into a single automated winner.
- Public worked examples are synthetic only.

## Synthetic evaluation

Run:

```bash
python scripts/validate_scientific_discovery.py .
```

Expected result:

```text
SCIENTIFIC DISCOVERY PROFILE PASS
```

The bundled synthetic case intentionally remains `REVIEW_REQUIRED` because specification-equivalence review and replication are incomplete. That unresolved state is part of the demonstration.
