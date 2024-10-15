import pytest
from subprocess import check_output


@pytest.mark.integration
@pytest.mark.medium
def test_load():
    """Test command load"""
    output = (
        check_output(["dundie", "load", "tests/assets/employees.csv"])
        .decode("utf-8")
        .split("\n")
    )
    assert len(output) == 2
