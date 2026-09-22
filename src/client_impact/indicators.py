"""Small, tested indicators used across the client-impact analysis."""

from __future__ import annotations


def debt_service_ratio(monthly_debt_payment: float, monthly_income: float) -> float | None:
    """Return monthly debt payments as a share of monthly income."""
    if monthly_income <= 0:
        return None
    return monthly_debt_payment / monthly_income


def income_change(baseline_income: float, followup_income: float) -> float:
    """Return the absolute change between baseline and follow-up income."""
    return followup_income - baseline_income
