from typing import Any, Callable

from openai.resources.chat import Completions, AsyncCompletions

from openai.types.chat import ChatCompletion as _ChatCompletion
from wrapt import wrap_function_wrapper

from genai_impact.compute_impacts import Impacts, compute_llm_impact
from genai_impact.model_repository import models


class ChatCompletion(_ChatCompletion):
    impacts: Impacts


def openai_chat_wrapper(
    wrapped: Callable, instance: Completions, args: Any, kwargs: Any  # noqa: ARG001
) -> ChatCompletion:
    response = wrapped(*args, **kwargs)
    model = models.find_model(provider="openai", model_name=response.model)
    if model is None:
        # TODO: Replace with proper logging
        print(f"Could not find model `{response.model}` for openai provider.")
        return response
    output_tokens = response.usage.completion_tokens
    model_size = model.active_parameters or model.active_parameters_range
    impacts = compute_llm_impact(
        model_parameter_count=model_size, output_token_count=output_tokens
    )
    return ChatCompletion(**response.model_dump(), impacts=impacts)


async def openai_async_chat_wrapper(
    wrapped: Callable,
    instance: AsyncCompletions,
    args: Any,
    kwargs: Any,  # noqa: ARG001
) -> ChatCompletion:
    response = await wrapped(*args, **kwargs)
    model = models.find_model(provider="openai", model_name=response.model)
    if model is None:
        # TODO: Replace with proper logging
        print(f"Could not find model `{response.model}` for openai provider.")
        return response
    output_tokens = response.usage.completion_tokens
    model_size = model.active_parameters or model.active_parameters_range
    impacts = compute_llm_impact(
        model_parameter_count=model_size, output_token_count=output_tokens
    )
    return ChatCompletion(**response.model_dump(), impacts=impacts)


class OpenAIInstrumentor:
    def __init__(self) -> None:
        self.wrapped_methods = [
            {
                "module": "openai.resources.chat.completions",
                "name": "Completions.create",
                "wrapper": openai_chat_wrapper,
            },
            {
                "module": "openai.resources.chat.completions",
                "name": "AsyncCompletions.create",
                "wrapper": openai_async_chat_wrapper,
            },
        ]

    def instrument(self) -> None:
        for wrapper in self.wrapped_methods:
            wrap_function_wrapper(
                wrapper["module"], wrapper["name"], wrapper["wrapper"]
            )
