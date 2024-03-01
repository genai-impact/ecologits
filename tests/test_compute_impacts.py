import pytest

from genai_impact.compute_impacts import compute_llm_impact


@pytest.mark.parametrize("model_size,output_tokens", [(130, 1000), (7, 150)])
def test_compute_impacts_is_positive(model_size: float, output_tokens: int) -> None:
    impacts = compute_llm_impact(model_size, output_tokens)
    assert impacts.energy >= 0
