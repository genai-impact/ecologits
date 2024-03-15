from typing import Any, Callable

from openai.resources.chat import Completions
from openai.types.chat import ChatCompletion as _ChatCompletion
from wrapt import wrap_function_wrapper

from genai_impact.compute_impacts import Impacts, compute_llm_impact

_MODEL_SIZES = {
    "gpt-4-0125-preview": None,
    "gpt-4-turbo-preview": None,
    "gpt-4-1106-preview": None,
    "gpt-4-vision-preview": None,
    "gpt-4": 440,
    "gpt-4-0314": 440,
    "gpt-4-0613": 440,
    "gpt-4-32k": 440,
    "gpt-4-32k-0314": 440,
    "gpt-4-32k-0613": 440,
    "gpt-3.5-turbo": 70,
    "gpt-3.5-turbo-16k": 70,
    "gpt-3.5-turbo-0301": 70,
    "gpt-3.5-turbo-0613": 70,
    "gpt-3.5-turbo-1106": 70,
    "gpt-3.5-turbo-0125": 70,
    "gpt-3.5-turbo-16k-0613": 70,
}


class ChatCompletion(_ChatCompletion):
    impacts: Impacts


def openai_chat_wrapper(
    wrapped: Callable, instance: Completions, args: Any, kwargs: Any  # noqa: ARG001
) -> ChatCompletion:
    response = wrapped(*args, **kwargs)
    model_size = _MODEL_SIZES.get(response.model)
    output_tokens = response.usage.completion_tokens
    impacts = compute_llm_impact(
        model_parameter_count=model_size, output_token_count=output_tokens
    )
    return ChatCompletion(**response.model_dump(), impacts=impacts)


class OpenAIInstrumentor:
    def __init__(self):
        self.wrapped_methods = [
            {
                "module": "openai.resources.chat.completions",
                "name": "Completions.create",
                "wrapper": openai_chat_wrapper,
            },
        ]

    def instrument(self):
        for wrapper in self.wrapped_methods:
            wrap_function_wrapper(
                wrapper["module"],
                wrapper["name"],
                wrapper["wrapper"]
            )
