.PHONY: install api test lint format typecheck doctor

install:
	uv sync --dev
	uv run playwright install chromium

api:
	uv run uvicorn monitor_comunitario.api.main:app --reload

doctor:
	uv run monitor-comunitario doctor

test:
	uv run pytest

lint:
	uv run ruff check .

format:
	uv run ruff format .

typecheck:
	uv run mypy src
