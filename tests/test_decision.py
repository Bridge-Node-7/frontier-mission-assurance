from pathlib import Path

import yaml

from frontier_assurance.decision import verify_decision
from frontier_assurance.io import load_structured

ROOT = Path(__file__).resolve().parents[1]
GRAPH = ROOT / "examples" / "frontier_program" / "graph.yaml"
DECISION = ROOT / "examples" / "frontier_program" / "decision-receipt.yaml"


def test_decision_receipt_passes():
    result = verify_decision(GRAPH, DECISION)
    assert result.ok, result.errors


def test_decision_reopen_conditions_must_be_list(tmp_path):
    doc = load_structured(DECISION)
    doc["decision"]["reopen_when"] = "not-a-list"
    path = tmp_path / "decision.yaml"
    path.write_text(yaml.safe_dump(doc, sort_keys=False), encoding="utf-8")
    result = verify_decision(GRAPH, path)
    assert not result.ok
    assert any("reopen_when" in error for error in result.errors)
