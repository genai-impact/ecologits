GenAI Impact
================

See package documentation on [GenAI Impact](<link-to-mkdocs-material>)

# Contributing


## Use a venv

    python3 -m venv name-of-your-venv

    source name-of-your-venv/bin/activate


## Install dependencies using Poetry

[Install Poetry](https://python-poetry.org/docs/):

    python3 -m pip install "poetry==1.4.0"

Install dependencies:

    poetry install

## Set up API keys

    export OPENAI_API_KEY="<your-key>"  # OpenAI

## Call API and get the impact

    python genai_impact/__main__.py

## Run pre-commit hooks locally

[Install pre-commit](https://pre-commit.com/)


    pre-commit run --all-files


## Utiliser Tox pour tester votre code

    tox -vv
