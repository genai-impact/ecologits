import time
from typing import Any, Callable, Union

from wrapt import wrap_function_wrapper

from ecologits.impacts import Impacts
from ecologits.tracers.utils import compute_llm_impacts

try:
    from google.generativeai import GenerativeModel
    from google.generativeai.types import (
        GenerateContentResponse as _GenerateContentResponse,
    )
except ImportError:
    GenerativeModel = object()
    _GenerateContentResponse = object()


PROVIDER = "google"


class GenerateContentResponse(_GenerateContentResponse):
    def __init__(self, done, iterator, result, impacts, *args, **kwargs):
        super().__init__(done, iterator, result, impacts, *args, **kwargs)
        self.impacts = impacts

    def __str__(self):
        return f"GenerateContentResponse(done={self._done}, iterator={self._iterator}, result={self._result}, impacts={self.impacts})"


def google_chat_wrapper(
    wrapped: Callable, instance: GenerativeModel, args: Any, kwargs: Any  # noqa: ARG001
) -> Union[GenerateContentResponse]:
    return google_chat_wrapper_non_stream(wrapped, instance, args, kwargs)


def google_chat_wrapper_non_stream(
    wrapped: Callable,
    instance: GenerativeModel,  # noqa: ARG001
    args: Any,
    kwargs: Any,
) -> GenerateContentResponse:
    timer_start = time.perf_counter()
    response = wrapped(*args, **kwargs)
    request_latency = time.perf_counter() - timer_start
    model_name = instance.model_name.replace("models/", "")
    impacts = compute_llm_impacts(
        provider=PROVIDER,
        model_name=model_name,  # ?
        output_token_count=response.usage_metadata.total_token_count,
        request_latency=request_latency,
    )
    if impacts is not None:
        # Convert the response object to a dictionary (model_dump() is not available in the response object)
        response_dict = response.__dict__

        # Retrieve the required arguments from the response_dict object
        done = response_dict.get("_done")
        iterator = response_dict.get("_iterator")
        result = response_dict.get("_result")

        # Remove problematic keys from the dictionary, if they exist
        if "_done" in response_dict:
            del response_dict["_done"]
        if "_iterator" in response_dict:
            del response_dict["_iterator"]
        if "_result" in response_dict:
            del response_dict["_result"]
        if "_chunks" in response_dict:
            del response_dict["_chunks"]
        if "_error" in response_dict:
            del response_dict["_error"]

        return GenerateContentResponse(
            done, iterator, result, impacts, **response_dict
        )
    else:
        return response


# TODO def google_chat_wrapper_stream(

# TODO async def google_async_chat_wrapper(
# TODO async def google_async_chat_wrapper_base(
# TODO async def google_async_chat_wrapper_stream(


class GoogleInstrumentor:
    def __init__(self) -> None:
        self.wrapped_methods = [
            {
                "module": "google.generativeai",
                "name": "GenerativeModel.generate_content",
                "wrapper": google_chat_wrapper,
            },
        ]

    def instrument(self) -> None:
        for wrapper in self.wrapped_methods:
            wrap_function_wrapper(
                wrapper["module"], wrapper["name"], wrapper["wrapper"]
            )
