import pytest
from google import genai


@pytest.mark.vcr
def test_google_genai_content(tracer_init):
    client = genai.Client()
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents="Tell me a joke!"
    )
    assert len(response.text) > 0
    assert response.impacts.energy.value > 0


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_google_genai_async_content(tracer_init):
    client = genai.Client()
    response = await client.aio.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents="Tell me a joke!"
    )
    assert len(response.text) > 0
    assert response.impacts.energy.value > 0


@pytest.mark.vcr
def test_google_genai_content_stream(tracer_init):
    client = genai.Client()
    stream = client.models.generate_content_stream(
        model="gemini-2.5-flash-lite",
        contents="Tell me a joke!"
    )
    for chunk in stream:
        assert len(chunk.text) > 0

        if chunk.candidates[0].finish_reason is not None:
            assert chunk.impacts.energy.value > 0


@pytest.mark.skip(reason="Test only passes without VCR.")
@pytest.mark.vcr
@pytest.mark.asyncio
async def test_google_genai_async_content_stream(tracer_init):
    client = genai.Client()
    stream = await client.aio.models.generate_content_stream(
        model="gemini-2.5-flash-lite",
        contents="Tell me a joke!"
    )
    async for chunk in stream:
        assert len(chunk.text) > 0

        if chunk.candidates[0].finish_reason is not None:
            assert chunk.impacts.energy.value > 0


@pytest.mark.vcr
def test_google_genai_chat(tracer_init):
    client = genai.Client()
    chat = client.chats.create(model="gemini-2.5-flash-lite")
    response = chat.send_message("Tell me a joke!")
    assert len(response.text) > 0
    assert response.impacts.energy.value > 0


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_google_genai_async_chat(tracer_init):
    client = genai.Client()
    chat = client.aio.chats.create(model="gemini-2.5-flash-lite")
    response = await chat.send_message("Tell me a joke!")
    assert len(response.text) > 0
    assert response.impacts.energy.value > 0


@pytest.mark.vcr
def test_google_genai_chat_stream(tracer_init):
    client = genai.Client()
    chat = client.chats.create(model="gemini-2.5-flash-lite")
    stream = chat.send_message_stream("Tell me a joke!")
    for chunk in stream:
        assert len(chunk.text) > 0

        if chunk.candidates[0].finish_reason is not None:
            assert chunk.impacts.energy.value > 0


@pytest.mark.skip(reason="Test only passes without VCR.")
@pytest.mark.vcr
@pytest.mark.asyncio
async def test_google_genai_async_chat_stream(tracer_init):
    client = genai.Client()
    chat = client.aio.chats.create(model="gemini-2.5-flash-lite")
    stream = await chat.send_message_stream("Tell me a joke!")
    async for chunk in stream:
        assert len(chunk.text) > 0

        if chunk.candidates[0].finish_reason is not None:
            assert chunk.impacts.energy.value > 0