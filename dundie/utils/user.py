"""User module for dundie"""

from random import sample
from string import ascii_letters, digits


def generate_simple_password(size=8) -> str:
    """
    Generates a simple password consisting of random letters and digits.

    Args:
        size (int): The length of the password to generate. Default is 8.

    Returns:
        str: A randomly generated password of the specified length.
    """

    password = "".join(sample(ascii_letters + digits, size))
    return password
