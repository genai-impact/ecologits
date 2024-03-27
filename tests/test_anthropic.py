import pytest
from anthropic import Anthropic, AsyncAnthropic


@pytest.mark.vcr
def test_anthropic_chat(tracer_init):
    client = Anthropic()
    response = client.messages.create(
        max_tokens=100,
        messages=[{"role": "user", "content": "Hello World!"}],
        model="claude-3-haiku-20240307",
    )
    assert len(response.content) > 0
    assert response.impacts.energy > 0


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_anthropic_async_chat(tracer_init):
    client = AsyncAnthropic()
    response = await client.messages.create(
        max_tokens=100,
        messages=[{"role": "user", "content": "Hello World!"}],
        model="claude-3-haiku-20240307",
    )
    assert len(response.content) > 0
    assert response.impacts.energy > 0

@pytest.mark.vcr
def test_anthropic_stream_chat(tracer_init):
    client = Anthropic()
    with client.messages.stream(
        max_tokens=1024,
        messages=[{"role": "user", "content": "Hello"}],
        model="claude-3-haiku-20240307",
    ) as stream:
        text_response = ''
        for text in stream.text_stream:
            text_response += text

    assert len(text_response) > 0
    
