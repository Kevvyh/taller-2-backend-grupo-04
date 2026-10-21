.PHONY: install dev prod lint format format-check clean check-tools

check-tools:
	@if ! command -v uv >/dev/null 2>&1; then \
		echo "uv no esta instalado. Instalalo aqui: https://docs.astral.sh/uv/getting-started/installation/"; \
		exit 1; \
	fi

install: check-tools
	uv sync

dev:
	uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 3000

prod:
	uv run uvicorn app.main:app --host 0.0.0.0 --port 3000

lint:
	uv run ruff check --fix app

format:
	uv run ruff format app

format-check:
	uv run ruff format --check app

clean:
	rm -rf .venv dist .ruff_cache
	find . -type d -name "__pycache__" -prune -exec rm -rf {} +
