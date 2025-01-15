import time
from collections.abc import AsyncIterator, Awaitable, Iterator
from types import TracebackType
from typing import Any, Callable, Generic, Optional, TypeVar

from anthropic import Anthropic, AsyncAnthropic
from anthropic.lib.streaming import AsyncMessageStream as _AsyncMessageStream
from anthropic.lib.streaming import MessageStream as _MessageStream
from anthropic.types import Message as _Message
from anthropic.types.message_delta_event import MessageDeltaEvent
from anthropic.types.message_start_event import MessageStartEvent
from typing_extensions import override

from ecologits.domain import Instrumentor, WrappedMethod
from ecologits.tracers.utils import ImpactsOutput, llm_impacts

MessageStreamT = TypeVar("MessageStreamT", bound=_MessageStream)
AsyncMessageStreamT = TypeVar("AsyncMessageStreamT", bound=_AsyncMessageStream)


class Message(_Message):
    impacts: ImpactsOutput


class MessageStream(_MessageStream):
    impacts: Optional[ImpactsOutput] = None

    @override
    def __stream_text__(self) -> Iterator[str]:  # type: ignore[misc]
        timer_start = time.perf_counter()
        output_tokens = 0
        model_name = None
        for chunk in self:
            if type(chunk) is MessageStartEvent:
                message = chunk.message
                model_name = message.model
                output_tokens += message.usage.output_tokens
            elif type(chunk) is MessageDeltaEvent:
                output_tokens += chunk.usage.output_tokens
            elif chunk.type == "content_block_delta" and chunk.delta.type == "text_delta":
                yield chunk.delta.text
        requests_latency = time.perf_counter() - timer_start
        if model_name is not None:
            self.impacts = llm_impacts(
                provider=AnthropicInstrumentor.name,
                model_name=model_name,
                output_token_count=output_tokens,
                request_latency=requests_latency,
            )

    def __init__(self, parent) -> None:  # noqa: ANN001
        super().__init__(
            cast_to=parent._cast_to,  # noqa: SLF001
            response=parent.response,
            client=parent._client,  # noqa: SLF001
        )


class AsyncMessageStream(_AsyncMessageStream):
    impacts: Optional[ImpactsOutput] = None

    @override
    async def __stream_text__(self) -> AsyncIterator[str]:  # type: ignore[misc]
        timer_start = time.perf_counter()
        output_tokens = 0
        model_name = None
        async for chunk in self:
            if type(chunk) is MessageStartEvent:
                message = chunk.message
                model_name = message.model
                output_tokens += message.usage.output_tokens
            elif type(chunk) is MessageDeltaEvent:
                output_tokens += chunk.usage.output_tokens
            elif chunk.type == "content_block_delta" and chunk.delta.type == "text_delta":
                yield chunk.delta.text
        requests_latency = time.perf_counter() - timer_start
        if model_name is not None:
            self.impacts = llm_impacts(
                provider=AnthropicInstrumentor.name,
                model_name=model_name,
                output_token_count=output_tokens,
                request_latency=requests_latency,
            )

    def __init__(self, parent) -> None:  # noqa: ANN001
        super().__init__(
            cast_to=parent._cast_to,  # noqa: SLF001
            response=parent.response,
            client=parent._client,  # noqa: SLF001
        )


class MessageStreamManager(Generic[MessageStreamT]):
    def __init__(self, api_request: Callable[[], MessageStream]) -> None:
        self.__api_request = api_request

    def __enter__(self) -> MessageStream:
        self.__stream = self.__api_request()
        self.__stream = MessageStream(self.__stream)
        return self.__stream

    def __exit__(
        self, exc_type: Optional[type[BaseException]], exc: Optional[BaseException], exc_tb: Optional[TracebackType]
    ) -> None:
        if self.__stream is not None:
            self.__stream.close()


class AsyncMessageStreamManager(Generic[AsyncMessageStreamT]):
    def __init__(self, api_request: Awaitable[AsyncMessageStream]) -> None:
        self.__api_request = api_request

    async def __aenter__(self) -> AsyncMessageStream:
        self.__stream = await self.__api_request
        self.__stream = AsyncMessageStream(self.__stream)
        return self.__stream

    async def __aexit__(
        self, exc_type: Optional[type[BaseException]], exc: Optional[BaseException], exc_tb: Optional[TracebackType]
    ) -> None:
        if self.__stream is not None:
            await self.__stream.close()


class AnthropicInstrumentor(Instrumentor):
    provider = "anthropic"

    @staticmethod
    def anthropic_chat_wrapper(
        wrapped: Callable,
        instance: Anthropic,
        args: Any,
        kwargs: Any,  # noqa: ARG001
    ) -> Message:
        timer_start = time.perf_counter()
        response = wrapped(*args, **kwargs)
        request_latency = time.perf_counter() - timer_start
        model_name = response.model
        impacts = llm_impacts(
            provider=AnthropicInstrumentor.name,
            model_name=model_name,
            output_token_count=response.usage.output_tokens,
            request_latency=request_latency,
        )
        if impacts is not None:
            return Message(**response.model_dump(), impacts=impacts)
        else:
            return response

    @staticmethod
    async def anthropic_async_chat_wrapper(
        wrapped: Callable,
        instance: AsyncAnthropic,
        args: Any,
        kwargs: Any,  # noqa: ARG001
    ) -> Message:
        timer_start = time.perf_counter()
        response = await wrapped(*args, **kwargs)
        request_latency = time.perf_counter() - timer_start
        model_name = response.model
        impacts = llm_impacts(
            provider=AnthropicInstrumentor.name,
            model_name=model_name,
            output_token_count=response.usage.output_tokens,
            request_latency=request_latency,
        )
        if impacts is not None:
            return Message(**response.model_dump(), impacts=impacts)
        else:
            return response

    @staticmethod
    def anthropic_stream_chat_wrapper(
        wrapped: Callable,
        instance: Anthropic,
        args: Any,
        kwargs: Any,  # noqa: ARG001
    ) -> MessageStreamManager:
        response = wrapped(*args, **kwargs)
        return MessageStreamManager(response._MessageStreamManager__api_request)  # noqa: SLF001

    @staticmethod
    def anthropic_async_stream_chat_wrapper(
        wrapped: Callable,
        instance: AsyncAnthropic,
        args: Any,
        kwargs: Any,  # noqa: ARG001
    ) -> AsyncMessageStreamManager:
        response = wrapped(*args, **kwargs)
        return AsyncMessageStreamManager(response._AsyncMessageStreamManager__api_request)  # noqa: SLF001

    def __init__(self) -> None:
        self.wrapped_methods = [
            WrappedMethod(
                module="anthropic.resources",
                name="Messages.create",
                wrapper=self.anthropic_chat_wrapper,
            ),
            WrappedMethod(
                module="anthropic.resources",
                name="AsyncMessages.create",
                wrapper=self.anthropic_async_chat_wrapper,
            ),
            WrappedMethod(
                module="anthropic.resources",
                name="Messages.stream",
                wrapper=self.anthropic_stream_chat_wrapper,
            ),
            WrappedMethod(
                module="anthropic.resources",
                name="AsyncMessages.stream",
                wrapper=self.anthropic_async_stream_chat_wrapper,
            ),
        ]
