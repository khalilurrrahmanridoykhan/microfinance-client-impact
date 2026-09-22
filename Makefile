PYTHON ?= python3

.PHONY: setup test lint synth quality outcomes check

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

check: lint test
