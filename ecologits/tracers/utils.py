from typing import Optional

from ecologits.electricity_mix_repository import electricity_mixes
from ecologits.impacts.llm import compute_llm_impacts
from ecologits.impacts.modeling import Impacts
from ecologits.log import logger
from ecologits.model_repository import ArchitectureTypes, models


def _avg(value_range: tuple) -> float:
    return sum(value_range) / len(value_range)


def llm_impacts(
    provider: str,
    model_name: str,
    output_token_count: int,
    request_latency: float,
    electricity_mix_zone: Optional[str] = "WOR",
) -> Optional[Impacts]:
    """
    High-level function to compute the impacts of an LLM generation request.

    Args:
        provider: Name of the provider.
        model_name: Name of the LLM used.
        output_token_count: Number of generated tokens.
        request_latency: Measured request latency in seconds.
        electricity_mix_zone: ISO 3166-1 alpha-3 code of the electricity mix zone (WOR by default).

    Returns:
        The impacts of an LLM generation request.
    """

    model = models.find_model(provider=provider, model_name=model_name)
    if model is None:
        logger.debug(f"Could not find model `{model_name}` for {provider} provider.")
        return None

    if model.architecture.type == ArchitectureTypes.MOE:
        model_total_params = model.architecture.parameters.total
        model_active_params = model.architecture.parameters.active
    else:
        model_total_params = model.architecture.parameters
        model_active_params = model.architecture.parameters

    electricity_mix = electricity_mixes.find_electricity_mix(zone=electricity_mix_zone)
    if electricity_mix is None:
        logger.debug(f"Could not find electricity mix `{electricity_mix_zone}` in the ADEME database")
        return None
    if_electricity_mix_adpe=electricity_mix.adpe
    if_electricity_mix_pe=electricity_mix.pe
    if_electricity_mix_gwp=electricity_mix.gwp
    return compute_llm_impacts(
        model_active_parameter_count=model_active_params,
        model_total_parameter_count=model_total_params,
        output_token_count=output_token_count,
        request_latency=request_latency,
        if_electricity_mix_adpe=if_electricity_mix_adpe,
        if_electricity_mix_pe=if_electricity_mix_pe,
        if_electricity_mix_gwp=if_electricity_mix_gwp,
    )
