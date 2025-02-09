import importlib.metadata
import importlib.util
import os
from dataclasses import dataclass, field

import toml  # type: ignore [import-untyped]
from packaging.version import Version

from ecologits.exceptions import EcoLogitsError
from ecologits.log import logger


def init_openai_instrumentor() -> None:
    if importlib.util.find_spec("openai") is not None:
        from ecologits.tracers.openai_tracer import OpenAIInstrumentor

        instrumentor = OpenAIInstrumentor()
        instrumentor.instrument()


def init_anthropic_instrumentor() -> None:
    if importlib.util.find_spec("anthropic") is not None:
        from ecologits.tracers.anthropic_tracer import AnthropicInstrumentor

        instrumentor = AnthropicInstrumentor()
        instrumentor.instrument()


def init_mistralai_instrumentor() -> None:
    if importlib.util.find_spec("mistralai") is not None:
        version = Version(importlib.metadata.version("mistralai"))
        if version < Version("1.0.0"):
            logger.warning("MistralAI client v0.*.* will soon no longer be supported by EcoLogits.")
            from ecologits.tracers.mistralai_tracer_v0 import MistralAIInstrumentor
        else:
            from ecologits.tracers.mistralai_tracer_v1 import MistralAIInstrumentor  # type: ignore[assignment]

        instrumentor = MistralAIInstrumentor()
        instrumentor.instrument()


def init_huggingface_instrumentor() -> None:
    if importlib.util.find_spec("huggingface_hub") is not None:
        version = Version(importlib.metadata.version("huggingface_hub"))
        if version >= Version("0.22.0"):
            from ecologits.tracers.huggingface_tracer import HuggingfaceInstrumentor

            instrumentor = HuggingfaceInstrumentor()
            instrumentor.instrument()


def init_cohere_instrumentor() -> None:
    if importlib.util.find_spec("cohere") is not None:
        from ecologits.tracers.cohere_tracer import CohereInstrumentor

        instrumentor = CohereInstrumentor()
        instrumentor.instrument()


def init_google_instrumentor() -> None:
    if importlib.util.find_spec("google") is not None \
            and importlib.util.find_spec("google.generativeai") is not None:
        from ecologits.tracers.google_tracer import GoogleInstrumentor

        instrumentor = GoogleInstrumentor()
        instrumentor.instrument()


def init_litellm_instrumentor() -> None:
    if importlib.util.find_spec("litellm") is not None:
        from ecologits.tracers.litellm_tracer import LiteLLMInstrumentor

        instrumentor = LiteLLMInstrumentor()
        instrumentor.instrument()


_INSTRUMENTS = {
    "openai": init_openai_instrumentor,
    "anthropic": init_anthropic_instrumentor,
    "mistralai": init_mistralai_instrumentor,
    "huggingface_hub": init_huggingface_instrumentor,
    "cohere": init_cohere_instrumentor,
    "google": init_google_instrumentor,
    "litellm": init_litellm_instrumentor
}

@dataclass
class _Config:
    electricity_mix_zone: str = field(default="WOR")
    providers: list[str] = field(default_factory=list)


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
    config= _Config()

    @staticmethod
    def _read_ecologits_config(config_path: str)-> dict[str, str]|None:

        with open(config_path) as config_file:
            config = toml.load(config_file).get("ecologits", None)
        if config is None:
            logger.warning("Provided file did not contain the ecologits key. Falling back on default configuration")
        return config

    @staticmethod
    def init(
        config_path: str| None = None,
        providers: str | list[str]|None = None,
        electricity_mix_zone: str|None = None,
    ) -> None:
        """
        Initialization static method. Will attempt to initialize all providers by default.

        Args:
            providers: list of providers to initialize (all providers by default).
            electricity_mix_zone: ISO 3166-1 alpha-3 code of the electricity mix zone (WOR by default).
        """
        default_providers = list(set(_INSTRUMENTS.keys()))
        default_electricity_mix_zone = "WOR"

        if config_path is not None and (providers is not None or electricity_mix_zone is not None):
            logger.warning("Both config path and init arguments provided, init arguments will be prioritized")

        if (config_path is None
            and providers is None
            and electricity_mix_zone is None
            and os.path.isfile("pyproject.toml")):

            config_path = "pyproject.toml"

        if config_path:
            try:
                user_config: dict[str, str]|None = EcoLogits._read_ecologits_config(config_path)
                logger.info("Ecologits configuration found in file and loaded")
            except FileNotFoundError:
                logger.warning("Provided file does not exist, will fall back on default values")
                user_config = None

            if user_config is not None:
                providers = user_config.get("providers", default_providers) if providers is None else providers
                electricity_mix_zone =  (user_config.get("electricity_mix_zone", electricity_mix_zone)
                                        if electricity_mix_zone is None
                                        else electricity_mix_zone)

        if isinstance(providers, str):
            providers = [providers]
        elif providers is None:
            providers = default_providers
        if electricity_mix_zone is None:
            electricity_mix_zone = default_electricity_mix_zone

        init_instruments(providers)

        EcoLogits.config=_Config(electricity_mix_zone=electricity_mix_zone, providers=providers)
        EcoLogits.config.providers = list(set(EcoLogits.config.providers))


def init_instruments(providers: list[str]) -> None:
    for provider in providers:
        if provider not in _INSTRUMENTS:
            raise EcoLogitsError(f"Could not find tracer for the `{provider}` provider.")
        if provider not in EcoLogits.config.providers:
            init_func = _INSTRUMENTS[provider]
            init_func()
