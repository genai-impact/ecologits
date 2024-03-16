import pytest

from genai_impact import Tracer


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
