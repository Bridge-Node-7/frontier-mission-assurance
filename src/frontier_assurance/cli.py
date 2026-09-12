from __future__ import annotations

import argparse
import json
from pathlib import Path

from . import __version__
from .analysis import dependency_impact, evidence_coverage, open_assumptions
from .decision import verify_decision
from .io import load_structured
from .receipt import reproduce_receipt, verify_receipt
from .report import render_markdown_report
from .validate import validate_graph


def _graph(path: str):
    graph = load_structured(path)
    validation = validate_graph(graph)
    if not validation.ok:
        for error in validation.errors:
            print(f"ERROR: {error}")
        raise SystemExit(2)
    return graph, validation


def _run() -> None:
    parser = argparse.ArgumentParser(prog="fma", description="Frontier Mission Assurance CLI")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    p_validate = sub.add_parser("validate", help="Validate an assurance graph")
    p_validate.add_argument("graph")

    p_assumptions = sub.add_parser(
        "assumptions",
        help="List unresolved assumptions without assigning an automated priority score",
    )
    p_assumptions.add_argument("graph")

    p_coverage = sub.add_parser(
        "coverage",
        help="Measure direct evidence coverage of critical mission/claim/requirement nodes",
    )
    p_coverage.add_argument("graph")

    p_impact = sub.add_parser("impact", help="Show transitive nodes impacted by a changed dependency")
    p_impact.add_argument("graph")
    p_impact.add_argument("node_id")

    p_receipt = sub.add_parser("receipt", help="Verify hashes and numerical checks in a research receipt")
    p_receipt.add_argument("receipt")

    p_reproduce = sub.add_parser(
        "reproduce",
        help="Explicitly execute a trusted receipt command, then verify resulting artifacts",
    )
    p_reproduce.add_argument("receipt")
    p_reproduce.add_argument("--timeout", type=int, default=300)

    p_decision = sub.add_parser("decision", help="Verify a decision receipt against an assurance graph")
    p_decision.add_argument("graph")
    p_decision.add_argument("decision_receipt")

    p_report = sub.add_parser("report", help="Render a Markdown assurance report")
    p_report.add_argument("graph")
    p_report.add_argument("--out", required=True)

    args = parser.parse_args()

    if args.command == "validate":
        _, validation = _graph(args.graph)
        for warning in validation.warnings:
            print(f"WARN: {warning}")
        print("VALID: graph passed structural and semantic checks")
        return

    if args.command == "assumptions":
        graph, _ = _graph(args.graph)
        for node in open_assumptions(graph):
            print(f"{node['id']:24}  {node['status']:12}  {node['title']}")
        return

    if args.command == "coverage":
        graph, _ = _graph(args.graph)
        print(json.dumps(evidence_coverage(graph), indent=2, sort_keys=True))
        return

    if args.command == "impact":
        graph, _ = _graph(args.graph)
        node_ids = {n.get("id") for n in graph.get("nodes", []) if isinstance(n, dict)}
        if args.node_id not in node_ids:
            raise ValueError(f"unknown graph node: {args.node_id}")
        for node_id in dependency_impact(graph, args.node_id):
            print(node_id)
        return

    if args.command == "receipt":
        result = verify_receipt(args.receipt)
        for check in result.checks:
            print(f"PASS: {check}")
        if result.errors:
            for error in result.errors:
                print(f"FAIL: {error}")
            raise SystemExit(2)
        print("RECEIPT PASS: artifact hashes and numerical checks verified")
        return

    if args.command == "reproduce":
        print("NOTICE: reproduction executes the command declared by the receipt; use trusted code only.")
        result = reproduce_receipt(args.receipt, timeout=args.timeout)
        if result.stdout.strip():
            print(result.stdout.rstrip())
        if result.stderr.strip():
            print(result.stderr.rstrip())
        for check in result.checks:
            print(f"PASS: {check}")
        if result.errors:
            for error in result.errors:
                print(f"FAIL: {error}")
            raise SystemExit(2)
        print("REPRODUCTION PASS: command executed and resulting receipt verified")
        return

    if args.command == "decision":
        result = verify_decision(args.graph, args.decision_receipt)
        for check in result.checks:
            print(f"PASS: {check}")
        if result.errors:
            for error in result.errors:
                print(f"FAIL: {error}")
            raise SystemExit(2)
        print("DECISION PASS: receipt references graph-valid decision basis nodes")
        return

    if args.command == "report":
        graph, _ = _graph(args.graph)
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(render_markdown_report(graph), encoding="utf-8")
        print(f"WROTE: {out}")
        return


def main() -> None:
    try:
        _run()
    except (FileNotFoundError, ValueError, TypeError, KeyError) as exc:
        print(f"ERROR: {exc}")
        raise SystemExit(2) from None


if __name__ == "__main__":
    main()
