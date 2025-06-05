import pytest

from huggingface_hub import InferenceClient, AsyncInferenceClient


@pytest.mark.vcr
def test_huggingface_hub_chat(tracer_init):
    client = InferenceClient(model="meta-llama/Meta-Llama-3-8B-Instruct")
    response = client.chat_completion(
        messages=[{"role": "user", "content": "Hello World!"}],
        max_tokens=15
    )
    assert len(response.choices) > 0
    assert response.impacts.energy.value > 0


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_huggingface_hub_async_chat(tracer_init):
    client = AsyncInferenceClient(model="meta-llama/Meta-Llama-3-8B-Instruct")
    response = await client.chat_completion(
        messages=[{"role": "user", "content": "Hello World!"}],
        max_tokens=15
    )
    assert len(response.choices) > 0
    assert response.impacts.energy.value > 0


@pytest.mark.vcr
def test_huggingface_hub_stream_chat(tracer_init):
    client = InferenceClient(model="meta-llama/Meta-Llama-3-8B-Instruct")
    stream = client.chat_completion(
        messages=[{"role": "user", "content": "Hello World!"}],
        max_tokens=15,
        stream=True
    )
    for chunk in stream:
        assert chunk.impacts.energy.value > 0


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_huggingface_hub_async_stream_chat(tracer_init):
    client = AsyncInferenceClient(model="meta-llama/Meta-Llama-3-8B-Instruct")
    stream = await client.chat_completion(
        messages=[{"role": "user", "content": "Hello World!"}],
        max_tokens=15,
        stream=True
    )
    async for chunk in stream:
        assert chunk.impacts.energy.value > 0
