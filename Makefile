
install:
	poetry install --all-extras --with dev,docs

test:
	poetry run pytest

test-record:
	poetry run pytest --record-mode=once
