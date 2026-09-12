# Executable Research Receipt Demo

This tiny deterministic example demonstrates provenance and tamper detection without requiring quantum hardware.

The input is a fixed sequence of synthetic ±1 measurement outcomes. `analysis.py` computes their mean, writes `outputs/result.json`, and the receipt binds both input and output with SHA-256 plus a numerical acceptance check.

Re-run:

```bash
python analysis.py
fma receipt receipt.yaml
```

If either the input or output is edited after the receipt is generated, verification fails.
