PYTHON ?= python3

.PHONY: setup test lint synth check

setup:
	$(PYTHON) -m pip install -e '.[dev]'

test:
	$(PYTHON) -m pytest

lint:
	$(PYTHON) -m ruff check src tests

synth:
	PYTHONPATH=src $(PYTHON) -c 'from pathlib import Path; from client_impact import generate_dataset, write_dataset; write_dataset(generate_dataset(), Path("data/synthetic"))'

check: lint test
