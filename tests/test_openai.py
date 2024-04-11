import pytest
from openai import OpenAI, AsyncOpenAI


@pytest.mark.vcr
def test_openai_chat(tracer_init):
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Hello World!"}]
    )
    assert len(response.choices) > 0
    assert response.impacts.energy.value > 0


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_openai_async_chat(tracer_init):
    client = AsyncOpenAI()
    response = await client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Hello World!"}]
    )
    assert len(response.choices) > 0
    assert response.impacts.energy.value > 0


@pytest.mark.vcr
def test_openai_stream_chat(tracer_init):
    client = OpenAI()
    stream = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Hello World!"}],
        stream=True
    )
    for chunk in stream:
        assert chunk.impacts.energy.value >= 0


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_openai_async_stream_chat(tracer_init):
    client = AsyncOpenAI()
    stream = await client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Hello World!"}],
        stream=True
    )
    async for chunk in stream:
        assert chunk.impacts.energy.value >= 0
