import litellm
import pytest

from ecologits.tracers.litellm_tracer import litellm_match_model


@pytest.mark.parametrize("model_name,expected_tuple", [
    ("gpt-4o", ("openai", "gpt-4o")),
    ("claude-3-opus", ("anthropic", "claude-3-opus-latest")),
    ("claude-3-5-sonnet", ("anthropic", "claude-3-5-sonnet-latest")),
    ("claude-3-5-sonnet-20240620", ("anthropic", "claude-3-5-sonnet-20240620")),
    ("anthropic/claude-3-5-sonnet-20240620", ("anthropic", "claude-3-5-sonnet-20240620")),
    ("mistral/mistral-large-latest", ("mistralai", "mistral-large-latest")),
    ("command-r", ("cohere", "command-r")),
    ("huggingface/meta-llama/Llama-2-7b", ("huggingface_hub", "meta-llama/Llama-2-7b")),
    ("gemini/gemini-pro", ("google", "gemini-1.0-pro")),
    ("gemini/gemini-pro-vision", ("google", "gemini-1.0-pro-vision")),
    ("gemini/gemini-1.5-pro-latest", ("google", "gemini-1.5-pro"))
])
def test_litellm_match_model(model_name, expected_tuple):
    assert litellm_match_model(model_name) == expected_tuple


@pytest.mark.vcr
def test_litellm_chat(tracer_init):
    response = litellm.completion(
        messages=[{"role": "user", "content": "Hello World!"}], model="claude-3-5-sonnet-20240620"
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
        messages=[{"role": "user", "content": "Hello World!"}], model="claude-3-5-sonnet-20240620", stream=True
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
