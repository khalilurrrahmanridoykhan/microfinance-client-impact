"""Client satisfaction, complaints and voluntary-exit analytics."""

from __future__ import annotations

import json
from pathlib import Path
from statistics import mean, median
from typing import Any


def client_voice_summary(tables: dict[str, list[dict[str, Any]]]) -> dict[str, Any]:
    """Calculate aggregate client-voice indicators without exposing client records."""
    active_clients = len(tables["clients"])
    complaints = tables["complaints"]
    resolved = [row for row in complaints if row["resolved"]]
    resolution_days = [row["resolution_days"] for row in resolved]
    satisfaction = [
        row["satisfaction_score"]
        for row in tables["outcome_surveys"]
        if row["survey_round"] == "followup" and row.get("satisfaction_score") is not None
    ]
    dropout_events = tables["dropout_events"]
    return {
        "active_clients": active_clients,
        "satisfaction_response_n": len(satisfaction),
        "mean_satisfaction_score": round(mean(satisfaction), 4) if satisfaction else None,
        "complaint_n": len(complaints),
        "complaint_rate_per_1000": round(len(complaints) / active_clients * 1000, 4)
        if active_clients
        else None,
        "complaint_resolution_rate": round(len(resolved) / len(complaints), 4)
        if complaints
        else None,
        "median_resolution_days": median(resolution_days) if resolution_days else None,
        "voluntary_exit_n": len(dropout_events),
        "voluntary_exit_rate": round(len(dropout_events) / active_clients, 4)
        if active_clients
        else None,
        "complaints_by_category": _count_by(complaints, "complaint_category"),
        "exits_by_reason": _count_by(dropout_events, "exit_reason"),
    }


def write_client_voice_report(report: dict[str, Any], output_path: Path) -> None:
    """Write aggregate client-voice results as stable JSON."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _count_by(rows: list[dict[str, Any]], field: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for row in rows:
        value = row.get(field)
        if value is not None:
            counts[str(value)] = counts.get(str(value), 0) + 1
    return dict(sorted(counts.items()))