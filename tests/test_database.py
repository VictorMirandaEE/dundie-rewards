"""dundie database unit test."""

from decimal import Decimal
from unittest.mock import patch

import pytest
from pydantic import ValidationError
from sqlmodel import MetaData, select

from dundie.database import get_session
from dundie.models import Employee
from dundie.settings import (
    DEFAULT_ACTOR,
    DEFAULT_ASSOCIATE_POINTS,
    DEFAULT_MANAGER_POINTS,
)
from dundie.utils.db import (
    add_employee,
    add_transaction,
    set_initial_balance,
    set_initial_password,
)

from .constants import (
    DATABASE_SCHEMA,
    INVALID_EMAILS,
    SALES_ASSOCIATE_DATA,
    SALES_MANAGER_DATA,
    TEST_DATABASE_FILE,
    VALID_EMAILS,
)


@pytest.mark.unit
def test_ensure_database_is_test():
    """Test that the database URL is set to a test database."""
    with get_session() as session:
        assert TEST_DATABASE_FILE in session.get_bind().engine.url.database


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
    with get_session() as session:
        metadata = MetaData()
        metadata.reflect(bind=session.bind)

        assert metadata.tables.keys() == DATABASE_SCHEMA.keys()


@pytest.mark.unit
def test_positive_add_employee_associate():
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
    with get_session() as session:
        SALES_ASSOCIATE_DATA["id"] = 1
        employee = Employee(**SALES_ASSOCIATE_DATA)
        instance, created = add_employee(session, employee)

        assert instance.model_dump() == SALES_ASSOCIATE_DATA
        assert created is True

        session.commit()

        sql = select(Employee).where(
            Employee.email == SALES_ASSOCIATE_DATA["email"]
        )
        result = session.exec(sql).first()

        assert result.model_dump() == SALES_ASSOCIATE_DATA
        assert result.balance[0].value == DEFAULT_ASSOCIATE_POINTS
        assert len(result.transaction) == 1
        assert result.transaction[-1].value == DEFAULT_ASSOCIATE_POINTS


@pytest.mark.unit
def test_positive_add_employee_manager():
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
    with get_session() as session:
        SALES_MANAGER_DATA["id"] = 1
        employee = Employee(**SALES_MANAGER_DATA)
        instance, created = add_employee(session, employee)

        assert instance.model_dump() == SALES_MANAGER_DATA
        assert created is True

        sql = select(Employee).where(
            Employee.email == SALES_MANAGER_DATA["email"]
        )
        result = session.exec(sql).first()

        assert result.model_dump() == SALES_MANAGER_DATA
        assert result.balance[0].value == DEFAULT_MANAGER_POINTS
        assert len(result.transaction) == 1
        assert result.transaction[-1].value == DEFAULT_MANAGER_POINTS


@pytest.mark.unit
def test_positive_set_initial_balance_associate():
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
    with get_session() as session:
        SALES_ASSOCIATE_DATA["id"] = 1
        employee = Employee(**SALES_ASSOCIATE_DATA)
        session.add(employee)
        set_initial_balance(session, employee)
        session.commit()

        sql = select(Employee).where(
            Employee.email == SALES_ASSOCIATE_DATA["email"]
        )
        result = session.exec(sql).first()

        assert result.model_dump() == SALES_ASSOCIATE_DATA
        assert result.balance[0].value == DEFAULT_ASSOCIATE_POINTS
        assert len(result.transaction) == 1
        assert result.transaction[-1].value == DEFAULT_ASSOCIATE_POINTS


@pytest.mark.unit
def test_positive_set_initial_balance_manager():
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
    with get_session() as session:
        SALES_MANAGER_DATA["id"] = 1
        employee = Employee(**SALES_MANAGER_DATA)
        session.add(employee)
        set_initial_balance(session, employee)
        session.commit()

        sql = select(Employee).where(
            Employee.email == SALES_MANAGER_DATA["email"]
        )
        result = session.exec(sql).first()

        assert result.model_dump() == SALES_MANAGER_DATA
        assert result.balance[0].value == DEFAULT_MANAGER_POINTS
        assert len(result.transaction) == 1
        assert result.transaction[-1].value == DEFAULT_MANAGER_POINTS


@pytest.mark.unit
@pytest.mark.parametrize("valid_email", VALID_EMAILS)
def test_positive_add_employee_valid_email(valid_email):
    """
    Test that adding an employee with an invalid email raises a ValueError.

    This test checks that the `add_employee` function raises a `ValueError`
    when provided with an invalid email address. The error message should
    match the format "Invalid email address: {email}".

    Raises:
        ValueError: If the email address is invalid.
    """
    with get_session() as session:
        SALES_ASSOCIATE_DATA["id"] = 1
        SALES_ASSOCIATE_DATA["email"] = valid_email
        employee = Employee(**SALES_ASSOCIATE_DATA)
        instance, created = add_employee(session, employee)

        assert type(instance) is Employee
        assert instance.model_dump() == SALES_ASSOCIATE_DATA
        assert created is True

        session.commit()


