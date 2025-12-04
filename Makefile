## Makefile

```makefile
.PHONY: help install run test lint clean setup

help:
	@echo ""
	@echo "Available commands:"
	@echo "  make setup       - Install all dependencies"
	@echo "  make run         - Run the full agentic pipeline"
	@echo "  make test        - Run tests with pytest"
	@echo "  make lint        - Run flake8 linting"
	@echo "  make clean       - Remove __pycache__ and cache files"
	@echo ""

setup: install

install:
	pip install --upgrade pip
	pip install -r requirements.txt

run:
	python3 -m src.orchestrator.run

test:
	python -m pytest

lint:
	flake8 src

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .pytest_cache logs/* reports/*
