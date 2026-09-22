"""Uncertainty and follow-up coverage helpers for descriptive outcomes."""

from __future__ import annotations

import json
import random
from pathlib import Path
from statistics import median
from typing import Any, Sequence

from .outcomes import client_outcomes


def bootstrap_median_interval(
    values: Sequence[float],
    *,
    seed: int = 20260922,
    resamples: int = 2_000,
    confidence: float = 0.95,
) -> dict[str, Any]:
    """Return a reproducible percentile bootstrap interval for a median."""
    if not values:
        raise ValueError("values must not be empty")
    if resamples < 1:
        raise ValueError("resamples must be at least 1")
    if not 0 < confidence < 1:
        raise ValueError("confidence must be between 0 and 1")

    rng = random.Random(seed)
    sample = list(values)
    medians = [median(rng.choices(sample, k=len(sample))) for _ in range(resamples)]
    alpha = (1 - confidence) / 2
    lower = _percentile(medians, alpha)
    upper = _percentile(medians, 1 - alpha)
    return {
        "estimate": round(median(sample), 2),
        "lower": round(lower, 2),
        "upper": round(upper, 2),
        "confidence": confidence,
        "resamples": resamples,
        "seed": seed,
        "n": len(sample),
    }


def followup_coverage(
    tables: dict[str, list[dict[str, Any]]], table_name: str = "wellbeing_surveys"
) -> dict[str, Any]:
    """Report baseline, follow-up and paired-client coverage for one survey table."""
    if table_name not in tables:
        raise ValueError(f"unknown survey table: {table_name}")
    rounds: dict[str, set[str]] = {"baseline": set(), "followup": set()}
    for row in tables[table_name]:
        survey_round = row.get("survey_round")
        if survey_round in rounds and row.get("client_id") is not None:
            rounds[survey_round].add(row["client_id"])
    baseline_count = len(rounds["baseline"])
    followup_count = len(rounds["followup"])
    paired_count = len(rounds["baseline"] & rounds["followup"])
    return {
        "table": table_name,
        "baseline_n": baseline_count,
        "followup_n": followup_count,
        "paired_n": paired_count,
        "followup_rate": round(followup_count / baseline_count, 4) if baseline_count else None,
        "paired_rate": round(paired_count / baseline_count, 4) if baseline_count else None,
    }


def uncertainty_report(tables: dict[str, list[dict[str, Any]]]) -> dict[str, Any]:
    """Build aggregate bootstrap intervals and survey coverage metrics."""
    outcomes = client_outcomes(tables)
    return {
        "data_layer": "synthetic",
        "interpretation": "bootstrap intervals describe synthetic paired changes; not causal evidence",
        "median_change_intervals": {
            "income": bootstrap_median_interval([row["income_change"] for row in outcomes]),
            "business_profit": bootstrap_median_interval(
                [row["business_profit_change"] for row in outcomes]
            ),
            "savings": bootstrap_median_interval([row["savings_change"] for row in outcomes]),
        },
        "coverage": {
            "wellbeing_surveys": followup_coverage(tables, "wellbeing_surveys"),
            "outcome_surveys": followup_coverage(tables, "outcome_surveys"),
            "savings": followup_coverage(tables, "savings"),
        },
    }


def write_uncertainty_report(report: dict[str, Any], output_path: Path) -> None:
    """Write aggregate uncertainty results as stable, human-readable JSON."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _percentile(values: Sequence[float], probability: float) -> float:
    ordered = sorted(values)
    position = (len(ordered) - 1) * probability
    lower = int(position)
    upper = min(lower + 1, len(ordered) - 1)
    fraction = position - lower
    return ordered[lower] + (ordered[upper] - ordered[lower]) * fraction