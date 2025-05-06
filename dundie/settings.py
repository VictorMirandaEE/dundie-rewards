"""Settings module for the Dundie Rewards application.

This module contains configuration constants used throughout the application.

Attributes:
  SMTP_HOST (str): The hostname of the SMTP server.
  SMTP_PORT (int): The port number of the SMTP server.
  SMTP_TIMEOUT (int): The timeout duration for SMTP connections in seconds.
  SMTP_USERNAME (str): The username for SMTP authentication.
  SMTP_PASSWORD (str): The password for SMTP authentication.
  CURRENT_PATH (str): The current directory path of the application.
  DATABASE_PATH (str): The file path to the database file.
  SQL_CONNECTION_STRING (str): The SQL connection string for the database.
  EMAIL_FROM (str): The default email address for outgoing emails.
  DEFAULT_ACTOR (str): The default actor for system actions.
  DEFAULT_MANAGER_POINTS (Decimal): The default points assigned to managers.
  DEFAULT_ASSOCIATE_POINTS (Decimal): The default points assigned to
    associates.
  PROJECT_NAME (str): The name of the project.
  DATE_FORMAT (str): The date format used in the application.
  LOGFILE (str): The name of the log file.
"""

import os
from decimal import Decimal
from typing import Any, Dict, List


class VariableWrapper:
    """
    A wrapper class for a variable that includes its value and name.

    Attributes:
      value: The value of the variable.
      name: The name of the variable.

    Methods:
      __init__(self, value, name): Initializes the VariableWrapper with a value
        and a name.
    """

    def __init__(self, value: str, name: str):
        """Initialize class."""
        self.value = value
        self.name = name


Query = Dict[str, Any]
ResultDict = List[Dict[str, Any]]

SMTP_HOST: str = "localhost"
SMTP_PORT: int = 8025
SMTP_TIMEOUT: int = 5
SMTP_USERNAME: str = "username"
SMTP_PASSWORD: str = "password"

CURRENT_PATH: str = os.curdir

DATABASE_DIR: str = os.path.join(CURRENT_PATH, "assets")
DATABASE_PATH: str = os.path.join(DATABASE_DIR, "database.db")
SQL_CONNECTION_STRING: str = f"sqlite:///{DATABASE_PATH}"

EMAIL_FROM: str = "system@dundie.com"

DEFAULT_ACTOR: str = "system"

DEFAULT_MANAGER_POINTS: Decimal = Decimal(100)
DEFAULT_ASSOCIATE_POINTS: Decimal = Decimal(500)

PROJECT_NAME: str = "dundie"

DATE_FORMAT: str = "%Y-%m-%d %H:%M:%S"

LOG_NAME: str = "dundie"
LOG_FILE: str = f"{LOG_NAME}.log"
log_file = VariableWrapper(LOG_FILE, "LOG_FILE")
LOG_FORMAT: str = (
    "%(asctime)s %(name)s %(levelname)s l:%(lineno)d f:%(filename)s: %(message)s"  # noqa: E501
)
LOG_LEVEL: str = "DEBUG"  # INFO, DEBUG, WARNING, ERROR, CRITICAL
LOG_MAX_BYTES: int = 10 * 1024  # recommended: 1_000_000
LOG_BACKUP_COUNT: int = 3

API_BASE_URL: str = (
    "https://economia.awesomeapi.com.br/json/last/USD-{currency}"
)
