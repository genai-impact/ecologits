from typing import Any, Callable, Dict

from wrapt import wrap_function_wrapper

from genai_impact.compute_impacts import Impacts, compute_llm_impact


try:
    from anthropic import Anthropic as _Anthropic
    from anthropic.types import Message as _Message
except ImportError:
    _Anthropic = object()
    _Message = object()

_MODEL_SIZES = {
    "claude-3-opus-20240229": 70,  # fake data
    "claude-3-sonnet-20240229": 10,  # fake data
}

class Message(_Message):
    impacts: Impacts

def _set_impacts(response):
    model_size = _MODEL_SIZES.get(response.model)
    output_tokens = response.usage.output_tokens
    impacts = compute_llm_impact(
        model_parameter_count=model_size, output_token_count=output_tokens
    )
    return impacts

# @wrap_function_wrapper
def chat_wrapper(
    wrapped: Callable, instance: _Anthropic, args: Any, kwargs: Any  # noqa: ARG001
) -> Message:
    response = wrapped(*args, **kwargs)
    impacts = _set_impacts(response)
    model_dump = response.model_dump()
    model_dump["impacts"] = impacts
    return Message(**model_dump)

class AnthropicInstrumentor:
    def __init__(self):
        self.wrapped_methods = [
            {
                "object": "Messages",
                "method": "create",
                "wrapper": chat_wrapper,
            },
        ]

    def instrument(self):
        for wrapped_method in self.wrapped_methods:
            wrap_object = wrapped_method["object"]
            wrap_method = wrapped_method["method"]
            wrap_function_wrapper(
                "anthropic.resources",
                f"{wrap_object}.{wrap_method}",
                wrapped_method["wrapper"],
            )

    # def uninstrument(self):
    #     for wrapped_method in self.wrapped_methods:
    #         wrap_object = wrapped_method["object"]
    #         unwrap(
    #             f"anthropic.resources.{wrap_object}",
    #             wrapped_method["method"],
    #         )
