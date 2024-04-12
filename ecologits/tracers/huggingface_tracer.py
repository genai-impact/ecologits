import time
from dataclasses import asdict, dataclass
from typing import Any, Callable

from wrapt import wrap_function_wrapper

from ecologits.impacts.models import Impacts
from ecologits.tracers.utils import compute_llm_impacts

try:
    import tiktoken
    from huggingface_hub import InferenceClient
    from huggingface_hub import AsyncInferenceClient
    from huggingface_hub import ChatCompletionOutput as _ChatCompletionOutput
except ImportError:
    InferenceClient = object()
    AsyncInferenceClient = object()
    _ChatCompletionOutput = object()


@dataclass
class ChatCompletionOutput(_ChatCompletionOutput):
    impacts: Impacts


def huggingface_chat_wrapper(
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
    impacts = compute_llm_impacts(
        provider="huggingface_hub",
        model_name=instance.model,
        output_token_count=output_tokens,
        request_latency=request_latency
    )
    if impacts is not None:
        return ChatCompletionOutput(**asdict(response), impacts=impacts)
    else:
        return response


async def huggingface_async_chat_wrapper(
    wrapped: Callable,
    instance: AsyncInferenceClient,
    args: Any,
    kwargs: Any,
) -> ChatCompletionOutput:
    timer_start = time.perf_counter()
    response = await wrapped(*args, **kwargs)
    request_latency = time.perf_counter() - timer_start
    encoder = tiktoken.get_encoding("cl100k_base")
    output_tokens = len(encoder.encode(response.choices[0].message.content))
    impacts = compute_llm_impacts(
        provider="huggingface_hub",
        model_name=instance.model,
        output_token_count=output_tokens,
        request_latency=request_latency
    )
    if impacts is not None:
        return ChatCompletionOutput(**asdict(response), impacts=impacts)
    else:
        return response


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
