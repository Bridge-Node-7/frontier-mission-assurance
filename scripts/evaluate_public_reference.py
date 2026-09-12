from __future__ import annotations

from pathlib import Path

from frontier_assurance.analysis import evidence_coverage, open_assumptions
from frontier_assurance.decision import verify_decision
from frontier_assurance.io import load_structured
from frontier_assurance.receipt import verify_receipt
from frontier_assurance.report import render_markdown_report
from frontier_assurance.validate import validate_graph

ROOT = Path(__file__).resolve().parents[1]
GRAPH = ROOT / "examples" / "frontier_program" / "graph.yaml"
RECEIPT = ROOT / "examples" / "research_receipt" / "receipt.yaml"
DECISION = ROOT / "examples" / "frontier_program" / "decision-receipt.yaml"
REPORT = ROOT / "build" / "assurance-report.md"


def fail(label: str, errors: list[str]) -> int:
    print(f"FAIL - {label}")
    for error in errors:
        print(f"  {error}")
    return 2


def main() -> int:
    graph = load_structured(GRAPH)
    validation = validate_graph(graph)
    if not validation.ok:
        return fail("GRAPH INVALID", validation.errors)
    print("PASS - GRAPH VALID")

    assumptions = open_assumptions(graph)
    print(f"PASS - OPEN ASSUMPTIONS VISIBLE ({len(assumptions)})")

    coverage = evidence_coverage(graph)
    print(
        "PASS - EVIDENCE COVERAGE "
        f"({coverage['covered_count']}/{coverage['critical_count']}; "
        f"{coverage['coverage_ratio']:.1%})"
    )
    if coverage["uncovered"]:
        print("INFO - VISIBLE CRITICAL GAPS: " + ", ".join(coverage["uncovered"]))

    receipt = verify_receipt(RECEIPT)
    if not receipt.ok:
        return fail("RESEARCH RECEIPT", receipt.errors)
    print("PASS - RESEARCH RECEIPT VERIFIED")

    decision = verify_decision(GRAPH, DECISION)
    if not decision.ok:
        return fail("DECISION RECEIPT", decision.errors)
    print("PASS - DECISION BASIS VERIFIED")

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(render_markdown_report(graph), encoding="utf-8")
    print(f"PASS - REPORT WRITTEN ({REPORT.relative_to(ROOT)})")
    print("RESULT - PUBLIC REFERENCE EVALUATION PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
