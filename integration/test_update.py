"""dundie update subcommand integration test."""

import pytest
from click.testing import CliRunner

from dundie.cli import load, update
from integration.constants import EMPLOYEES_FILE


@pytest.fixture
def runner():
    """
    Create and return a new instance of CliRunner.

    Returns:
        CliRunner: An instance of the CliRunner class.
    """
    return CliRunner()


def test_positive_update_add_points_all_employees(runner):
    """
    Test the update functionality to add points to all employees.

    This test performs the following steps:
    1. Invokes the `load` command with the `EMPLOYEES_FILE`.
    2. Invokes the `update` command with the argument "10".
    3. Asserts that the exit code of the `update` command is 0.
    4. Asserts that the output of the `update` command contains "510".
    5. Asserts that the output of the `update` command contains "110".

    Args:
        runner: The test runner instance used to invoke commands.
    """
    runner.invoke(load, EMPLOYEES_FILE)

    result = runner.invoke(update, "10")

    assert result.exit_code == 0
    assert "510" in result.output
    assert "110" in result.output


def test_positive_update_subtract_points_all_employees(runner):
    """
    Test the update functionality to subtract points from all employees.

    This test performs the following steps:
    1. Invokes the `load` command with the `EMPLOYEES_FILE`.
    2. Invokes the `update` command with the argument "-10".
    3. Asserts that the exit code of the `update` command is 0.
    4. Asserts that the output of the `update` command contains "490".
    5. Asserts that the output of the `update` command contains "90".

    Args:
        runner: The test runner instance used to invoke commands.
    """
    runner.invoke(load, EMPLOYEES_FILE)

    result = runner.invoke(update, "-- -10")

    assert result.exit_code == 0
    assert "490" in result.output
    assert "90" in result.output


def test_positive_update_add_points_filter_email(runner):
    """
    Test the update command to add points to a user filtered by email.

    This test performs the following steps:
    1. Loads the employee data from the EMPLOYEES_FILE.
    2. Invokes the update command to add 10 points to the user with the
      specified email.
    3. Asserts that the command exits with a code of 0 (success).
    4. Asserts that the updated points (510) are present in the output.
    5. Asserts that the incorrect points (110) are not present in the output.
    6. Asserts that the specified email is present in the output.

    Args:
        runner: The CliRunner instance used to invoke commands.
    """
    runner.invoke(load, EMPLOYEES_FILE)

    email = "jim@dundermifflin.com"
    result = runner.invoke(update, ["10", "--email", email])

    assert result.exit_code == 0
    assert "510" in result.output
    assert "110" not in result.output
    assert email in result.output


def test_positive_update_subtract_points_filter_email(runner):
    """
    Test the update command to subtract points from a user filtered by email.

    This test performs the following steps:
    1. Loads the employee data from the EMPLOYEES_FILE.
    2. Invokes the update command to subtract 10 points from the user with the
      specified email.
    3. Asserts that the command exits with a code of 0 (success).
    4. Asserts that the updated points (490) are present in the output.
    5. Asserts that the incorrect points (90) are not present in the output.
    6. Asserts that the specified email is present in the output.

    Args:
        runner: The CliRunner instance used to invoke commands.
    """
    runner.invoke(load, EMPLOYEES_FILE)

    email = "jim@dundermifflin.com"
    result = runner.invoke(update, ["--email", email, "--", "-10"])

    assert result.exit_code == 0
    assert "490" in result.output
    assert email in result.output


def test_positive_update_add_points_filter_department(runner):
    """
    Test the update command to add points to employees filtered by department.

    This test performs the following steps:
    1. Loads the employee data from the EMPLOYEES_FILE.
    2. Invokes the update command to add 10 points to employees in the "Sales"
      department.
    3. Asserts that the command exits with a code of 0 (success).
    4. Asserts that the output contains the updated points for employees in the
      "Sales" department.
    5. Asserts that the output contains the department name "Sales".

    Args:
        runner (CliRunner): The CLI runner used to invoke commands.
    """
    runner.invoke(load, EMPLOYEES_FILE)

    department = "Sales"
    result = runner.invoke(update, ["10", "--department", department])

    assert result.exit_code == 0
    assert "510" in result.output
    assert "110" in result.output
    assert department in result.output


def test_positive_update_subtract_points_filter_department(runner):
    """
    Test the update command to subtract points from employees filtered by\
    department.

    This test performs the following steps:
    1. Loads the employee data from the EMPLOYEES_FILE.
    2. Invokes the update command to subtract 10 points from employees in the
      "Sales" department.
    3. Asserts that the command exits with a code of 0 (success).
    4. Asserts that the output contains the updated points for employees in the
      "Sales" department.
    5. Asserts that the output contains the department name "Sales".

    Args:
        runner (CliRunner): The CLI runner used to invoke commands.
    """
    runner.invoke(load, EMPLOYEES_FILE)

    department = "Sales"
    result = runner.invoke(update, ["--department", department, "--", "-10"])

    assert result.exit_code == 0
    assert "490" in result.output
    assert "90" in result.output
    assert department in result.output
