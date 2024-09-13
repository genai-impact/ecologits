import pytest
import mistralai
import os
from importlib.metadata import version

_mistral_v0 = version("mistralai").split(".")[0] == "0"
_api_key = os.getenv("MISTRAL_API_KEY", "")

@pytest.mark.vcr
def test_mistralai_chat(tracer_init):
    if _mistral_v0:
        client = mistralai.client.MistralClient()
        response = client.chat(
            messages=[{"role": "user", "content": "Hello World!"}], model="mistral-tiny"
        )
    else:
        client = mistralai.Mistral(
            api_key=_api_key
        )
        response = client.chat.complete(
            messages=[{"role": "user", "content": "Hello World!"}], model="mistral-tiny"
        )
    assert len(response.choices) > 0
    assert response.impacts.energy.value > 0


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_mistralai_async_chat(tracer_init):
    if _mistral_v0:
        client = mistralai.async_client.MistralAsyncClient()
        response = await client.chat(
            messages=[{"role": "user", "content": "Hello World!"}], model="mistral-tiny"
        )
    else:
        client = mistralai.Mistral(
            api_key=_api_key
        )
        response = await client.chat.complete_async(
            messages=[{"role": "user", "content": "Hello World!"}], model="mistral-tiny"
        )
    assert len(response.choices) > 0
    assert response.impacts.energy.value > 0


@pytest.mark.vcr
def test_mistralai_stream_chat(tracer_init):
    if _mistral_v0:
        client = mistralai.client.MistralClient()
        stream = client.chat_stream(
            messages=[{"role": "user", "content": "Hello World!"}], model="mistral-tiny"
        )
    else:
        client = mistralai.Mistral(
            api_key=_api_key
        )
        stream = client.chat.stream(
            messages=[{"role": "user", "content": "Hello World!"}], model="mistral-tiny"
        )
    for chunk in stream:
        assert chunk.data.impacts.energy.value >= 0


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_mistralai_async_stream_chat(tracer_init):
    if _mistral_v0:
        client = mistralai.async_client.MistralAsyncClient()
        stream = client.chat_stream(
            messages=[{"role": "user", "content": "Hello World!"}], model="mistral-tiny"
        )
    else:
        client = mistralai.Mistral(
            api_key=_api_key
        )
        stream = await client.chat.stream_async(
            messages=[{"role": "user", "content": "Hello World!"}], model="mistral-tiny"
        )
    async for chunk in stream:
        if hasattr(chunk, "impacts"):
            assert chunk.data.impacts.energy.value >= 0
