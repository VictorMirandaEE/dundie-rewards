"""Logging module for dundie."""

import logging
import os
from logging import Logger
from logging.handlers import RotatingFileHandler

from dundie.settings import (
    LOG_BACKUP_COUNT,
    LOG_FILE,
    LOG_FORMAT,
    LOG_LEVEL,
    LOG_MAX_BYTES,
    LOG_NAME,
)

# TODO: Use lib (loguru)

log: logging.Logger | None = None


def set_logger(logfile: str = LOG_FILE) -> None:
    """Create and configure a log.

    Args:
        logfile (str): The path to the log file. Defaults to LOGFILE.

    Returns:
        log: Configured log instance.

    The log is configured to write log messages to a rotating file handler
    with a maximum file size of 500 bytes and up to 3 backup files. The log
    level is determined by the 'LOG_LEVEL' environment variable, defaulting
    to 'WARNING' if not set. The log messages are formatted to include the
    timestamp, log name, log level, line number, filename, and message.
    """
    global log

    # Create local logging instance
    log = logging.getLogger(LOG_NAME)

    # Set the log level based on the environment variable or use the default
    log_level = os.getenv("LOG_LEVEL", LOG_LEVEL).upper()
    log.setLevel(log_level)

    # Setup rotating file handler
    handler = RotatingFileHandler(
        logfile,
        maxBytes=LOG_MAX_BYTES,
        backupCount=LOG_BACKUP_COUNT,
    )

    # Set the log formatter
    formatter = logging.Formatter(LOG_FORMAT)
    handler.setFormatter(formatter)

    # Add the handler to the logger
    log.addHandler(handler)


def get_logger() -> Logger:
    """
    Retrieve the global logger instance.

    This function ensures that a logger instance is initialized and available
    for use. If the logger is not already initialized, it attempts to initialize
    it by calling `set_logger()`. If the logger still remains uninitialized,
    a `RuntimeError` is raised.

    Returns:
        Logger: The global logger instance.

    Raises:
        RuntimeError: If the logger is not initialized after attempting to set it.
    """
    global log

    if log is None:
        set_logger()

    if log is None:
        raise RuntimeError("Logger not initialized")

    return log
