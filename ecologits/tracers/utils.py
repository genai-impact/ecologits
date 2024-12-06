from typing import Optional

from ecologits.impacts.llm import compute_llm_impacts
from ecologits.impacts.modeling import Impacts
from ecologits.log import logger
from ecologits.repositories.electricity_mix_repository import electricity_mixes
from ecologits.repositories.electricity_wue_repository import electricity_wue_list
from ecologits.repositories.model_repository import ParametersMoE, models

DEFAULT_ZONE = "WOR"


def _avg(value_range: tuple) -> float:
    return sum(value_range) / len(value_range)


def llm_impacts(
    provider: str,
    model_name: str,
    output_token_count: int,
    request_latency: float,
    electricity_zone: Optional[str] = DEFAULT_ZONE,
) -> Optional[Impacts]:
    """
    High-level function to compute the impacts of an LLM generation request.

    Args:
        provider: Name of the provider.
        model_name: Name of the LLM used.
        output_token_count: Number of generated tokens.
        request_latency: Measured request latency in seconds.
        electricity_zone: ISO 3166-1 alpha-3 code of the electricity mix zone (WOR by default).

    Returns:
        The impacts of an LLM generation request.
    """

    model = models.find_model(provider=provider, model_name=model_name)
    if model is None:
        logger.debug(f"Could not find model `{model_name}` for {provider} provider.")
        return None

    if isinstance(model.architecture.parameters, ParametersMoE):
        model_total_params = model.architecture.parameters.total
        model_active_params = model.architecture.parameters.active
    else:
        model_total_params = model.architecture.parameters
        model_active_params = model.architecture.parameters

    electricity_mix = electricity_mixes.find_electricity_mix(zone=electricity_zone)
    electricity_wue = electricity_wue_list.find_electricity_wue(zone=electricity_zone)

    # TODO: here handle if defined for one but not the other
    if electricity_mix is None:
        logger.warning(f"Could not find zone `{electricity_zone}` in the electricity \
                       mixes database (ADEME), world average used instead.")
        electricity_mix = electricity_mixes.find_electricity_mix(zone=DEFAULT_ZONE)
    if electricity_wue is None:
        logger.warning(f"Could not find zone `{electricity_zone}` in the electricty \
                       WUE database (WRI), world average used instead.")
        electricity_wue = electricity_wue_list.find_electricity_mix(zone=DEFAULT_ZONE)

    if_electricity_mix_adpe=electricity_mix.adpe
    if_electricity_mix_pe=electricity_mix.pe
    if_electricity_mix_gwp=electricity_mix.gwp
    wue_off_site=electricity_wue.wue
    return compute_llm_impacts(
        model_active_parameter_count=model_active_params,
        model_total_parameter_count=model_total_params,
        output_token_count=output_token_count,
        request_latency=request_latency,
        if_electricity_mix_adpe=if_electricity_mix_adpe,
        if_electricity_mix_pe=if_electricity_mix_pe,
        if_electricity_mix_gwp=if_electricity_mix_gwp,
        wue_off_site=wue_off_site,
    )
