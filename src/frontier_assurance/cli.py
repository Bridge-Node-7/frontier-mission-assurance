from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml

from . import __version__
from .analysis import dependency_impact, evidence_coverage, open_assumptions
from .decision import verify_decision
from .io import load_structured
from .receipt import ReceiptResult, reproduce_receipt, verify_receipt
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


def _receipt_summary(result: ReceiptResult) -> str:
    return (
        f"receipt_version={result.receipt_version} "
        f"code={result.artifact_counts.get('code', 0)} "
        f"inputs={result.artifact_counts.get('inputs', 0)} "
        f"outputs={result.artifact_counts.get('outputs', 0)} "
        f"numerical_checks={result.numerical_checks}"
    )


def _run() -> None:
    parser = argparse.ArgumentParser(
        prog="fma",
        description="Frontier Mission Assurance CLI",
        epilog="Start with the bounded walkthrough in docs/FIVE_MINUTE_EVALUATION.md.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    sub = parser.add_subparsers(dest="command")

    p_validate = sub.add_parser(
        "validate",
        help="Validate an assurance graph",
        epilog="Example: fma validate examples/frontier_program/graph.yaml",
    )
    p_validate.add_argument(
        "graph", metavar="GRAPH", help="Path to an assurance-graph YAML/JSON file"
    )

    p_assumptions = sub.add_parser(
        "assumptions",
        help="List unresolved assumptions without assigning an automated priority score",
        epilog="Example: fma assumptions examples/frontier_program/graph.yaml",
    )
    p_assumptions.add_argument(
        "graph", metavar="GRAPH", help="Path to an assurance-graph YAML/JSON file"
    )

    p_coverage = sub.add_parser(
        "coverage",
        help="Measure direct evidence coverage of critical mission/claim/requirement nodes",
        epilog="Example: fma coverage examples/frontier_program/graph.yaml",
    )
    p_coverage.add_argument(
        "graph", metavar="GRAPH", help="Path to an assurance-graph YAML/JSON file"
    )

    p_impact = sub.add_parser(
        "impact",
        help="Show transitive nodes impacted by a changed dependency",
        epilog="Example: fma impact examples/frontier_program/graph.yaml CLAIM-CYCLE-TARGET",
    )
    p_impact.add_argument(
        "graph", metavar="GRAPH", help="Path to an assurance-graph YAML/JSON file"
    )
    p_impact.add_argument(
        "node_id", metavar="NODE_ID", help="Declared graph node identifier that changed"
    )

    p_receipt = sub.add_parser(
        "receipt",
        help="Verify hashes and numerical checks in a research receipt without executing code",
        epilog="Example: fma receipt examples/research_receipt/receipt.yaml",
    )
    p_receipt.add_argument(
        "receipt", metavar="RECEIPT", help="Path to a research-receipt YAML/JSON file"
    )

    p_reproduce = sub.add_parser(
        "reproduce",
        help="Execute a trusted v2 receipt in a fresh declared-artifact workspace",
        epilog="Example: fma reproduce examples/research_receipt/receipt.yaml --timeout 30",
    )
    p_reproduce.add_argument(
        "receipt", metavar="RECEIPT", help="Path to a version 2.0 research receipt"
    )
    p_reproduce.add_argument(
        "--timeout",
        type=int,
        default=300,
        metavar="SECONDS",
        help="Maximum command runtime in seconds (default: 300)",
    )

    p_decision = sub.add_parser(
        "decision",
        help="Verify a decision receipt against an assurance graph",
        epilog=(
            "Example: fma decision examples/frontier_program/graph.yaml "
            "examples/frontier_program/decision-receipt.yaml"
        ),
    )
    p_decision.add_argument(
        "graph", metavar="GRAPH", help="Path to an assurance-graph YAML/JSON file"
    )
    p_decision.add_argument(
        "decision_receipt",
        metavar="DECISION_RECEIPT",
        help="Path to a decision-receipt YAML/JSON file",
    )

    p_report = sub.add_parser(
        "report",
        help="Render a Markdown assurance report",
        epilog=(
            "Example: fma report examples/frontier_program/graph.yaml "
            "--out build/assurance-report.md"
        ),
    )
    p_report.add_argument(
        "graph", metavar="GRAPH", help="Path to an assurance-graph YAML/JSON file"
    )
    p_report.add_argument("--out", required=True, metavar="PATH", help="Markdown output path")

    args = parser.parse_args()
    if args.command is None:
        parser.print_help(sys.stderr)
        print("\nFirst run: see docs/FIVE_MINUTE_EVALUATION.md", file=sys.stderr)
        raise SystemExit(2)

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
        print(f"RECEIPT PASS: {_receipt_summary(result)}")
        if result.receipt_version == "1.0":
            print("WARN: legacy receipt verified; fresh reproduction requires receipt_version 2.0")
        return

    if args.command == "reproduce":
        if args.timeout <= 0:
            raise ValueError("--timeout must be greater than zero")
        print(
            "NOTICE: reproduction executes trusted receipt-declared code in a fresh "
            "artifact workspace; "
            "it is not a sandbox."
        )
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
        print(f"REPRODUCTION PASS: fresh code-bound execution verified; {_receipt_summary(result)}")
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
    except (OSError, UnicodeError, yaml.YAMLError, ValueError, TypeError, KeyError) as exc:
        message = " ".join(str(exc).split())
        print(f"FAIL: {message}")
        raise SystemExit(2) from None


if __name__ == "__main__":
    main()
