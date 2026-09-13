from copy import deepcopy
from pathlib import Path

import yaml

from frontier_assurance.decision import verify_decision
from frontier_assurance.io import load_structured

ROOT = Path(__file__).resolve().parents[1]
GRAPH = ROOT / "examples" / "frontier_program" / "graph.yaml"
DECISION = ROOT / "examples" / "frontier_program" / "decision-receipt.yaml"


def _write(path: Path, doc: dict) -> None:
    path.write_text(yaml.safe_dump(doc, sort_keys=False), encoding="utf-8")


def test_decision_receipt_passes():
    result = verify_decision(GRAPH, DECISION)
    assert result.ok, result.errors


def test_invalid_graph_stops_decision_verification(tmp_path):
    graph = load_structured(GRAPH)
    graph["graph_version"] = "bad"
    graph_path = tmp_path / "graph.yaml"
    _write(graph_path, graph)
    result = verify_decision(graph_path, DECISION)
    assert not result.ok
    assert any("graph invalid" in error for error in result.errors)


def test_decision_rejection_branches_are_fail_closed(tmp_path):
    base = load_structured(DECISION)
    cases = []

    doc = deepcopy(base)
    doc["decision_version"] = "9.0"
    cases.append(("decision_version", doc))

    doc = deepcopy(base)
    doc["decision"] = "bad"
    cases.append(("decision must be a mapping", doc))

    doc = deepcopy(base)
    doc["decision"]["disposition"] = "MAYBE"
    cases.append(("decision.disposition", doc))

    doc = deepcopy(base)
    doc["decision"]["rationale"] = ""
    cases.append(("decision.rationale", doc))

    doc = deepcopy(base)
    doc["decision"]["reopen_when"] = []
    cases.append(("decision.reopen_when", doc))

    doc = deepcopy(base)
    doc["decision"]["reopen_when"] = [""]
    cases.append(("decision.reopen_when", doc))

    doc = deepcopy(base)
    doc["decision"]["id"] = "UNKNOWN-NODE"
    cases.append(("decision node not found", doc))

    doc = deepcopy(base)
    doc["decision"]["id"] = "CLAIM-CYCLE-TARGET"
    cases.append(("is not kind=decision", doc))

    doc = deepcopy(base)
    doc["basis"] = "bad"
    cases.append(("basis must be a mapping", doc))

    doc = deepcopy(base)
    doc["basis"]["node_refs"] = []
    cases.append(("basis.node_refs", doc))

    doc = deepcopy(base)
    doc["basis"]["node_refs"] = [123]
    cases.append(("non-empty strings", doc))

    doc = deepcopy(base)
    doc["basis"]["node_refs"] = ["UNKNOWN-NODE"]
    cases.append(("unknown graph node", doc))

    for index, (expected, doc) in enumerate(cases):
        path = tmp_path / f"decision-{index}.yaml"
        _write(path, doc)
        result = verify_decision(GRAPH, path)
        assert not result.ok, expected
        assert any(expected in error for error in result.errors), (expected, result.errors)
