"""dundie read function unit test."""

import pytest

from dundie.core import read
from dundie.database import get_session
from dundie.models import Employee
from dundie.utils.db import add_employee

from .constants import CEO_DATA, SALES_ASSOCIATE_DATA, SALES_MANAGER_DATA


@pytest.mark.unit
def test_positive_read_no_query():
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
    employees_data = [
        SALES_ASSOCIATE_DATA,
        SALES_MANAGER_DATA,
        CEO_DATA,
    ]
    with get_session() as session:
        for data in employees_data:
            employee = Employee(**data)
            add_employee(session, employee)
        session.commit()

    result = read()

    assert len(result) == 3
    assert result[0]["email"] == SALES_ASSOCIATE_DATA["email"]
    assert result[0]["name"] == SALES_ASSOCIATE_DATA["name"]
    assert result[1]["email"] == SALES_MANAGER_DATA["email"]
    assert result[1]["name"] == SALES_MANAGER_DATA["name"]
    assert result[2]["email"] == CEO_DATA["email"]
    assert result[2]["name"] == CEO_DATA["name"]


@pytest.mark.unit
def test_negative_read_no_query():
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
    result = read()

    assert len(result) == 0


@pytest.mark.unit
def test_positive_read_with_email_query():
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
    with get_session() as session:
        employee = Employee(**SALES_ASSOCIATE_DATA)
        add_employee(session, employee)
        employee = Employee(**SALES_MANAGER_DATA)
        session.add(employee)
        add_employee(session, employee)
        session.commit()

    result = read(email=SALES_ASSOCIATE_DATA["email"])

    assert len(result) == 1
    assert result[0]["email"] == SALES_ASSOCIATE_DATA["email"]
    assert result[0]["name"] == SALES_ASSOCIATE_DATA["name"]


@pytest.mark.unit
def test_negative_read_with_email_query():
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
    with get_session() as session:
        employee = Employee(**SALES_ASSOCIATE_DATA)
        add_employee(session, employee)
        employee = Employee(**SALES_MANAGER_DATA)
        session.add(employee)
        add_employee(session, employee)
        session.commit()

    result = read(email="nobody@none.com")

    assert len(result) == 0


@pytest.mark.unit
def test_positive_read_with_department_query_single_match():
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
    employees_data = [
        SALES_ASSOCIATE_DATA,
        SALES_MANAGER_DATA,
        CEO_DATA,
    ]
    with get_session() as session:
        for data in employees_data:
            employee = Employee(**data)
            add_employee(session, employee)
        session.commit()

    result = read(department="Board of Directors")

    assert len(result) == 1
    assert result[0]["email"] == CEO_DATA["email"]
    assert result[0]["department"] == CEO_DATA["department"]


@pytest.mark.unit
def test_positive_read_with_department_query_multiple_matches():
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
    employees_data = [
        SALES_ASSOCIATE_DATA,
        SALES_MANAGER_DATA,
        CEO_DATA,
    ]
    with get_session() as session:
        for data in employees_data:
            employee = Employee(**data)
            add_employee(session, employee)
        session.commit()

    result = read(department="Sales")

    assert len(result) == 2
    assert result[0]["email"] == SALES_ASSOCIATE_DATA["email"]
    assert result[0]["department"] == SALES_ASSOCIATE_DATA["department"]
    assert result[1]["email"] == SALES_MANAGER_DATA["email"]
    assert result[1]["department"] == SALES_MANAGER_DATA["department"]


@pytest.mark.unit
def test_negative_read_with_department_query():
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
    with get_session() as session:
        employee = Employee(**SALES_ASSOCIATE_DATA)
        add_employee(session, employee)
        employee = Employee(**SALES_MANAGER_DATA)
        session.add(employee)
        add_employee(session, employee)
        session.commit()

    result = read(department="None")

    assert len(result) == 0
