from client_impact.evaluation import (
    descriptive_evaluation_summary,
    evaluation_readiness,
    evaluation_report,
    write_evaluation_report,
)
from client_impact.generate import SyntheticConfig, generate_dataset


def test_current_synthetic_data_is_not_causal_ready():
    readiness = evaluation_readiness(generate_dataset(SyntheticConfig(seed=7, clients=4)))

    assert readiness["causal_ready"] is False
    assert readiness["group_count"] == 0
    assert "evaluation_group" in readiness["reasons"][0]


def test_two_groups_are_causal_ready_for_further_diagnostics():
    tables = generate_dataset(SyntheticConfig(seed=7, clients=4))
    for index, client in enumerate(tables["clients"]):
        client["evaluation_group"] = "treatment" if index < 2 else "comparison"

    readiness = evaluation_readiness(tables)

    assert readiness["causal_ready"] is True
    assert readiness["group_count"] == 2


def test_descriptive_summary_disallows_causal_interpretation():
    summary = descriptive_evaluation_summary(generate_dataset(SyntheticConfig(seed=7, clients=4)))

    assert summary["estimand"] == "paired descriptive change"
    assert summary["causal_interpretation_allowed"] is False
    assert summary["summary"]["n"] == 4


def test_evaluation_report_is_aggregate_and_exportable(tmp_path):
    report = evaluation_report(generate_dataset(SyntheticConfig(seed=7, clients=4)))
    output_path = tmp_path / "evaluation.json"

    write_evaluation_report(report, output_path)

    assert report["data_layer"] == "synthetic"
    assert report["readiness"]["causal_ready"] is False
    assert "client_id" not in report
    assert '"data_layer": "synthetic"' in output_path.read_text(encoding="utf-8")