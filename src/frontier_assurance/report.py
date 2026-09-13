from __future__ import annotations

import os
from datetime import UTC, datetime
from typing import Any

from .analysis import evidence_coverage, open_assumptions


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
    lines = [
        "# Mission Assurance Report",
        "",
        f"Generated: {_generation_time().isoformat()}",
        "",
        "## Evidence coverage",
        "",
        f"- Critical nodes: **{coverage['critical_count']}**",
        f"- Directly covered: **{coverage['covered_count']}**",
        f"- Coverage ratio: **{coverage['coverage_ratio']:.1%}**",
        "",
    ]
    if coverage["uncovered"]:
        lines += ["### Critical nodes without direct evidence", ""]
        lines += [f"- `{node_id}`" for node_id in coverage["uncovered"]]
        lines.append("")

    lines += ["## Open assumptions", ""]
    if assumptions:
        lines += ["| Assumption | Status | Title |", "|---|---|---|"]
        for node in assumptions:
            lines.append(f"| `{node['id']}` | {node['status']} | {node['title']} |")
    else:
        lines.append("No unresolved assumptions are declared in this graph.")

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
    ]
    return "\n".join(lines)
