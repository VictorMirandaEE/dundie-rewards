"""Database module of dundie."""

from decimal import Decimal
from typing import Optional

from sqlmodel import Session, select

from dundie.models import Balance, Employee, Transaction, User
from dundie.settings import (
    DEFAULT_ACTOR,
    DEFAULT_ASSOCIATE_POINTS,
    DEFAULT_MANAGER_POINTS,
    EMAIL_FROM,
)
from dundie.utils.email import send_email
from dundie.utils.user import generate_password_hash


def add_employee(
    session: Session, employee: Employee, password: str | None = None
) -> tuple:
    """
    Add an employee to the database.

    This function adds an employee to the provided session if the email is
    valid and the employee does not already exist. If the employee is newly
    created, it sets the initial balance and password, and sends an email with
    the password.

    Args:
        session (Session): The database session to use for adding the employee.
        employee (Employee): The employee object to add.
        password (str | None, optional): The password to set for the employee.
          If None, an auto-generated random password will be used.

    Returns:
        tuple: A tuple containing the employee object and a boolean indicating
               whether the employee was created (True) or updated (False).

    Raises:
        ValueError: If the email address is invalid.
    """
    existing = session.exec(
        select(Employee).where(Employee.email == employee.email)
    ).first()

    created = existing is None

    if existing:
        existing.name = employee.name
        existing.department = employee.department
        existing.role = employee.role
        existing.currency = employee.currency
        session.add(existing)
    else:
        session.add(employee)
        set_initial_balance(session, employee)
        password = set_initial_password(session, employee, password)
        # TODO: Encrypt password and send link to reset it
        # TODO: Use queue to send email
        send_email(
            EMAIL_FROM,
            employee.email,
            "Your dundie password",
            f"Your password is: {password}",
        )

    return employee, created


def set_initial_balance(session: Session, employee: Employee) -> None:
    """
    Set the initial balance for an employee in the database.

    Args:
        session (Session): The database session to use for setting the balance.
        employee (Employee): The employee object for whom the balance is set.

    Returns:
        None
    """
    roles = ["Manager", "Director"]
    departments = ["Board", "Management"]
    value = (
        DEFAULT_MANAGER_POINTS
        if any(role in employee.role for role in roles)
        or any(department in employee.department for department in departments)
        else DEFAULT_ASSOCIATE_POINTS
    )
    add_transaction(session, employee, value, "Initial balance")


def add_transaction(
    session: Session,
    employee: Employee,
    value: Decimal,
    description: str,
    actor: Optional[str] = DEFAULT_ACTOR,
) -> None:
    """
    Add a transaction to the database for a given employee and update their\
    balance.

    Args:
        session (Session): The database session to use for adding the
          transaction.
        employee (Employee): The employee object for whom the transaction is
          added.
        value (Decimal): The value of the transaction to add.
        description (str): A description of the transaction.
        actor (Optional[str]): The actor responsible for the transaction.
          Defaults to DEFAULT_ACTOR.

    Returns:
        None
    """
    balance: Decimal

    transaction = Transaction(
        employee=employee,
        value=value,
        description=description,
        actor=actor,
    )
    session.add(transaction)
    session.commit()
    session.refresh(transaction)

    transactions = session.exec(
        select(Transaction).where(Transaction.employee == employee)
    )

    balance = Decimal(sum([row.value for row in transactions]))

    if not employee.balance:
        session.add(Balance(employee=employee, value=balance))
    else:
        employee.balance.value = balance
        session.add(employee)


def set_initial_password(
    session: Session, employee: Employee, password: str | None = None
) -> str:
    """Set the initial password for an employee in the database.

    Args:
        session (Session): The database session to use for setting the
          password.
        employee (Employee): The employee object for whom the password is set.
        password (str | None, optional): The password to set for the employee.
          If None, an auto-generated random password will be used.

    Returns:
        str: The password that was set for the employee.
    """
    user = User(employee=employee)

    if password is not None:
        user.password = password
    else:
        password = user.password

    user.password = generate_password_hash(password)

    session.add(user)

    return password
