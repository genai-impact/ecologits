from typing import Any, Callable

from wrapt import wrap_function_wrapper

from genai_impact.compute_impacts import Impacts, compute_llm_impact

try:
    from mistralai.client import MistralClient as _MistralClient
    from mistralai.models.chat_completion import (
        ChatCompletionResponse as _ChatCompletionResponse,
    )
except ImportError:
    _MistralClient = object()
    _ChatCompletionResponse = object()


_MODEL_SIZES = {
    "mistral-tiny": 7.3,
    "mistral-small": 12.9,  # mixtral active parameters count
    "mistral-medium": 70,
    "mistral-large": 440,
}


class ChatCompletionResponse(_ChatCompletionResponse):
    impacts: Impacts


def mistralai_chat_wrapper(
    wrapped: Callable, instance: _MistralClient, args: Any, kwargs: Any  # noqa: ARG001
) -> ChatCompletionResponse:
    response = wrapped(*args, **kwargs)
    model_size = _MODEL_SIZES.get(response.model)
    output_tokens = response.usage.completion_tokens
    impacts = compute_llm_impact(
        model_parameter_count=model_size, output_token_count=output_tokens
    )
    return ChatCompletionResponse(**response.model_dump(), impacts=impacts)


class MistralAIInstrumentor:
    def __init__(self) -> None:
        self.wrapped_methods = [
            {
                "module": "mistralai.client",
                "name": "MistralClient.chat",
                "wrapper": mistralai_chat_wrapper,
            },
        ]

    def instrument(self) -> None:
        for wrapper in self.wrapped_methods:
            wrap_function_wrapper(
                wrapper["module"],
                wrapper["name"],
                wrapper["wrapper"]
            )
