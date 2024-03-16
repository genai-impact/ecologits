from typing import Any, Callable

from wrapt import wrap_function_wrapper

from genai_impact.compute_impacts import Impacts, compute_llm_impact

try:
    from anthropic import Anthropic as _Anthropic
    from anthropic.types import Message as _Message
except ImportError:
    _Anthropic = object()
    _Message = object()

_MODEL_SIZES = {
    "claude-3-haiku-20240307": 10,
    "claude-3-sonnet-20240229": 10,  # fake data
    "claude-3-opus-20240229": 440,  # fake data
}


class Message(_Message):
    impacts: Impacts


def _set_impacts(response: Message) -> Impacts:
    model_size = _MODEL_SIZES.get(response.model)
    output_tokens = response.usage.output_tokens
    impacts = compute_llm_impact(
        model_parameter_count=model_size, output_token_count=output_tokens
    )
    return impacts


def anthropic_chat_wrapper(
    wrapped: Callable, instance: _Anthropic, args: Any, kwargs: Any  # noqa: ARG001
) -> Message:
    response = wrapped(*args, **kwargs)
    impacts = _set_impacts(response)
    return Message(**response.model_dump(), impacts=impacts)


class AnthropicInstrumentor:
    def __init__(self) -> None:
        self.wrapped_methods = [
            {
                "module": "anthropic.resources",
                "name": "Messages.create",
                "wrapper": anthropic_chat_wrapper,
            },
        ]

    def instrument(self) -> None:
        for wrapper in self.wrapped_methods:
            wrap_function_wrapper(
                wrapper["module"],
                wrapper["name"],
                wrapper["wrapper"]
            )
