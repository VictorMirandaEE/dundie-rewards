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
