from typing import Optional

from ecologits.impacts.llm import compute_llm_impacts as _compute_llm_impacts
from ecologits.impacts.models import Impacts
from ecologits.model_repository import models


def _avg(value_range: tuple) -> float:
    return sum(value_range) / len(value_range)


def compute_llm_impacts(
    provider: str,
    model_name: str,
    output_token_count: int,
    request_latency: float,
) -> Optional[Impacts]:
    """
    High-level function to compute the impacts of an LLM generation request.

    Args:
        provider: Name of the provider.
        model_name: Name of the LLM used.
        output_token_count: Number of generated tokens.
        request_latency: Measured request latency.

    Returns:
        The impacts of an LLM generation request.
    """
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
