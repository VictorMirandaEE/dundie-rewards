"""Database models for the Dundie app.

This module defines the database models for the Dundie app using SQLModel.
It includes models for Employee, Balance, Transaction, and User, along with
a helper class for validation.

Classes:
    SQLModelValidation: Helper class to allow for validation in SQLModel
        classes with table=True.
    Employee: Model representing an employee in the system.
    Balance: Model representing an employee's balance.
    Transaction: Model representing a financial transaction.
    User: Model representing a user in the system.

Usage:
    Run this script standalone to test the models and their relationships.
"""

from datetime import datetime
from decimal import Decimal

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel
from sqlmodel._compat import SQLModelConfig
from typing_extensions import Annotated, Optional

from dundie.utils.user import generate_simple_password


class SQLModelValidation(SQLModel):
    """Helper class to allow for validation in SQLModel classes with\
        table=True.

    This class is a workaround for the issue with SQLModel not validating
    attributes when using table=True.
    See: https://github.com/fastapi/sqlmodel/issues/52
    """

    model_config = SQLModelConfig(
        from_attributes=True, validate_assignment=True
    )


class Employee(SQLModelValidation, table=True):
    """
    Employee model representing an employee in the system.

    Attributes:
        id (Optional[int]): Unique identifier for the employee. Primary key.
        email (EmailStr): Email address of the employee. Must be unique and not
          nullable.
        name (str): Name of the employee. Not nullable.
        department (str): Department where the employee works. Not nullable and
          indexed.
        role (str): Role of the employee within the department. Not nullable.
        balance (list["Balance"]): List of balances associated with the
          employee.
        transaction (list["Transaction"]): List of transactions associated with
          the employee.
        user (list["User"]): List of users associated with the employee.
    """

    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    email: EmailStr = Field(unique=True, nullable=False, index=True)
    name: str = Field(nullable=False)
    department: str = Field(nullable=False, index=True)
    role: str = Field(nullable=False)
    currency: str = Field(
        nullable=False,
        sa_column_kwargs={
            "server_default": "USD",
        },
    )

    @property
    def superuser(self) -> bool:
        """Determine if the employee has superuser privileges based on their role.

        A superuser is identified by having a role that matches one of the predefined
        superuser roles, such as "Manager" or "Director".

        Returns:
            bool: True if the employee is a superuser, False otherwise.
        """
        # TODO: Implement as Field or RBAC (Role-Based Access Control) table
        superuser_roles = ["Manager", "Director"]
        return any(
            superuser_role in self.role for superuser_role in superuser_roles
        )

    balance: list["Balance"] = Relationship(back_populates="employee")
    transaction: list["Transaction"] = Relationship(back_populates="employee")
    user: list["User"] = Relationship(back_populates="employee")


class Balance(SQLModelValidation, table=True):
    """
    Dataclass for employee balance.

    Attributes:
        id (Optional[int]): The unique identifier for the balance record. It is
          the primary key and indexed.
        value (Decimal): The balance value for the employee. It is a required
          field with up to 3 decimal places.
        employee_id (int): The foreign key linking to the employee's ID. It
          must be unique.
        employee (Employee): The relationship to the Employee model, with
          back-population to the balance.
    """

    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    value: Annotated[Decimal, Field(nullable=False, decimal_places=3)]

    employee_id: int = Field(foreign_key="employee.id", unique=True)
    employee: Employee = Relationship(back_populates="balance")


class Transaction(SQLModelValidation, table=True):
    """
    Transaction model representing a financial transaction.

    Attributes:
        id (Optional[int]): Unique identifier for the transaction, primary key.
        value (Decimal): The monetary value of the transaction. Precision and
          scale need to be set.
        description (str): Description of the transaction.
        actor (str): The person or entity responsible for the transaction.
        date (datetime): The date and time when the transaction was created.
          Defaults to the current date and time.
        employee_id (int): Foreign key referencing the employee associated with
          the transaction.
        employee (Employee): Relationship to the Employee model, back-populated
          by the transaction.
    """

    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    value: Annotated[
        Decimal, Field(nullable=False)
    ]  # FIXME: Set decimal precision and scale
    description: str = Field(nullable=False)
    actor: str = Field(nullable=False, index=True)
    date: datetime = Field(default_factory=datetime.now)

    employee_id: int = Field(foreign_key="employee.id")
    employee: Employee = Relationship(back_populates="transaction")


