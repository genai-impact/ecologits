import time
from typing import Any, Callable, Union

from wrapt import wrap_function_wrapper

from ecologits.impacts import Impacts
from ecologits.model_repository import models
from ecologits.tracers.utils import llm_impacts

try:
    import litellm
    from litellm import AsyncCompletions, Completions
    from litellm.types.utils import ModelResponse
    from litellm.utils import CustomStreamWrapper

except ImportError:
    ModelResponse = object()
    CustomStreamWrapper = object()
    Completions = object()
    AsyncCompletions = object()


class ChatCompletion(ModelResponse):
    impacts: Impacts


class ChatCompletionChunk(ModelResponse):
    impacts: Impacts


def litellm_chat_wrapper(
    wrapped: Callable,
    instance: Completions,
    args: Any,
    kwargs: Any
) -> Union[ChatCompletion, CustomStreamWrapper]:
    if kwargs.get("stream", False):
        return litellm_chat_wrapper_stream(wrapped, instance, args, kwargs)
    else:
        return litellm_chat_wrapper_non_stream(wrapped, instance, args, kwargs)


def litellm_chat_wrapper_stream(
    wrapped: Callable,
    instance: Completions,      # noqa: ARG001
    args: Any,
    kwargs: Any
) -> CustomStreamWrapper:
    timer_start = time.perf_counter()
    stream = wrapped(*args, **kwargs)
    token_count = 0
    for i, chunk in enumerate(stream):
        if i > 0 and chunk.choices[0].finish_reason is None:
            token_count += 1
        request_latency = time.perf_counter() - timer_start
        model_name = chunk.model
        impacts = llm_impacts(
            provider=models.find_provider(model_name=model_name),
            model_name=model_name,
            output_token_count=token_count,
            request_latency=request_latency,
        )
        if impacts is not None:
            yield ChatCompletionChunk(**chunk.model_dump(), impacts=impacts)
        else:
            yield chunk


def litellm_chat_wrapper_non_stream(
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
        provider=models.find_provider(model_name=model_name),
        model_name=model_name,
        output_token_count=response.usage.completion_tokens,
        request_latency=request_latency,
    )
    if impacts is not None:
        return ChatCompletion(**response.model_dump(), impacts=impacts)
    else:
        return response


async def litellm_async_chat_wrapper(
    wrapped: Callable,
    instance: AsyncCompletions,
    args: Any,
    kwargs: Any
) -> Union[ChatCompletion,CustomStreamWrapper]:
    if kwargs.get("stream", False):
        return litellm_async_chat_wrapper_stream(wrapped, instance, args, kwargs)
    else:
        return await litellm_async_chat_wrapper_base(wrapped, instance, args, kwargs)


async def litellm_async_chat_wrapper_base(
    wrapped: Callable,
    instance: AsyncCompletions,      # noqa: ARG001
    args: Any,
    kwargs: Any
) -> ChatCompletion:
    timer_start = time.perf_counter()
    response = await wrapped(*args, **kwargs)
    request_latency = time.perf_counter() - timer_start
    model_name = response.model
    impacts = llm_impacts(
        provider=models.find_provider(model_name=model_name),
        model_name=model_name,
        output_token_count=response.usage.completion_tokens,
        request_latency=request_latency,
    )
    if impacts is not None:
        return ChatCompletion(**response.model_dump(), impacts=impacts)
    else:
        return response


async def litellm_async_chat_wrapper_stream(
    wrapped: Callable,
    instance: AsyncCompletions,      # noqa: ARG001
    args: Any,
    kwargs: Any
) -> CustomStreamWrapper:
    timer_start = time.perf_counter()
    stream = await wrapped(*args, **kwargs)
    i = 0
    token_count = 0
    async for chunk in stream:
        if i > 0 and chunk.choices[0].finish_reason is None:
            token_count += 1
        request_latency = time.perf_counter() - timer_start
        model_name = chunk.model
        impacts = llm_impacts(
            provider=models.find_provider(model_name=model_name),
            model_name=model_name,
            output_token_count=token_count,
            request_latency=request_latency,
        )
        if impacts is not None:
            yield ChatCompletionChunk(**chunk.model_dump(), impacts=impacts)
        else:
            yield chunk
        i += 1


class LiteLLMInstrumentor:
    def __init__(self) -> None:
        self.wrapped_methods = [
            {
                "module": litellm,
                "name": "completion",
                "wrapper": litellm_chat_wrapper,
            },
            {
                "module": litellm,
                "name": "acompletion",
                "wrapper": litellm_async_chat_wrapper,
            },
        ]

    def instrument(self) -> None:
        for wrapper in self.wrapped_methods:
            wrap_function_wrapper(
                wrapper["module"], wrapper["name"], wrapper["wrapper"]
            )
