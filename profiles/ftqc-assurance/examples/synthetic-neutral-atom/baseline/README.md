# Synthetic Neutral-Atom Baseline

This fixture is intentionally synthetic. Its values exist only to demonstrate FTQC Assurance contracts and change propagation.

The baseline decision is `HOLD` because two decision-gating Evidence Validity Envelopes (`ENV-RESOURCE-001` and `ENV-LOSS-001`) have only a declared applicability basis. That is a truthful profile behavior, not a conclusion about any real FTQC architecture.

Run from the repository root:

```bash
python scripts/evaluate_ftqc_reference.py .
```
