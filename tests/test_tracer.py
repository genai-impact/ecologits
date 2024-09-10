import pytest
from ecologits import EcoLogits

from openai import OpenAI
from anthropic import Anthropic

@pytest.mark.vcr
def test_double_init(tracer_init):
    EcoLogits.init() # second init
    openai_client = OpenAI()
    openai_response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Hello World!"}]
    )
    assert len(openai_response.choices) > 0
    assert hasattr(openai_response, "impacts")

@pytest.mark.skip(reason="Must implement un-instrument behavior first.")
def test_init_with_different_providers():
    EcoLogits.init(providers=["openai"])

    openai_client = OpenAI()
    openai_response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Hello World!"}]
    )
    assert len(openai_response.choices) > 0
    assert hasattr(openai_response, "impacts")

    anthropic_client = Anthropic()
    anthropic_response = anthropic_client.messages.create(
        max_tokens=100,
        messages=[{"role": "user", "content": "Hello World!"}],
        model="claude-3-5-sonnet-20240620",
    )
    assert len(anthropic_response.content) > 0
    assert not hasattr(anthropic_response, "impacts")

    EcoLogits.init(providers=["anthropic"]) # adds anthropic

    openai_response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Hello World!"}]
    )
    assert len(openai_response.choices) > 0
    assert hasattr(openai_response, "impacts")

    anthropic_response = anthropic_client.messages.create(
        max_tokens=100,
        messages=[{"role": "user", "content": "Hello World!"}],
        model="claude-3-5-sonnet-20240620",
    )
    assert len(anthropic_response.content) > 0
    assert hasattr(anthropic_response, "impacts")

@pytest.mark.vcr
def test_init_with_different_mixes():
    seed = 0 # Define seed for having the same answers
    EcoLogits.init() # World's mix
    openai_client = OpenAI()
    openai_response_world = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Hello World!"}], 
        seed=seed,
    )
    EcoLogits.init(electricity_mix_zone="FRA") # Switch to France's mix
    openai_response_france = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Hello World!"}], 
        seed=seed,
    )
    assert openai_response_france.choices == openai_response_world.choices and openai_response_france.impacts.gwp.value < openai_response_world.impacts.gwp.value    