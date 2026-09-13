from __future__ import annotations

from copy import deepcopy
from pathlib import Path

from frontier_assurance.analysis import evidence_coverage, open_assumptions
from frontier_assurance.io import load_structured
from frontier_assurance.report import render_markdown_report
from frontier_assurance.validate import validate_graph

ROOT = Path(__file__).resolve().parents[1]
GRAPH = ROOT / "examples" / "frontier_program" / "graph.yaml"


def _graph():
    return load_structured(GRAPH)


def test_example_graph_valid():
    result = validate_graph(_graph())
    assert result.ok, result.errors


def test_open_assumptions_are_visible_without_scoring():
    assumptions = open_assumptions(_graph())
    ids = [node["id"] for node in assumptions]
    assert ids == sorted(ids)
    assert "ASSUMP-SCALE-PERFORMANCE" in ids


def test_coverage_exposes_evidence_gap():
    coverage = evidence_coverage(_graph())
    assert "CLAIM-CYCLE-TARGET" in coverage["uncovered"]
    assert coverage["coverage_ratio"] < 1.0


def test_graph_rejection_branches_are_fail_closed():
    base = _graph()
    mutations: list[tuple[str, dict]] = []

    doc = deepcopy(base)
    doc["unexpected_field"] = "x"
    mutations.append(("unsupported graph fields", doc))

    doc = deepcopy(base)
    doc["graph_version"] = "9.0"
    mutations.append(("graph_version", doc))

    doc = deepcopy(base)
    doc["metadata"] = []
    mutations.append(("graph.metadata", doc))

    doc = deepcopy(base)
    doc["nodes"] = []
    mutations.append(("graph.nodes", doc))

    doc = deepcopy(base)
    doc["nodes"] = "bad"
    mutations.append(("graph.nodes", doc))

    doc = deepcopy(base)
    doc["edges"] = "bad"
    mutations.append(("graph.edges", doc))

    doc = deepcopy(base)
    doc["nodes"][0] = "bad"
    mutations.append(("must be a mapping", doc))

    doc = deepcopy(base)
    doc["nodes"][0].pop("id")
    mutations.append(("id is required", doc))

    doc = deepcopy(base)
    doc["nodes"].append(deepcopy(doc["nodes"][0]))
    mutations.append(("duplicate node id", doc))

    doc = deepcopy(base)
    doc["nodes"][0]["kind"] = "mystery"
    mutations.append(("unsupported kind", doc))

    doc = deepcopy(base)
    doc["nodes"][0]["title"] = ""
    mutations.append(("title is required", doc))

    doc = deepcopy(base)
    doc["nodes"][0]["status"] = "mystery"
    mutations.append(("unsupported status", doc))

    for bad in (9, -1, "high"):
        doc = deepcopy(base)
        doc["nodes"][0]["criticality"] = bad
        mutations.append(("criticality must be between 0 and 5", doc))

    doc = deepcopy(base)
    doc["edges"][0] = "bad"
    mutations.append(("must be a mapping", doc))

    doc = deepcopy(base)
    doc["edges"][0]["extra"] = True
    mutations.append(("unsupported fields", doc))

    doc = deepcopy(base)
    doc["edges"][0]["from"] = "UNKNOWN-NODE"
    mutations.append(("unknown source node", doc))

    doc = deepcopy(base)
    doc["edges"][0]["to"] = "UNKNOWN-NODE"
    mutations.append(("unknown target node", doc))

    doc = deepcopy(base)
    doc["edges"][0]["relation"] = "mystery"
    mutations.append(("unsupported relation", doc))

    for expected, graph in mutations:
        result = validate_graph(graph)
        assert not result.ok, expected
        assert any(expected in error for error in result.errors), (expected, result.errors)


def test_graph_warning_branches_are_visible():
    graph = _graph()
    graph["edges"].append(deepcopy(graph["edges"][0]))
    result = validate_graph(graph)
    assert result.ok
    assert any("duplicate edge" in warning for warning in result.warnings)

    graph = _graph()
    graph["edges"].append(
        {
            "from": "CLAIM-CYCLE-TARGET",
            "to": "CLAIM-CYCLE-TARGET",
            "relation": "depends_on",
        }
    )
    result = validate_graph(graph)
    assert result.ok
    assert any("self dependency" in warning for warning in result.warnings)

    graph = _graph()
    graph["edges"].append(
        {
            "from": "ASSUMP-CYCLE-COMPOSITION",
            "to": "CLAIM-RESOURCE-FEASIBILITY",
            "relation": "depends_on",
        }
    )
    result = validate_graph(graph)
    assert result.ok
    assert any("depends_on cycle detected" in warning for warning in result.warnings)

    graph = _graph()
    evidence = next(node for node in graph["nodes"] if node["kind"] == "evidence")
    evidence.pop("source", None)
    result = validate_graph(graph)
    assert result.ok
    assert any("has no source/provenance field" in warning for warning in result.warnings)

    graph = _graph()
    evidence_id = next(node["id"] for node in graph["nodes"] if node["kind"] == "evidence")
    graph["edges"] = [edge for edge in graph["edges"] if edge.get("from") != evidence_id]
    result = validate_graph(graph)
    assert result.ok
    assert any("evidence is not linked" in warning for warning in result.warnings)


def test_report_is_byte_reproducible_with_source_date_epoch(monkeypatch):
    monkeypatch.setenv("SOURCE_DATE_EPOCH", "0")
    first = render_markdown_report(_graph())
    second = render_markdown_report(_graph())
    assert first == second
    assert "Generated: 1970-01-01T00:00:00+00:00" in first
