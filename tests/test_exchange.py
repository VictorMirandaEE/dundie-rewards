"""dundie exchange unit test."""

from decimal import Decimal
from unittest.mock import Mock, patch

import pytest

from dundie.utils.exchange import get_exchange_rates


@pytest.fixture
def mock_get_logger():
    """
    Mock the `get_logger` function from `dundie.utils.exchange` module.

    This function uses `unittest.mock.patch` to replace the `get_logger`
    function with a mock object for testing purposes. It yields the mocked
    logger, allowing tests to assert calls and interactions with the logger.
    Yields:
        unittest.mock.MagicMock: The mocked logger object.
    """
    with patch("dundie.utils.exchange.get_logger") as mock_logger:
        yield mock_logger


@pytest.fixture
def mock_httpx_get():
    """
    Mock function to patch the `httpx.get` method used in the\
    `dundie.utils.exchange` module.

    This function uses the `patch` context manager to replace the `httpx.get`
    method with a mock object for testing purposes. It yields the mocked
    `httpx.get` method, allowing tests to configure its behavior and assert its
    usage.

    Yields:
        unittest.mock.MagicMock: The mocked `httpx.get` method.
    """
    with patch("dundie.utils.exchange.httpx.get") as mock_get:
        yield mock_get


@pytest.mark.unit
def test_get_exchange_rates_usd(mock_get_logger):
    """
    Test the `get_exchange_rates` function for the USD currency.

    This test verifies that the `get_exchange_rates` function correctly
    retrieves exchange rate information for the USD currency. It checks the
    following:
    - The returned currency code is "USD".
    - The target currency code is "BRL".
    - The currency name is "Dollar/Real".
    - The exchange rate value is 1 (as a Decimal).

    Args:
        mock_get_logger: A mock object for the logger used in the function.
    """
    result = get_exchange_rates(["USD"])
    assert result["USD"].code == "USD"
    assert result["USD"].codein == "BRL"
    assert result["USD"].name == "Dollar/Real"
    assert result["USD"].value == Decimal(1)


@pytest.mark.unit
def test_get_exchange_rates_success(mock_httpx_get, mock_get_logger):
    """
    Test the successful retrieval of exchange rates using the\
    `get_exchange_rates` function.

    This test verifies that the `get_exchange_rates` function correctly
    processes the response from an external API and returns the expected
    exchange rate data for the specified currencies.

    Mocks:
        - `mock_httpx_get`: Mocks the `httpx.get` function to simulate an API
          response.
        - `mock_get_logger`: Mocks the logger used in the function (not
          directly utilized in this test).
        - `mock_response`: Simulates the API response with a predefined JSON
          payload and status handling.

    Assertions:
        - Ensures the returned exchange rate data contains the correct currency
          codes, names, and values.
    """
    mock_response = Mock()
    mock_response.json.return_value = {
        "USDEUR": {
            "code": "USD",
            "codein": "EUR",
            "name": "Dollar/Euro",
            "ask": "0.85",
        }
    }
    mock_response.raise_for_status = Mock()
    mock_httpx_get.return_value = mock_response

    result = get_exchange_rates(["EUR"])
    assert result["EUR"].code == "USD"
    assert result["EUR"].codein == "EUR"
    assert result["EUR"].name == "Dollar/Euro"
    assert result["EUR"].value == Decimal("0.85")


@pytest.mark.unit
def test_get_exchange_rates_api_error(mock_httpx_get, mock_get_logger):
    """
    Test the behavior of the `get_exchange_rates` function when an API error\
    occurs.

    This test simulates an exception being raised during an HTTP request to
    fetch exchange rates. It verifies that the function handles the error
    gracefully by returning a result with the currency name set to "API Error"
    and the value set to Decimal(0).

    Args:
        mock_httpx_get: Mock object for the `httpx.get` function, configured to
                        raise an exception to simulate an API error.
        mock_get_logger: Mock object for the logger used in the function.

    Assertions:
        - The result for the "EUR" currency has the name "API Error".
        - The result for the "EUR" currency has the value Decimal(0).
    """
    mock_httpx_get.side_effect = Exception("API Error")

    result = get_exchange_rates(["EUR"])
    assert result["EUR"].name == "API Error"
    assert result["EUR"].value == Decimal(0)
