"""Main place to adjust pytest settings and creating global fixtures."""

from unittest.mock import patch

import pytest

MARKER = """\
unit: Mark unit test
integration: Mark integration test
high: High priority
medium: Medium priority
low: Low priority
"""


def pytest_configure(config):
    """
    Configure pytest settings.

    This function is called to configure pytest settings before running tests.
    It reads marker definitions from the MARKER variable and adds them to
      the pytest configuration.
        config: The pytest configuration object.
    """
    for line in MARKER.split("\n"):
        config.addinivalue_line("markers", line)


@pytest.fixture(autouse=True)
def go_to_tmpdir(request):
    """
    Fixture to change the current working directory to a temporary directory\
    for the duration of a test.

    This fixture uses the `tmpdir` fixture provided by pytest to create
      a temporary directory.
    It then changes the current working directory to this temporary directory
      for the duration of the test.

    Args:
        request: A pytest fixture that provides information about
          the requesting test function.

    Yields:
        None: This fixture does not return any value. It only changes
          the working directory context.
    """
    tmpdir = request.getfixturevalue("tmpdir")
    with tmpdir.as_cwd():
        yield


@pytest.fixture(autouse=True, scope="function")
def setup_test_database(request):
    """
    Fixture to set up a temporary test database for testing purposes.

    This fixture creates a temporary directory and a test database file within
    it. It then patches the `DATABASE_PATH` in the `dundie.database` module to
    point to this test database file.

    Args:
      request (FixtureRequest): The request object for the fixture, used to
                    get other fixtures.

    Yields:
      None
    """
    tmpdir = request.getfixturevalue("tmpdir")
    test_database = str(tmpdir.join("test_database.json"))
    with patch("dundie.database.DATABASE_PATH", test_database):
        yield
