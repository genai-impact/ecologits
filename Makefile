
install:
	poetry install --all-extras --with dev,docs

test:
	poetry run pytest

test-record:
	poetry run pytest --record-mode=once

pre-commit:
	pre-commit run --all-files
