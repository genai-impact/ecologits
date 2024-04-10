from types import TracebackType
from typing import Any, Callable, Generic, Iterator, Optional, TypeVar

from typing_extensions import override
from wrapt import wrap_function_wrapper

from genai_impact.compute_impacts import Impacts, compute_llm_impact
from genai_impact.model_repository import models

try:
    from anthropic import Anthropic, AsyncAnthropic
    from anthropic.lib.streaming import MessageStream as _MessageStream
    from anthropic.types import Message as _Message
    from anthropic.types.message_delta_event import MessageDeltaEvent
    from anthropic.types.message_start_event import MessageStartEvent
except ImportError:
    Anthropic = object()
    AsyncAnthropic = object()
    _Message = object()
    _MessageStream = object()
    MessageDeltaEvent = object()
    MessageStartEvent = object()


MessageStreamT = TypeVar("MessageStreamT", bound=_MessageStream)


class Message(_Message):
    impacts: Impacts


class MessageStream(_MessageStream):
    @override
    def __stream_text__(self) -> Iterator[str]:
        output_tokens = 0
        model = None
        for chunk in self:
            if type(chunk) is MessageStartEvent:
                message = chunk.message
                model = models.find_model(provider="anthropic", model_name=message.model)
                output_tokens += message.usage.output_tokens
            elif type(chunk) is MessageDeltaEvent:
                output_tokens += chunk.usage.output_tokens
            elif chunk.type == "content_block_delta" and chunk.delta.type == "text_delta":
                yield chunk.delta.text
        model_size = model.active_parameters or model.active_parameters_range
        impacts = compute_llm_impact(
            model_parameter_count=model_size, output_token_count=output_tokens
        )
        self.impacts = impacts

    def __init__(self, parent) -> None:     # noqa: ANN001
        super().__init__(
            cast_to=parent._cast_to,        # noqa: SLF001
            response=parent.response,
            client=parent._client           # noqa: SLF001
        )


class MessageStreamManager(Generic[MessageStreamT]):
    def __init__(self, api_request: Callable[[], MessageStreamT]) -> None:
        self.__stream: Optional[MessageStreamT] = None
        self.__api_request = api_request

    def __enter__(self) -> MessageStreamT:
        self.__stream = self.__api_request()
        self.__stream = MessageStream(self.__stream)
        return self.__stream

    def __exit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc: Optional[BaseException],
        exc_tb: Optional[TracebackType]
    ) -> None:
        if self.__stream is not None:
            self.__stream.close()


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
    wrapped: Callable, instance: Anthropic, args: Any, kwargs: Any  # noqa: ARG001
) -> Message:
    response = wrapped(*args, **kwargs)
    return compute_impacts_and_return_response(response)


async def anthropic_async_chat_wrapper(
    wrapped: Callable, instance: AsyncAnthropic, args: Any, kwargs: Any  # noqa: ARG001
) -> Message:
    response = await wrapped(*args, **kwargs)
    return compute_impacts_and_return_response(response)


def anthropic_stream_chat_wrapper(
    wrapped: Callable, instance: Anthropic, args: Any, kwargs: Any  # noqa: ARG001
) -> MessageStreamManager:
    response = wrapped(*args, **kwargs)
    return MessageStreamManager(response._MessageStreamManager__api_request)    # noqa: SLF001


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
