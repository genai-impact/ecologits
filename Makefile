
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

.PHONY: paper
paper: 
	docker run --rm \
		--volume "${PWD}"/paper:/data \
		--user $(id -u):$(id -g) \
		--env JOURNAL=joss \
		openjournals/inara
