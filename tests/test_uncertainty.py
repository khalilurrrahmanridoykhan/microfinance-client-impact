import pytest

from client_impact.generate import SyntheticConfig, generate_dataset
from client_impact.uncertainty import bootstrap_median_interval, followup_coverage


def test_bootstrap_median_interval_is_reproducible():
    values = [10, 20, 30, 40, 50]

    first = bootstrap_median_interval(values, seed=7, resamples=100)
    second = bootstrap_median_interval(values, seed=7, resamples=100)

    assert first == second
    assert first["estimate"] == 30
    assert first["lower"] <= first["estimate"] <= first["upper"]


def test_bootstrap_median_interval_rejects_invalid_arguments():
    with pytest.raises(ValueError, match="must not be empty"):
        bootstrap_median_interval([])
    with pytest.raises(ValueError, match="at least 1"):
        bootstrap_median_interval([1], resamples=0)


def test_followup_coverage_reports_paired_records():
    tables = generate_dataset(SyntheticConfig(seed=7, clients=4))

    coverage = followup_coverage(tables)

    assert coverage["baseline_n"] == 4
    assert coverage["followup_n"] == 4
    assert coverage["paired_n"] == 4
    assert coverage["paired_rate"] == 1.0