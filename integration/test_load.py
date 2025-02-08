"""dundie load subcommand integration test"""

import pytest
from click.testing import CliRunner

from dundie.cli import load, main

from .constants import EMPLOYEES_FILE


@pytest.fixture
def runner():
    return CliRunner()


@pytest.mark.integration
@pytest.mark.medium
def test_positive_load_command(runner):
    """
    Test the 'load' command with a positive scenario.
    This test uses the 'runner' fixture to invoke the 'load' command with the
    EMPLOYEES_FILE argument. It verifies that the command exits with a status
    code of 0 and that the output contains the expected table headers.
    Args:
        runner (CliRunner): A Click CliRunner instance used to invoke CLI
          commands.
    """

    result = runner.invoke(load, EMPLOYEES_FILE)

    # Check that the command exits with a status code of 0
    assert result.exit_code == 0

    # Check that the output contains the expected table headers
    assert "Dunder Mifflin Employees" in result.output


@pytest.mark.integration
@pytest.mark.medium
@pytest.mark.parametrize("wrong_command", ["open", "start", "init"])
def test_negative_wrong_command(runner, wrong_command):
    """
    Test that invoking the main function with a wrong command results in an
      error.

    Args:
        runner (CliRunner): The Click CLI runner used to invoke commands.
        wrong_command (str): The incorrect command to test.
    """

    output = runner.invoke(main, [wrong_command, EMPLOYEES_FILE])

    assert output.exit_code != 0

    assert f"No such command '{wrong_command}'." in output.output
