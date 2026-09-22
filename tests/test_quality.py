from client_impact.generate import SyntheticConfig, generate_dataset
from client_impact.quality import quality_report, write_quality_report


def test_generated_dataset_has_no_quality_errors():
    report = quality_report(generate_dataset(SyntheticConfig(seed=7, clients=4)))
    assert report["ok"] is True
    assert report["error_count"] == 0
    assert report["table_counts"]["clients"] == 4


def test_quality_report_detects_unknown_client_and_negative_loan():
    tables = generate_dataset(SyntheticConfig(seed=7, clients=2))
    tables["loans"][0]["client_id"] = "C999999"
    tables["loans"][1]["loan_amount"] = -1

    report = quality_report(tables)

    assert report["ok"] is False
    assert report["error_count"] == 2
    assert any("unknown client_id" in error for error in report["errors"])
    assert any("invalid loan_amount" in error for error in report["errors"])


def test_quality_report_allows_declared_optional_agency_scores():
    tables = generate_dataset(SyntheticConfig(seed=7, clients=2))
    tables["agency_surveys"][0]["women_loan_control_score"] = None

    report = quality_report(tables)

    assert report["ok"] is True


def test_quality_report_can_be_written_as_json(tmp_path):
    report = quality_report(generate_dataset(SyntheticConfig(seed=7, clients=2)))
    output_path = tmp_path / "data-quality.json"

    write_quality_report(report, output_path)

    assert '"ok": true' in output_path.read_text(encoding="utf-8")