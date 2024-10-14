import pytest
from dundie.core import load
from .constants import EMPLOYEES_FILE


@pytest.mark.unit
@pytest.mark.high
def test_load():
    """Test load function"""
    assert len(load(EMPLOYEES_FILE)) == 2
    assert load(EMPLOYEES_FILE)[0][0] == "J"
