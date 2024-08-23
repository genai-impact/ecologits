import time
from typing import Any, Callable, Union

from wrapt import wrap_function_wrapper

from ecologits.impacts import Impacts
from ecologits.tracers.utils import llm_impacts

try:
    from openai import AsyncStream, Stream
    from openai.resources.chat import AsyncCompletions, Completions
    from openai.types.chat import ChatCompletion as _ChatCompletion
    from openai.types.chat import ChatCompletionChunk as _ChatCompletionChunk
except ImportError:
    AsyncStream = object()
    Stream = object()
    AsyncCompletions = object()
    Completions = object()
    _ChatCompletion = object()
    _ChatCompletionChunk = object()


PROVIDER = "openai"


class ChatCompletion(_ChatCompletion):
    impacts: Impacts


class ChatCompletionChunk(_ChatCompletionChunk):
    impacts: Impacts


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
    timer_start = time.perf_counter()
    response = wrapped(*args, **kwargs)
    request_latency = time.perf_counter() - timer_start
    model_name = response.model
    impacts = llm_impacts(
        provider=PROVIDER,
        model_name=model_name,
        output_token_count=response.usage.completion_tokens,
        request_latency=request_latency,
    )
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
    timer_start = time.perf_counter()
    stream = wrapped(*args, **kwargs)
    token_count = 0
    for i, chunk in enumerate(stream):
        # azure openai has an empty first chunk so we skip it
        if i == 0 and chunk.model == "":
            continue
        if i > 0 and chunk.choices[0].finish_reason is None:
            token_count += 1
        request_latency = time.perf_counter() - timer_start
        model_name = chunk.model
        impacts = llm_impacts(
            provider=PROVIDER,
            model_name=model_name,
            output_token_count=token_count,
            request_latency=request_latency,
        )
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
    timer_start = time.perf_counter()
    response = await wrapped(*args, **kwargs)
    request_latency = time.perf_counter() - timer_start
    model_name = response.model
    impacts = llm_impacts(
        provider=PROVIDER,
        model_name=model_name,
        output_token_count=response.usage.completion_tokens,
        request_latency=request_latency,
    )
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
    timer_start = time.perf_counter()
    stream = await wrapped(*args, **kwargs)
    i = 0
    token_count = 0
    async for chunk in stream:
        if i == 0 and chunk.model == "":
            continue
        if i > 0 and chunk.choices[0].finish_reason is None:
            token_count += 1
        request_latency = time.perf_counter() - timer_start
        model_name = chunk.model
        impacts = llm_impacts(
            provider=PROVIDER,
            model_name=model_name,
            output_token_count=token_count,
            request_latency=request_latency,
        )
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
