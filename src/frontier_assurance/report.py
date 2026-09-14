from __future__ import annotations

import os
from datetime import UTC, datetime
from typing import Any

from .analysis import evidence_coverage, open_assumptions
from .validate import validate_graph


NON_CLAIMS = (
    "A PASS proves only the declared mechanics. It does not establish scientific truth, "
    "authenticated authorship, regulatory compliance, supplier qualification, mission "
    "readiness, legal priority, research-boundary enforcement, or authorization for "
    "consequential decisions."
)


def _generation_time() -> datetime:
    source_date_epoch = os.environ.get("SOURCE_DATE_EPOCH")
    if source_date_epoch is None:
        return datetime.now(UTC)
    try:
        epoch = int(source_date_epoch)
    except ValueError as exc:
        raise ValueError("SOURCE_DATE_EPOCH must be an integer Unix timestamp") from exc
    if epoch < 0:
        raise ValueError("SOURCE_DATE_EPOCH must be non-negative")
    return datetime.fromtimestamp(epoch, UTC)


def render_markdown_report(graph: dict[str, Any]) -> str:
    coverage = evidence_coverage(graph)
    assumptions = open_assumptions(graph)
    validation = validate_graph(graph)
    lines = [
        "# Mission Assurance Report",
        "",
        f"Generated: {_generation_time().isoformat()}",
        "",
        "## Assurance boundary",
        "",
        NON_CLAIMS,
        "",
        "Evidence coverage below is **declared and unverified by this report**. It measures "
        "whether graph nodes have declared evidence links; it does not establish that the "
        "underlying evidence exists, is authentic, is independent, or proves the claim.",
        "",
        "## Declared evidence coverage (unverified)",
        "",
        f"- Critical nodes: **{coverage['critical_count']}**",
        f"- Directly covered by declared evidence links: **{coverage['covered_count']}**",
        f"- Declared evidence coverage ratio (unverified): **{coverage['coverage_ratio']:.1%}**",
        f"- Graph validation warnings: **{len(validation.warnings)}**",
        "",
    ]
    if validation.warnings:
        lines += ["### Validation warnings", ""]
        lines += [f"- {warning}" for warning in validation.warnings]
        lines.append("")

    if coverage["uncovered"]:
        lines += ["### Critical nodes without direct declared evidence", ""]
        lines += [f"- `{node_id}`" for node_id in coverage["uncovered"]]
        lines.append("")

    lines += ["## Open assumptions", ""]
    if assumptions:
        lines += ["| Assumption | Status | Title |", "|---|---|---|"]
        for node in assumptions:
            lines.append(f"| `{node['id']}` | {node['status']} | {node['title']} |")
    else:
        lines.append(
            "No unresolved assumptions are **declared** in this graph. This does not establish "
            "that no real-world assumptions exist."
        )

    lines += [
        "",
        "## Interpretation",
        "",
        (
            "This reference report exposes declared gaps and assumptions without calculating "
            "a hidden or automatic engineering priority. Consequence, urgency, resource "
            "allocation, and final decisions remain human-owned or belong to private program "
            "policy."
        ),
        "",
        NON_CLAIMS,
        "",
    ]
    return "\n".join(lines)
