"""Export aggregate synthetic reports for the static dashboard."""

from __future__ import annotations

import json
from pathlib import Path

from client_impact import (
    client_voice_summary,
    evaluation_report,
    financial_health_report,
    generate_dataset,
    inclusion_report,
    outcome_report,
    uncertainty_report,
)


def main() -> None:
    output_dir = Path("web/public/data")
    output_dir.mkdir(parents=True, exist_ok=True)
    tables = generate_dataset()
    reports = {
        "outcomes": outcome_report(tables),
        "uncertainty": uncertainty_report(tables),
        "financial-health": financial_health_report(tables),
        "inclusion": inclusion_report(tables),
        "client-voice": client_voice_summary(tables),
        "evaluation": evaluation_report(tables),
    }
    for name, report in reports.items():
        (output_dir / f"{name}.json").write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )


if __name__ == "__main__":
    main()