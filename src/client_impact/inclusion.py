"""Gender and inclusion analytics with small-group suppression."""

from __future__ import annotations

import json
from pathlib import Path
from statistics import mean
from typing import Any


def inclusion_rows(tables: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    """Join client gender and agency responses for descriptive inclusion analysis."""
    clients = {row["client_id"]: row for row in tables["clients"]}
    rows: list[dict[str, Any]] = []
    for agency in tables["agency_surveys"]:
        client = clients[agency["client_id"]]
        rows.append(
            {
                "client_id": agency["client_id"],
                "gender": client["gender"],
                "district": client["district"],
                "loan_control_score": agency["women_loan_control_score"],
                "income_control_score": agency["women_income_control_score"],
            }
        )
    return rows


def inclusion_summary(rows: list[dict[str, Any]], *, minimum_group_size: int = 5) -> dict[str, Any]:
    """Summarize agency scores while suppressing small groups."""
    if minimum_group_size < 1:
        raise ValueError("minimum_group_size must be at least 1")
    women = [row for row in rows if row["gender"] == "woman"]
    scored = [row for row in women if row["loan_control_score"] is not None]
    if len(scored) < minimum_group_size:
        return {"n": len(scored), "suppressed": True}
    return {
        "n": len(scored),
        "suppressed": False,
        "mean_loan_control_score": round(mean(row["loan_control_score"] for row in scored), 4),
        "mean_income_control_score": round(mean(row["income_control_score"] for row in scored), 4),
    }


def inclusion_by_district(
    rows: list[dict[str, Any]], *, minimum_group_size: int = 5
) -> dict[str, dict[str, Any]]:
    """Return women agency summaries by district with small-cell suppression."""
    groups: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        if row["gender"] == "woman":
            groups.setdefault(row["district"], []).append(row)
    return {
        district: inclusion_summary(group, minimum_group_size=minimum_group_size)
        for district, group in sorted(groups.items())
    }


def inclusion_report(
    tables: dict[str, list[dict[str, Any]]], *, minimum_group_size: int = 5
) -> dict[str, Any]:
    """Build aggregate inclusion results without exposing client-level rows."""
    rows = inclusion_rows(tables)
    return {
        "data_layer": "synthetic",
        "interpretation": "reported agency differences; not automatically causal",
        "minimum_group_size": minimum_group_size,
        "overall": inclusion_summary(rows, minimum_group_size=minimum_group_size),
        "by_district": inclusion_by_district(rows, minimum_group_size=minimum_group_size),
    }


def write_inclusion_report(report: dict[str, Any], output_path: Path) -> None:
    """Write aggregate inclusion results as stable JSON."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")