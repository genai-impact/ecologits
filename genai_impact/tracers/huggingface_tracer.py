from dataclasses import asdict, dataclass
from typing import Any, Callable

from wrapt import wrap_function_wrapper

from genai_impact.compute_impacts import Impacts, compute_llm_impact
from genai_impact.model_repository import models

try:
    import tiktoken
    from huggingface_hub import InferenceClient as _InferenceClient, ChatCompletionOutputChoice
    from huggingface_hub import AsyncInferenceClient as _AsyncInferenceClient
    from huggingface_hub import ChatCompletionOutput as _ChatCompletionOutput
except ImportError:
    _InferenceClient = object()
    _AsyncInferenceClient = object()
    _ChatCompletionOutput = object()


@dataclass
class ChatCompletionOutput(_ChatCompletionOutput):
    impacts: Impacts


def huggingface_chat_wrapper(
    wrapped: Callable, instance: _InferenceClient, args: Any, kwargs: Any  # noqa: ARG001
) -> ChatCompletionOutput:
    response = wrapped(*args, **kwargs)
    model = models.find_model(provider="huggingface_hub", model_name=instance.model)
    if model is None:
        # TODO: Replace with proper logging
        print(f"Could not find model `{response.model}` for huggingface provider.")
        return response
    encoder = tiktoken.get_encoding("cl100k_base")
    output_tokens = len(encoder.encode(response.choices[0].message.content))
    model_size = model.active_parameters or model.active_parameters_range
    impacts = compute_llm_impact(
        model_parameter_count=model_size, output_token_count=output_tokens
    )
    return ChatCompletionOutput(**asdict(response), impacts=impacts)


async def huggingface_async_chat_wrapper(
    wrapped: Callable,
    instance: _AsyncInferenceClient,  # noqa: ARG001
    args: Any,
    kwargs: Any,
) -> ChatCompletionOutput:
    response = await wrapped(*args, **kwargs)
    model = models.find_model(provider="huggingface_hub", model_name=instance.model)
    if model is None:
        # TODO: Replace with proper logging
        print(f"Could not find model `{response.model}` for huggingface provider.")
        return response
    output_tokens = 250
    model_size = model.active_parameters or model.active_parameters_range
    impacts = compute_llm_impact(
        model_parameter_count=model_size, output_token_count=output_tokens
    )
    return ChatCompletionOutput(**asdict(response), impacts=impacts)


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
