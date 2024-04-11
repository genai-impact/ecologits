from typing import Optional

from genai_impact.model_repository import models
from genai_impact.impacts.llm import compute_llm_impacts as _compute_llm_impacts
from genai_impact.impacts.models import Impacts


def compute_llm_impacts(
    provider: str,
    model_name: str,
    output_token_count: int,
    request_latency: float,
) -> Optional[Impacts]:
    model = models.find_model(provider=provider, model_name=model_name)
    if model is None:
        # TODO: Replace with proper logging
        print(f"Could not find model `{model_name}` for openai provider.")
        return None
    model_size = model.active_parameters or model.active_parameters_range
    if isinstance(model_size, (tuple, list)):
        model_size = sum(model_size) / len(model_size)      # TODO: handle ranges
    return _compute_llm_impacts(
        model_parameter_count=model_size,
        output_token_count=output_token_count,
        request_latency=request_latency
    )
