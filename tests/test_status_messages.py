from ecologits.tracers.utils import llm_impacts
from ecologits.status_messages import (
    ModelArchNotReleasedWarning,
    ModelArchMultimodalWarning,
    ModelNotRegisteredError,
    ZoneNotRegisteredError
)


def test_warnings():
    impacts = llm_impacts(
        provider="openai",
        model_name="gpt-4o-mini",
        output_token_count=10,
        request_latency=10
    )
    assert impacts.energy.value > 0
    assert impacts.has_warnings
    assert isinstance(impacts.warnings[0], (ModelArchNotReleasedWarning, ModelArchMultimodalWarning))
    assert isinstance(impacts.warnings[1], (ModelArchNotReleasedWarning, ModelArchMultimodalWarning))


def test_model_error():
    impacts = llm_impacts(
        provider="openai",
        model_name="unknown-model",
        output_token_count=10,
        request_latency=10
    )
    assert impacts.energy is None
    assert impacts.has_errors
    assert isinstance(impacts.errors[0], ModelNotRegisteredError)


def test_zone_error():
    impacts = llm_impacts(
        provider="openai",
        model_name="gpt-4o-mini",
        output_token_count=10,
        request_latency=10,
        electricity_mix_zone="UNKNOWN-ZONE"
    )
    assert impacts.energy is None
    assert impacts.has_errors
    assert isinstance(impacts.errors[0], ZoneNotRegisteredError)
