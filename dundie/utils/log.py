"""Logging module for dundie."""

import logging
import os
from logging import Logger, handlers

from dundie.settings import (
    LOG_BACKUP_COUNT,
    LOG_FILE,
    LOG_FORMAT,
    LOG_LEVEL,
    LOG_MAX_BYTES,
    LOG_NAME,
)

# TODO: Use lib (loguru)


def get_logger(logfile: str = LOG_FILE) -> Logger:
    """
    Create and configure a logger.

    Args:
        logfile (str): The path to the log file. Defaults to LOGFILE.

    Returns:
        Logger: Configured logger instance.

    The logger is configured to write log messages to a rotating file handler
    with a maximum file size of 500 bytes and up to 3 backup files. The log
    level is determined by the 'LOG_LEVEL' environment variable, defaulting
    to 'WARNING' if not set. The log messages are formatted to include the
    timestamp, logger name, log level, line number, filename, and message.
    """
    # logging handler
    # ch = logging.StreamHandler() # write to console/terminal/stderr
    # by default the log file has the same name as the script with the
    # extension .log

    log_level = os.getenv("LOG_LEVEL", LOG_LEVEL).upper()

    # local logging instance
    log = logging.getLogger(LOG_NAME)
    # logfile = sys.argv[0]
    # logfile = logfile[2:-3] + ".log"
    fmt = logging.Formatter(LOG_FORMAT)

    fh = handlers.RotatingFileHandler(
        logfile,
        maxBytes=LOG_MAX_BYTES,
        backupCount=LOG_BACKUP_COUNT,
    )
    # logging handler logging level
    # ch.setLevel(log_level)
    fh.setLevel(log_level)
    # logging formatting
    # ch.setFormatter(fmt)
    fh.setFormatter(fmt)
    # logging destination
    # log.addHandler(ch)
    log.addHandler(fh)
    return log
