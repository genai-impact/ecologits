import logging


class EcoLogitsLogger(logging.Logger):

    def __init__(self, name, level=logging.NOTSET):
        super().__init__(name, level)
        self.__once_messages = set()

    def _log_once(self, level, msg, *args, **kwargs):
        if msg not in self.__once_messages:
            self.__once_messages.add(msg)
            self.log(level, msg, *args, **kwargs)

    def debug_once(self, msg, *args, **kwargs):
        self._log_once(logging.DEBUG, msg, *args, **kwargs)

    def info_once(self, msg, *args, **kwargs):
        self._log_once(logging.INFO, msg, *args, **kwargs)

    def warning_once(self, msg, *args, **kwargs):
        self._log_once(logging.WARNING, msg, *args, **kwargs)

    def error_once(self, msg, *args, **kwargs):
        self._log_once(logging.ERROR, msg, *args, **kwargs)

    def critical_once(self, msg, *args, **kwargs):
        self._log_once(logging.CRITICAL, msg, *args, **kwargs)


logging.setLoggerClass(EcoLogitsLogger)
logger = logging.getLogger(__name__)
