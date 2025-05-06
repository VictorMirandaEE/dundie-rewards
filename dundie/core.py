"""Core module of dundie.

This module contains the business logic for the Dundie application.
"""

from csv import DictReader
from csv import Error as CSVError
from decimal import Decimal
from typing import Any

from pydantic import ValidationError
from sqlmodel import select

from dundie.database import get_session
from dundie.models import Employee
from dundie.settings import DATE_FORMAT, Query, ResultDict
from dundie.utils.authentication import require_authentication
from dundie.utils.db import add_employee, add_transaction
from dundie.utils.exchange import get_exchange_rates
from dundie.utils.log import get_logger


def loc_to_dot_sep(loc: tuple[str | int, ...]) -> str:
    """
    Convert a tuple of strings and integers to a dot-separated string.

    Args:
        loc (tuple[str | int, ...]): A tuple containing strings and integers.

    Returns:
        str: A string where each string element in the tuple is separated by a
             dot, and each integer element is enclosed in square brackets.

    Raises:
        TypeError: If an element in the tuple is neither a string nor an
          integer.

    Example:
        >>> loc_to_dot_sep(('a', 'b', 1, 'c', 2))
        'a.b[1].c[2]'
    """
    path = ""
    for i, x in enumerate(loc):
        if isinstance(x, str):
            if i > 0:
                path += "."
            path += x
        elif isinstance(x, int):
            path += f"[{x}]"
        else:
            raise TypeError("Unexpected type")
    return path


def convert_errors(e: ValidationError) -> list[dict[str, Any]]:
    """
    Convert Pydantic validation errors to a list of dictionaries.

    Args:
        e (ValidationError): The Pydantic ValidationError instance containing
          the errors.

    Returns:
        list[dict[str, Any]]: A list of dictionaries where each dictionary
            represents an error. The 'loc' key in each dictionary is converted
            to a dot-separated string.
    """
    new_errors: list[dict[str, Any]] = e.errors()  # type: ignore
    for error in new_errors:
        error["loc"] = loc_to_dot_sep(error["loc"])
    return new_errors


def load(filepath: str) -> ResultDict:
    """
    Load employee data from a CSV file, add employees to the database, and\
    return a list of employee records.

    Args:
        filepath (str): The path to the CSV file containing employee data.

    Returns:
        list[dict[str, Any]]: A list of dictionaries, each containing employee
          data including name, department, role, email, and creation status.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        CSVError: If there is an error reading the CSV file.
        ValidationError: If there is an error validating the employee data.
    """
    employees = []

    log = get_logger()

    try:
        csv_data = DictReader(
            open(filepath), strict=True, dialect="unix", skipinitialspace=True
        )

        csv_data_list = list(csv_data)

        if not csv_data_list:
            log.error(f"Empty CSV file provided {filepath!r}")
            return []

        with get_session() as session:
            for employee_data in csv_data_list:
                employee = Employee(**employee_data)
                _, created = add_employee(session, employee)
                return_data = employee_data.copy()
                return_data["created"] = created
                employees.append(return_data)

            session.commit()

    except FileNotFoundError as exception_msg:
        log.error(f"FileNotFoundError: {exception_msg}")
        pass
    except CSVError as exception_msg:
        log.error(f"CSVError: {exception_msg}")
        pass
    except ValidationError as error:
        pretty_errors = convert_errors(error)
        error_msg = f"""\
Employee {employee_data!r} has an invalid email {pretty_errors[0]["input"]!r}:\
 [ValidationError] {pretty_errors[0]["ctx"]["reason"]}
"""
        log.error(error_msg)
        pass

    return employees


def read(**query: Query) -> ResultDict:
    """
    Read and filter employee data from the database based on the provided\
    query parameters.

    Keyword Args:
        email (str, optional): Filter by employee email.
        department (str, optional): Filter by employee department.

    Returns:
        list[dict[str, Any]]: A list of dictionaries containing employee data,
            including name, email, role, department, balance, and last
            transaction date.
    """
    return_data = []

    sql_statement = []
    if query.get("department"):
        sql_statement.append(Employee.department == query["department"])
    if query.get("email"):
        sql_statement.append(Employee.email == query["email"])

    sql = select(Employee)
    if sql_statement:
        sql = sql.where(*sql_statement)

    with get_session() as session:
        currencies = session.exec(select(Employee.currency).distinct())
        exchange_rates = get_exchange_rates(list(currencies))

        results = session.exec(sql)
        for employee in results:
            total = (
                exchange_rates[employee.currency].value
                * employee.balance.value
            )

            return_data.append(
                {
                    "name": employee.name,
                    "email": employee.email,
                    "role": employee.role,
                    "department": employee.department,
                    "balance": employee.balance.value,
                    "currency": employee.currency,
                    "total": total,
                    "last_transaction": employee.transaction[-1].date.strftime(
                        DATE_FORMAT
                    ),
                }
            )

    return return_data


@require_authentication
def update(value: Decimal, from_employee: Employee, **query: Query) -> str:
    """
    Update the balance of employees based on the given value and query\
    parameters.

    This function retrieves employees matching the provided query parameters,
    updates their balance by the specified value, and logs the transaction. If
    no employees are found, or if an employee is not present in the database,
    appropriate messages are returned. Additionally, it ensures that the
    initiating employee has sufficient funds or superuser privileges to
    perform the operation.

    Args:
        value (Decimal): The amount to update the balance by.
        from_employee (Employee): The employee initiating the update.
        **query: Arbitrary keyword arguments used to filter employees.

    Returns:
        str: A message indicating the result of the operation. If no employees
        are found, or if an employee is missing in the database, a descriptive
        message is returned. Otherwise, an empty string is returned.
    """
    result = ""

    employees = read(**query)

    if not employees:
        result = "No employees found"
        return result

    total = len(employees) * value

    if from_employee.balance.value < total and not from_employee.superuser:
        result = f"Insufficient funds to transfer {total}"
        return result

    with get_session() as session:
        for employee in employees:
            if employee["email"] == from_employee.email:
                continue

            email = employee["email"]
            instance = session.exec(
                select(Employee).where(Employee.email == email)
            ).first()
            if instance:
                add_transaction(
                    session,
                    instance,
                    value,
                    "Updated points",
                    from_employee.email,
                )
            else:
                result = f"Employee {email!r} not found in the database"
                return result

            if not from_employee.superuser:
                instance = session.exec(
                    select(Employee).where(
                        Employee.email == from_employee.email
                    )
                ).first()
                if instance:
                    add_transaction(
                        session,
                        instance,
                        -value,
                        "Updated points",
                        from_employee.email,
                    )
                else:
                    result = f"Employee {from_employee.email!r}\
                          not found in the database"
                    return result

        session.commit()

    return result
