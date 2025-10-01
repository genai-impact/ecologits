
.PHONY: install
install:
	poetry install --all-extras --with dev,docs

.PHONY: test
test:
	poetry run pytest

.PHONY: test-record
test-record:
	poetry run pytest --record-mode=once

.PHONY: pre-commit
pre-commit:
	pre-commit run --all-files

.PHONY: docs
docs:
	poetry run mkdocs build

.PHONY: serve-docs
serve-docs:
	poetry run mkdocs serve
