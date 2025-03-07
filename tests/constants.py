"""Common constants for tests."""

import os
from typing import Any, Dict, List

TEST_PATH: str = os.path.dirname(__file__)
EMPLOYEES_FILE: str = os.path.join(TEST_PATH, "assets/employees.csv")

TEST_DATABASE_FILE: str = "test_database.db"
TEST_LOG_FILE: str = "test_dundie.log"

DATABASE_SCHEMA: Dict[str, Dict[str, Any]] = {
    "balance": {},
    "employee": {},
    "transaction": {},
    "user": {},
}

SALES_ASSOCIATE_DATA: Dict[str, str] = {
    "name": "John Doe",
    "email": "john@doe.com",
    "role": "Salesman",
    "department": "Sales",
}

SALES_MANAGER_DATA: Dict[str, str] = {
    "name": "Jane Doe",
    "email": "jane@doe.com",
    "role": "Manager",
    "department": "Sales",
}

CEO_DATA: Dict[str, str] = {
    "name": "CEO Doe",
    "email": "ceo@doe.com",
    "role": "CEO",
    "department": "Board of Directors",
}

VALID_EMAILS: List[str] = [
    "alice@example.com",
    "bob.smith@example.co.uk",
    "charlie123@example.org",
    "david_jones@example.net",
    "eve-adams@example.io",
    "frank@example.edu",
    "george@example.com",
    "hannah@example.com",
    "ian@example.com",
    "julia@example.com",
]

INVALID_EMAILS: List[str] = [
    "alice.example.com",  # Missing @
    "bob.smith@.co.uk",  # Missing domain
    "charlie123@.org",  # Missing domain
    "david_jones@example",  # Missing TLD
    "eve-adams@.io",  # Missing domain
    "frank@.edu",  # Missing domain
    "george@com",  # Missing domain
    "@example.com",  # Missing username
    "hannah@example..com",  # Double dots
    "ian@.com",  # Missing domain
    "julia@com",  # Missing domain
    "kate@",  # Missing domain
    "laura",  # Missing domain
    "@",  # Missing username and domain
    "",  # Empty string
    " ",  # Space
    '""',  # Empty quotes
    '" "',  # Space in quotes
    "''",  # Empty single quotes
    "' '",  # Space in single quotes
]

INVALID_EMAILS2: List[str] = [
    "",  # Empty string
    " ",  # Space
    '""',  # Empty quotes
    '" "',  # Space in quotes
    "''",  # Empty single quotes
    "' '",  # Space in single quotes
]
