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
    Test that the first employee's name in the loaded employee file starts
      with "Jim".
    Args:
        request: A fixture that provides information about the test function.
    Asserts:
        The first three characters of the first employee's name in the loaded
          employee file are "Jim".
    """
    assert load(EMPLOYEES_FILE)[0][:3] == "Jim"


@pytest.mark.unit
@pytest.mark.high
def test_load_positive_second_employee_name(request):
    """
    Test that the second employee's name in the loaded employee file starts
      with "Dwight".
    Args:
        request: A fixture that provides information about the test function.
    Asserts:
        The first 6 characters of the second employee's name in the loaded
          employee file are "Dwight".
    """
    assert load(EMPLOYEES_FILE)[1][:6] == "Dwight"
