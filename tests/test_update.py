"""dundie update subcommand unit test."""

from collections import deque
from typing import Generator

import pytest
from sqlmodel import select

from dundie.core import read, update
from dundie.database import get_session
from dundie.models import Employee
from dundie.utils.db import add_employee

from .constants import CEO_DATA, SALES_ASSOCIATE_DATA, SALES_MANAGER_DATA


@pytest.fixture(autouse=True)
def _auth(monkeypatch: pytest.MonkeyPatch) -> Generator[None, None, None]:
    """Fixture to set up an authenticated environment for testing.

    This function uses a monkeypatch context to set environment variables
    for an employee's email and password. It creates a manager employee
    in the database with the specified credentials and commits the session.

    Args:
        monkeypatch: A pytest fixture used to modify or set environment variables.

    Yields:
        None: This is a generator function that sets up the environment
        and yields control back to the test.
    """
    with get_session() as session, monkeypatch.context() as ctx:
        data = {
            "name": "A manager",
            "email": "manager@dm.com",
            "role": "Manager",
            "department": "Management",
            "currency": "USD",
        }
        password = "1234"
        employee, _ = add_employee(session, Employee(**data), password)
        ctx.setenv("EMPLOYEE_EMAIL", employee.email)
        ctx.setenv("EMPLOYEE_PASSWORD", password)
        session.commit()
        yield


@pytest.mark.unit
def test_update_points_to_existing_employee() -> None:
    """
    Test the update of points to an existing employee.

    This test performs the following steps:
    1. Connects to the database.
    2. Adds a new employee with a specified email and employee data.
    3. Commits the changes to the database.
    4. Reconnects to the database.
    5. Retrieves the previous balance of the employee.
    6. Updates the employee's balance by adding 100 points.
    7. Reads the employee data from the database.
    8. Asserts that the employee's balance has been correctly updated.
    """
    with get_session() as session:
        employee = Employee(**SALES_ASSOCIATE_DATA)
        add_employee(session, employee)
        session.commit()

    with get_session() as session:
        sql = select(Employee).where(
            Employee.email == SALES_ASSOCIATE_DATA["email"]
        )
        result = session.exec(sql).first()

        previous_balance = result.balance.value

    update(100, email=SALES_ASSOCIATE_DATA["email"])

    employees = read(email=SALES_ASSOCIATE_DATA["email"])

    assert employees[0]["balance"] == previous_balance + 100


@pytest.mark.unit
def test_update_points_to_multiple_employees() -> None:
    """
    Test updating points for multiple employees in the Engineering department.

    This test performs the following steps:
    1. Connects to the database.
    2. Adds two employees to the database with their respective details.
    3. Commits the changes to the database.
    4. Reconnects to the database and retrieves the previous balance for each
      employee.
    5. Updates the points for all employees in the Engineering department by
      adding 50 points.
    6. Asserts that the balance for each employee has been correctly updated
      by 50 points.
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

    previous_balance = []

    with get_session() as session:
        sql = select(Employee).order_by(Employee.id)
        result = session.exec(sql)

        for data in result:
            previous_balance.append(data.balance.value)

    previous_balance = deque(previous_balance)

    department = SALES_ASSOCIATE_DATA["department"]
    update(50, department=department)

    with get_session() as session:
        sql = select(Employee).order_by(Employee.id)
        result = session.exec(sql)

        for data in result:
            if data.department == department:
                assert data.balance.value == previous_balance.popleft() + 50
            else:
                assert data.balance.value == previous_balance.popleft()


@pytest.mark.unit
def test_update_points_no_employees_found() -> None:
    """
    Test case for updating points when no employees are found.

    This test ensures that the `update` function returns the message "No
    employees found" when attempting to update points for a non-existent
    employee.
    """
    assert update(100, email="nonexistent@example.com") == "No employees found"


@pytest.mark.unit
def test_update_points_to_all_employees() -> None:
    """
    Test the update of points to all employees.

    This test performs the following steps:
    1. Connects to the database.
    2. Creates a list of employee data with email, name, department, and role.
    3. Adds each employee to the database.
    4. Commits the changes to the database.
    5. Reconnects to the database.
    6. Retrieves and stores the previous balance of each employee.
    7. Reverses the order of the previous balances.
    8. Updates the points of all employees by a specified amount
      (25 in this case).
    9. Reads the updated employee data from the database.
    10. Asserts that the new balance of each employee is equal to the previous
      balance plus the update amount.
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

    previous_balance = []

    with get_session() as session:
        sql = select(Employee).order_by(Employee.id)
        result = session.exec(sql)

        for data in result:
            previous_balance.append(data.balance.value)

    previous_balance = deque(previous_balance)

    update(25)

    with get_session() as session:
        sql = select(Employee).order_by(Employee.id)
        result = session.exec(sql)

        for data in result:
            if data.email == "manager@dm.com":
                assert data.balance.value == previous_balance.popleft()
            else:
                assert data.balance.value == previous_balance.popleft() + 25
