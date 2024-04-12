import os

import pytest
import tiktoken

from ecologits import EcoLogits


tiktoken.get_encoding("cl100k_base")


@pytest.fixture(autouse=True)
def environment():
    set_envvar_if_unset("ANTHROPIC_API_KEY", "test-api-key")
    set_envvar_if_unset("MISTRAL_API_KEY", "test-api-key")
    set_envvar_if_unset("OPENAI_API_KEY", "test-api-key")


def set_envvar_if_unset(name: str, value: str):
    if os.getenv(name) is None:
        os.environ[name] = value


@pytest.fixture(scope="session")
def vcr_config():
    return {"filter_headers": [
        "authorization",
        "api-key",
        "x-api-key"
    ]}


@pytest.fixture(scope="session")
def tracer_init():
    EcoLogits.init()
