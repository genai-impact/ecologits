import pytest
from mistralai.client import MistralClient


@pytest.mark.vcr
def test_mistralai_chat(tracer_init):
    client = MistralClient()
    response = client.chat(
        messages=[
            {"role": "user", "content": "Hello World!"}
        ],
        model="mistral-tiny"
    )
    assert len(response.choices) > 0
    assert response.impacts.energy > 0
