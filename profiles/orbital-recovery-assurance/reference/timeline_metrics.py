"""Recovery timeline metrics.

Technical restoration and trustworthy restoration are distinct milestones.
All timestamps are declared inputs. This module only measures elapsed time.
"""

from __future__ import annotations

from datetime import datetime

ORDER = (
    "anomaly_recognized",
    "contained",
    "evidence_established",
    "minimum_credible_capability",
    "trust_reestablished",
    "recovery_verified",
)

METRICS = {
    "contained": "TTC",
    "evidence_established": "TTE",
    "minimum_credible_capability": "TTMC",
    "trust_reestablished": "TTT",
    "recovery_verified": "TTV",
}


def _parse(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("timeline timestamps must include timezone information")
    return parsed


def compute_timeline_metrics(events: dict[str, str]) -> dict[str, float]:
    if "anomaly_recognized" not in events:
        raise ValueError("anomaly_recognized is required")
    parsed = {name: _parse(value) for name, value in events.items()}
    unknown = set(parsed) - set(ORDER)
    if unknown:
        raise ValueError(f"unknown timeline event(s): {sorted(unknown)}")

    previous = None
    for name in ORDER:
        if name not in parsed:
            continue
        if previous is not None and parsed[name] < previous:
            raise ValueError("timeline events are not monotonic")
        previous = parsed[name]

    start = parsed["anomaly_recognized"]
    result: dict[str, float] = {}
    for event_name, metric_name in METRICS.items():
        if event_name in parsed:
            result[metric_name] = (parsed[event_name] - start).total_seconds()
    return result
