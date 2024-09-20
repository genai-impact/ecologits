import pytest
import mistralai


@pytest.mark.vcr
def test_mistralai_chat(tracer_init):
    client = mistralai.Mistral()
    response = client.chat.complete(
        messages=[{"role": "user", "content": "Hello World!"}], model="mistral-tiny"
    )
    assert len(response.choices) > 0
    assert response.impacts.energy.value > 0


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_mistralai_async_chat(tracer_init):
    client = mistralai.Mistral()
    response = await client.chat.complete_async(
        messages=[{"role": "user", "content": "Hello World!"}], model="mistral-tiny"
    )
    assert len(response.choices) > 0
    assert response.impacts.energy.value > 0


@pytest.mark.vcr
def test_mistralai_stream_chat(tracer_init):
    client = mistralai.Mistral()
    stream = client.chat.stream(
        messages=[{"role": "user", "content": "Hello World!"}], model="mistral-tiny"
    )
    for chunk in stream:
        assert chunk.data.impacts.energy.value >= 0


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_mistralai_async_stream_chat(tracer_init):
    client = mistralai.Mistral()
    stream = await client.chat.stream_async(
        messages=[{"role": "user", "content": "Hello World!"}], model="mistral-tiny"
    )
    async for chunk in stream:
        if hasattr(chunk, "impacts"):
            assert chunk.data.impacts.energy.value >= 0


@pytest.mark.skip(reason="mistralai v0 will be deprecated")
@pytest.mark.vcr
def test_mistralai_chat_v0(tracer_init):
    client = mistralai.client.MistralClient()
    response = client.chat(
        messages=[{"role": "user", "content": "Hello World!"}], model="mistral-tiny"
    )
    assert len(response.choices) > 0
    assert response.impacts.energy.value > 0


@pytest.mark.skip(reason="mistralai v0 will be deprecated")
@pytest.mark.vcr
@pytest.mark.asyncio
async def test_mistralai_async_chat_v0(tracer_init):
    client = mistralai.async_client.MistralAsyncClient()
    response = await client.chat(
        messages=[{"role": "user", "content": "Hello World!"}], model="mistral-tiny"
    )
    assert len(response.choices) > 0
    assert response.impacts.energy.value > 0


@pytest.mark.skip(reason="mistralai v0 will be deprecated")
@pytest.mark.vcr
def test_mistralai_stream_chat_v0(tracer_init):
    client = mistralai.client.MistralClient()
    stream = client.chat_stream(
        messages=[{"role": "user", "content": "Hello World!"}], model="mistral-tiny"
    )
    for chunk in stream:
        assert chunk.data.impacts.energy.value >= 0


@pytest.mark.skip(reason="mistralai v0 will be deprecated")
@pytest.mark.vcr
@pytest.mark.asyncio
async def test_mistralai_async_stream_chat_v0(tracer_init):
    client = mistralai.async_client.MistralAsyncClient()
    stream = client.chat_stream(
        messages=[{"role": "user", "content": "Hello World!"}], model="mistral-tiny"
    )
    async for chunk in stream:
        if hasattr(chunk, "impacts"):
            assert chunk.data.impacts.energy.value >= 0
