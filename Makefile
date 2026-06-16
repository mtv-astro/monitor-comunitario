.PHONY: install api test lint format typecheck doctor docker-up docker-down docker-logs docker-build

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

docker-build:
	docker compose --env-file .env.docker.example build

docker-up:
	docker compose --env-file .env.docker.example up --build

docker-down:
	docker compose --env-file .env.docker.example down

docker-logs:
	docker compose --env-file .env.docker.example logs -f
