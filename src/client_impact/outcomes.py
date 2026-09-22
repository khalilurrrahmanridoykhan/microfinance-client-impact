"""Descriptive client-outcome calculations for paired synthetic observations."""

from __future__ import annotations

from statistics import median
from typing import Any


def client_outcomes(tables: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    """Return one paired, descriptive outcome row per client."""
    clients = {row["client_id"]: row for row in tables["clients"]}
    wellbeing = _rounds_by_client(tables["wellbeing_surveys"])
    business = _rounds_by_client(tables["outcome_surveys"])
    savings = _rounds_by_client(tables["savings"])
    rows: list[dict[str, Any]] = []

    for client_id, client in clients.items():
        baseline_wellbeing = wellbeing[client_id]["baseline"]
        followup_wellbeing = wellbeing[client_id]["followup"]
        baseline_business = business[client_id]["baseline"]
        followup_business = business[client_id]["followup"]
        baseline_savings = savings[client_id]["baseline"]
        followup_savings = savings[client_id]["followup"]
        baseline_income = baseline_wellbeing["monthly_household_income"]
        followup_income = followup_wellbeing["monthly_household_income"]
        rows.append(
            {
                "client_id": client_id,
                "gender": client["gender"],
                "district": client["district"],
                "income_change": round(followup_income - baseline_income, 2),
                "income_growth_rate": round((followup_income - baseline_income) / baseline_income, 4),
                "business_profit_change": round(
                    followup_business["monthly_business_profit"]
                    - baseline_business["monthly_business_profit"],
                    2,
                ),
                "business_survived": followup_business["business_operating"],
                "savings_change": round(
                    followup_savings["savings_balance"] - baseline_savings["savings_balance"], 2
                ),
                "food_security_change": (
                    followup_wellbeing["food_security_score"]
                    - baseline_wellbeing["food_security_score"]
                ),
                "essential_expense_reduction": followup_wellbeing["essential_expense_reduction"],
            }
        )
    return rows


def outcome_summary(outcomes: list[dict[str, Any]]) -> dict[str, Any]:
    """Summarize paired outcomes using counts, medians and descriptive rates."""
    if not outcomes:
        return {"n": 0}
    return {
        "n": len(outcomes),
        "median_income_change": round(median(row["income_change"] for row in outcomes), 2),
        "median_business_profit_change": round(
            median(row["business_profit_change"] for row in outcomes), 2
        ),
        "median_savings_change": round(median(row["savings_change"] for row in outcomes), 2),
        "business_survival_rate": round(
            sum(row["business_survived"] for row in outcomes) / len(outcomes), 4
        ),
        "essential_expense_reduction_rate": round(
            sum(row["essential_expense_reduction"] for row in outcomes) / len(outcomes), 4
        ),
    }


def subgroup_summary(outcomes: list[dict[str, Any]], field: str) -> dict[str, dict[str, Any]]:
    """Return the same descriptive summary separately for each subgroup value."""
    groups: dict[str, list[dict[str, Any]]] = {}
    for row in outcomes:
        value = row.get(field)
        if value is not None:
            groups.setdefault(str(value), []).append(row)
    return {value: outcome_summary(rows) for value, rows in sorted(groups.items())}


def _rounds_by_client(rows: list[dict[str, Any]]) -> dict[str, dict[str, dict[str, Any]]]:
    indexed: dict[str, dict[str, dict[str, Any]]] = {}
    for row in rows:
        indexed.setdefault(row["client_id"], {})[row["survey_round"]] = row
    return indexed