class User(SQLModelValidation, table=True):
    """
    User model representing a user in the system.

    Attributes:
        id (Optional[int]): The unique identifier for the user. It is the
          primary key and indexed.
        password (str): The password for the user. It is generated using a
          default factory function.
        employee_id (int): The foreign key linking to the employee table. It is
          unique.
        employee (Employee): The relationship to the Employee model, with
          back_populates set to "user".
    """

    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    password: str = Field(
        nullable=False, default_factory=lambda: generate_simple_password()
    )

    employee_id: int = Field(foreign_key="employee.id", unique=True)
    employee: Employee = Relationship(back_populates="user")


if __name__ == "__main__":
    """Run this script to test it standalone."""

    import os

    from sqlmodel import Session, create_engine, select

    os.remove("/tmp/sql_model.db")

    engine = create_engine("sqlite:////tmp/sql_model.db", echo=False)

    SQLModel.metadata.create_all(bind=engine)

    with Session(engine) as session:
        employee = Employee(
            name="Victor",
            email="victor@email.com",
            department="IT",
            role="Developer",
        )
        session.add(employee)

        balance = Balance(employee=employee, value=333.0)
        session.add(balance)

        transaction = Transaction(
            employee=employee,
            value=Decimal(3000.0),
            description="Bonus",
            actor="system",
        )
        print(transaction.employee.id)
        session.add(transaction)

        user = User(employee=employee)
        session.add(user)

        sql = select(Employee)
        print(sql)
        print()
        employees = session.exec(sql)
        for _employee in employees:
            print(
                "Employee: ",
                _employee.name,
                "-",
                _employee.email,
                "-",
                _employee.department,
                "-",
                _employee.role,
                "-",
                _employee.balance[0].value,
            )
        print()

        sql2 = select(Balance)
        balances = session.exec(sql2)
        for _balance in balances:
            print("Balance: ", _balance.employee.name, "-", _balance.value)
        print()

        sql3 = select(Transaction)
        transactions = session.exec(sql3)
        for _transaction in transactions:
            print(
                "Transaction: ",
                _transaction.employee.name,
                "-",
                _transaction.date,
                "-",
                _transaction.value,
                "-",
                _transaction.description,
                "-",
                _transaction.actor,
            )
        print()

        sql4 = select(User)
        users = session.exec(sql4)
        for _user in users:
            print("User: ", _user.employee.name, "-", _user.password)
        print()

        sql5 = select(Employee, Balance).where(
            Employee.id == Balance.employee_id
        )
        employees5 = session.exec(sql5)
        for _employee5, _balance5 in employees5:
            print(
                "Employee & Balance (without JOIN): ",
                _employee5.name,
                "-",
                _balance5.value,
            )
        print()

        sql6 = select(Employee, Balance).join(Balance, isouter=True)
        employees6 = session.exec(sql6)
        for _employee6, _balance6 in employees6:
            print(
                "Employee & Balance (with JOIN): ",
                _employee6.name,
                "-",
                _balance6.value,
            )
        print()

        print("Employee Object: ")
        print(employee)
        print(employee.model_dump())
        print(employee.model_dump_json())
        print()

        print("Balance Object: ")
        print(balance)
        print(balance.model_dump())
        print(balance.model_dump_json())
        print()

        print("Transaction Object: ")
        print(transaction)
        print(transaction.model_dump())
        print(transaction.model_dump_json())
        print()

        print("User Object: ")
        print(user)
        print(user.model_dump())
        print(user.model_dump_json())
        print()

        session.commit()
        session.refresh(employee)
        session.refresh(balance)
        session.refresh(transaction)

    with Session(engine) as _session:
        newtransaction = Transaction(
            value=Decimal(33.0),
            description="Bonus extra",
            actor="victor",
            employee=employee,
        )
        session.add(newtransaction)
        session.commit()
