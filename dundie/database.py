"""Database module of dundie."""

import json
from datetime import datetime

from dundie.settings import (
    DATABASE_PATH,
    DEFAULT_ASSOCIATE_POINTS,
    DEFAULT_MANAGER_POINTS,
    EMAIL_FROM,
)
from dundie.utils.email import check_valid_email, send_email
from dundie.utils.user import generate_simple_password

DATABASE_SCHEMA = {
    "employees": {},
    "balance": {},
    "transactions": {},
    "users": {},
}


def connect() -> dict:
    """
    Connect to the database and returns its contents as a dictionary.

    This function attempts to open and read the database file specified by
    the DATABASE_PATH variable. If the file is successfully read and its
    contents are valid JSON, the function returns the parsed JSON data as
    a dictionary. If the file is not found or the contents are not valid
    JSON, the function returns the default database schema defined by the
    DATABASE_SCHEMA variable.

    Returns:
        dict: The contents of the database as a dictionary, or the default
        database schema if the file is not found or contains invalid JSON.
    """
    try:
        with open(DATABASE_PATH, "r") as database_file:
            return json.loads(database_file.read())
    except (json.JSONDecodeError, FileNotFoundError):
        return DATABASE_SCHEMA


def commit(database: dict) -> None:
    """
    Commit the given database dictionary to a file.

    This function checks if the provided database dictionary matches the
    expected database schema. If the schema is valid, it writes the database
    to a file in JSON format. If the schema is invalid, it raises a
    RuntimeError.

    Args:
        database (dict): The database dictionary to be committed.

    Raises:
        RuntimeError: If the database schema is invalid.
        Exception: If there is an error writing to the file.
    """
    if database.keys() != DATABASE_SCHEMA.keys():
        raise RuntimeError("Invalid database schema")
    try:
        with open(DATABASE_PATH, "w") as database_file:
            database_file.write(json.dumps(database, indent=4))
    except Exception as error:
        raise error


def add_employee(database: dict, email: str, data: dict) -> tuple:
    """
    Add an employee to the database.

    This function adds an employee to the provided database if the email is
    valid and the employee does not already exist. If the employee is newly
    created, it sets the initial balance and password, and sends an email with
    the password.

    Args:
        database (dict): The database containing employee information.
        email (str): The email address of the employee.
        data (dict): Additional data for the employee.

    Returns:
        tuple: A tuple containing the employee data and a boolean indicating
               whether the employee was created (True) or updated (False).

    Raises:
        ValueError: If the email address is invalid.
    """
    if not check_valid_email(email):
        raise ValueError(f"Invalid email address: {email}")
    # Email is unique is resolved by dictionary hash table
    # if email in database["employees"]:
    #     raise ValueError("Employee already exists")
    employees = database["employees"]
    employee = employees.get(email, {})
    created = not bool(employee)
    employee.update(data)
    employees[email] = employee
    if created:
        set_initial_balance(database, email, employee)
        password = set_initial_password(database, email)
        # TODO: Encrypt password and send link to reset it
        send_email(
            EMAIL_FROM,
            [email],
            "Your dundie password",
            f"Your password is: {password}",
        )
    return employee, created


def set_initial_balance(database: dict, email: str, employee: dict) -> None:
    """
    Set the initial balance for an employee in the database.

    Args:
        database (dict): The database where the employee's balance is stored.
        email (str): The email of the employee.
        employee (dict): A dictionary containing employee details, including
          their role.

    Returns:
        None
    """
    roles = ["Manager", "Director"]
    points = (
        DEFAULT_MANAGER_POINTS
        if any(role in employee["role"] for role in roles)
        else DEFAULT_ASSOCIATE_POINTS
    )
    add_transaction(database, email, points, "Initial balance")


def add_transaction(
    database: dict,
    email: str,
    points: int,
    description: str,
    actor: str = "system",
) -> None:
    """
    Add a transaction to the database for a given user and update their\
    balance.

    Args:
        database (dict): The database containing transactions and balances.
        email (str): The email of the user to add the transaction for.
        points (int): The number of points to add or subtract.
        description (str): A description of the transaction.
        actor (str, optional): The actor responsible for the transaction.
        Defaults to "system".
    Returns:
        None
    """
    transactions = database["transactions"].setdefault(email, [])
    transactions.append(
        {
            "date": datetime.now().isoformat(),
            "points": points,
            "description": description,
            "actor": actor,
        }
    )
    database["balance"][email] = sum(
        transaction["points"] for transaction in transactions
    )


def set_initial_password(database: dict, email: str) -> str:
    """
    Set the initial password for an employee in the database.

    Args:
        database (dict): The database where the employee's password is stored.
        email (str): The email of the employee.
    Returns:
        str: The password that was set for the employee.
    """
    employee = database["users"].setdefault(email, {})
    password = generate_simple_password()
    employee["password"] = password
    return password
