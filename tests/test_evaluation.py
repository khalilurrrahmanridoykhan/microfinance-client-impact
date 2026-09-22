from client_impact.evaluation import descriptive_evaluation_summary, evaluation_readiness
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