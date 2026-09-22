PYTHON ?= python3

.PHONY: setup test lint check

setup:
	$(PYTHON) -m pip install -e '.[dev]'

test:
	$(PYTHON) -m pytest

lint:
	$(PYTHON) -m ruff check src tests

check: lint test
