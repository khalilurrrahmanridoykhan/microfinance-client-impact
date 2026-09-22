from client_impact.financial_health import FinancialHealthConfig, financial_health_rows, support_review_flags


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