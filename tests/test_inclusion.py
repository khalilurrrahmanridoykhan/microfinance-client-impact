from client_impact.generate import SyntheticConfig, generate_dataset
from client_impact.inclusion import inclusion_by_district, inclusion_rows, inclusion_summary


def test_inclusion_rows_preserve_gender_and_agency_scores():
    rows = inclusion_rows(generate_dataset(SyntheticConfig(seed=7, clients=4)))

    assert len(rows) == 4
    assert {row["gender"] for row in rows}
    assert all("loan_control_score" in row for row in rows)


def test_inclusion_summary_suppresses_small_groups():
    rows = [
        {"gender": "woman", "loan_control_score": 0.8, "income_control_score": 0.6},
        {"gender": "woman", "loan_control_score": 0.9, "income_control_score": 0.7},
    ]

    summary = inclusion_summary(rows, minimum_group_size=3)

    assert summary == {"n": 2, "suppressed": True}


def test_inclusion_summary_calculates_women_agency_scores():
    rows = [
        {"gender": "woman", "loan_control_score": 0.8, "income_control_score": 0.6},
        {"gender": "woman", "loan_control_score": 0.9, "income_control_score": 0.8},
        {"gender": "man", "loan_control_score": None, "income_control_score": None},
    ]

    summary = inclusion_summary(rows, minimum_group_size=2)

    assert summary["n"] == 2
    assert summary["mean_loan_control_score"] == 0.85


def test_inclusion_by_district_returns_suppressed_groups():
    rows = [
        {"gender": "woman", "district": "Dhaka", "loan_control_score": 0.8, "income_control_score": 0.6}
    ]

    summary = inclusion_by_district(rows, minimum_group_size=2)

    assert summary["Dhaka"]["suppressed"] is True