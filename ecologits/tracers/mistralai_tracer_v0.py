import time
from collections.abc import AsyncGenerator, Iterable
from typing import Any, Callable

from mistralai.async_client import MistralAsyncClient
from mistralai.client import MistralClient
from mistralai.models.chat_completion import (  # type: ignore[import-not-found]
    ChatCompletionResponse as _ChatCompletionResponse,  # type: ignore[import-not-found]
)
from mistralai.models.chat_completion import (  # type: ignore[import-not-found]
    ChatCompletionStreamResponse as _ChatCompletionStreamResponse,  # type: ignore[import-not-found]
)
from wrapt import wrap_function_wrapper  # type: ignore[import-untyped]

from ecologits._ecologits import EcoLogits
from ecologits.tracers.utils import ImpactsOutput, llm_impacts

PROVIDER = "mistralai"


class ChatCompletionResponse(_ChatCompletionResponse):
    """
    Wrapper of `mistralai.models.chat_completion.ChatCompletionResponse` with `ImpactsOutput`
    """
    impacts: ImpactsOutput


class ChatCompletionStreamResponse(_ChatCompletionStreamResponse):
    """
    Wrapper of `mistralai.models.chat_completion.ChatCompletionStreamResponse` with `ImpactsOutput`
    """
    impacts: ImpactsOutput



def mistralai_chat_wrapper(
    wrapped: Callable, instance: MistralClient, args: Any, kwargs: Any  # noqa: ARG001
) -> ChatCompletionResponse:
    """
    Function that wraps a MistralAI answer with computed impacts

    Args:
        wrapped: Callable that returns the LLM response
        instance: Never used - for compatibility with `wrapt`
        args: Arguments of the callable
        kwargs: Keyword arguments of the callable

    Returns:
        A wrapped `ChatCompletionResponse` with impacts
    """

    timer_start = time.perf_counter()
    response = wrapped(*args, **kwargs)
    request_latency = time.perf_counter() - timer_start
    impacts = llm_impacts(
        provider=PROVIDER,
        model_name=response.model,
        output_token_count=response.usage.completion_tokens,
        request_latency=request_latency,
        electricity_mix_zone=EcoLogits.config.electricity_mix_zone
    )
    if impacts is not None:
        return ChatCompletionResponse(**response.model_dump(), impacts=impacts)
    else:
        return response


def mistralai_chat_wrapper_stream(
    wrapped: Callable, instance: MistralClient, args: Any, kwargs: Any  # noqa: ARG001
) -> Iterable[ChatCompletionStreamResponse]:
    """
    Function that wraps a MistralAI answer with computed impacts in streaming mode

    Args:
        wrapped: Callable that returns the LLM response
        instance: Never used - for compatibility with `wrapt`
        args: Arguments of the callable
        kwargs: Keyword arguments of the callable

    Returns:
        A wrapped `Iterable[ChatCompletionStreamResponse]` with impacts
    """

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
            electricity_mix_zone=EcoLogits.config.electricity_mix_zone
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
    """
    Function that wraps a MistralAI answer with computed impacts in async mode

    Args:
        wrapped: Async callable that returns the LLM response
        instance: Never used - for compatibility with `wrapt`
        args: Arguments of the callable
        kwargs: Keyword arguments of the callable

    Returns:
        A wrapped `ChatCompletionResponse` with impacts
    """
    timer_start = time.perf_counter()
    response = await wrapped(*args, **kwargs)
    request_latency = time.perf_counter() - timer_start
    impacts = llm_impacts(
        provider=PROVIDER,
        model_name=response.model,
        output_token_count=response.usage.completion_tokens,
        request_latency=request_latency,
        electricity_mix_zone=EcoLogits.config.electricity_mix_zone
    )
    if impacts is not None:
        return ChatCompletionResponse(**response.model_dump(), impacts=impacts)
    else:
        return response


async def mistralai_async_chat_wrapper_stream(
    wrapped: Callable,
    instance: MistralAsyncClient,  # noqa: ARG001
    args: Any,
    kwargs: Any,
) -> AsyncGenerator[ChatCompletionStreamResponse, None]:
    """
    Function that wraps a MistralAI answer with computed impacts in streaming and async mode

    Args:
        wrapped: Callable that returns the LLM response
        instance: Never used - for compatibility with `wrapt`
        args: Arguments of the callable
        kwargs: Keyword arguments of the callable

    Returns:
        A wrapped `AsyncGenerator[ChatCompletionStreamResponse, None]` with impacts
    """
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
            electricity_mix_zone=EcoLogits.config.electricity_mix_zone
        )
        if impacts is not None:
            yield ChatCompletionStreamResponse(**chunk.model_dump(), impacts=impacts)
        else:
            yield chunk


class MistralAIInstrumentor:
    """
    Instrumentor initialized by EcoLogits to automatically wrap all MistralAI calls
    """
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
                "wrapper": mistralai_chat_wrapper_stream,
            },
            {
                "module": "mistralai.async_client",
                "name": "MistralAsyncClient.chat_stream",
                "wrapper": mistralai_async_chat_wrapper_stream,
            },
        ]

    def instrument(self) -> None:
        for wrapper in self.wrapped_methods:
            wrap_function_wrapper(
                wrapper["module"], wrapper["name"], wrapper["wrapper"]
            )
