from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

EXPECTED = {
    "schemas/assurance-graph.schema.json": (
        "https://bridge-node-7.github.io/frontier-mission-assurance/assurance-graph.schema.json"
    ),
    "schemas/research-receipt.schema.json": (
        "https://bridge-node-7.github.io/frontier-mission-assurance/research-receipt.schema.json"
    ),
    "schemas/decision-receipt.schema.json": (
        "https://bridge-node-7.github.io/frontier-mission-assurance/decision-receipt.schema.json"
    ),
}


def test_core_schema_ids_are_stable_and_unique():
    observed = {}
    for relative, expected in EXPECTED.items():
        document = json.loads((ROOT / relative).read_text(encoding="utf-8"))
        observed[relative] = document.get("$id")
        assert observed[relative] == expected
    assert len(set(observed.values())) == len(EXPECTED)
