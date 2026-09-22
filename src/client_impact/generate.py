"""Generate a linked, deterministic synthetic client-impact dataset."""

from __future__ import annotations

import csv
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class SyntheticConfig:
    """Controls the size and reproducibility of a generated dataset."""

    seed: int = 20260922
    clients: int = 100
    start_month: str = "2025-01"


TABLE_NAMES = (
    "clients",
    "households",
    "businesses",
    "loans",
    "other_debts",
    "savings",
    "outcome_surveys",
    "wellbeing_surveys",
    "agency_surveys",
    "complaints",
    "dropout_events",
)


def generate_dataset(config: SyntheticConfig = SyntheticConfig()) -> dict[str, list[dict[str, Any]]]:
    """Generate linked synthetic records using a local, deterministic random stream."""
    if config.clients < 1:
        raise ValueError("clients must be at least 1")
    if len(config.start_month) != 7 or config.start_month[4] != "-":
        raise ValueError("start_month must use YYYY-MM format")

    rng = random.Random(config.seed)
    tables = {name: [] for name in TABLE_NAMES}
    districts = ("Dhaka", "Cumilla", "Sunamganj", "Rajshahi", "Khulna")
    genders = ("woman", "man", "nonbinary_or_other")
    business_types = ("retail", "agriculture", "food", "services", "livestock")
    loan_purposes = ("productive", "emergency", "consumption", "debt_replacement")

    for number in range(1, config.clients + 1):
        client_id = f"C{number:06d}"
        household_id = f"H{number:06d}"
        business_id = f"B{number:06d}"
        loan_id = f"L{number:06d}"
        gender = rng.choice(genders)
        age_band = rng.choice(("18-24", "25-34", "35-44", "45-54", "55+"))
        district = rng.choice(districts)
        household_size = rng.randint(2, 8)
        baseline_income = rng.randint(8_000, 45_000)
        business_type = rng.choice(business_types)
        baseline_revenue = rng.randint(5_000, 55_000)
        baseline_profit = max(500, baseline_revenue * rng.uniform(0.08, 0.32))
        loan_amount = rng.randint(10_000, 100_000)
        loan_purpose = rng.choice(loan_purposes)
        monthly_payment = round(loan_amount * rng.uniform(0.055, 0.12), 2)
        other_lender_count = rng.choices((0, 1, 2, 3), weights=(55, 25, 15, 5))[0]
        other_debt = round(other_lender_count * rng.uniform(4_000, 25_000), 2)
        savings_balance = round(rng.uniform(500, 25_000), 2)
        income_change_factor = rng.uniform(-0.10, 0.35)
        followup_income = round(baseline_income * (1 + income_change_factor), 2)
        followup_revenue = round(baseline_revenue * (1 + rng.uniform(-0.15, 0.45)), 2)
        followup_profit = round(max(0, followup_revenue * rng.uniform(0.08, 0.34)), 2)
        followup_savings = round(max(0, savings_balance + rng.uniform(-2_000, 8_000)), 2)
        essential_reduction = income_change_factor < 0 and rng.random() < 0.45
        business_operating = rng.random() > 0.08
        loan_control = round(rng.uniform(0.35, 1.0), 2)
        income_control = round(rng.uniform(0.25, loan_control), 2)

        tables["clients"].append(
            {
                "client_id": client_id,
                "age_band": age_band,
                "gender": gender,
                "district": district,
                "enrolment_month": config.start_month,
                "borrower_status": "active",
            }
        )
        tables["households"].append(
            {
                "household_id": household_id,
                "client_id": client_id,
                "household_size": household_size,
                "monthly_household_income": baseline_income,
            }
        )
        tables["businesses"].append(
            {
                "business_id": business_id,
                "client_id": client_id,
                "business_type": business_type,
                "monthly_revenue": round(baseline_revenue, 2),
                "monthly_profit": round(baseline_profit, 2),
                "business_operating": True,
            }
        )
        tables["loans"].append(
            {
                "loan_id": loan_id,
                "client_id": client_id,
                "loan_purpose": loan_purpose,
                "loan_amount": loan_amount,
                "loan_cycle": rng.randint(1, 4),
                "monthly_debt_payment": monthly_payment,
            }
        )
        tables["other_debts"].append(
            {
                "client_id": client_id,
                "other_lender_count": other_lender_count,
                "total_other_lender_debt": other_debt,
            }
        )
        tables["savings"].append(
            {
                "client_id": client_id,
                "survey_round": "baseline",
                "savings_balance": savings_balance,
            }
        )
        tables["savings"].append(
            {
                "client_id": client_id,
                "survey_round": "followup",
                "savings_balance": followup_savings,
            }
        )
        tables["outcome_surveys"].extend(
            [
                {
                    "client_id": client_id,
                    "survey_round": "baseline",
                    "monthly_business_revenue": round(baseline_revenue, 2),
                    "monthly_business_profit": round(baseline_profit, 2),
                    "business_operating": True,
                },
                {
                    "client_id": client_id,
                    "survey_round": "followup",
                    "monthly_business_revenue": followup_revenue,
                    "monthly_business_profit": followup_profit,
                    "business_operating": business_operating,
                },
            ]
        )
        tables["wellbeing_surveys"].extend(
            [
                {
                    "client_id": client_id,
                    "survey_round": "baseline",
                    "monthly_household_income": baseline_income,
                    "food_security_score": rng.randint(35, 75),
                    "essential_expense_reduction": False,
                },
                {
                    "client_id": client_id,
                    "survey_round": "followup",
                    "monthly_household_income": followup_income,
                    "food_security_score": rng.randint(35, 85),
                    "essential_expense_reduction": essential_reduction,
                },
            ]
        )
        tables["agency_surveys"].append(
            {
                "client_id": client_id,
                "survey_round": "followup",
                "women_loan_control_score": loan_control if gender == "woman" else None,
                "women_income_control_score": income_control if gender == "woman" else None,
            }
        )
        if rng.random() < 0.18:
            tables["complaints"].append(
                {
                    "complaint_id": f"CP{number:06d}",
                    "client_id": client_id,
                    "complaint_category": rng.choice(("pricing", "treatment", "schedule", "service")),
                    "resolved": rng.random() > 0.12,
                    "resolution_days": rng.randint(1, 21),
                }
            )
        if rng.random() < 0.10:
            tables["dropout_events"].append(
                {
                    "client_id": client_id,
                    "exit_reason": rng.choice(("income_shock", "moved", "dissatisfied", "completed")),
                    "exit_month": "2025-12",
                }
            )

    validate_dataset(tables)
    return tables


