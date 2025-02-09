"""dundie show subcommand integration test."""

import json

import pytest
from click.testing import CliRunner

from dundie.cli import load, main, show

from .constants import EMPLOYEES_FILE


@pytest.fixture
def runner():
    """
    Create and return a new instance of CliRunner.

    Returns:
        CliRunner: An instance of the CliRunner class.
    """
    return CliRunner()


@pytest.mark.integration
@pytest.mark.medium
def test_positive_show_with_no_results(runner):
    """
    Test the 'show' command when there are no results.

    This test uses the runner to invoke the 'show' command and verifies that:
    1. The command exits with a status code of 0.
    2. The output contains the message "No results found".

    Args:
        runner: A CliRunner instance used to invoke the command.
    """
    result = runner.invoke(show)

    # Check that the command exits with a status code of 0
    assert result.exit_code == 0

    # Check that the output contains the expected table headers
    assert "No results found" in result.output


@pytest.mark.integration
@pytest.mark.medium
def test_positive_show_without_option(runner):
    """
    Test the 'show' command without any options.

    This test ensures that the 'show' command can be called successfully
      without any additional options.
    It verifies that the command exits with a status code of 0 and that the
      output contains the expected table headers.
    Args:
        runner: A Click testing runner instance used to invoke commands.
    Steps:
        1. Load the employees file using the 'load' command.
        2. Invoke the 'show' command.
        3. Assert that the command exits with a status code of 0.
        4. Assert that the output contains the expected table headers.
    """
    runner.invoke(load, EMPLOYEES_FILE)

    result = runner.invoke(show)

    # Check that the command exits with a status code of 0
    assert result.exit_code == 0

    # Check that the output contains the expected table headers
    assert "Dunder Mifflin Rewards Report" in result.output


def test_positive_show_filter_email(runner):
    """
    Test the 'show' command with an email filter.

    This test ensures that the 'show' command correctly filters results
    based on the provided email address. It first loads the employee data
    using the 'load' command, then invokes the 'show' command with the
    specified email filter. The test asserts that the command exits
    successfully and that the output contains the expected email address.
    Args:
        runner: A CliRunner instance used to invoke CLI commands.
    """
    runner.invoke(load, EMPLOYEES_FILE)
    result = runner.invoke(main, ["show", "--email", "jim@dundermifflin.com"])
    assert result.exit_code == 0
    assert "jim@dundermifflin.com" in result.output


def test_positive_show_filter_department(runner):
    """
    Test the 'show' command with a department filter.

    This test ensures that the 'show' command correctly filters employees
    by the specified department. It first loads the employee data from the
    EMPLOYEES_FILE and then invokes the 'show' command with the '--department'
    option set to "Sales". The test verifies that the command exits with a
    status code of 0 and that the output contains the string "Sales".
    Args:
        runner: A Click testing runner instance used to invoke commands.
    """
    runner.invoke(load, EMPLOYEES_FILE)
    result = runner.invoke(main, ["show", "--department", "Sales"])
    assert result.exit_code == 0
    assert "Sales" in result.output


def test_positive_show_format_txt(runner):
    """
    Test the 'show' command with TXT format.

    This test ensures that the 'show' command, when invoked with the
    '--format txt' option, produces the expected output in TXT format. It
    first loads the employee data using the 'load' command and then checks the
    following:
    - The command exits with a status code of 0.
    - The output contains the header "Dunder Mifflin Rewards Report".
    - The output includes the columns "Email" and "Department".
    """
    runner.invoke(load, EMPLOYEES_FILE)
    result = runner.invoke(main, ["show", "--format", "txt"])
    assert result.exit_code == 0
    assert "Dunder Mifflin Rewards Report" in result.output
    assert "Email" in result.output
    assert "Department" in result.output


def test_positive_show_format_json(runner):
    """
    Test the 'show' command with JSON format.

    This test ensures that the 'show' command outputs the correct JSON format
    when invoked. It first loads the employee data using the 'load' command,
    then invokes the 'show' command with the '--format json' option. The test
    checks that the command exits with a status code of 0, the output is a
    JSON-formatted list, the list is not empty, and the first item in the list
    contains the keys 'email' and 'department'.
    Args:
        runner: A CliRunner instance to invoke CLI commands.
    Raises:
        AssertionError: If any of the assertions fail.
    """
    runner.invoke(load, EMPLOYEES_FILE)
    result = runner.invoke(main, ["show", "--format", "json"])
    assert result.exit_code == 0
    content = json.loads(result.output)
    assert isinstance(content, list)
    assert len(content) > 0
    assert "email" in content[0]
    assert "department" in content[0]


def test_positive_show_output_to_file_format_txt(runner, tmp_path):
    """
    Test the 'show' command with output to a file in TXT format.

    This test ensures that the 'show' command generates the correct output
    when the results are written to a file in TXT format. It verifies that
    the command executes successfully and that the output file contains the
    expected headers and content.
    Args:
        runner: A CliRunner instance to invoke the command.
        tmp_path: A temporary directory path provided by pytest.
    Assertions:
        - The command exits with a status code of 0.
        - The output file contains the "Dunder Mifflin Rewards Report" header.
        - The output file contains the "Email" header.
        - The output file contains the "Department" header.
    """
    runner.invoke(load, EMPLOYEES_FILE)
    file_path = tmp_path / "output.txt"
    result = runner.invoke(
        main, ["show", "--file", file_path, "--format", "txt"]
    )
    assert result.exit_code == 0
    with open(file_path) as f:
        content = f.read()
    assert "Dunder Mifflin Rewards Report" in content
    assert "Email" in content
    assert "Department" in content


def test_positive_show_output_to_file_format_json(runner, tmp_path):
    """
    Test the 'show' command with JSON output format.

    This test ensures that the 'show' command correctly outputs data to a file
    in JSON format. It performs the following steps:
    1. Invokes the 'load' command to load employee data.
    2. Invokes the 'show' command with the '--file' and '--format' options to
        generate a JSON file.
    3. Asserts that the command exits with a status code of 0 (success).
    4. Reads the generated JSON file and verifies its content:
        - The content is a list.
        - The list is not empty.
        - Each item in the list contains 'email' and 'department' keys.
    """
    runner.invoke(load, EMPLOYEES_FILE)
    file_path = tmp_path / "output.json"
    result = runner.invoke(
        main, ["show", "--file", file_path, "--format", "json"]
    )
    assert result.exit_code == 0
    with open(file_path) as f:
        content = json.load(f)
    assert isinstance(content, list)
    assert len(content) > 0
    assert "email" in content[0]
    assert "department" in content[0]
