import pytest
from mistralai.client import MistralClient
from mistralai.async_client import MistralAsyncClient


@pytest.mark.vcr
def test_mistralai_chat(tracer_init):
    client = MistralClient()
    response = client.chat(
        messages=[{"role": "user", "content": "Hello World!"}], model="mistral-tiny"
    )
    assert len(response.choices) > 0
    assert response.impacts.energy > 0


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_async_mistralai_chat(tracer_init):
    client = MistralAsyncClient()
    response = await client.chat(
        messages=[{"role": "user", "content": "Hello World!"}], model="mistral-tiny"
    )
    assert len(response.choices) > 0
    assert response.impacts.energy > 0
