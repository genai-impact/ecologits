from dataclasses import asdict
from typing import Optional

from openai import OpenAI as _OpenAI
from wrapt import wrap_function_wrapper

from genai_impact.compute_impacts import MODEL_SIZES, compute_llm_impact


def chat_wrapper(wrapped, instance, args, kwargs):
    response = wrapped(*args, **kwargs)
    model_size = MODEL_SIZES.get(response.model)
    output_tokens = response.usage.completion_tokens
    impacts = compute_llm_impact(model_parameter_count=model_size, output_token_count=output_tokens)
    response.impacts = asdict(impacts)
    return response


class OpenAI:
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        **kwargs
    ):
        self.__client = _OpenAI(
            api_key=api_key,
            base_url=base_url,
            **kwargs
        )

    wrap_function_wrapper(
        "openai.resources.chat.completions",
        "Completions.create",
        chat_wrapper
    )

    def __getattr__(self, name):
        """
        Redirect attribute access to the underlying openai client if the attribute
        is not defined in this class.
        """
        return getattr(self.__client, name)
