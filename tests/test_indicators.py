from client_impact.indicators import debt_service_ratio, income_change


def test_debt_service_ratio_uses_monthly_income_denominator():
    assert debt_service_ratio(2500, 10000) == 0.25


def test_debt_service_ratio_returns_none_for_nonpositive_income():
    assert debt_service_ratio(2500, 0) is None


def test_income_change_is_followup_minus_baseline():
    assert income_change(12000, 15000) == 3000
