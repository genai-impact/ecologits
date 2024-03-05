from typing import Any, Callable

from wrapt import wrap_function_wrapper

from genai_impact.compute_impacts import Impacts, compute_llm_impact

try:
    from anthropic import Anthropic as _Anthropic
    # from mistralai.models.chat_completion import (
    #     ChatCompletionResponse as _ChatCompletionResponse,
    # )
except ImportError:
    _Anthropic = object()
    # _ChatCompletionResponse = object()


#model names found here: https://docs.anthropic.com/claude/docs/models-overview#model-recommendations
#TODO update model sizes for anthropic
_MODEL_SIZES = {
    "claude-3-opus-20240229": 70, # fake data
    "claude-3-sonnet-20240229" : 10 # fake data
}


class ChatCompletionResponse(_ChatCompletionResponse):
    impacts: Impacts


def chat_wrapper(
    wrapped: Callable, instance: _Anthropic, args: Any, kwargs: Any  # noqa: ARG001
) -> ChatCompletionResponse:
    response = wrapped(*args, **kwargs)
    model_size = _MODEL_SIZES.get(response.model)
    output_tokens = response.usage.completion_tokens
    impacts = compute_llm_impact(
        model_parameter_count=model_size, output_token_count=output_tokens
    )
    return ChatCompletionResponse(**response.model_dump(), impacts=impacts)


class Anthropic(_Anthropic):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

    wrap_function_wrapper("anthropic.messages.create", chat_wrapper)
