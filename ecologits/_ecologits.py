import importlib.metadata
import importlib.util
from dataclasses import dataclass, field
from typing import Optional, Union

from packaging.version import Version

from ecologits.exceptions import EcoLogitsError
from ecologits.log import logger
from ecologits.utils.opentelemetry import OpenTelemetry


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
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": "Tell me a funny joke!"}
            ]
        )

        # Get estimated environmental impacts of the inference
        print(f"Energy consumption: {response.impacts.energy.value} kWh")
        print(f"GHG emissions: {response.impacts.gwp.value} kgCO2eq")
        ```

    """
    @dataclass
    class _Config:
        electricity_mix_zone: str = field(default="WOR")
        providers: list[str] = field(default_factory=list)
        opentelemetry: Optional[OpenTelemetry] = None

    config = _Config()

    @staticmethod
    def init(
        providers: Optional[Union[str, list[str]]] = None,
        electricity_mix_zone: str = "WOR",
        enable_opentelemetry: bool = False,
        opentelemetry_endpoint: Optional[str] = None
    ) -> None:
        """
        Initialization static method. Will attempt to initialize all providers by default.

        Args:
            providers: list of providers to initialize (all providers by default).
            electricity_mix_zone: ISO 3166-1 alpha-3 code of the electricity mix zone (WOR by default).
        """
        if isinstance(providers, str):
            providers = [providers]
        if providers is None:
            providers = list(_INSTRUMENTS.keys())

        init_instruments(providers)

        EcoLogits.config.electricity_mix_zone = electricity_mix_zone
        EcoLogits.config.providers += providers
        EcoLogits.config.providers = list(set(EcoLogits.config.providers))

        if enable_opentelemetry:
            if opentelemetry_endpoint is None:
                raise EcoLogitsError("Telemetry is enabled but no telemetry endpoint is provided.")
            EcoLogits.config.opentelemetry = OpenTelemetry(endpoint=opentelemetry_endpoint)


def init_instruments(providers: list[str]) -> None:
    for provider in providers:
        if provider not in _INSTRUMENTS:
            raise EcoLogitsError(f"Could not find tracer for the `{provider}` provider.")
        if provider not in EcoLogits.config.providers:
            init_func = _INSTRUMENTS[provider]
            init_func()
