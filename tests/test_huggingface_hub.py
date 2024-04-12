import pytest

from huggingface_hub import InferenceClient, AsyncInferenceClient


@pytest.mark.vcr
def test_huggingface_hub_chat(tracer_init):
    client = InferenceClient(model="HuggingFaceH4/zephyr-7b-beta")
    response = client.chat_completion(
        messages=[{"role": "user", "content": "Hello World!"}],
        max_tokens=15
    )
    assert len(response.choices) > 0
    assert response.impacts.energy.value > 0


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_huggingface_hub_async_chat(tracer_init):
    client = AsyncInferenceClient(model="HuggingFaceH4/zephyr-7b-beta")
    response = await client.chat_completion(
        messages=[{"role": "user", "content": "Hello World!"}],
        max_tokens=15
    )
    assert len(response.choices) > 0
    assert response.impacts.energy.value > 0
