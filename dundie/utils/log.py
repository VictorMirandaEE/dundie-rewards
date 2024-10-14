import os
import logging
from logging import handlers

# TODO: Use lib (loguru)

LOG_LEVEL = os.getenv("LOG_LEVEL", "WARNING").upper()

# local logging instance
log = logging.getLogger("dundie")
# logfile = sys.argv[0]
# logfile = logfile[2:-3] + ".log"
fmt = logging.Formatter(
    "%(asctime)s  %(name)s  %(levelname)s l:%(lineno)d f:%(filename)s: %(message)s"
)


def get_logger(logfile="dundie.log"):
    """Returns a configured logger.

    Args:
        logfile (str, optional): _description_. Defaults to "dundie.log".

    Returns:
        _type_: _description_
    """
    # logging handler
    # ch = logging.StreamHandler() # write to console/terminal/stderr by default
    # the log file has the same name as the script with the extension .log
    fh = handlers.RotatingFileHandler(
        logfile,
        maxBytes=500,  # recommended 10**6
        backupCount=3,
    )
    # logging handler logging level
    # ch.setLevel(log_level)
    fh.setLevel(LOG_LEVEL)
    # logging formatting
    # ch.setFormatter(fmt)
    fh.setFormatter(fmt)
    # logging destination
    # log.addHandler(ch)
    log.addHandler(fh)
    return log
