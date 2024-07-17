import pytest
import litellm


@pytest.mark.vcr
def test_litellm_chat(tracer_init):
    response = litellm.completion(
        messages=[{"role": "user", "content": "Hello World!"}], model="mistral/mistral-small-latest"
    )
    assert len(response.choices) > 0
    assert response.impacts.energy.value > 0


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_litellm_async_chat(tracer_init):
    response = await litellm.acompletion(
        messages=[{"role": "user", "content": "Hello World!"}], model="command-r"
    )
    assert len(response.choices) > 0
    assert response.impacts.energy.value > 0


@pytest.mark.vcr
def test_litellm_stream_chat(tracer_init):
    stream = litellm.completion(
        messages=[{"role": "user", "content": "Hello World!"}], model="mistral/mistral-small-latest", stream=True
    )
    for chunk in stream:
        assert chunk.impacts.energy.value >= 0


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_litellm_async_stream_chat(tracer_init):
    stream = await litellm.acompletion(
        messages=[{"role": "user", "content": "Hello World!"}], model="claude-3-5-sonnet-20240620", stream=True
    )
    async for chunk in stream:
        assert chunk.impacts.energy.value >= 0
