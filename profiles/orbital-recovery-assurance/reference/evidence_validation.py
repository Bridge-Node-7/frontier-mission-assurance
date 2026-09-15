"""Evidence and cross-record validation helpers for the synthetic public profile."""

from __future__ import annotations

from collections import defaultdict


def validate_evidence_record(record: dict) -> list[str]:
    problems: list[str] = []
    evidence = {item["id"]: item for item in record.get("evidence", [])}
    if len(evidence) != len(record.get("evidence", [])):
        problems.append("duplicate evidence id")
    for plane_name, plane in record.get("planes", {}).items():
        for subject, claim in plane.items():
            state = claim.get("state")
            refs = claim.get("evidence_refs", [])
            if state and state != "unknown" and not refs:
                problems.append(f"{plane_name}.{subject}: state '{state}' cites no evidence")
            for ref in refs:
                if ref not in evidence:
                    problems.append(
                    f"{plane_name}.{subject}: evidence_ref '{ref}' does not resolve"
                )
    return problems


def provenance_correlation_components(record: dict) -> list[list[str]]:
    """Group evidence connected by any declared shared provenance root.

    Connectivity is transitive. The output identifies known correlation; absence of
    a shared declared root does *not* establish statistical or epistemic independence.
    Evidence with no provenance roots is conservatively grouped as correlation-unresolved.
    """
    evidence = record.get("evidence", [])
    ids = [item["id"] for item in evidence]
    parent = {item_id: item_id for item_id in ids}

    def find(item_id: str) -> str:
        while parent[item_id] != item_id:
            parent[item_id] = parent[parent[item_id]]
            item_id = parent[item_id]
        return item_id

    def union(left: str, right: str) -> None:
        a, b = find(left), find(right)
        if a != b:
            parent[b] = a

    by_root: dict[tuple[str, str], list[str]] = defaultdict(list)
    unresolved: list[str] = []
    for item in evidence:
        roots = {k: v for k, v in item.get("provenance_roots", {}).items() if v}
        if not roots:
            unresolved.append(item["id"])
            continue
        for key, value in roots.items():
            by_root[(key, value)].append(item["id"])

    for members in by_root.values():
        first = members[0]
        for other in members[1:]:
            union(first, other)

    if unresolved:
        first = unresolved[0]
        for other in unresolved[1:]:
            union(first, other)

    groups: dict[str, list[str]] = defaultdict(list)
    for item_id in ids:
        groups[find(item_id)].append(item_id)
    return sorted((sorted(g) for g in groups.values()), key=lambda g: g[0])


def resolve_refs(refs: list[str], records: list[dict]) -> list[str]:
    known = {item["id"] for record in records for item in record.get("evidence", [])}
    return [ref for ref in refs if ref not in known]
