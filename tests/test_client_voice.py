from client_impact.client_voice import client_voice_summary, write_client_voice_report


def _tables():
    return {
        "clients": [{"client_id": "C1"}, {"client_id": "C2"}],
        "complaints": [
            {"client_id": "C1", "complaint_category": "pricing", "resolved": True, "resolution_days": 4},
            {"client_id": "C2", "complaint_category": "pricing", "resolved": False, "resolution_days": 12},
        ],
        "dropout_events": [{"client_id": "C2", "exit_reason": "income_shock"}],
        "outcome_surveys": [
            {"client_id": "C1", "survey_round": "followup", "satisfaction_score": 4},
            {"client_id": "C2", "survey_round": "followup", "satisfaction_score": 2},
        ],
    }


def test_client_voice_summary_calculates_rates_and_counts():
    summary = client_voice_summary(_tables())

    assert summary["mean_satisfaction_score"] == 3
    assert summary["complaint_rate_per_1000"] == 1000
    assert summary["complaint_resolution_rate"] == 0.5
    assert summary["median_resolution_days"] == 4
    assert summary["voluntary_exit_rate"] == 0.5
    assert summary["complaints_by_category"] == {"pricing": 2}


def test_client_voice_report_can_be_written_as_json(tmp_path):
    output_path = tmp_path / "client-voice.json"
    write_client_voice_report(client_voice_summary(_tables()), output_path)

    assert '"complaint_n": 2' in output_path.read_text(encoding="utf-8")