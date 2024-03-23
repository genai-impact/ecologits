from typing import Any, Callable

from wrapt import wrap_function_wrapper

from genai_impact.compute_impacts import Impacts, compute_llm_impact
from genai_impact.model_repository import models

try:
    from mistralai.async_client import MistralAsyncClient as _MistralAsyncClient
    from mistralai.client import MistralClient as _MistralClient
    from mistralai.models.chat_completion import (
        ChatCompletionResponse as _ChatCompletionResponse,
    )
except ImportError:
    _MistralClient = object()
    _MistralAsyncClient = object()
    _ChatCompletionResponse = object()


class ChatCompletionResponse(_ChatCompletionResponse):
    impacts: Impacts


def compute_impacts_and_return_response(response: Any) -> ChatCompletionResponse:
    model = models.find_model(provider="mistralai", model_name=response.model)
    if model is None:
        # TODO: Replace with proper logging
        print(f"Could not find model `{response.model}` for mistralai provider.")
        return response
    output_tokens = response.usage.completion_tokens
    model_size = model.active_parameters or model.active_parameters_range
    impacts = compute_llm_impact(
        model_parameter_count=model_size, output_token_count=output_tokens
    )
    return ChatCompletionResponse(**response.model_dump(), impacts=impacts)


def mistralai_chat_wrapper(
    wrapped: Callable, instance: _MistralClient, args: Any, kwargs: Any  # noqa: ARG001
) -> ChatCompletionResponse:
    response = wrapped(*args, **kwargs)
    return compute_impacts_and_return_response(response)


async def mistralai_async_chat_wrapper(
    wrapped: Callable,
    instance: _MistralAsyncClient, # noqa: ARG001
    args: Any,
    kwargs: Any,
) -> ChatCompletionResponse:
    response = await wrapped(*args, **kwargs)
    return compute_impacts_and_return_response(response)


class MistralAIInstrumentor:
    def __init__(self) -> None:
        self.wrapped_methods = [
            {
                "module": "mistralai.client",
                "name": "MistralClient.chat",
                "wrapper": mistralai_chat_wrapper,
            },
            {
                "module": "mistralai.async_client",
                "name": "MistralAsyncClient.chat",
                "wrapper": mistralai_async_chat_wrapper,
            },
        ]

    def instrument(self) -> None:
        for wrapper in self.wrapped_methods:
            wrap_function_wrapper(
                wrapper["module"], wrapper["name"], wrapper["wrapper"]
            )
