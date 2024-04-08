from typing import Any, Callable, Iterator
from typing_extensions import override

from wrapt import wrap_function_wrapper

from genai_impact.compute_impacts import Impacts, compute_llm_impact
from genai_impact.model_repository import models

try:
    from anthropic import Anthropic as _Anthropic
    from anthropic import AsyncAnthropic as _AsyncAnthropic
    from anthropic.lib.streaming import MessageStream as _MessageStream
    from anthropic.types import Message as _Message
    from anthropic.types.message_delta_event import MessageDeltaEvent
    from anthropic.types.message_start_event import MessageStartEvent
except ImportError:
    _Anthropic = object()
    _AsyncAnthropic = object()
    _Message = object()
    _MessageStream = object()

class Message(_Message):
    impacts: Impacts

class MessageStream(_MessageStream):
    impacts: Impacts

    @override
    def __stream_text__(self) -> Iterator[str]:
        return self.stream_save

    def __init__(self, parent, impacts) -> None:
        self.stream_save = parent.text_stream
        super().__init__(
            cast_to = parent._cast_to, 
            response = parent.response, 
            client = parent._client
        )
        self.impacts = impacts

def compute_impacts_and_return_response(response: Any) -> Message:
    model = models.find_model(provider="anthropic", model_name=response.model)
    if model is None:
        # TODO: Replace with proper logging
        print(f"Could not find model `{response.model}` for anthropic provider.")
        return response
    output_tokens = response.usage.output_tokens
    model_size = model.active_parameters or model.active_parameters_range
    impacts = compute_llm_impact(
        model_parameter_count=model_size, output_token_count=output_tokens
    )
    return Message(**response.model_dump(), impacts=impacts)

def anthropic_chat_wrapper(
    wrapped: Callable, instance: _Anthropic, args: Any, kwargs: Any  # noqa: ARG001
) -> Message:
    response = wrapped(*args, **kwargs)
    return compute_impacts_and_return_response(response)


async def anthropic_async_chat_wrapper(
    wrapped: Callable, instance: _AsyncAnthropic, args: Any, kwargs: Any  # noqa: ARG001
) -> Message:
    response = await wrapped(*args, **kwargs)
    return compute_impacts_and_return_response(response)

def compute_impacts_and_return_stream_response(response: Any) -> MessageStream:
    output_tokens = 0
    with response as stream:
        for i, event in enumerate(stream):
            if i == 0:
                if type(event) is MessageStartEvent:
                    message = event.message
                    model = models.find_model(provider="anthropic", model_name=message.model)
                    output_tokens += message.usage.output_tokens
                else:
                    print("Stream is not initialized with MessageStartEvent")
                    return stream
            elif type(event) is MessageDeltaEvent:
                output_tokens += event.usage.output_tokens
        model_size = model.active_parameters or model.active_parameters_range
        impacts = compute_llm_impact(
            model_parameter_count=model_size, output_token_count=output_tokens
        )

        return MessageStream(stream, impacts)
        
def anthropic_stream_chat_wrapper(
    wrapped: Callable, instance: _Anthropic, args: Any, kwargs: Any  # noqa: ARG001
) -> MessageStream:
    response = wrapped(*args, **kwargs)
    return compute_impacts_and_return_stream_response(response)

class AnthropicInstrumentor:
    def __init__(self) -> None:
        self.wrapped_methods = [
            {
                "module": "anthropic.resources",
                "name": "Messages.create",
                "wrapper": anthropic_chat_wrapper,
            },
            {
                "module": "anthropic.resources",
                "name": "AsyncMessages.create",
                "wrapper": anthropic_async_chat_wrapper,
            },
            {
                "module": "anthropic.resources",
                "name": "Messages.stream",
                "wrapper": anthropic_stream_chat_wrapper,
            },
        ]

    def instrument(self) -> None:
        for wrapper in self.wrapped_methods:
            wrap_function_wrapper(
                wrapper["module"], wrapper["name"], wrapper["wrapper"]
            )
