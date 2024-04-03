from typing import Any, Callable

from wrapt import wrap_function_wrapper

from genai_impact.compute_impacts import Impacts, compute_llm_impact
from genai_impact.model_repository import models

try:
    from huggingface_hub import InferenceClient as _InferenceClient
    from huggingface_hub import AsyncInferenceClient as _AsyncInferenceClient
    from huggingface_hub import ChatCompletionOutput as _ChatCompletionOutput
except ImportError:
    _InferenceClient = object()
    _AsyncInferenceClient = object()
    _ChatCompletionOutput = object()

class ChatCompletionOutput(_ChatCompletionOutput):
    impacts: Impacts


def compute_impacts_and_return_response(response: Any) -> ChatCompletionOutput:
    model = models.find_model(provider="HuggingFaceH4", model_name=response.model)
    if model is None:
        # TODO: Replace with proper logging
        print(f"Could not find model `{response.model}` for huggingface provider.")
        return response
    # output_tokens = response.usage.output_tokens
    output_tokens = 250 # Usage stats and more features to come. https://github.com/huggingface/huggingface_hub/blob/a9453d9f08b1d8ec926f57cc3f18f5902021b7cc/README.md?plain=1#L148
    model_size = model.active_parameters or model.active_parameters_range
    impacts = compute_llm_impact(
        model_parameter_count=model_size, output_token_count=output_tokens
    )
    return ChatCompletionOutput(**response.model_dump(), impacts=impacts)

def huggingface_chat_wrapper(
    wrapped: Callable, instance: _InferenceClient, args: Any, kwargs: Any  # noqa: ARG001
) -> ChatCompletionOutput:
    response = wrapped(*args, **kwargs)
    return compute_impacts_and_return_response(response)

async def huggingface_async_chat_wrapper(
    wrapped: Callable,
    instance: _AsyncInferenceClient,  # noqa: ARG001
    args: Any,
    kwargs: Any,
) -> ChatCompletionOutput:
    response = await wrapped(*args, **kwargs)
    return compute_impacts_and_return_response(response)

class HuggingfaceInstrumentor:
    def __init__(self) -> None:
        self.wrapped_methods = [
            {
                "module": "huggingface_hub.inference._client",
                "name": "InferenceClient.chat_completion",
                "wrapper": huggingface_chat_wrapper,
            },
            {
                "module": "huggingface_hub.inference._client",
                "name": "AsyncInferenceClient.chat_completion",
                "wrapper": huggingface_async_chat_wrapper,
            },
        ]

    def instrument(self) -> None:
        for wrapper in self.wrapped_methods:
            wrap_function_wrapper(
                wrapper["module"], wrapper["name"], wrapper["wrapper"]
            )
