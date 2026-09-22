"""Descriptive financial-health and responsible-lending support signals."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from statistics import median
from typing import Any

from .indicators import debt_service_ratio


@dataclass(frozen=True)
class FinancialHealthConfig:
    """Documented thresholds for descriptive human-review support signals."""

    high_total_debt_service_ratio: float = 0.40
    multiple_lender_minimum: int = 2
    other_debt_months: int = 12


def financial_health_rows(
    tables: dict[str, list[dict[str, Any]]],
    config: FinancialHealthConfig = FinancialHealthConfig(),
) -> list[dict[str, Any]]:
    """Return one financial-health row per client without making a credit decision."""
    households = {row["client_id"]: row for row in tables["households"]}
    loans = {row["client_id"]: row for row in tables["loans"]}
    debts = {row["client_id"]: row for row in tables["other_debts"]}
    rows: list[dict[str, Any]] = []

    for client in tables["clients"]:
        client_id = client["client_id"]
        household = households[client_id]
        loan = loans[client_id]
        other_debt = debts[client_id]
        income = household["monthly_household_income"]
        project_payment = loan["monthly_debt_payment"]
        estimated_other_payment = other_debt["total_other_lender_debt"] / config.other_debt_months
        total_monthly_payment = project_payment + estimated_other_payment
        total_ratio = debt_service_ratio(total_monthly_payment, income)
        flags = support_review_flags(
            total_debt_service_ratio=total_ratio,
            other_lender_count=other_debt["other_lender_count"],
            loan_purpose=loan["loan_purpose"],
            config=config,
        )
        rows.append(
            {
                "client_id": client_id,
                "gender": client["gender"],
                "district": client["district"],
                "monthly_income": income,
                "project_monthly_payment": project_payment,
                "estimated_other_monthly_payment": round(estimated_other_payment, 2),
                "total_monthly_payment": round(total_monthly_payment, 2),
                "project_debt_service_ratio": _rounded_ratio(
                    debt_service_ratio(project_payment, income)
                ),
                "total_debt_service_ratio": _rounded_ratio(total_ratio),
                "other_lender_count": other_debt["other_lender_count"],
                "multiple_borrowing": other_debt["other_lender_count"] >= config.multiple_lender_minimum,
                "debt_replacement_purpose": loan["loan_purpose"] == "debt_replacement",
                "support_review_flags": flags,
                "support_review_flagged": bool(flags),
            }
        )
    return rows


def support_review_flags(
    *,
    total_debt_service_ratio: float | None,
    other_lender_count: int,
    loan_purpose: str,
    config: FinancialHealthConfig = FinancialHealthConfig(),
) -> list[str]:
    """Return transparent support signals, never an approval or rejection decision."""
    flags: list[str] = []
    if (
        total_debt_service_ratio is not None
        and total_debt_service_ratio >= config.high_total_debt_service_ratio
    ):
        flags.append("high_total_debt_service_ratio")
    if other_lender_count >= config.multiple_lender_minimum:
        flags.append("multiple_borrowing")
    if loan_purpose == "debt_replacement":
        flags.append("debt_replacement")
    return flags


def financial_health_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    """Summarize financial-health rows for a population or subgroup."""
    if not rows:
        return {"n": 0}
    return {
        "n": len(rows),
        "median_total_debt_service_ratio": round(
            median(row["total_debt_service_ratio"] for row in rows), 4
        ),
        "multiple_borrowing_rate": round(
            sum(row["multiple_borrowing"] for row in rows) / len(rows), 4
        ),
        "debt_replacement_rate": round(
            sum(row["debt_replacement_purpose"] for row in rows) / len(rows), 4
        ),
        "support_review_flag_rate": round(
            sum(row["support_review_flagged"] for row in rows) / len(rows), 4
        ),
    }


def financial_health_report(
    tables: dict[str, list[dict[str, Any]]],
    config: FinancialHealthConfig = FinancialHealthConfig(),
) -> dict[str, Any]:
    """Build aggregate financial-health results without exposing client records."""
    rows = financial_health_rows(tables, config)
    return {
        "data_layer": "synthetic",
        "interpretation": "support signals for human review; not credit decisions",
        "assumptions": {
            "high_total_debt_service_ratio": config.high_total_debt_service_ratio,
            "multiple_lender_minimum": config.multiple_lender_minimum,
            "other_debt_months": config.other_debt_months,
        },
        "overall": financial_health_summary(rows),
        "by_gender": _subgroup_financial_summary(rows, "gender"),
        "by_district": _subgroup_financial_summary(rows, "district"),
    }


def write_financial_health_report(report: dict[str, Any], output_path: Path) -> None:
    """Write aggregate financial-health results as stable JSON."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _rounded_ratio(value: float | None) -> float | None:
    return round(value, 4) if value is not None else None


def _subgroup_financial_summary(
    rows: list[dict[str, Any]], field: str
) -> dict[str, dict[str, Any]]:
    groups: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        value = row.get(field)
        if value is not None:
            groups.setdefault(str(value), []).append(row)
    return {value: financial_health_summary(group) for value, group in sorted(groups.items())}