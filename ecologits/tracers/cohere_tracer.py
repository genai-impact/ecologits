import time
from typing import Callable, Any, Iterator

from cohere import Client, AsyncClient
from cohere.types.non_streamed_chat_response import NonStreamedChatResponse as _NonStreamedChatResponse
from cohere.types.streamed_chat_response import StreamedChatResponse
from cohere.types.streamed_chat_response import StreamedChatResponse_StreamEnd as _StreamedChatResponse_StreamEnd
from wrapt import wrap_function_wrapper

from ecologits.impacts import Impacts
from ecologits.tracers.utils import compute_llm_impacts

PROVIDER = "cohere"

class NonStreamedChatResponse(_NonStreamedChatResponse):
    impacts: Impacts

    class Config:
        arbitrary_types_allowed = True    


class StreamedChatResponse_StreamEnd(_StreamedChatResponse_StreamEnd):
    impacts: Impacts

    class Config:
        arbitrary_types_allowed = True    


def cohere_chat_wrapper(
    wrapped: Callable, instance: Client, args: Any, kwargs: Any  # noqa: ARG001
) -> NonStreamedChatResponse:
    timer_start = time.perf_counter()
    response = wrapped(*args, **kwargs)
    request_latency = time.perf_counter() - timer_start
    output_tokens = response.meta.tokens.output_tokens
    model_name = kwargs.get("model", "command-r")
    impacts = compute_llm_impacts(
        provider=PROVIDER,
        model_name=model_name,
        output_token_count=output_tokens,
        request_latency=request_latency,
    )
    return NonStreamedChatResponse(**response.dict(), impacts=impacts)


async def cohere_async_chat_wrapper(
    wrapped: Callable, instance: AsyncClient, args: Any, kwargs: Any  # noqa: ARG001
) -> NonStreamedChatResponse:
    timer_start = time.perf_counter()
    response = await wrapped(*args, **kwargs)
    request_latency = time.perf_counter() - timer_start
    output_tokens = response.meta.tokens.output_tokens
    model_name = kwargs.get("model", "command-r")
    impacts = compute_llm_impacts(
        provider=PROVIDER,
        model_name=model_name,
        output_token_count=output_tokens,
        request_latency=request_latency,
    )
    return NonStreamedChatResponse(**response.dict(), impacts=impacts)


def cohere_stream_chat_wrapper(
    wrapped: Callable, instance: Client, args: Any, kwargs: Any  
) -> Iterator[StreamedChatResponse]:
    model_name = kwargs.get("model", "command-r")
    timer_start = time.perf_counter()
    stream = wrapped(*args, **kwargs)
    for event in stream:
        if event.event_type == "stream-end":
            request_latency = time.perf_counter() - timer_start
            output_tokens = event.response.meta.tokens.output_tokens
            impacts = compute_llm_impacts(
                provider=PROVIDER,
                model_name=model_name,
                output_token_count=output_tokens,
                request_latency=request_latency,
            )
            yield StreamedChatResponse_StreamEnd(**event.dict(), impacts=impacts)
        else:
            yield event


class CohereInstrumentor:
    def __init__(self) -> None:
        self.wrapped_methods = [
            {
                "module": "cohere.base_client",
                "name": "BaseCohere.chat",
                "wrapper": cohere_chat_wrapper,
            }, 
            {
                "module": "cohere.base_client",
                "name": "AsyncBaseCohere.chat",
                "wrapper": cohere_async_chat_wrapper,
            }, 
            {
                "module": "cohere.base_client",
                "name": "BaseCohere.chat_stream",
                "wrapper": cohere_stream_chat_wrapper,
            }
        ]

    def instrument(self) -> None:
        for wrapper in self.wrapped_methods:
            wrap_function_wrapper(
                wrapper["module"], wrapper["name"], wrapper["wrapper"]
            )

