import time
from collections.abc import Iterable
from typing import Any, Callable, Union

from wrapt import wrap_function_wrapper

from ecologits.tracers.utils import llm_impacts

try:
    from google.generativeai import GenerativeModel
    from google.generativeai.types import AsyncGenerateContentResponse as _AsyncGenerateContentResponse
    from google.generativeai.types import (
        GenerateContentResponse as _GenerateContentResponse,
    )
except ImportError:
    GenerativeModel = object()
    _GenerateContentResponse = object()
    _AsyncGenerateContentResponse = object()


PROVIDER = "google"


class GenerateContentResponse(_GenerateContentResponse):
    def __init__(self, done, iterator, result, impacts, *args, **kwargs) -> None:   # noqa: ANN001 ANN002 ANN003
        super().__init__(done, iterator, result, impacts, *args, **kwargs)
        self.impacts = impacts

    def __str__(self):  # noqa: ANN204
        return f"GenerateContentResponse(done={self._done}, iterator={self._iterator}, result={self._result}, impacts={self.impacts})" # noqa: E501


class AsyncGenerateContentResponse(_AsyncGenerateContentResponse):
    def __init__(self, done, iterator, result, impacts, *args, **kwargs) -> None: # noqa: ANN001 ANN002 ANN003
        super().__init__(done, iterator, result, impacts, *args, **kwargs)
        self.impacts = impacts

    def __str__(self): # noqa: ANN204
        return f"AsyncGenerateContentResponse(done={self._done}, iterator={self._iterator}, result={self._result}, impacts={self.impacts})" # noqa: E501


def wrap_from_dict(response_dict: dict, impacts, async_mode = False) -> Union[GenerateContentResponse, AsyncGenerateContentResponse]: # noqa: ANN001 E501
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

    if async_mode:
        return AsyncGenerateContentResponse(
            done, iterator, result, impacts, **response_dict
        )

    return GenerateContentResponse(
        done, iterator, result, impacts, **response_dict
    )


def google_chat_wrapper(
    wrapped: Callable, instance: GenerativeModel, args: Any, kwargs: Any
) -> Union[GenerateContentResponse, Iterable[GenerateContentResponse]]:
    if kwargs.get("stream", False):
        return google_chat_wrapper_stream(wrapped, instance, args, kwargs)
    else:
        return google_chat_wrapper_non_stream(wrapped, instance, args, kwargs)


def google_chat_wrapper_non_stream(
    wrapped: Callable,
    instance: GenerativeModel,
    args: Any,
    kwargs: Any,
) -> GenerateContentResponse:
    timer_start = time.perf_counter()
    response = wrapped(*args, **kwargs)
    request_latency = time.perf_counter() - timer_start
    model_name = instance.model_name.replace("models/", "")
    impacts = llm_impacts(
        provider=PROVIDER,
        model_name=model_name,  # ?
        output_token_count=response.usage_metadata.total_token_count,
        request_latency=request_latency,
    )
    if impacts is not None:
        # Convert the response object to a dictionary (model_dump() is not available in the response object)
        response = wrap_from_dict(response.__dict__, impacts)
    return response


def google_chat_wrapper_stream(
    wrapped: Callable,
    instance: GenerativeModel,
    args: Any,
    kwargs: Any,
) -> Iterable[GenerateContentResponse]:
    model_name = instance.model_name.replace("models/", "")
    timer_start = time.perf_counter()
    stream = wrapped(*args, **kwargs)
    for chunk in stream:
        request_latency = time.perf_counter() - timer_start
        impacts = llm_impacts(
            provider=PROVIDER,
            model_name=model_name,  # ?
            output_token_count=chunk.usage_metadata.total_token_count,
            request_latency=request_latency,
        )
        if impacts is not None:
            chunk = wrap_from_dict(chunk.__dict__, impacts) # noqa: PLW2901
        yield chunk


async def google_async_chat_wrapper(
    wrapped: Callable, instance: GenerativeModel, args: Any, kwargs: Any
) -> Union[AsyncGenerateContentResponse, Iterable[AsyncGenerateContentResponse]]:
    if kwargs.get("stream", False):
        return google_async_chat_wrapper_stream(wrapped, instance, args, kwargs)
    else:
        return await google_async_chat_wrapper_non_stream(wrapped, instance, args, kwargs)


async def google_async_chat_wrapper_non_stream(
    wrapped: Callable,
    instance: GenerativeModel,
    args: Any,
    kwargs: Any,
) -> AsyncGenerateContentResponse:
    timer_start = time.perf_counter()
    response = await wrapped(*args, **kwargs)
    request_latency = time.perf_counter() - timer_start
    model_name = instance.model_name.replace("models/", "")
    impacts = llm_impacts(
        provider=PROVIDER,
        model_name=model_name,  # ?
        output_token_count=response.usage_metadata.total_token_count,
        request_latency=request_latency,
    )
    if impacts is not None:
        # Convert the response object to a dictionary (model_dump() is not available in the response object)
        response = wrap_from_dict(response.__dict__, impacts, async_mode = True)
    return response


async def google_async_chat_wrapper_stream(
    wrapped: Callable,
    instance: GenerativeModel,
    args: Any,
    kwargs: Any,
) -> Iterable[AsyncGenerateContentResponse]:
    model_name = instance.model_name.replace("models/", "")
    timer_start = time.perf_counter()
    stream = await wrapped(*args, **kwargs)
    async for chunk in stream:
        request_latency = time.perf_counter() - timer_start
        impacts = llm_impacts(
            provider=PROVIDER,
            model_name=model_name,  # ?
            output_token_count=chunk.usage_metadata.total_token_count,
            request_latency=request_latency,
        )
        if impacts is not None:
            chunk = wrap_from_dict(chunk.__dict__, impacts, async_mode = True) # noqa: PLW2901
        yield chunk


class GoogleInstrumentor:
    def __init__(self) -> None:
        self.wrapped_methods = [
            {
                "module": "google.generativeai",
                "name": "GenerativeModel.generate_content",
                "wrapper": google_chat_wrapper,
            },
            {
                "module": "google.generativeai",
                "name": "GenerativeModel.generate_content_async",
                "wrapper": google_async_chat_wrapper
            }
        ]

    def instrument(self) -> None:
        for wrapper in self.wrapped_methods:
            wrap_function_wrapper(
                wrapper["module"], wrapper["name"], wrapper["wrapper"]
            )
