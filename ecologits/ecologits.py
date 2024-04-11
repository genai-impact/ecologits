import importlib.util

from ecologits.exceptions import TracerInitializationError


class Ecologits:
    initialized = False

    @staticmethod
    def init() -> None:
        if Ecologits.initialized:
            raise TracerInitializationError()
        init_instruments()
        Ecologits.initialized = True


def init_instruments() -> None:
    init_openai_instrumentor()
    init_anthropic_instrumentor()
    init_mistralai_instrumentor()


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
