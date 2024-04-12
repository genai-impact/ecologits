import importlib.util

from ecologits.exceptions import TracerInitializationError


class EcoLogits:
    initialized = False

    @staticmethod
    def init() -> None:
        if EcoLogits.initialized:
            raise TracerInitializationError()
        init_instruments()
        EcoLogits.initialized = True


def init_instruments() -> None:
    init_openai_instrumentor()
    init_anthropic_instrumentor()
    init_mistralai_instrumentor()
    init_huggingface_instrumentor()
    init_cohere_instrumentor()


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
        from ecologits.tracers.mistralai_tracer import MistralAIInstrumentor

        instrumentor = MistralAIInstrumentor()
        instrumentor.instrument()


def init_huggingface_instrumentor() -> None:
    if importlib.util.find_spec("huggingface_hub") is not None:
        from ecologits.tracers.huggingface_tracer import HuggingfaceInstrumentor

        instrumentor = HuggingfaceInstrumentor()
        instrumentor.instrument()


def init_cohere_instrumentor() -> None:
    if importlib.util.find_spec("cohere") is not None:
        from ecologits.tracers.cohere_tracer import CohereInstrumentor

        instrumentor = CohereInstrumentor()
        instrumentor.instrument()
