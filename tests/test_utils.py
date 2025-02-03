"""dundie utils unit test"""

import pytest

from dundie.utils.email import check_valid_email
from dundie.utils.user import generate_simple_password


@pytest.mark.unit
@pytest.mark.parametrize(
    "valid_email",
    [
        "alice@example.com",
        "bob.smith@example.co.uk",
        "charlie123@example.org",
        "david_jones@example.net",
        "eve-adams@example.io",
        "frank@example.edu",
        "george@example.com",
        "hannah@example.com",
        "ian@example.com",
        "julia@example.com",
    ],
)
def test_positive_check_valid_email(valid_email):
    """
    Test that the check_valid_email function correctly identifies a valid email
      address.
    Asserts:
        The check_valid_email function returns True for a valid email address.
    """
    assert check_valid_email(valid_email) is True


@pytest.mark.unit
@pytest.mark.parametrize(
    "invalid_email",
    [
        "alice.example.com",
        "bob.smith@.co.uk",
        "charlie123@.org",
        "david_jones@example",
        "eve-adams@.io",
        "frank@.edu",
        "george@com",
        "@example.com",
        "hannah@example..com",
        "ian@.com",
        "julia@com",
    ],
)
def test_negative_check_valid_email(invalid_email):
    """
    Test that the check_valid_email function correctly identifies an invalid
      email address.
    Asserts:
      The check_valid_email function returns False for an invalid email
        address.
    """
    assert check_valid_email(invalid_email) is False


@pytest.mark.unit
def test_positive_generate_simple_password():
    """
    Test that the generate_simple_password function generates a password of the
      correct length.
    Asserts:
        The generated password is of the correct length.
    """
    # TODO: Generate hashed complex password with encryption
    passwords = []
    for _ in range(100):
        password = generate_simple_password(8)
        passwords.append(password)

    assert len(set(passwords)) == 100  # Conversion to set removes duplicates
