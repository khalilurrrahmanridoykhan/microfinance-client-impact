import pytest

from client_impact.generate import SyntheticConfig, generate_dataset
from client_impact.uncertainty import (
    bootstrap_median_interval,
    followup_coverage,
    uncertainty_report,
    write_uncertainty_report,
)


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


def test_uncertainty_report_is_aggregate_only():
    report = uncertainty_report(generate_dataset(SyntheticConfig(seed=7, clients=4)))

    assert report["data_layer"] == "synthetic"
    assert report["coverage"]["wellbeing_surveys"]["paired_rate"] == 1.0
    assert "client_id" not in report


def test_uncertainty_report_can_be_written_as_json(tmp_path):
    report = uncertainty_report(generate_dataset(SyntheticConfig(seed=7, clients=2)))
    output_path = tmp_path / "uncertainty.json"

    write_uncertainty_report(report, output_path)

    assert '"data_layer": "synthetic"' in output_path.read_text(encoding="utf-8")