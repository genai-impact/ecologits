import logging
from typing import Any, Union, cast


class EcoLogitsLogger(logging.Logger):
    """
    Logger for EcoLogits (implements `logging.Logger`)
    """

    def __init__(self, name: str, level: Union[int, str] = logging.NOTSET) -> None:
        super().__init__(name, level)
        self.__once_messages: set[str] = set()

    def _log_once(self, level: int, msg: str, *args: Any, **kwargs: Any) -> None:
        if msg not in self.__once_messages:
            self.__once_messages.add(msg)
            self.log(level, msg, *args, **kwargs)

    def debug_once(self, msg: str, *args: Any, **kwargs: Any) -> None:
        self._log_once(logging.DEBUG, msg, *args, **kwargs)

    def info_once(self, msg: str, *args: Any, **kwargs: Any) -> None:
        self._log_once(logging.INFO, msg, *args, **kwargs)

    def warning_once(self, msg: str, *args: Any, **kwargs: Any) -> None:
        self._log_once(logging.WARNING, msg, *args, **kwargs)

    def error_once(self, msg: str, *args: Any, **kwargs: Any) -> None:
        self._log_once(logging.ERROR, msg, *args, **kwargs)

    def critical_once(self, msg: str, *args: Any, **kwargs: Any) -> None:
        self._log_once(logging.CRITICAL, msg, *args, **kwargs)


logging.setLoggerClass(EcoLogitsLogger)
logger: EcoLogitsLogger = cast(EcoLogitsLogger, logging.getLogger("ecologits"))
