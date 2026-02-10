.PHONY: lint format format-check typecheck test ci

lint:
	ruff check .

format:
	ruff format .

format-check:
	ruff format --check .

typecheck:
	mypy .

test:
	pytest -q

ci: lint format-check typecheck test
