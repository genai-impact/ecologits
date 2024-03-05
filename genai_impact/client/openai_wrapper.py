from typing import Any, Callable

from openai import OpenAI as _OpenAI
from openai.resources.chat import Completions
from openai.types.chat import ChatCompletion as _ChatCompletion
from wrapt import wrap_function_wrapper

from genai_impact.compute_impacts import Impacts, compute_llm_impact

_MODEL_SIZES = {
    "gpt-4-0125-preview": None,
    "gpt-4-turbo-preview": None,
    "gpt-4-1106-preview": None,
    "gpt-4-vision-preview": None,
    "gpt-4": 220,
    "gpt-4-0314": 220,
    "gpt-4-0613": 220,
    "gpt-4-32k": 220,
    "gpt-4-32k-0314": 220,
    "gpt-4-32k-0613": 220,
    "gpt-3.5-turbo": 20,
    "gpt-3.5-turbo-16k": 20,
    "gpt-3.5-turbo-0301": 20,
    "gpt-3.5-turbo-0613": 20,
    "gpt-3.5-turbo-1106": 20,
    "gpt-3.5-turbo-0125": 20,
    "gpt-3.5-turbo-16k-0613": 20,
}


class ChatCompletion(_ChatCompletion):
    impacts: Impacts


def chat_wrapper(
    wrapped: Callable, instance: Completions, args: Any, kwargs: Any  # noqa: ARG001
) -> ChatCompletion:
    response = wrapped(*args, **kwargs)
    model_size = _MODEL_SIZES.get(response.model)
    output_tokens = response.usage.completion_tokens
    impacts = compute_llm_impact(
        model_parameter_count=model_size, output_token_count=output_tokens
    )
    return ChatCompletion(**response.model_dump(), impacts=impacts)


class OpenAI(_OpenAI):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

    wrap_function_wrapper(
        "openai.resources.chat.completions", "Completions.create", chat_wrapper
    )
