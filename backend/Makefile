.PHONY: help install install-dev test lint format type-check clean

help:
	@echo "Available commands:"
	@echo "  make install       - Install production dependencies"
	@echo "  make install-dev   - Install development dependencies"
	@echo "  make test          - Run tests with coverage"
	@echo "  make lint          - Run flake8 linter"
	@echo "  make format        - Format code with black and isort"
	@echo "  make format-check  - Check code formatting without changes"
	@echo "  make type-check    - Run mypy type checker"
	@echo "  make clean         - Remove build artifacts and cache"

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

test:
	pytest --cov=. --cov-report=term-missing --cov-report=html

lint:
	flake8 .

format:
	black .
	isort .

format-check:
	black --check .
	isort --check-only .

type-check:
	mypy .

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache .mypy_cache .coverage htmlcov
	rm -rf *.egg-info build dist