def validate_dataset(tables: dict[str, list[dict[str, Any]]]) -> None:
    """Raise ValueError when generated records violate the CI2 data contract."""
    missing = set(TABLE_NAMES) - set(tables)
    if missing:
        raise ValueError(f"missing tables: {sorted(missing)}")
    client_ids = {row["client_id"] for row in tables["clients"]}
    if len(client_ids) != len(tables["clients"]):
        raise ValueError("client_id values must be unique")
    for table_name, rows in tables.items():
        for row in rows:
            if "client_id" in row and row["client_id"] not in client_ids:
                raise ValueError(f"{table_name} contains an unknown client_id")
    for row in tables["households"]:
        if row["household_size"] < 1 or row["monthly_household_income"] <= 0:
            raise ValueError("households contain an invalid size or income")
    for row in tables["loans"]:
        if row["loan_amount"] <= 0 or row["monthly_debt_payment"] <= 0:
            raise ValueError("loans contain a non-positive amount or payment")
    for row in tables["other_debts"]:
        if row["other_lender_count"] < 0 or row["total_other_lender_debt"] < 0:
            raise ValueError("other debts contain a negative value")
    for row in tables["agency_surveys"]:
        for field in ("women_loan_control_score", "women_income_control_score"):
            score = row[field]
            if score is not None and not 0 <= score <= 1:
                raise ValueError(f"{field} must be between 0 and 1")


def write_dataset(tables: dict[str, list[dict[str, Any]]], output_dir: Path) -> None:
    """Write each generated table as a UTF-8 CSV file."""
    output_dir.mkdir(parents=True, exist_ok=True)
    for table_name, rows in tables.items():
        if not rows:
            continue
        fields = list(rows[0])
        with (output_dir / f"{table_name}.csv").open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)