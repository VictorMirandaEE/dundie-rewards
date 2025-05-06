"""Security module for dundie."""

import os
from functools import wraps
from typing import Any, Callable

from sqlalchemy.orm import selectinload
from sqlmodel import select

from dundie.database import get_session
from dundie.models import Employee
from dundie.utils.user import verify_password


class AuthenticationError(Exception):
    """Custom exception for authentication errors."""

    pass


def require_authentication(func: Callable) -> Callable:
    """Implement decorator to enforce authentication for a function.

    This decorator ensures that the function it wraps can only be executed
    if valid authentication credentials are provided via environment variables.
    It retrieves the employee's email and password from the environment,
    verifies the credentials against the database, and injects the authenticated
    employee object into the wrapped function as a keyword argument.

    Args:
        func (Callable): The function to be wrapped by the decorator.

    Returns:
        Callable: The wrapped function with authentication enforced.

    Raises:
        AuthenticationError: If the required environment variables are not set,
            if the employee is not found in the database, or if the password is
            invalid.
    """

    @wraps(func)
    def decorator(*args: Any, **kwargs: Any) -> Any:
        """Implement decorator to require authentication for a function."""
        email = os.getenv("EMPLOYEE_EMAIL")
        password = os.getenv("EMPLOYEE_PASSWORD")

        if not all([email, password]):
            raise AuthenticationError(
                "Variables EMPLOYEE_EMAIL and EMPLOYEE_PASSWORD are undefined."
            )

        with get_session() as session:
            employee = session.exec(
                select(Employee)
                .options(
                    selectinload(Employee.balance),  # type: ignore
                    selectinload(Employee.transaction),  # type: ignore
                    selectinload(Employee.user),  # type: ignore
                )
                .where(Employee.email == email)
            ).first()

            if not employee:
                raise AuthenticationError(
                    f"Employee with email {email!r} not found."
                )

            if password is not None and not verify_password(
                password, employee.user.password
            ):
                raise AuthenticationError("Invalid password.")

        # Dependency injection
        return func(*args, from_employee=employee, **kwargs)

    return decorator
