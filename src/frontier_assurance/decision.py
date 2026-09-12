from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from .io import load_structured
from .validate import validate_graph


@dataclass
class DecisionResult:
    errors: list[str] = field(default_factory=list)
    checks: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors


def verify_decision(graph_path: str | Path, decision_path: str | Path) -> DecisionResult:
    graph = load_structured(graph_path)
    validation = validate_graph(graph)
    result = DecisionResult()
    if not validation.ok:
        result.errors.extend(f"graph invalid: {e}" for e in validation.errors)
        return result

    doc = load_structured(decision_path)
    if str(doc.get("decision_version")) != "1.0":
        result.errors.append("decision_version must be '1.0'")

    decision = doc.get("decision")
    if not isinstance(decision, dict):
        result.errors.append("decision must be a mapping")
        decision = {}
    decision_id = decision.get("id")
    disposition = decision.get("disposition")
    if disposition not in {"APPROVE", "HOLD", "REVISE", "REJECT"}:
        result.errors.append("decision.disposition must be APPROVE, HOLD, REVISE, or REJECT")
    rationale = decision.get("rationale")
    if not isinstance(rationale, str) or not rationale.strip():
        result.errors.append("decision.rationale is required")
    reopen_when = decision.get("reopen_when")
    if not isinstance(reopen_when, list) or not reopen_when or not all(
        isinstance(item, str) and item.strip() for item in reopen_when
    ):
        result.errors.append("decision.reopen_when must contain at least one explicit reopen condition")

    nodes = {n["id"]: n for n in graph.get("nodes", []) if isinstance(n, dict) and "id" in n}
    if decision_id not in nodes:
        result.errors.append(f"decision node not found in graph: {decision_id}")
    elif nodes[decision_id].get("kind") != "decision":
        result.errors.append(f"graph node {decision_id} is not kind=decision")
    else:
        result.checks.append(f"decision node exists: {decision_id}")

    basis = doc.get("basis")
    if not isinstance(basis, dict):
        result.errors.append("basis must be a mapping")
        basis = {}
    refs = basis.get("node_refs")
    if not isinstance(refs, list) or not refs:
        result.errors.append("basis.node_refs must list the graph nodes supporting the decision")
    else:
        for ref in refs:
            if not isinstance(ref, str) or not ref.strip():
                result.errors.append("basis.node_refs entries must be non-empty strings")
            elif ref not in nodes:
                result.errors.append(f"basis references unknown graph node: {ref}")
            else:
                result.checks.append(f"basis node exists: {ref}")

    return result
