"""dundie load subcommand unit test"""

import os
import uuid
import pytest
from dundie.core import load
from .constants import EMPLOYEES_FILE


def setup_module():
    """
    This functions runs once before any tests in the module are executed.
    It is typically used to perform any necessary setup or initialization
    that is required for the tests in the module.
    """
    print()
    print("setup_module called\n")


def teardown_module():
    """
    This function runs once after all the tests in the module have been executed.
    It is typically used to clean up any resources or perform any necessary
    teardown operations after the tests have run.
    """
    print()
    print("teardown_module called\n")


@pytest.fixture(scope="function", autouse=True)
def create_new_file(tmpdir):
    """
    Create a temporary file for each test.
    This function creates a new temporary file in the given temporary directory.
    After the test is done, the file is removed.
    Args:
        tmpdir: A temporary directory provided by the pytest fixture.
    Yields:
        None
    """
    file = tmpdir.join("dummy2.txt")
    file.write("This is another dummy file")
    yield
    file.remove()


@pytest.mark.unit
@pytest.mark.high
def test_load(request):
    """
    Test the load function to ensure it correctly reads and processes the EMPLOYEES_FILE.
    This test creates a dummy file to simulate the loading process and verifies:
    1. The length of the loaded data is 2.
    2. The first entry in the loaded data starts with "Jim".
    3. The second entry in the loaded data starts with "Dwight".
    Args:
        request (FixtureRequest): A pytest fixture that provides a request object for managing test state and resources.
    The test also ensures that the dummy file is removed after the test completes.
    """
    filepath = f"dummy-{uuid.uuid4()}.txt"
    request.addfinalizer(lambda: os.unlink(filepath))

    with open(filepath, mode="w") as file:
        file.write("This is a dummy file")

    assert len(load(EMPLOYEES_FILE)) == 2
    assert load(EMPLOYEES_FILE)[0][:3] == "Jim"
    assert load(EMPLOYEES_FILE)[1][:6] == "Dwight"
