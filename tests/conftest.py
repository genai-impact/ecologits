import os

import pytest

from genai_impact import Tracer


@pytest.fixture(autouse=True)
def environment():
    os.environ["ANTHROPIC_API_KEY"] = "test-api-key"
    os.environ["MISTRAL_API_KEY"] = "test-api-key"
    os.environ["OPENAI_API_KEY"] = "test-api-key"


@pytest.fixture(scope="session")
def vcr_config():
    return {"filter_headers": [
        "authorization",
        "api-key",
        "x-api-key"
    ]}


@pytest.fixture(scope="session")
def tracer_init():
    Tracer.init()
