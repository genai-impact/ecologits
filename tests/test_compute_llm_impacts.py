import pytest

from genai_impact.impacts.llm import compute_llm_impacts


@pytest.mark.parametrize(
    ['model_active_parameter_count', 'model_total_parameter_count', 'output_token_count', 'request_latency'],
    [
        (7.3, 7.3, 200, 5),         # Mistral 7B
        (12.9, 46.7, 200, 10)       # Mixtral 8x7B
    ]
)
def test_compute_llm_impacts(model_active_parameter_count: float,
                             model_total_parameter_count: float,
                             output_token_count: int,
                             request_latency: float) -> None:
    impacts = compute_llm_impacts(
        model_active_parameter_count=model_active_parameter_count,
        model_total_parameter_count=model_total_parameter_count,
        output_token_count=output_token_count,
        request_latency=request_latency
    )
    assert impacts.energy.value > 0
    assert impacts.gwp.value > 0
    assert impacts.adpe.value > 0
    assert impacts.pe.value > 0
    assert impacts.usage.energy.value > 0
    assert impacts.usage.gwp.value > 0
    assert impacts.usage.adpe.value > 0
    assert impacts.usage.pe.value > 0
    assert impacts.embodied.gwp.value > 0
    assert impacts.embodied.adpe.value > 0
    assert impacts.embodied.pe.value > 0
