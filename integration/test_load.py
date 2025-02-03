"""dundie load subcommand integration test"""

import pytest
from click.testing import CliRunner

from dundie.cli import load, main

from .constants import EMPLOYEES_FILE

cmd = CliRunner()


@pytest.mark.integration
@pytest.mark.medium
def test_load_positive_call_load_command():
    """Test command load"""
    output = cmd.invoke(load, EMPLOYEES_FILE)
    assert "Dunder Mifflin Employees" in output.output


@pytest.mark.integration
@pytest.mark.medium
@pytest.mark.parametrize("wrong_command", ["open", "start", "init"])
def test_load_negative_call_load_command_with_wrong_parameters(wrong_command):
    """Test command load"""
    output = cmd.invoke(main, wrong_command, EMPLOYEES_FILE)
    assert output.exit_code != 0
    assert f"No such command '{wrong_command}'." in output.output
