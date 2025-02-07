"""dundie load subcommand unit test"""

import pytest

from dundie.core import load

from .constants import EMPLOYEES_FILE


@pytest.mark.unit
@pytest.mark.high
def test_load_positive_has_2_employees(request):
    """
    Test that the load function correctly loads and returns 2 employees from
      the EMPLOYEES_FILE.
    Args:
        request: A pytest fixture that provides information about the test
          execution.
    Asserts:
        The length of the list returned by the load function is 2.
    """
    assert len(load(EMPLOYEES_FILE)) == 3


@pytest.mark.unit
@pytest.mark.high
def test_load_positive_first_employee_name(request):
    """
    Test that the first employee's name in the loaded employee file is
      "Jim Halpert".
    Args:
        request: A fixture that provides information about the test function.
    Asserts:
        The first employee's name in the loaded employee file is "Jim Halpert".
    """
    assert load(EMPLOYEES_FILE)[0]["name"] == "Jim Halpert"


@pytest.mark.unit
@pytest.mark.high
def test_load_positive_second_employee_name(request):
    """
    Test that the second employee's name in the loaded employee file is
      "Dwight Schrute".
    Args:
        request: A fixture that provides information about the test function.
    Asserts:
        The second employee's name in the loaded employee file is
          "Dwight Schrute".
    """
    assert load(EMPLOYEES_FILE)[1]["name"] == "Dwight Schrute"


@pytest.mark.unit
@pytest.mark.high
def test_load_positive_third_employee_name(request):
    """
    Test that the third employee's name in the loaded employee file is
      "Gabe Lewis".
    Args:
        request: A fixture that provides information about the test function.
    Asserts:
        The third employee's name in the loaded employee file is
          "Gabe Lewis".
    """
    assert load(EMPLOYEES_FILE)[2]["name"] == "Gabe Lewis"
