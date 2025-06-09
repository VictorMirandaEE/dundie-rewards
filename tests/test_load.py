"""dundie load subcommand unit test."""

import os
from unittest.mock import patch

import pytest

from dundie.core import load
from dundie.settings import CURRENT_PATH, LOG_FILE
from tests.constants import (
    CEO_DATA,
    INVALID_EMAILS,
    SALES_ASSOCIATE_DATA,
    SALES_MANAGER_DATA,
    VALID_EMAILS,
)


@pytest.fixture
def mock_logger():
    """
    Mock the logger used in the dundie.core module for testing purposes.

    This function uses the `patch` context manager to replace the `get_logger`
    function in the `dundie.core` module with a mock object. It yields the mock
    logger, allowing tests to assert logging behavior.

    Yields:
        unittest.mock.MagicMock: A mock object for the logger.
    """
    with patch("dundie.core.get_logger") as mock_log:
        yield mock_log


@pytest.mark.unit
def test_negative_load_empty_csv():
    """
    Test that the load function correctly loads and returns 2 employees from\
    the EMPLOYEES_FILE.

    Args:
        request: A pytest fixture that provides information about the test
          execution.
    Asserts:
        The length of the list returned by the load function is 2.
    """
    empty_csv_file = "empty.csv"
    open(os.path.join(CURRENT_PATH, empty_csv_file), "w").close()

    assert len(load(empty_csv_file)) == 0


@pytest.mark.unit
@pytest.mark.parametrize(
    "employees_data",
    [
        [SALES_ASSOCIATE_DATA],
        [SALES_ASSOCIATE_DATA, SALES_MANAGER_DATA],
        [SALES_ASSOCIATE_DATA, SALES_MANAGER_DATA, CEO_DATA],
    ],
)
@pytest.mark.parametrize("valid_email", VALID_EMAILS)
def test_positive_load_csv_with_multiple_employees_and_valid_email(
    employees_data, valid_email
):
    """
    Test that the load function raises a ValidationError when an invalid email\
    address is provided in the EMPLOYEES_FILE.

    Args:
        request: A pytest fixture that provides information about the test
          execution.
        invalid_email: A string representing an invalid email address.
    Asserts:
        A ValidationError is raised when an invalid email address is provided.
    """
    employees_file = "multiple_employees.csv"

    employees_data[0]["email"] = valid_email

    with open(os.path.join(CURRENT_PATH, employees_file), "w") as file:
        file.write(", ".join(employees_data[0].keys()) + "\n")
        for employee_data in employees_data:
            file.write(", ".join(employee_data.values()) + "\n")

    result = load(employees_file)

    assert len(result) == len(employees_data)

    for employee_data in employees_data:
        assert result[0]["name"] == employee_data["name"]
        assert result[0]["email"] == employee_data["email"]
        assert result[0]["role"] == employee_data["role"]
        assert result[0]["department"] == employee_data["department"]
        assert result[0]["currency"] == employee_data["currency"]
        result.pop(0)


@pytest.mark.unit
@pytest.mark.parametrize(
    "invalid_employee_id",
    [
        0,
        1,
    ],
)
@pytest.mark.parametrize(
    "employees_data",
    [
        [SALES_ASSOCIATE_DATA],
        [SALES_ASSOCIATE_DATA, SALES_MANAGER_DATA],
    ],
)
@pytest.mark.parametrize("invalid_email", INVALID_EMAILS)
def test_negative_load_csv_with_multiple_employees_and_invalid_email(
    invalid_employee_id, employees_data, invalid_email
):
    """
    Test that the load function raises a ValidationError when an invalid email\
    address is provided in the EMPLOYEES_FILE.

    Args:
        request: A pytest fixture that provides information about the test
          execution.
        invalid_email: A string representing an invalid email address.
    Asserts:
        A ValidationError is raised when an invalid email address is provided.
    """
    employees_file = "invalid_email.csv"

    if len(employees_data) == 1:
        invalid_employee = employees_data[0]
    else:
        invalid_employee = employees_data[invalid_employee_id]

    invalid_employee["email"] = invalid_email

    trimmed_invalid_email = invalid_email.strip('"')

    if not invalid_email.strip():
        invalid_employee_msg = f"{{'name': {invalid_employee['name']!r}, 'email': '', 'role': {invalid_employee['role']!r}, 'department': {invalid_employee['department']!r}, 'currency': {invalid_employee['currency']!r}}}"  # noqa E501
        error_msg = f"Employee {invalid_employee_msg} has an invalid email ''"
    else:
        invalid_employee_msg = f"{{'name': {invalid_employee['name']!r}, 'email': {trimmed_invalid_email!r}, 'role': {invalid_employee['role']!r}, 'department': {invalid_employee['department']!r}, 'currency': {invalid_employee['currency']!r}}}"  # noqa E501
        error_msg = f"Employee {invalid_employee_msg} has an invalid email {trimmed_invalid_email!r}"  # noqa E501

    with open(os.path.join(CURRENT_PATH, employees_file), "w") as file:
        file.write(", ".join(employees_data[0].keys()) + "\n")
        for employee_data in employees_data:
            file.write(", ".join(employee_data.values()) + "\n")

    assert len(load(employees_file)) == (
        0 if invalid_employee_id == 0 else len(employees_data) - 1
    )

    with open(os.path.join(CURRENT_PATH, LOG_FILE), "r") as logfile:
        assert error_msg in logfile.read()


@pytest.mark.unit
def test_negative_load_file_not_found(mock_logger):
    """
    Test that the load function handles a FileNotFoundError when the specified\
    file does not exist.

    Asserts:
        The logger records an error message indicating the file was not found.
        The load function returns an empty list when the file is missing.
    """
    with patch(
        "builtins.open", side_effect=FileNotFoundError("File not found")
    ):
        result = load("nonexistent.csv")

    mock_logger().error.assert_called_with("FileNotFoundError: File not found")

    assert result == []
