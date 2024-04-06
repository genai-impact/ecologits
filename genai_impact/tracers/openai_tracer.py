from typing import Any, Callable, Optional, Union

from openai import AsyncStream, Stream
from openai.resources.chat import AsyncCompletions, Completions
from openai.types.chat import ChatCompletion as _ChatCompletion
from openai.types.chat import ChatCompletionChunk as _ChatCompletionChunk
from wrapt import wrap_function_wrapper

from genai_impact.compute_impacts import Impacts, compute_llm_impact
from genai_impact.model_repository import models


class ChatCompletion(_ChatCompletion):
    impacts: Impacts


class ChatCompletionChunk(_ChatCompletionChunk):
    impacts: Impacts


def compute_impacts(response: Any) -> Optional[Impacts]:
    model = models.find_model(provider="openai", model_name=response.model)
    if model is None:
        # TODO: Replace with proper logging
        print(f"Could not find model `{response.model}` for openai provider.")
        return None
    output_tokens = response.usage.completion_tokens
    model_size = model.active_parameters or model.active_parameters_range
    impacts = compute_llm_impact(
        model_parameter_count=model_size, output_token_count=output_tokens
    )
    return impacts


def compute_impacts_stream(chunk: Any, token_count: int) -> Optional[Impacts]:
    model = models.find_model(provider="openai", model_name=chunk.model)
    if model is None:
        # TODO: Replace with proper logging
        print(f"Could not find model `{chunk.model}` for openai provider.")
        return None
    model_size = model.active_parameters or model.active_parameters_range
    impacts = compute_llm_impact(
        model_parameter_count=model_size, output_token_count=token_count
    )
    return impacts


def openai_chat_wrapper(
    wrapped: Callable,
    instance: Completions,
    args: Any,
    kwargs: Any
) -> Union[ChatCompletion, Stream[ChatCompletionChunk]]:
    if kwargs.get("stream", False):
        return openai_chat_wrapper_stream(wrapped, instance, args, kwargs)
    else:
        return openai_chat_wrapper_non_stream(wrapped, instance, args, kwargs)


def openai_chat_wrapper_non_stream(
    wrapped: Callable,
    instance: Completions,      # noqa: ARG001
    args: Any,
    kwargs: Any
) -> ChatCompletion:
    response = wrapped(*args, **kwargs)
    impacts = compute_impacts(response)
    if impacts is not None:
        return ChatCompletion(**response.model_dump(), impacts=impacts)
    else:
        return response


def openai_chat_wrapper_stream(
    wrapped: Callable,
    instance: Completions,      # noqa: ARG001
    args: Any,
    kwargs: Any
) -> Stream[ChatCompletionChunk]:
    stream = wrapped(*args, **kwargs)
    token_count = 0
    for i, chunk in enumerate(stream):
        if i > 0 and chunk.choices[0].finish_reason is None:
            token_count += 1
        impacts = compute_impacts_stream(chunk, token_count)
        if impacts is not None:
            yield ChatCompletionChunk(**chunk.model_dump(), impacts=impacts)
        else:
            yield chunk


async def openai_async_chat_wrapper(
    wrapped: Callable,
    instance: AsyncCompletions,
    args: Any,
    kwargs: Any,
) -> Union[ChatCompletion, AsyncStream[ChatCompletionChunk]]:
    if kwargs.get("stream", False):
        return openai_async_chat_wrapper_stream(wrapped, instance, args, kwargs)
    else:
        return await openai_async_chat_wrapper_base(wrapped, instance, args, kwargs)


async def openai_async_chat_wrapper_base(
    wrapped: Callable,
    instance: AsyncCompletions,     # noqa: ARG001
    args: Any,
    kwargs: Any,
) -> ChatCompletion:
    response = await wrapped(*args, **kwargs)
    impacts = compute_impacts(response)
    if impacts is not None:
        return ChatCompletion(**response.model_dump(), impacts=impacts)
    else:
        return response


async def openai_async_chat_wrapper_stream(
    wrapped: Callable,
    instance: AsyncCompletions,     # noqa: ARG001
    args: Any,
    kwargs: Any,
) -> AsyncStream[ChatCompletionChunk]:
    stream = await wrapped(*args, **kwargs)
    i = 0
    token_count = 0
    async for chunk in stream:
        if i > 0 and chunk.choices[0].finish_reason is None:
            token_count += 1
        impacts = compute_impacts_stream(chunk, token_count)
        if impacts is not None:
            yield ChatCompletionChunk(**chunk.model_dump(), impacts=impacts)
        else:
            yield chunk
        i += 1


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
