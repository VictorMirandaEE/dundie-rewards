"""User module for dundie."""

from random import sample
from string import ascii_letters, digits

from pwdlib import PasswordHash
from pwdlib.exceptions import UnknownHashError

password_hash_instance = PasswordHash.recommended()


def generate_password_hash(password_plain: str) -> str:
    """
    Generate a hashed password using the PasswordHash instance.

    Args:
        password_plain (str): The plain text password to hash.

    Returns:
        str: The hashed password as a string.
    """
    global password_hash_instance
    return password_hash_instance.hash(password=password_plain)


def verify_password(password_plain: str, password_hash: str) -> bool:
    """Verify if a plain text password matches a hashed password.

    Args:
        password_plain (str): The plain text password to verify.
        password_hash (str): The hashed password to compare against.

    Returns:
        bool: True if the plain text password matches the hashed password,
              False otherwise.
    """
    global password_hash_instance

    try:
        result = password_hash_instance.verify(
            password=password_plain, hash=password_hash
        )
    except UnknownHashError:
        # If the hash is not valid, return False
        return False

    return result


def generate_simple_password(size: int = 8) -> str:
    """
    Generate a simple password consisting of random letters and digits.

    Args:
        size (int): The length of the password to generate. Default is 8.
          Minimum is 1. Maximum is 62.

    Returns:
        str: A randomly generated password of the specified length.
    """
    if size < 1:
        size = 8
    elif size > 62:
        size = 62

    password = "".join(sample(ascii_letters + digits, size))
    return password
