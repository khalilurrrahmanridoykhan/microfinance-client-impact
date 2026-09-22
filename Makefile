PYTHON ?= python3

.PHONY: setup test lint synth quality outcomes uncertainty financial-health inclusion client-voice evaluation check

setup:
	$(PYTHON) -m pip install -e '.[dev]'

test:
	$(PYTHON) -m pytest

lint:
	$(PYTHON) -m ruff check src tests

synth:
	PYTHONPATH=src $(PYTHON) -c 'from pathlib import Path; from client_impact import generate_dataset, write_dataset; write_dataset(generate_dataset(), Path("data/synthetic"))'

quality:
	PYTHONPATH=src $(PYTHON) -c 'from pathlib import Path; from client_impact import generate_dataset, quality_report, write_quality_report; write_quality_report(quality_report(generate_dataset()), Path("results/generated/data-quality.json"))'

outcomes:
	PYTHONPATH=src $(PYTHON) -c 'from pathlib import Path; from client_impact import generate_dataset, outcome_report, write_outcome_report; write_outcome_report(outcome_report(generate_dataset()), Path("results/generated/outcomes.json"))'

uncertainty:
	PYTHONPATH=src $(PYTHON) -c 'from pathlib import Path; from client_impact import generate_dataset, uncertainty_report, write_uncertainty_report; write_uncertainty_report(uncertainty_report(generate_dataset()), Path("results/generated/uncertainty.json"))'

financial-health:
	PYTHONPATH=src $(PYTHON) -c 'from pathlib import Path; from client_impact import financial_health_report, generate_dataset, write_financial_health_report; write_financial_health_report(financial_health_report(generate_dataset()), Path("results/generated/financial-health.json"))'

inclusion:
	PYTHONPATH=src $(PYTHON) -c 'from pathlib import Path; from client_impact import generate_dataset, inclusion_report, write_inclusion_report; write_inclusion_report(inclusion_report(generate_dataset()), Path("results/generated/inclusion.json"))'

client-voice:
	PYTHONPATH=src $(PYTHON) -c 'from pathlib import Path; from client_impact import client_voice_summary, generate_dataset, write_client_voice_report; write_client_voice_report(client_voice_summary(generate_dataset()), Path("results/generated/client-voice.json"))'

evaluation:
	PYTHONPATH=src $(PYTHON) -c 'from pathlib import Path; from client_impact import evaluation_report, generate_dataset, write_evaluation_report; write_evaluation_report(evaluation_report(generate_dataset()), Path("results/generated/evaluation.json"))'

check: lint test
