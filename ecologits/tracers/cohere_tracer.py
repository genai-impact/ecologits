import time
from typing import Callable, Any

from wrapt import wrap_function_wrapper

from ecologits.impacts.models import Impacts
from ecologits.tracers.utils import compute_llm_impacts

try:
    from cohere import Client as _Client
    from cohere.types.non_streamed_chat_response import NonStreamedChatResponse as _NonStreamedChatResponse
except ImportError:
    Client = object()
    _NonStreamedChatResponse = object()


PROVIDER = "cohere"

class NonStreamedChatResponse(_NonStreamedChatResponse):
    impacts: Impacts


def cohere_chat_wrapper(
    wrapped: Callable, instance: _Client, args: Any, kwargs: Any  # noqa: ARG001
) -> NonStreamedChatResponse:
    timer_start = time.perf_counter()
    response = wrapped(*args, **kwargs)
    request_latency = time.perf_counter() - timer_start

    return response


    # model_name = response.model
    # impacts = compute_llm_impacts(
    #     provider=PROVIDER,
    #     model_name=model_name,
    #     output_token_count=response.usage.output_tokens,
    #     request_latency=request_latency,
    # )
    # if impacts is not None:
    #     return Message(**response.model_dump(), impacts=impacts)
    # else:
    #     return response


# async def anthropic_async_chat_wrapper(
#     wrapped: Callable, instance: AsyncAnthropic, args: Any, kwargs: Any  # noqa: ARG001
# ) -> Message:
#     timer_start = time.perf_counter()
#     response = await wrapped(*args, **kwargs)
#     request_latency = time.perf_counter() - timer_start
#     return ...


class CohereInstrumentor:
    def __init__(self) -> None:
        self.wrapped_methods = [
            {
                "module": "cohere.base_client",
                "name": "BaseCohere.chat",
                "wrapper": cohere_chat_wrapper,
            }
        ]

    def instrument(self) -> None:
        for wrapper in self.wrapped_methods:
            wrap_function_wrapper(
                wrapper["module"], wrapper["name"], wrapper["wrapper"]
            )

