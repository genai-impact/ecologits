import pytest
from anthropic import Anthropic


@pytest.mark.vcr
def test_anthropic_chat(tracer_init):
    client = Anthropic()
    response = client.messages.create(
        max_tokens=100,
        messages=[
            {"role": "user", "content": "Hello World!"}
        ],
        model="claude-3-haiku-20240307"
    )
    assert len(response.content) > 0
    assert response.impacts.energy > 0
