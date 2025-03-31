"""Convert currency using the exchange rate from the European Central Bank."""

from decimal import Decimal
from typing import Dict, List

import httpx
from pydantic import BaseModel, Field

from dundie.settings import API_BASE_URL
from dundie.utils.log import get_logger


class USDRate(BaseModel):
    """Currency exchange rate model.

    Attributes:
        code (str): The currency code for USD. Defaults to "USD".
        codein (str): The currency code for BRL. Defaults to "BRL".
        name (str): The name of the currency pair. Defaults to "Dollar/Real".
        value (Decimal): The exchange rate value from USD to BRL.
    """

    code: str = Field(default="USD", alias="code")
    codein: str = Field(default="BRL", alias="codein")
    name: str = Field(default="Dollar/Real", alias="name")
    value: Decimal = Field(alias="ask")


def get_exchange_rates(currencies: List[str]) -> Dict[str, USDRate]:
    """Get the exchange rates for the given currencies.

    This function fetches the exchange rates for a list of currency codes
    from an external API and returns a dictionary where the keys are the
    currency codes and the values are USDRate objects representing the
    exchange rates.

    If there is an error fetching the exchange rate for a currency, the value
    will be a USDRate object with the name "API Error" and ask value of 0.

    Args:
        currencies (List[str]): A list of currency codes.

    Returns:
        Dict[str, USDRate]: A dictionary with currency codes as keys and
          USDRate objects as values.
    """
    exchange_rates = {}
    log = get_logger()

    for currency in currencies:
        if currency == "USD":
            exchange_rates[currency] = USDRate(ask=Decimal(1))
        else:
            url = API_BASE_URL.format(currency=currency)
            try:
                response = httpx.get(url)
                response.raise_for_status()
                key = f"USD{currency}"
                data = response.json()[key]
                exchange_rates[currency] = USDRate(**data)
            except Exception as error_msg:
                log.error(f"Error {error_msg} for currency {currency}")
                exchange_rates[currency] = USDRate(
                    name="API Error", ask=Decimal(0)
                )
    return exchange_rates
