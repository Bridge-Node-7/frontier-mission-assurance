from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .constants import NODE_KINDS, RELATIONS, STATUSES


@dataclass
class ValidationResult:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors


def _depends_on_cycle_warnings(
    edges: list[Any], by_id: dict[str, dict[str, Any]]
) -> list[str]:
    adjacency: dict[str, set[str]] = {node_id: set() for node_id in by_id}
    for edge in edges:
        if not isinstance(edge, dict) or edge.get("relation") != "depends_on":
            continue
        src, dst = edge.get("from"), edge.get("to")
        if src in adjacency and dst in adjacency and src != dst:
            adjacency[src].add(dst)

    state: dict[str, int] = {}
    stack: list[str] = []
    stack_index: dict[str, int] = {}
    cycles: set[tuple[str, ...]] = set()

    def canonical(nodes: list[str]) -> tuple[str, ...]:
        body = nodes[:-1]
        rotations = [tuple(body[i:] + body[:i]) for i in range(len(body))]
        return min(rotations)

    def visit(node: str) -> None:
        state[node] = 1
        stack_index[node] = len(stack)
        stack.append(node)
        for nxt in sorted(adjacency[node]):
            nxt_state = state.get(nxt, 0)
            if nxt_state == 0:
                visit(nxt)
            elif nxt_state == 1:
                start = stack_index[nxt]
                cycle = stack[start:] + [nxt]
                if len(cycle) > 2:
                    cycles.add(canonical(cycle))
        stack.pop()
        stack_index.pop(node, None)
        state[node] = 2

    for node in sorted(adjacency):
        if state.get(node, 0) == 0:
            visit(node)

    warnings = []
    for cycle in sorted(cycles):
        warnings.append("depends_on cycle detected: " + " -> ".join((*cycle, cycle[0])))
    return warnings


def validate_graph(graph: dict[str, Any]) -> ValidationResult:
    result = ValidationResult()

    allowed_root = {"graph_version", "metadata", "nodes", "edges"}
    extra_root = sorted(set(graph) - allowed_root)
    if extra_root:
        result.errors.append(f"unsupported graph fields: {', '.join(extra_root)}")

    if str(graph.get("graph_version")) != "1.0":
        result.errors.append("graph_version must be '1.0'")

    metadata = graph.get("metadata")
    if metadata is not None and not isinstance(metadata, dict):
        result.errors.append("graph.metadata must be a mapping when present")

    nodes = graph.get("nodes")
    edges = graph.get("edges")

    if not isinstance(nodes, list) or not nodes:
        result.errors.append("graph.nodes must be a non-empty list")
        return result
    if not isinstance(edges, list):
        result.errors.append("graph.edges must be a list")
        return result

    by_id: dict[str, dict[str, Any]] = {}
    for i, node in enumerate(nodes):
        if not isinstance(node, dict):
            result.errors.append(f"nodes[{i}] must be a mapping")
            continue
        node_id = node.get("id")
        kind = node.get("kind")
        title = node.get("title")
        status = node.get("status")
        if not isinstance(node_id, str) or not node_id.strip():
            result.errors.append(f"nodes[{i}].id is required")
            continue
        if node_id in by_id:
            result.errors.append(f"duplicate node id: {node_id}")
        by_id[node_id] = node
        if kind not in NODE_KINDS:
            result.errors.append(f"{node_id}: unsupported kind {kind!r}")
        if not isinstance(title, str) or not title.strip():
            result.errors.append(f"{node_id}: title is required")
        if status not in STATUSES:
            allowed = ", ".join(sorted(STATUSES))
            result.errors.append(
                f"{node_id}: unsupported status {status!r}; allowed: {allowed}"
            )

        criticality = node.get("criticality")
        if criticality is not None and (
            not isinstance(criticality, (int, float)) or not 0 <= float(criticality) <= 5
        ):
            result.errors.append(f"{node_id}: criticality must be between 0 and 5")

        if kind == "evidence" and not node.get("source"):
            result.warnings.append(f"{node_id}: evidence has no source/provenance field")

    seen_edges: set[tuple[str, str, str]] = set()
    for i, edge in enumerate(edges):
        if not isinstance(edge, dict):
            result.errors.append(f"edges[{i}] must be a mapping")
            continue
        extra_edge = sorted(set(edge) - {"from", "to", "relation"})
        if extra_edge:
            result.errors.append(f"edges[{i}]: unsupported fields: {', '.join(extra_edge)}")
        src, dst, relation = edge.get("from"), edge.get("to"), edge.get("relation")
        if src not in by_id:
            result.errors.append(f"edges[{i}]: unknown source node {src!r}")
        if dst not in by_id:
            result.errors.append(f"edges[{i}]: unknown target node {dst!r}")
        if relation not in RELATIONS:
            result.errors.append(f"edges[{i}]: unsupported relation {relation!r}")
        key = (str(src), str(dst), str(relation))
        if key in seen_edges:
            result.warnings.append(f"duplicate edge: {src} -[{relation}]-> {dst}")
        seen_edges.add(key)
        if relation == "depends_on" and src == dst and src in by_id:
            result.warnings.append(f"self dependency: {src} -[depends_on]-> {dst}")

    result.warnings.extend(_depends_on_cycle_warnings(edges, by_id))

    outgoing: dict[str, list[dict[str, Any]]] = {node_id: [] for node_id in by_id}
    for edge in edges:
        if isinstance(edge, dict) and edge.get("from") in outgoing:
            outgoing[edge["from"]].append(edge)
    for node_id, node in by_id.items():
        if node.get("kind") == "evidence":
            useful = any(
                e.get("relation") in {"supports", "verifies", "validates"}
                for e in outgoing[node_id]
            )
            if not useful:
                result.warnings.append(
                    f"{node_id}: evidence is not linked to a supported claim/assumption"
                )

    return result
