# FTQC processor-evidence adapter

FMA can consume bounded FTQC technical evidence without becoming the simulator,
processor evaluator, or evidence store.

The source-profile adapter at
`scripts/ftqc_processor_evidence_adapter.py` accepts two serialized artifacts:

1. `na-ftqc.experiment-result/2.0.0`
2. `na-ftqc.processor-evidence-receipt/2.0.0`

The producing domain remains authoritative for those portable contracts. FMA
does **not** copy their schema files into this repository. Instead the operator
supplies the exact schema files alongside the artifacts; the adapter verifies
their reviewed SHA-256 identities before JSON Schema validation.

## Current reviewed identities

- ExperimentResult schema SHA-256:
  `923f28bd45729008f54eea09281caacf359311f9a7e0486344d41a336a4c3c33`
- ProcessorEvidenceReceipt schema SHA-256:
  `1e8c164ddabbf1f6a1f0274e3b3225ec2ba81a1a566a33d69d00b91e1788ccdb`
- reviewed experiment producer: `naftk 0.5.0`
- reviewed processor producer: `neutral-atom-ftqc-processor-contract 0.4.0`

A future producer release is rejected until explicitly reviewed even if it uses
the same portable schema.

## Mapping rules

The adapter preserves the source result and only projects the minimum FMA state
needed for assurance work:

- current `decoder_backlog` model evidence → `SIMULATED`;
- `GENERATED` → reproduction `NOT_ASSESSED`;
- `REPRODUCED` → reproduction `REPRODUCED`;
- cross-architecture comparison → applicability `REVIEW_REQUIRED`;
- same declared configuration → applicability `IN_SCOPE`, while authority
  remains `DECLARED`;
- `WITHIN_TARGET_ENVELOPE` → `RE-EVALUATION_OPPORTUNITY`, never approval;
- unfavorable technical status → bounded `REVIEW_REQUIRED`, not a mission or
  company-level conclusion.

The resulting evidence-validity envelope uses existing FTQC Assurance profile
contract `0.2`. No new FMA graph ontology and no assurance-context `0.2.0`
are introduced.

## Authority boundary

Schema validity, hash integrity, and a processor technical status do not establish
scientific truth, hardware readiness, system applicability, certification,
independent V&V, or consequential authority. Qualified review and accountable
human decision ownership remain required.

## Public/private boundary

The adapter accepts artifact paths. Real protected evidence stays in the system
authorized to hold it. The public FMA repository contains no customer-specific
architecture, raw evidence, or private producer artifact.
