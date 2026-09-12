from copy import deepcopy
from pathlib import Path

from frontier_assurance.analysis import evidence_coverage, open_assumptions
from frontier_assurance.io import load_structured
from frontier_assurance.validate import validate_graph

ROOT = Path(__file__).resolve().parents[1]
GRAPH = ROOT / "examples" / "frontier_program" / "graph.yaml"


def test_example_graph_valid():
    result = validate_graph(load_structured(GRAPH))
    assert result.ok, result.errors


def test_open_assumptions_are_visible_without_scoring():
    assumptions = open_assumptions(load_structured(GRAPH))
    ids = [node["id"] for node in assumptions]
    assert ids == sorted(ids)
    assert "ASSUMP-SCALE-PERFORMANCE" in ids


def test_coverage_exposes_evidence_gap():
    coverage = evidence_coverage(load_structured(GRAPH))
    assert "CLAIM-CYCLE-TARGET" in coverage["uncovered"]
    assert coverage["coverage_ratio"] < 1.0


def test_dangling_edge_fails():
    graph = deepcopy(load_structured(GRAPH))
    graph["edges"].append({"from": "MISSING", "to": "MISSION-FRONTIER-SYSTEM", "relation": "supports"})
    result = validate_graph(graph)
    assert not result.ok
    assert any("unknown source node" in error for error in result.errors)


def test_graph_version_required():
    graph = deepcopy(load_structured(GRAPH))
    graph.pop("graph_version")
    result = validate_graph(graph)
    assert not result.ok
    assert any("graph_version" in error for error in result.errors)


def test_node_status_required():
    graph = deepcopy(load_structured(GRAPH))
    graph["nodes"][0].pop("status")
    result = validate_graph(graph)
    assert not result.ok
    assert any("unsupported status" in error for error in result.errors)


def test_unknown_root_field_fails():
    graph = deepcopy(load_structured(GRAPH))
    graph["private_context"] = "should-not-be-accepted"
    result = validate_graph(graph)
    assert not result.ok
    assert any("unsupported graph fields" in error for error in result.errors)


def test_unknown_edge_field_fails():
    graph = deepcopy(load_structured(GRAPH))
    graph["edges"][0]["hidden_weight"] = 0.5
    result = validate_graph(graph)
    assert not result.ok
    assert any("unsupported fields" in error for error in result.errors)


def test_invalid_status_fails_runtime_and_schema():
    graph = deepcopy(load_structured(GRAPH))
    graph["nodes"][0]["status"] = "mystery"
    result = validate_graph(graph)
    assert not result.ok
    assert any("unsupported status" in error for error in result.errors)
