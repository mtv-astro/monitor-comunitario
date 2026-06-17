.PHONY: install api test lint format typecheck doctor db-upgrade db-current db-history docker-up docker-down docker-logs docker-build docker-migrate

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

db-upgrade:
	uv run monitor-comunitario db-upgrade

db-current:
	uv run monitor-comunitario db-current

db-history:
	uv run monitor-comunitario db-history

docker-build:
	docker compose --env-file .env.docker.example build

docker-migrate:
	docker compose --env-file .env.docker.example run --rm migrate

docker-up:
	docker compose --env-file .env.docker.example up --build

docker-down:
	docker compose --env-file .env.docker.example down

docker-logs:
	docker compose --env-file .env.docker.example logs -f
