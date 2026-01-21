"""
Unit tests for the OpenPrices widgets module.

Tests the functions:
- selectedAllYear
- selectedCurrencyOrCountry

Uses pytest as the test framework and unittest.mock for Streamlit widget mocking.
"""

from typing import Any, Tuple
from unittest.mock import patch

import pandas as pd

from open_prices.widgets import selectedAllYear, selectedCurrencyOrCountry


@patch("open_prices.widgets.st.checkbox")
def testSelectedAllYearAllYearsChecked(mockCheckbox: Any) -> None:
    df: pd.DataFrame = pd.DataFrame({"year": [2022, 2023, 2024]})
    mockCheckbox.return_value = True
    result: int | None = selectedAllYear(df, "id")

    assert result is None


@patch("open_prices.widgets.st.checkbox")
@patch("open_prices.widgets.st.selectbox")
def testSelectedAllYearAllYearsNotChecked(mockSelectbox: Any, mockCheckbox: Any) -> None:
    df: pd.DataFrame = pd.DataFrame({"year": [2022, 2023, 2024]})
    mockCheckbox.return_value = False
    mockSelectbox.return_value = 2023
    result: int | None = selectedAllYear(df, "id")

    assert result == 2023


@patch("open_prices.widgets.st.radio")
@patch("open_prices.widgets.st.selectbox")
def testSelectedCurrencyOrCountryCheckCurrency(mockSelectbox: Any, mockRadio: Any) -> None:
    currencies: pd.Series = pd.Series(["EUR", "USD"])
    countries: pd.Series = pd.Series(["France", "Germany"])
    mockRadio.return_value = "Devise"
    mockSelectbox.return_value = "USD"
    result: Tuple = selectedCurrencyOrCountry(currencies, countries, "id")

    assert result == ("proof_currency", "USD")


@patch("open_prices.widgets.st.radio")
@patch("open_prices.widgets.st.selectbox")
def testSelectedCurrencyOrCountryCheckCountry(mockSelectbox: Any, mockRadio: Any) -> None:
    currencies: pd.api = pd.Series(["EUR", "USD"])
    countries: pd.api = pd.Series(["France", "Germany"])
    mockRadio.return_value = "Pays"
    mockSelectbox.return_value = "Germany"
    result: Tuple = selectedCurrencyOrCountry(currencies, countries, "id")

    assert result == ("location_osm_address_country", "Germany")