@pytest.mark.unit
@pytest.mark.parametrize("invalid_email", INVALID_EMAILS)
def test_negative_add_employee_invalid_email(invalid_email):
    """
    Test that adding an employee with an invalid email raises a ValueError.

    This test checks that the `add_employee` function raises a `ValueError`
    when provided with an invalid email address. The error message should
    match the format "Invalid email address: {email}".

    Raises:
        ValueError: If the email address is invalid.
    """
    SALES_ASSOCIATE_DATA["email"] = invalid_email
    with pytest.raises(ValidationError):
        Employee(**SALES_ASSOCIATE_DATA)


@pytest.mark.unit
def test_positive_update_employee() -> None:
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
    with get_session() as session:
        initial_data = {
            "id": 1,
            "email": "employee@example.com",
            "name": "Initial Name",
            "role": "Initial Role",
            "department": "Initial Department",
            "currency": "USD",
        }
        employee = Employee(**initial_data)
        initial_instance, initial_created = add_employee(session, employee)

        assert initial_instance.model_dump() == initial_data
        assert initial_created is True

        session.commit()

    with get_session() as session:
        updated_data = {
            "id": 1,
            "email": "employee@example.com",
            "name": "Updated Name",
            "role": "Updated Role",
            "department": "Updated Department",
            "currency": "BRL",
        }
        employee = Employee(**updated_data)
        updated_instance, updated_created = add_employee(session, employee)

        assert updated_instance.model_dump() == updated_data
        assert updated_created is False

        session.commit()

    with get_session() as session:
        sql = select(Employee).where(Employee.email == initial_data["email"])
        result = session.exec(sql).first()

        assert (
            result
            is not None
            # Workaround to avoid MyPy error due to None check.
            # See https://github.com/python/mypy/issues/2608
        )
        assert result.model_dump() == updated_data
        assert result.balance[0].value == DEFAULT_ASSOCIATE_POINTS
        assert len(result.transaction) == 1
        assert result.transaction[-1].value == DEFAULT_ASSOCIATE_POINTS


@pytest.mark.unit
@pytest.mark.parametrize(
    "value",
    [
        100,  # Positive points
        -100,  # Negative points
        0,  # Zero points
        100.5,  # Decimal points
        -100.5,  # Negative decimal points
        -0,  # Negative zero points
    ],
)
def test_positive_add_transaction(value: int | float) -> None:
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
    with get_session() as session:
        employee = Employee(**SALES_ASSOCIATE_DATA)
        add_employee(session, employee)
        session.add(employee)
        session.commit()

    with get_session() as session:
        sql = select(Employee).where(
            Employee.email == SALES_ASSOCIATE_DATA["email"]
        )
        instance = session.exec(sql).first()

        assert (
            instance
            is not None
            # Workaround to avoid MyPy error due to None check.
            # See https://github.com/python/mypy/issues/2608
        )

        previous_balance = instance.balance[0].value

        add_transaction(
            session, instance, Decimal(value), "Updated points", "manager"
        )

        session.commit()

    with get_session() as session:
        sql = select(Employee).where(
            Employee.email == SALES_ASSOCIATE_DATA["email"]
        )
        instance = session.exec(sql).first()

        assert (
            instance
            is not None
            # Workaround to avoid MyPy error due to None check.
            # See https://github.com/python/mypy/issues/2608
        )
        assert instance.balance[0].value == previous_balance + Decimal(value)
        assert len(instance.transaction) == 2
        assert instance.transaction[1].value == Decimal(value)
        assert instance.transaction[1].description == "Updated points"
        assert instance.transaction[1].actor == "manager"


@pytest.mark.unit
def test_positive_add_transaction_default_actor() -> None:
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
    value = 100

    with get_session() as session:
        employee = Employee(**SALES_ASSOCIATE_DATA)
        add_employee(session, employee)
        session.add(employee)
        session.commit()

    with get_session() as session:
        sql = select(Employee).where(
            Employee.email == SALES_ASSOCIATE_DATA["email"]
        )
        instance = session.exec(sql).first()

        assert (
            instance
            is not None
            # Workaround to avoid MyPy error due to None check.
            # See https://github.com/python/mypy/issues/2608
        )

        previous_balance = instance.balance[0].value

        add_transaction(session, instance, Decimal(value), "Updated points")

        session.commit()

    with get_session() as session:
        sql = select(Employee).where(
            Employee.email == SALES_ASSOCIATE_DATA["email"]
        )
        instance = session.exec(sql).first()

        assert (
            instance
            is not None
            # Workaround to avoid MyPy error due to None check.
            # See https://github.com/python/mypy/issues/2608
        )
        assert instance.balance[0].value == previous_balance + Decimal(value)
        assert len(instance.transaction) == 2
        assert instance.transaction[1].value == Decimal(value)
        assert instance.transaction[1].description == "Updated points"
        assert instance.transaction[1].actor == DEFAULT_ACTOR


@pytest.mark.unit
@patch("dundie.models.generate_simple_password")
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

    with get_session() as session:
        employee = Employee(**SALES_ASSOCIATE_DATA)
        session.add(employee)
        password = set_initial_password(session, employee)

        assert password == "mocked_password"

        session.commit()

    with get_session() as session:
        sql = select(Employee).where(
            Employee.email == SALES_ASSOCIATE_DATA["email"]
        )
        result = session.exec(sql).first()

        assert result.user[0].password == "mocked_password"
