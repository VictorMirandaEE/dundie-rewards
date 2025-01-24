"""dundie load subcommand integration test"""

import pytest

from subprocess import CalledProcessError, check_output


@pytest.mark.integration
@pytest.mark.medium
def test_load_positive_call_load_command():
    """Test command load"""
    output = (
        check_output(["dundie", "load", "tests/assets/employees.csv"])
        .decode("utf-8")
        .split("\n")
    )
    assert len(output) == 2


def test2():
    """Test command load"""
    output = (
        check_output(["dundie", "load", "tests/assets/employees.csv"])
        .decode("utf-8")
        .split("\n")
    )
    assert len(output) == 2


@pytest.mark.integration
@pytest.mark.medium
@pytest.mark.parametrize("wrong_command", ["open", "start", "init"])
def test_load_negative_call_load_command_with_wrong_parameters(wrong_command):
    """Test command load"""
    with pytest.raises(CalledProcessError) as error_msg:
        check_output(
            ["dundie", wrong_command, "tests/assets/employees.csv"]
        ).decode("utf-8").split("\n")
    assert "status 2" in str(error_msg.getrepr())
