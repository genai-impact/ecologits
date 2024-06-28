import time
from collections.abc import AsyncGenerator, Iterable
from typing import Any, Callable

from wrapt import wrap_function_wrapper

from ecologits.impacts import Impacts
from ecologits.tracers.utils import llm_impacts

try:
    from mistralai.async_client import MistralAsyncClient
    from mistralai.client import MistralClient
    from mistralai.models.chat_completion import (
        ChatCompletionResponse as _ChatCompletionResponse,
    )
    from mistralai.models.chat_completion import (
        ChatCompletionStreamResponse as _ChatCompletionStreamResponse,
    )
except ImportError:
    MistralClient = object()
    MistralAsyncClient = object()
    _ChatCompletionResponse = object()
    _ChatCompletionStreamResponse = object()


PROVIDER = "mistralai"


class ChatCompletionResponse(_ChatCompletionResponse):
    impacts: Impacts


class ChatCompletionStreamResponse(_ChatCompletionStreamResponse):
    impacts: Impacts



def mistralai_chat_wrapper(
    wrapped: Callable, instance: MistralClient, args: Any, kwargs: Any  # noqa: ARG001
) -> ChatCompletionResponse:
    timer_start = time.perf_counter()
    response = wrapped(*args, **kwargs)
    request_latency = time.perf_counter() - timer_start
    impacts = llm_impacts(
        provider=PROVIDER,
        model_name=response.model,
        output_token_count=response.usage.completion_tokens,
        request_latency=request_latency,
    )
    if impacts is not None:
        return ChatCompletionResponse(**response.model_dump(), impacts=impacts)
    else:
        return response


def mistralai_chat_wrapper_stream_wrapper(
    wrapped: Callable, instance: MistralClient, args: Any, kwargs: Any  # noqa: ARG001
) -> Iterable[ChatCompletionStreamResponse]:
    timer_start = time.perf_counter()
    stream = wrapped(*args, **kwargs)
    token_count = 0
    for i, chunk in enumerate(stream):
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
            yield ChatCompletionStreamResponse(**chunk.model_dump(), impacts=impacts)
        else:
            yield chunk


async def mistralai_async_chat_wrapper(
    wrapped: Callable,
    instance: MistralAsyncClient,  # noqa: ARG001
    args: Any,
    kwargs: Any,
) -> ChatCompletionResponse:
    timer_start = time.perf_counter()
    response = await wrapped(*args, **kwargs)
    request_latency = time.perf_counter() - timer_start
    impacts = llm_impacts(
        provider=PROVIDER,
        model_name=response.model,
        output_token_count=response.usage.completion_tokens,
        request_latency=request_latency,
    )
    if impacts is not None:
        return ChatCompletionResponse(**response.model_dump(), impacts=impacts)
    else:
        return response


async def mistralai_async_chat_wrapper_stream_wrapper(
    wrapped: Callable,
    instance: MistralAsyncClient,  # noqa: ARG001
    args: Any,
    kwargs: Any,
) -> AsyncGenerator[ChatCompletionStreamResponse, None]:
    timer_start = time.perf_counter()
    stream = wrapped(*args, **kwargs)
    token_count = 0
    async for chunk in stream:
        if chunk.usage is not None:
            token_count = chunk.usage.completion_tokens
        request_latency = time.perf_counter() - timer_start
        model_name = chunk.model
        impacts = llm_impacts(
            provider=PROVIDER,
            model_name=model_name,
            output_token_count=token_count,
            request_latency=request_latency,
        )
        if impacts is not None:
            yield ChatCompletionStreamResponse(**chunk.model_dump(), impacts=impacts)
        else:
            yield chunk


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
            {
                "module": "mistralai.client",
                "name": "MistralClient.chat_stream",
                "wrapper": mistralai_chat_wrapper_stream_wrapper,
            },
            {
                "module": "mistralai.async_client",
                "name": "MistralAsyncClient.chat_stream",
                "wrapper": mistralai_async_chat_wrapper_stream_wrapper,
            },
        ]

    def instrument(self) -> None:
        for wrapper in self.wrapped_methods:
            wrap_function_wrapper(
                wrapper["module"], wrapper["name"], wrapper["wrapper"]
            )
