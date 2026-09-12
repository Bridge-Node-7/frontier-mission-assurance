# ADR-0001: Minimum Sufficient Assurance

- Status: Accepted
- Date: 2026-09-09

## Context

Frontier research organizations require high iteration speed. Traditional process-heavy V&V can create schedule burden, while weak evidence discipline creates hidden technical debt and late integration failures.

## Decision

FMA will optimize for **minimum sufficient assurance**. The unit of work is not a document; it is a claim linked to the evidence necessary for a consequential decision.

Verification effort should increase with:

- mission consequence;
- uncertainty;
- irreversibility;
- cross-domain coupling;
- independence required for confidence.

## Consequences

Positive:

- low adoption burden;
- Git-native evidence history;
- explicit assumption debt;
- easy automation;
- compatible with AI-assisted research.

Trade-offs:

- scores remain judgment-dependent until connected to executable system models;
- graph validity does not prove scientific truth;
- teams must agree on evidence sufficiency and claim semantics.
