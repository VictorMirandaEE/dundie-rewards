"""dundie read function unit test."""

from dundie.core import read
from dundie.database import add_employee, commit, connect


def test_read_no_query():
    """
    Test the read function without any query parameters.

    This test case performs the following steps:
    1. Connects to the database.
    2. Adds two employees to the database:
    3. Commits the changes to the database.
    4. Calls the read function to retrieve all employees.
    5. Asserts that the result contains exactly two entries.
    6. Asserts that the email and name of the returned entry match the
      expected values.
    """
    db = connect()
    add_employee(
        db,
        "john.doe@example.com",
        {"name": "John Doe", "department": "Sales", "role": "Manager"},
    )
    add_employee(
        db,
        "jane.doe@example.com",
        {"name": "Jane Doe", "department": "Marketing", "role": "Executive"},
    )
    commit(db)

    result = read()
    assert len(result) == 2
    assert result[0]["email"] == "john.doe@example.com"
    assert result[0]["name"] == "John Doe"
    assert result[1]["email"] == "jane.doe@example.com"
    assert result[1]["name"] == "Jane Doe"


def test_read_with_email_query():
    """
    Test the read function with an email query.

    This test function performs the following steps:
    1. Connects to the database.
    2. Adds two employees to the database.
    3. Commits the changes to the database.
    4. Queries the database for an employee with a specific email.
    5. Asserts that the result contains exactly one entry.
    6. Asserts that the email and name of the returned entry match the
      expected values.
    """
    db = connect()
    add_employee(
        db,
        "john.doe@example.com",
        {"name": "John Doe", "department": "Sales", "role": "Manager"},
    )
    add_employee(
        db,
        "jane.doe@example.com",
        {"name": "Jane Doe", "department": "Marketing", "role": "Executive"},
    )
    commit(db)

    result = read(email="john.doe@example.com")
    assert len(result) == 1
    assert result[0]["email"] == "john.doe@example.com"
    assert result[0]["name"] == "John Doe"


def test_read_with_department_query():
    """
    Test the read function with a department query.

    This test function performs the following steps:
    1. Connects to the database.
    2. Adds two employees to the database with different departments.
    3. Commits the changes to the database.
    4. Queries the database for an employee with a specific department.
    5. Asserts that the result contains exactly one entry.
    6. Asserts that the email and name of the returned entry match the
      expected values.
    """
    db = connect()
    add_employee(
        db,
        "john.doe@example.com",
        {"name": "John Doe", "department": "Sales", "role": "Manager"},
    )
    add_employee(
        db,
        "jane.doe@example.com",
        {"name": "Jane Doe", "department": "Marketing", "role": "Executive"},
    )
    commit(db)

    result = read(department="Marketing")
    assert len(result) == 1
    assert result[0]["email"] == "jane.doe@example.com"
    assert result[0]["department"] == "Marketing"
