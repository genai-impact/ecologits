import pytest
import google.generativeai as genai


@pytest.mark.vcr
def test_google_chat(tracer_init):
    genai.configure(transport='rest')
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content("Write a story about a magic backpack.")
    assert len(response.text) > 0
    assert response.impacts.energy.value > 0


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_google_async_chat(tracer_init):
    genai.configure(transport='grpc_asyncio')
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = await model.generate_content_async("Write a story about a magic backpack.")
    assert len(response.text) > 0
    assert response.impacts.energy.value > 0


@pytest.mark.vcr
def test_google_stream_chat(tracer_init):
    genai.configure(transport='rest')
    model = genai.GenerativeModel("gemini-1.5-flash")
    stream = model.generate_content(
        "Write a story about a magic backpack.", 
        stream = True
    )
    for chunk in stream:
        assert chunk.impacts.energy.value > 0


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_google_async_stream_chat(tracer_init):
    genai.configure(transport='grpc_asyncio')
    model = genai.GenerativeModel("gemini-1.5-flash")
    stream = await model.generate_content_async(
        "Write a story about a magic backpack.", 
        stream = True
    )
    async for chunk in stream:
        assert chunk.impacts.energy.value > 0
