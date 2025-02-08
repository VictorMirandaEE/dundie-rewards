"""dundie database unit test"""

from unittest.mock import patch

import pytest

from dundie.database import (
    DATABASE_SCHEMA,
    add_employee,
    add_transaction,
    commit,
    connect,
    set_initial_password,
)
from dundie.settings import DEFAULT_ASSOCIATE_POINTS, DEFAULT_MANAGER_POINTS


@pytest.mark.unit
def test_database_schema():
    """
    Test the database schema.

    This function connects to the database and asserts that the keys in the
    database match the expected keys defined in the DATABASE_SCHEMA.

    Raises:
        AssertionError: If the keys in the database do not match the expected
          keys.
    """
    db = connect()
    assert db.keys() == DATABASE_SCHEMA.keys()


@pytest.mark.unit
def test_database_commit():
    """
    Test the commit operation of the database.

    This test function performs the following steps:
    1. Connects to the database.
    2. Creates a sample employee data dictionary.
    3. Inserts the sample data into the database.
    4. Commits the changes to the database.
    5. Reconnects to the database to ensure changes are persisted.
    6. Asserts that the inserted data is correctly stored in the database.

    Raises:
        AssertionError: If the data is not correctly stored in the database
          after commit.
    """
    db = connect()
    data = {"name": "John Doe", "role": "Manager", "department": "Sales"}
    db["employees"]["john@doe.com"] = data
    commit(db)

    db = connect()
    assert db["employees"]["john@doe.com"] == data


@pytest.mark.unit
@patch("dundie.database.generate_simple_password")
def test_set_initial_password(mock_generate_password):
    """
    Test the set_initial_password function.

    This test function performs the following steps:
    1. Mocks the generate_simple_password function to return a known password.
    2. Connects to the database.
    3. Calls set_initial_password with a sample email.
    4. Asserts that the password is set correctly in the database.
    5. Asserts that the returned password matches the mocked password.

    Raises:
        AssertionError: If the password is not set correctly in the database
            or the returned password does not match the mocked password.
    """
    mock_generate_password.return_value = "mocked_password"
    db = connect()
    email = "test@example.com"
    password = set_initial_password(db, email)
    commit(db)

    db = connect()
    assert db["users"][email]["password"] == "mocked_password"
    assert password == "mocked_password"


@pytest.mark.unit
def test_positive_add_employee_new_associate():
    """
    Test the addition of a new associate employee to the database.

    This test verifies that a new associate employee is correctly added to the
    database with the appropriate data and initial points balance.

    It checks the following:
    - The employee data is correctly stored in the database.
    - The employee creation flag is set to True.
    - The employee's initial points balance is set to the default associate
      points.
    - A transaction is created for the employee with the initial points.

    Steps:
    1. Connect to the database.
    2. Define the email and data for the new associate employee.
    3. Add the employee to the database and verify the returned data and
      creation flag.
    4. Commit the changes to the database.
    5. Reconnect to the database and verify the stored employee data, balance,
      and transactions.
    """
    db = connect()
    email = "new_associate@example.com"
    data = {
        "name": "New Associate",
        "role": "Associate",
        "department": "Engineering",
    }
    employee, created = add_employee(db, email, data)
    assert employee == data
    assert created is True
    commit(db)

    db = connect()
    assert db["employees"][email] == data
    assert db["balance"][email] == DEFAULT_ASSOCIATE_POINTS
    assert len(db["transactions"][email]) == 1
    assert db["transactions"][email][0]["points"] == DEFAULT_ASSOCIATE_POINTS


@pytest.mark.unit
def test_positive_add_employee_new_manager():
    """
    Test the addition of a new manager employee to the database.

    This test verifies that a new manager employee is correctly added to the
    database with the appropriate data and initial points balance.

    It checks the following:
    - The employee data is correctly stored in the database.
    - The employee creation flag is set to True.
    - The employee's initial points balance is set to the default manager
      points.
    - A transaction is created for the employee with the initial points.

    Steps:
    1. Connect to the database.
    2. Define the email and data for the new manager employee.
    3. Add the employee to the database and verify the returned data and
      creation flag.
    4. Commit the changes to the database.
    5. Reconnect to the database and verify the stored employee data, balance,
      and transactions.
    """
    db = connect()
    email = "new_manager@example.com"
    data = {
        "name": "New Manager",
        "role": "Manager",
        "department": "Engineering",
    }
    employee, created = add_employee(db, email, data)
    assert employee == data
    assert created is True
    commit(db)

    db = connect()
    assert db["employees"][email] == data
    assert db["balance"][email] == DEFAULT_MANAGER_POINTS
    assert len(db["transactions"][email]) == 1
    assert db["transactions"][email][0]["points"] == DEFAULT_MANAGER_POINTS


