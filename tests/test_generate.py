from client_impact.generate import SyntheticConfig, generate_dataset, validate_dataset


def test_generation_is_deterministic_for_a_seed():
    config = SyntheticConfig(seed=7, clients=4)
    assert generate_dataset(config) == generate_dataset(config)


def test_generation_creates_expected_links_and_rounds():
    tables = generate_dataset(SyntheticConfig(seed=7, clients=4))
    assert len(tables["clients"]) == 4
    assert len(tables["outcome_surveys"]) == 8
    assert {row["survey_round"] for row in tables["savings"]} == {"baseline", "followup"}
    assert all(row["client_id"].startswith("C") for row in tables["loans"])


def test_validation_rejects_unknown_client():
    tables = generate_dataset(SyntheticConfig(seed=7, clients=2))
    tables["loans"][0]["client_id"] = "C999999"
    try:
        validate_dataset(tables)
    except ValueError as error:
        assert "unknown client_id" in str(error)
    else:
        raise AssertionError("invalid client link was accepted")