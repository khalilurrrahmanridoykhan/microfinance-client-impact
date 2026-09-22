"""Evaluation-design diagnostics that keep causal claims evidence-based."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .outcomes import client_outcomes, outcome_summary


def evaluation_readiness(
    tables: dict[str, list[dict[str, Any]]], group_field: str = "evaluation_group"
) -> dict[str, Any]:
    """Assess whether the tables contain the minimum structure for causal comparison."""
    clients = tables.get("clients", [])
    groups = {row.get(group_field) for row in clients if row.get(group_field) is not None}
    reasons: list[str] = []
    if not groups:
        reasons.append(f"clients table has no non-null {group_field} field")
    elif len(groups) < 2:
        reasons.append("fewer than two evaluation groups are present")
    if not tables.get("wellbeing_surveys"):
        reasons.append("no repeated outcome observations are present")
    if reasons:
        return {
            "causal_ready": False,
            "evaluation_group_field": group_field,
            "group_count": len(groups),
            "reasons": reasons,
        }
    return {
        "causal_ready": True,
        "evaluation_group_field": group_field,
        "group_count": len(groups),
        "reasons": [],
    }


def descriptive_evaluation_summary(tables: dict[str, list[dict[str, Any]]]) -> dict[str, Any]:
    """Return a paired before/after summary explicitly labeled as non-causal."""
    return {
        "estimand": "paired descriptive change",
        "causal_interpretation_allowed": False,
        "summary": outcome_summary(client_outcomes(tables)),
    }


def evaluation_report(tables: dict[str, list[dict[str, Any]]]) -> dict[str, Any]:
    """Build an aggregate evaluation-design and descriptive-outcome report."""
    return {
        "data_layer": "synthetic",
        "readiness": evaluation_readiness(tables),
        "descriptive_analysis": descriptive_evaluation_summary(tables),
    }


def write_evaluation_report(report: dict[str, Any], output_path: Path) -> None:
    """Write the evaluation report as stable, human-readable JSON."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")