@pytest.mark.unit
def test_negative_add_employee_invalid_email():
    """
    Test that adding an employee with an invalid email raises a ValueError.

    This test checks that the `add_employee` function raises a `ValueError`
    when provided with an invalid email address. The error message should
    match the format "Invalid email address: {email}".

    Raises:
        ValueError: If the email address is invalid.
    """
    email = "invalid_email"

    with pytest.raises(ValueError, match=f"Invalid email address: {email}"):
        add_employee({}, email, {})


@pytest.mark.unit
def test_negative_add_employee_duplicated():
    """
    Test the behavior of adding a duplicated employee to the database.

    This test ensures that when attempting to add an employee with an email
    that already exists in the database, the function correctly identifies the
    duplicate and does not overwrite the existing employee data. It also
    verifies that the employee's initial data remains unchanged and that no
    additional transactions are created for the duplicated entry.

    Steps:
    1. Connect to the database.
    2. Add an employee with initial data and verify the employee is created.
    3. Commit the changes to the database.
    4. Attempt to add the same employee with updated data and verify the
        employee is not created again.
    5. Reconnect to the database and verify the employee's data remains as the
        initial data.
    6. Verify the employee's balance and transaction history remain unchanged.
    """
    db = connect()
    email = "existing_employee@example.com"
    initial_data = {
        "name": "Existing Employee",
        "role": "Developer",
        "department": "Engineering",
    }
    employee, created = add_employee(db, email, initial_data)
    assert employee == initial_data
    assert created is True
    commit(db)

    updated_data = {
        "name": "Updated Employee",
        "role": "Manager",
        "department": "Engineering",
    }
    employee, created = add_employee(db, email, updated_data)
    assert employee == updated_data
    assert created is False

    db = connect()
    assert db["employees"][email] == initial_data
    assert db["balance"][email] == DEFAULT_ASSOCIATE_POINTS
    assert len(db["transactions"][email]) == 1
    assert db["transactions"][email][0]["points"] == DEFAULT_ASSOCIATE_POINTS


@pytest.mark.unit
def test_positive_add_points():
    """
    Test the addition of points to an existing employee's balance.
    This test performs the following steps:
    1. Connects to the database and adds an existing employee.
    2. Verifies that the employee is added correctly and commits the
      transaction.
    3. Reconnects to the database and adds points to the employee's balance.
    4. Commits the transaction.
    5. Reconnects to the database and verifies that the points were added
      correctly.
    6. Checks that the transaction details are correct.
    """
    db = connect()
    email = "existing_employee@example.com"
    initial_data = {
        "name": "Existing Employee",
        "role": "Developer",
        "department": "Engineering",
    }
    employee, created = add_employee(db, email, initial_data)
    assert employee == initial_data
    assert created is True
    commit(db)

    db = connect()
    points = 100
    previous_balance = db["balance"][email]
    add_transaction(db, email, points, "Bonus points", "manager")
    commit(db)

    db = connect()
    assert db["balance"][email] == previous_balance + points
    assert len(db["transactions"][email]) == 2
    assert db["transactions"][email][1]["points"] == points
    assert db["transactions"][email][1]["description"] == "Bonus points"
    assert db["transactions"][email][1]["actor"] == "manager"


@pytest.mark.unit
def test_positive_remove_points():
    """
    Test the removal of points from an employee's balance.
    This test verifies that points can be successfully removed from an existing
    employee's balance and that the transaction is recorded correctly in th
      database.
    Steps:
    1. Connect to the database.
    2. Add an employee with initial data.
    3. Verify that the employee is added and committed to the database.
    4. Connect to the database again.
    5. Remove points from the employee's balance due to a bad performance
      review.
    6. Commit the transaction to the database.
    7. Connect to the database again.
    8. Verify that the employee's balance is updated correctly.
    9. Verify that the transaction is recorded with the correct details.
    """
    db = connect()
    email = "existing_employee@example.com"
    initial_data = {
        "name": "Existing Employee",
        "role": "Developer",
        "department": "Engineering",
    }
    employee, created = add_employee(db, email, initial_data)
    assert employee == initial_data
    assert created is True
    commit(db)

    db = connect()
    points = -100
    previous_balance = db["balance"][email]
    add_transaction(db, email, points, "Bad performance review", "manager")
    commit(db)

    db = connect()
    assert db["balance"][email] == previous_balance + points
    assert len(db["transactions"][email]) == 2
    assert db["transactions"][email][1]["points"] == points
    assert (
        db["transactions"][email][1]["description"] == "Bad performance review"
    )
    assert db["transactions"][email][1]["actor"] == "manager"
