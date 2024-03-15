import pytest
from openai import OpenAI


@pytest.mark.vcr
def test_openai_chat(tracer_init):
    client = OpenAI()
    response = client.chat.completions.create(
        messages=[
            {"role": "user", "content": "Hello World!"}
        ],
        model="gpt-3.5-turbo"
    )
    assert len(response.choices) > 0
    assert response.impacts.energy > 0
