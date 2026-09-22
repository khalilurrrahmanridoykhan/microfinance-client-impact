from client_impact.financial_health import (
    FinancialHealthConfig,
    financial_health_report,
    financial_health_rows,
    financial_health_summary,
    support_review_flags,
    write_financial_health_report,
)
from client_impact.generate import SyntheticConfig, generate_dataset


def _tables():
    return {
        "clients": [{"client_id": "C1", "gender": "woman", "district": "Dhaka"}],
        "households": [{"client_id": "C1", "monthly_household_income": 10_000}],
        "loans": [
            {
                "client_id": "C1",
                "loan_purpose": "debt_replacement",
                "monthly_debt_payment": 3_000,
            }
        ],
        "other_debts": [{"client_id": "C1", "other_lender_count": 2, "total_other_lender_debt": 12_000}],
    }


def test_financial_health_rows_calculates_total_debt_service():
    rows = financial_health_rows(_tables())

    assert rows[0]["estimated_other_monthly_payment"] == 1_000
    assert rows[0]["total_debt_service_ratio"] == 0.4
    assert rows[0]["multiple_borrowing"] is True
    assert rows[0]["debt_replacement_purpose"] is True
    assert rows[0]["support_review_flagged"] is True


def test_support_flags_are_configurable_and_transparent():
    flags = support_review_flags(
        total_debt_service_ratio=0.35,
        other_lender_count=1,
        loan_purpose="productive",
        config=FinancialHealthConfig(high_total_debt_service_ratio=0.30),
    )

    assert flags == ["high_total_debt_service_ratio"]


def test_zero_income_does_not_create_ratio_flag():
    flags = support_review_flags(
        total_debt_service_ratio=None,
        other_lender_count=0,
        loan_purpose="productive",
    )

    assert flags == []


def test_financial_health_summary_calculates_flag_rates():
    rows = financial_health_rows(_tables())

    summary = financial_health_summary(rows)

    assert summary["n"] == 1
    assert summary["multiple_borrowing_rate"] == 1.0
    assert summary["support_review_flag_rate"] == 1.0


def test_financial_health_report_is_aggregate_only(tmp_path):
    report = financial_health_report(generate_dataset(SyntheticConfig(seed=7, clients=4)))
    output_path = tmp_path / "financial-health.json"

    write_financial_health_report(report, output_path)

    assert report["data_layer"] == "synthetic"
    assert report["overall"]["n"] == 4
    assert "client_id" not in report
    assert '"data_layer": "synthetic"' in output_path.read_text(encoding="utf-8")