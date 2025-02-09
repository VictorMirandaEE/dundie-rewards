"""Core module of dundie.

This module contains the business logic for the Dundie application.
"""

import os
from csv import reader

from dundie.database import add_employee, add_transaction, commit, connect
from dundie.utils.log import get_logger

log = get_logger()


def load(filepath: str):
    """
    Load employee data from a CSV file, add employees to the database, and\
    return a list of employee records.

    Args:
        filepath (str): The path to the CSV file containing employee data.

    Returns:
        list: A list of dictionaries, each containing employee data including
          name, department, role, email, and creation status.

    Raises:
        FileNotFoundError: If the specified file does not exist.

    """
    try:
        with open(filepath) as file:
            csv_data = reader(file)
            db = connect()
            employees = []
            headers = ["name", "department", "role", "email"]
            for row in csv_data:
                employee_data = dict(
                    zip(headers, [item.strip() for item in row])
                )
                email = employee_data.pop("email")
                employee_data, created = add_employee(db, email, employee_data)

                return_data = employee_data.copy()
                return_data["email"] = email
                return_data["created"] = created
                employees.append(return_data)

            commit(db)
            return employees

    except FileNotFoundError as error_msg:
        log.error(str(error_msg))
        raise error_msg


def read(**query):
    """
    Read and filter employee data from the database based on the provided\
    query parameters.

    Keyword Args:
        email (str, optional): Filter by employee email.
        department (str, optional): Filter by employee department.

    Returns:
        list: A list of dictionaries containing employee data, including email,
          balance, last transaction date, and other employee details.
    """
    db = connect()
    return_data = []

    for email, data in db["employees"].items():
        if query.get("email") and query["email"] != email:
            continue
        if (
            query.get("department")
            and query["department"] != data["department"]
        ):
            continue

        return_data.append(
            {
                "email": email,
                "balance": db["balance"].get(email, 0),
                "last_transaction": db["transactions"][email][-1]["date"],
                **data,
            }
        )

    return return_data


def update(value: int, **query):
    """
    Update the balance of employees based on the given value and query\
    parameters.

    Args:
        value (int): The amount to update the balance by.
        **query: Arbitrary keyword arguments used to filter employees.

    Raises:
        RuntimeError: If no employees are found matching the query.

    Environment Variables:
        USER: The username of the person performing the update. Defaults to
          "system" if not set.

    The function performs the following steps:
        1. Reads employees based on the query parameters.
        2. Raises an error if no employees are found.
        3. Connects to the database.
        4. Updates the balance for each employee.
        5. Adds a transaction record for the update.
        6. Commits the changes to the database.
    """
    employees = read(**query)

    if not employees:
        raise RuntimeError("No employees found")

    db = connect()
    user = os.getenv("USER", "system")
    for employee in employees:
        email = employee["email"]
        new_balance = db["balance"].get(email, 0) + value
        db["balance"][email] = new_balance
        add_transaction(db, email, value, user, "Updated points")

    commit(db)
