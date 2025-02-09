"""Settings module for the Dundie Rewards application.

This module contains configuration constants used throughout the application.

Attributes:
    SMTP_HOST (str): The hostname of the SMTP server.
    SMTP_PORT (int): The port number of the SMTP server.
    SMTP_TIMEOUT (int): The timeout duration for SMTP connections in seconds.
    SMTP_USERNAME (str): The username for SMTP authentication.
    SMTP_PASSWORD (str): The password for SMTP authentication.
    ROOT_PATH (str): The root directory path of the application.
    DATABASE_PATH (str): The file path to the database JSON file.
    EMAIL_FROM (str): The default email address for outgoing emails.
    DEFAULT_MANAGER_POINTS (int): The default points assigned to managers.
    DEFAULT_ASSOCIATE_POINTS (int): The default points assigned to associates.
"""

import os

SMTP_HOST = "localhost"
SMTP_PORT = 8025
SMTP_TIMEOUT = 5
SMTP_USERNAME = "username"
SMTP_PASSWORD = "password"

ROOT_PATH = os.path.dirname(__file__)
DATABASE_PATH = os.path.join(ROOT_PATH, "..", "assets", "database.json")

EMAIL_FROM = "admin@dundie.com"

DEFAULT_MANAGER_POINTS = 100
DEFAULT_ASSOCIATE_POINTS = 500
