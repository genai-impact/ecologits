import pytest
from ecologits import EcoLogits
from ecologits.exceptions import EcoLogitsError

from openai import OpenAI
from anthropic import Anthropic


@pytest.mark.skip(reason="Double init does not raise an error anymore, but we should test that it works correctly.")
def test_double_init(tracer_init):
    with pytest.raises(EcoLogitsError) as e:
        EcoLogits.init()   # Second initialization


@pytest.mark.skip(reason="Must implement un-instrument behavior first.")
def test_init_openai_only():
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

@pytest.mark.vcr
def test_init_with_different_mixes():
    client = Anthropic()

    EcoLogits.init(electricity_mix_zone="FRA")
    message_under_french_mix = client.messages.create(
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": "Hello, Claude",
            }
        ],
        model="claude-3-opus-20240229",
    )

    EcoLogits.init(electricity_mix_zone="BEL")
    message_under_belgian_mix = client.messages.create(
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": "Hello, Claude",
            }
        ],
        model="claude-3-opus-20240229",
    )

    assert message_under_belgian_mix.impacts.energy.value.min != message_under_french_mix.impacts.energy.value.min
    