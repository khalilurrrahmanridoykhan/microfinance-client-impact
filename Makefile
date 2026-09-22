PYTHON ?= python3

.PHONY: setup test lint synth quality outcomes uncertainty financial-health check

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

check: lint test
