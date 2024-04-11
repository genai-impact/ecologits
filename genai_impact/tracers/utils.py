from typing import Optional

from genai_impact.impacts.llm import compute_llm_impacts as _compute_llm_impacts
from genai_impact.impacts.models import Impacts
from genai_impact.model_repository import models


def _avg(value_range: tuple) -> float:
    return sum(value_range) / len(value_range)


def compute_llm_impacts(
    provider: str,
    model_name: str,
    output_token_count: int,
    request_latency: float,
) -> Optional[Impacts]:
    model = models.find_model(provider=provider, model_name=model_name)
    if model is None:
        # TODO: Replace with proper logging
        print(f"Could not find model `{model_name}` for {provider} provider.")
        return None
    model_active_params = model.active_parameters or _avg(model.active_parameters_range)    # TODO: handle ranges
    model_total_params = model.total_parameters or _avg(model.total_parameters_range)       # TODO: handle ranges
    return _compute_llm_impacts(
        model_active_parameter_count=model_active_params,
        model_total_parameter_count=model_total_params,
        output_token_count=output_token_count,
        request_latency=request_latency
    )
