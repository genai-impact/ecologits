import pytest
import google.generativeai as genai


@pytest.mark.vcr
def test_google_chat(tracer_init):
    genai.configure(api_key="") #TODO add a key or record VCR
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content("Write a story about a magic backpack.")
    assert len(response.text) > 0
    assert response.impacts.energy.value > 0
