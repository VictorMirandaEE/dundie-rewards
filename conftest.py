"""Main place to adjust pytest settings and creating global fixtures."""

import pytest
from sqlmodel import create_engine

import dundie.utils.log as log
from dundie import models
from dundie.settings import log_file
from tests.constants import TEST_DATABASE_FILE, TEST_LOG_FILE

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
def _go_to_tmpdir(request):
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


@pytest.fixture(autouse=True)
def _setup_test_database(request, monkeypatch):
    """
    Fixture to set up a temporary test database for testing purposes.

    This fixture creates a temporary directory and a test database file within
    it. It then patches the `engine` in the `dundie.database` module to
    point to this test database file.

    Args:
      request (FixtureRequest): The request object for the fixture, used to
            get other fixtures.
      monkeypatch (MonkeyPatch): The monkeypatch fixture for dynamically
            modifying attributes.

    Yields:
      None
    """
    tmpdir = request.getfixturevalue("tmpdir")
    test_database = str(tmpdir.join(TEST_DATABASE_FILE))
    engine = create_engine(f"sqlite:///{test_database}")
    models.SQLModel.metadata.create_all(bind=engine)
    with monkeypatch.context() as m:
        m.setattr("dundie.database.engine", engine)
        yield


@pytest.fixture(autouse=True)
def _setup_test_logfile(request, monkeypatch):
    """
    Fixture to set up a temporary test log file for testing purposes.

    This fixture creates a temporary directory and a test log file within
    it. It then patches the `LOGFILE` in the `dundie.core` module to
    point to this test log file.

    Args:
      request (FixtureRequest): The request object for the fixture, used to
            get other fixtures.
      monkeypatch (MonkeyPatch): The monkeypatch fixture for dynamically
            modifying attributes.

    Yields:
      None
    """
    # FIXME: It is not changing the file name.
    tmpdir = request.getfixturevalue("tmpdir")
    test_log_file = str(tmpdir.join(TEST_LOG_FILE))
    print("test_log_file", test_log_file)
    with monkeypatch.context() as m:
        m.setattr(log, f"{log_file.name}", test_log_file)
        yield
