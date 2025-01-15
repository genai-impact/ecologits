import importlib.metadata
import importlib.util
from dataclasses import dataclass, field
from typing import Optional, Union

from packaging.version import Version

from ecologits.domain import EcoLogitsConfiguration, Instrumentor, Provider
from ecologits.exceptions import EcoLogitsError
from ecologits.log import logger
from ecologits.tracers.anthropic_tracer import AnthropicInstrumentor



class EcoLogits:
    """
    EcoLogits instrumentor to initialize function patching for each provider.

    By default, the initialization will be done on all available and compatible providers that are supported by the
    library.

    Examples:
        EcoLogits initialization example with OpenAI.
        ```python
        from ecologits import EcoLogits
        from openai import OpenAI

        EcoLogits.init()

        client = OpenAI(api_key="<OPENAI_API_KEY>")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "Tell me a funny joke!"}
            ]
        )

        # Get estimated environmental impacts of the inference
        print(f"Energy consumption: {response.impacts.energy.value} kWh")
        print(f"GHG emissions: {response.impacts.gwp.value} kgCO2eq")
        ```

    """

    config: EcoLogitsConfiguration
    providers: list[type[Provider]]


@staticmethod
def init(
    config_path: str = None,
    providers: Union[str, list[str]] = None,
    electricity_mix_zone: str = "WOR",
) -> None:
    """
    Initialization method.

    Args:
        providers: list of providers to initialize (all providers by default).
        electricity_mix_zone: ISO 3166-1 alpha-3 code of the electricity mix zone (WOR by default).
    """
    for provider_name in providers:
        try:
            EcoLogits.providers += providers_tracers[provider_name](provider_name)
        except KeyError as e:
            raise EcoLogitsError(f"Could not find tracer for the `{provider_name}` provider.") from e
