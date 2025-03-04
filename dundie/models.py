"""Database models for the Dundie app."""

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, EmailStr, field_validator


class Employees(BaseModel):
    """Dataclass for employees."""

    email: EmailStr
    name: str
    department: str
    role: str

    def __str__(self):
        """Return string representation of the employee."""
        return f"{self.name} - {self.role}"


class Balance(BaseModel):
    """Dataclass for employee balance."""

    employee: Employees
    points: Decimal

    @field_validator("points", mode="before")
    @classmethod
    def points_logic(cls, points: Decimal) -> Decimal:
        """Validate points."""
        return points * 2

    model_config = ConfigDict(
        json_encoders={Employees: lambda employee: employee.name}
    )


class Transactions(BaseModel):
    """Dataclass for transactions."""

    employee: Employees
    date: datetime
    points: Decimal
    description: str
    actor: str


class Users(BaseModel):
    """Dataclass for users."""

    employee: Employees
    password: str


if __name__ == "__main__":
    """Run this script to test it standalone."""
    employee = Employees(
        email="victor@email.com",
        name="Victor",
        department="IT",
        role="Developer",
    )

    print(employee)
    print(employee.model_dump())
    print(employee.model_dump_json())
    print()

    balance = Balance(employee=employee, points=Decimal(100))
    print(balance)
    print(balance.model_dump())
    print(balance.model_dump_json())
    print()

    transaction = Transactions(
        employee=employee,
        date=datetime.now(),
        points=Decimal(10),
        description="Initial balance",
        actor="system",
    )
    print(transaction)
    print(transaction.model_dump())
    print(transaction.model_dump_json())
    print()
