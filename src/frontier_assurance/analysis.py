from __future__ import annotations

from collections import defaultdict, deque
from typing import Any


def open_assumptions(graph: dict[str, Any]) -> list[dict[str, Any]]:
    """Return visible unresolved assumptions without calculating a priority score."""
    assumptions = [
        node
        for node in graph.get("nodes", [])
        if isinstance(node, dict)
        and node.get("kind") == "assumption"
        and node.get("status") not in {"retired", "superseded", "verified", "validated"}
    ]
    return sorted(assumptions, key=lambda node: str(node.get("id", "")))


def evidence_coverage(graph: dict[str, Any]) -> dict[str, Any]:
    nodes = {n["id"]: n for n in graph.get("nodes", []) if isinstance(n, dict) and "id" in n}
    direct_support = defaultdict(list)
    for edge in graph.get("edges", []):
        if not isinstance(edge, dict):
            continue
        src, dst, rel = edge.get("from"), edge.get("to"), edge.get("relation")
        if rel in {"supports", "verifies", "validates"} and nodes.get(src, {}).get("kind") == "evidence":
            direct_support[dst].append(src)

    critical = []
    uncovered = []
    for node in nodes.values():
        if node.get("kind") in {"mission", "claim", "requirement"} and float(node.get("criticality", 0)) >= 4:
            critical.append(node["id"])
            if not direct_support[node["id"]]:
                uncovered.append(node["id"])

    return {
        "critical_count": len(critical),
        "covered_count": len(critical) - len(uncovered),
        "coverage_ratio": (len(critical) - len(uncovered)) / len(critical) if critical else 1.0,
        "uncovered": uncovered,
        "direct_support": dict(direct_support),
    }


def dependency_impact(graph: dict[str, Any], changed_node: str) -> list[str]:
    """Return nodes transitively dependent on changed_node through depends_on/requires."""
    reverse = defaultdict(list)
    for edge in graph.get("edges", []):
        if edge.get("relation") in {"depends_on", "requires"}:
            reverse[edge.get("to")].append(edge.get("from"))
    seen = {changed_node}
    q = deque([changed_node])
    impacted = []
    while q:
        cur = q.popleft()
        for nxt in reverse.get(cur, []):
            if nxt not in seen:
                seen.add(nxt)
                impacted.append(nxt)
                q.append(nxt)
    return impacted
