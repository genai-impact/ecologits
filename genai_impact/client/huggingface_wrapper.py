from typing import Any, Callable

from wrapt import wrap_function_wrapper

from genai_impact.compute_impacts import Impacts, compute_llm_impact

try:
    from huggingface_hub import InferenceClient as _InferenceClient
    from huggingface_hub.inference._text_generation import (
        TextGenerationResponse as _TextGenerationResponse,
    )
except ImportError:
    _InferenceClient = object()
    _TextGenerationResponse = object()


_MODEL_SIZES = {
    "test": 7.3,
}

class TextGenerationResponse(_TextGenerationResponse):
    impacts: Impacts


def chat_wrapper(
    wrapped: Callable, instance: _InferenceClient, args: Any, kwargs: Any  # noqa: ARG001
) -> TextGenerationResponse:
    response = wrapped(*args, **kwargs)
    # model_size = _MODEL_SIZES.get(response.model)
    model_size = 7.3
    # output_tokens = response.usage.completion_tokens
    output_tokens = 12
    impacts = compute_llm_impact(
        model_parameter_count=model_size, output_token_count=output_tokens
    )
    # return TextGenerationResponse(**response.model_dump(), impacts=impacts)
    return TextGenerationResponse(response, impacts=impacts)


class InferenceClient(_InferenceClient):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

    wrap_function_wrapper("huggingface_hub", "InferenceClient.text_generation", chat_wrapper)
