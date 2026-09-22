from client_impact.generate import SyntheticConfig, generate_dataset
from client_impact.outcomes import client_outcomes, outcome_summary, subgroup_summary


def test_client_outcomes_calculates_paired_changes():
    outcomes = client_outcomes(generate_dataset(SyntheticConfig(seed=7, clients=4)))

    assert len(outcomes) == 4
    assert {row["gender"] for row in outcomes}
    assert all("income_change" in row for row in outcomes)
    assert all("savings_change" in row for row in outcomes)


def test_outcome_summary_uses_descriptive_rates():
    outcomes = [
        {
            "income_change": 100,
            "business_profit_change": 20,
            "savings_change": 5,
            "business_survived": True,
            "essential_expense_reduction": False,
        },
        {
            "income_change": 300,
            "business_profit_change": 40,
            "savings_change": 15,
            "business_survived": False,
            "essential_expense_reduction": True,
        },
    ]

    summary = outcome_summary(outcomes)

    assert summary["n"] == 2
    assert summary["median_income_change"] == 200
    assert summary["business_survival_rate"] == 0.5
    assert summary["essential_expense_reduction_rate"] == 0.5


def test_subgroup_summary_groups_by_gender():
    outcomes = [
        {
            "gender": "woman",
            "income_change": 100,
            "business_profit_change": 20,
            "savings_change": 5,
            "business_survived": True,
            "essential_expense_reduction": False,
        },
        {
            "gender": "man",
            "income_change": 300,
            "business_profit_change": 40,
            "savings_change": 15,
            "business_survived": True,
            "essential_expense_reduction": False,
        },
    ]

    summary = subgroup_summary(outcomes, "gender")

    assert set(summary) == {"man", "woman"}
    assert summary["woman"]["median_income_change"] == 100