import logging

import pytest

from ecologits.log import logger


@pytest.mark.parametrize("logging_func", [
    logger.debug,
    logger.info,
    logger.warning,
    logger.error,
    logger.critical
])
def test_logging(caplog, logging_func):
    with caplog.at_level(logging.DEBUG, logger="ecologits"):
        logging_func("test")
        assert "test" in caplog.text


@pytest.mark.parametrize("logging_func", [
    logger.debug_once,
    logger.info_once,
    logger.warning_once,
    logger.error_once,
    logger.critical_once
])
def test_logging_once(caplog, logging_func):
    with caplog.at_level(logging.DEBUG, logger="ecologits"):
        logging_func(f"test({logging_func.__name__})")
        logging_func(f"test({logging_func.__name__})")  # This shouldn't be logged
        logging_func(f"test2({logging_func.__name__})")
        assert len(caplog.records) == 2
        assert "test" in caplog.text
        assert "test2" in caplog.text
