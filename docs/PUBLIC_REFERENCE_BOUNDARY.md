# Public Reference Boundary

Frontier Mission Assurance is intentionally a **public reference implementation**, not a canonical operational assurance kernel.

## What this repository exposes

- portable assurance-graph structure;
- minimal structural and semantic validation;
- open-assumption visibility;
- direct evidence-coverage checks;
- simple dependency-impact traversal;
- research-receipt verification and explicit trusted reproduction;
- decision-basis reference checks;
- synthetic examples;
- public-safe CI and OPSEC controls.

## What this repository intentionally does not expose

- internal operational graph topology or canonical private object ownership;
- private evidence stores or customer/program identifiers;
- proprietary prioritization, attention, scoring, inference, or optimization logic;
- private failure-domain reasoning;
- classification or internal access-control semantics;
- private adapters, connectors, dashboards, or cross-program analytics;
- real program evidence, performance values, schedules, risks, or decision records.

## Interoperability rule

Private systems may consume or emit compatible public contracts, but interoperability does not require disclosure of private implementation details. Public artifacts should be treated as bounded interchange/reference formats, not as a description of internal architecture.

## Human authority

This repository can verify declared structure, artifact integrity, and selected acceptance checks. It does not autonomously determine engineering priority or make consequential decisions.
