"""Database models for the Dundie app."""

import json
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from dundie.utils.email import check_valid_email


class InvalidEmailError(Exception):
    """Custom exception for invalid email addresses."""

    ...


class Serializable(ABC):
    """Abstract base class for serializable objects."""

    @abstractmethod
    def to_dict(self) -> dict:
        """Return a dictionary representation of the object."""
        return vars(self)

    def to_json(self) -> str:
        """Return a JSON representation of the object."""
        return json.dumps(self.to_dict())


@dataclass
class Employees(Serializable):
    """Dataclass for employees."""

    email: str
    name: str
    department: str
    role: str

    def __post_init__(self):
        """Validate the email address."""
        if not check_valid_email(self.email):
            raise InvalidEmailError(f"Invalid email address: {self.email!r}")

    def __str__(self):
        """Return string representation of the employee."""
        return f"{self.name} - {self.role}"

    def to_dict(self) -> dict:
        """Return a dictionary representation of the employee."""
        return super().to_dict()  # Override to_dict method


@dataclass
class Balance(Serializable):
    """Dataclass for employee balance."""

    employee: Employees
    points: Decimal

    def to_dict(self):
        """Return a dictionary representation of the balance."""
        return {
            f"{employee.email}": str(self.points),
        }


@dataclass
class Transactions(Serializable):
    """Dataclass for transactions."""

    employee: Employees
    date: datetime
    points: Decimal
    description: str
    actor: str

    def to_dict(self):
        """Return a dictionary representation of the transaction."""
        return {
            "employee": self.employee.email,
            "date": self.date.isoformat(),
            "points": str(self.points),
            "description": self.description,
            "actor": self.actor,
        }


@dataclass
class Users(Serializable):
    """Dataclass for users."""

    employee: Employees
    password: str


if __name__ == "__main__":
    """Run this script to test the models."""
    employee = Employees(
        email="victor@email.com",
        name="Victor",
        department="IT",
        role="Developer",
    )

    print(employee)
    print(vars(employee))
    print(json.dumps(vars(employee)))
    print(employee.to_dict())
    print(employee.to_json())
    print()

    balance = Balance(employee=employee, points=Decimal(100))
    print(balance)
    print(vars(balance))
    # print(json.dumps(vars(balance)))
    print(balance.to_dict())
    print(balance.to_json())
    print()

    transaction = Transactions(
        employee=employee,
        date=datetime.now(),
        points=Decimal(10),
        description="Initial balance",
        actor="system",
    )
    print(transaction)
    print(vars(transaction))
    # print(json.dumps(vars(transaction)))
    print(transaction.to_dict())
    print(transaction.to_json())
