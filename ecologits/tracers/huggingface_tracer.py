import time
from collections.abc import AsyncIterable, Iterable
from dataclasses import asdict, dataclass
from typing import Any, Callable, Union

from wrapt import wrap_function_wrapper

from ecologits.impacts import Impacts
from ecologits.tracers.utils import llm_impacts

try:
    import tiktoken
    from huggingface_hub import AsyncInferenceClient, InferenceClient
    from huggingface_hub import ChatCompletionOutput as _ChatCompletionOutput
    from huggingface_hub import ChatCompletionStreamOutput as _ChatCompletionStreamOutput
except ImportError:
    InferenceClient = object()
    AsyncInferenceClient = object()

    @dataclass
    class _ChatCompletionOutput:
        pass

    @dataclass
    class _ChatCompletionStreamOutput:
        pass


PROVIDER = "huggingface_hub"


@dataclass
class ChatCompletionOutput(_ChatCompletionOutput):
    impacts: Impacts


@dataclass
class ChatCompletionStreamOutput(_ChatCompletionStreamOutput):
    impacts: Impacts


def huggingface_chat_wrapper(
    wrapped: Callable,
    instance: InferenceClient,
    args: Any,
    kwargs: Any
) -> Union[ChatCompletionOutput, Iterable[ChatCompletionStreamOutput]]:
    if kwargs.get("stream", False):
        return huggingface_chat_wrapper_stream(wrapped, instance, args, kwargs)
    else:
        return huggingface_chat_wrapper_non_stream(wrapped, instance, args, kwargs)


def huggingface_chat_wrapper_non_stream(
    wrapped: Callable,
    instance: InferenceClient,
    args: Any,
    kwargs: Any
) -> ChatCompletionOutput:
    timer_start = time.perf_counter()
    response = wrapped(*args, **kwargs)
    request_latency = time.perf_counter() - timer_start
    encoder = tiktoken.get_encoding("cl100k_base")
    output_tokens = len(encoder.encode(response.choices[0].message.content))
    impacts = llm_impacts(
        provider=PROVIDER,
        model_name=instance.model,
        output_token_count=output_tokens,
        request_latency=request_latency
    )
    if impacts is not None:
        return ChatCompletionOutput(**asdict(response), impacts=impacts)
    else:
        return response


def huggingface_chat_wrapper_stream(
    wrapped: Callable,
    instance: InferenceClient,
    args: Any,
    kwargs: Any
) -> Iterable[ChatCompletionStreamOutput]:
    timer_start = time.perf_counter()
    stream = wrapped(*args, **kwargs)
    token_count = 0
    for chunk in stream:
        token_count += 1
        request_latency = time.perf_counter() - timer_start
        impacts = llm_impacts(
            provider=PROVIDER,
            model_name=instance.model,
            output_token_count=token_count,
            request_latency=request_latency
        )
        if impacts is not None:
            yield ChatCompletionStreamOutput(**asdict(chunk), impacts=impacts)
        else:
            yield chunk


async def huggingface_async_chat_wrapper(
    wrapped: Callable,
    instance: AsyncInferenceClient,
    args: Any,
    kwargs: Any
) -> Union[ChatCompletionOutput, AsyncIterable[ChatCompletionStreamOutput]]:
    if kwargs.get("stream", False):
        return huggingface_async_chat_wrapper_stream(wrapped, instance, args, kwargs)
    else:
        return await huggingface_async_chat_wrapper_non_stream(wrapped, instance, args, kwargs)


async def huggingface_async_chat_wrapper_non_stream(
    wrapped: Callable,
    instance: AsyncInferenceClient,
    args: Any,
    kwargs: Any
) -> ChatCompletionOutput:
    timer_start = time.perf_counter()
    response = await wrapped(*args, **kwargs)
    request_latency = time.perf_counter() - timer_start
    encoder = tiktoken.get_encoding("cl100k_base")
    output_tokens = len(encoder.encode(response.choices[0].message.content))
    impacts = llm_impacts(
        provider=PROVIDER,
        model_name=instance.model,
        output_token_count=output_tokens,
        request_latency=request_latency
    )
    if impacts is not None:
        return ChatCompletionOutput(**asdict(response), impacts=impacts)
    else:
        return response


async def huggingface_async_chat_wrapper_stream(
    wrapped: Callable,
    instance: AsyncInferenceClient,
    args: Any,
    kwargs: Any
) -> AsyncIterable[ChatCompletionStreamOutput]:
    timer_start = time.perf_counter()
    stream = await wrapped(*args, **kwargs)
    token_count = 0
    async for chunk in stream:
        token_count += 1
        request_latency = time.perf_counter() - timer_start
        impacts = llm_impacts(
            provider=PROVIDER,
            model_name=instance.model,
            output_token_count=token_count,
            request_latency=request_latency
        )
        if impacts is not None:
            yield ChatCompletionStreamOutput(**asdict(chunk), impacts=impacts)
        else:
            yield chunk


class HuggingfaceInstrumentor:
    def __init__(self) -> None:
        self.wrapped_methods = [
            {
                "module": "huggingface_hub.inference._client",
                "name": "InferenceClient.chat_completion",
                "wrapper": huggingface_chat_wrapper,
            },
            {
                "module": "huggingface_hub.inference._generated._async_client",
                "name": "AsyncInferenceClient.chat_completion",
                "wrapper": huggingface_async_chat_wrapper,
            },
        ]

    def instrument(self) -> None:
        for wrapper in self.wrapped_methods:
            wrap_function_wrapper(
                wrapper["module"], wrapper["name"], wrapper["wrapper"]
            )
