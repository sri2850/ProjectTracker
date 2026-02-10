lint:
	ruff check .
format:
	ruff format .
typecheck:
	mypy .
test:
	pytest -q

ci: lint typecheck test
