"""dundie update subcommand unit test."""

import pytest

from dundie.core import read, update
from dundie.database import add_employee, commit, connect


def test_update_points_to_existing_employee():
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
    db = connect()
    email = "test@example.com"
    employee_data = {
        "name": "Test User",
        "department": "Engineering",
        "role": "Developer",
    }
    add_employee(db, email, employee_data)
    commit(db)

    db = connect()
    previous_balance = db["balance"][email]

    update(100, email=email)

    employees = read(email=email)
    assert employees[0]["balance"] == previous_balance + 100


def test_update_points_to_multiple_employees():
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
    db = connect()
    employees_data = [
        {
            "email": "test1@example.com",
            "name": "Test User 1",
            "department": "Engineering",
            "role": "Developer",
        },
        {
            "email": "test2@example.com",
            "name": "Test User 2",
            "department": "Engineering",
            "role": "Manager",
        },
    ]
    for data in employees_data:
        add_employee(db, data["email"], data)
    commit(db)

    db = connect()
    previous_balance = []
    for data in employees_data:
        employees = read(email=data["email"])
        previous_balance.append(db["balance"][data["email"]])

    previous_balance.reverse()

    update(50, department="Engineering")

    for data in employees_data:
        employees = read(email=data["email"])
        assert employees[0]["balance"] == previous_balance.pop() + 50


def test_update_points_no_employees_found():
    """
    Test case for updating points when no employees are found.

    This test ensures that the `update` function raises a `RuntimeError`
    with the message "No employees found" when attempting to update points
    for a non-existent employee.

    Raises:
        RuntimeError: If no employees are found with the given email.
    """
    with pytest.raises(RuntimeError, match="No employees found"):
        update(100, email="nonexistent@example.com")


def test_update_points_to_all_employees():
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
    db = connect()
    employees_data = [
        {
            "email": "test1@example.com",
            "name": "Test User 1",
            "department": "Engineering",
            "role": "Developer",
        },
        {
            "email": "test2@example.com",
            "name": "Test User 2",
            "department": "Engineering",
            "role": "Manager",
        },
        {
            "email": "test3@example.com",
            "name": "Test User 3",
            "department": "HR",
            "role": "Recruiter",
        },
    ]
    for data in employees_data:
        add_employee(db, data["email"], data)
    commit(db)

    db = connect()
    previous_balance = []
    for data in employees_data:
        previous_balance.append(db["balance"][data["email"]])

    previous_balance.reverse()

    update(25)

    for data in employees_data:
        employees = read(email=data["email"])
        assert employees[0]["balance"] == previous_balance.pop() + 25
