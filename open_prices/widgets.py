"""
Streamlit UI helpers for OpenPrices.

Provides helper functions to create Streamlit widgets for filtering and
selecting data (years, currencies, countries, items). These helpers simplify
the UI code and ensure consistent widget behavior across the application.
"""

import numpy as np
import pandas as pd
import streamlit as st


def slider(id: str, title: str) -> int:
    """
    Create a Streamlit slider widget and return the selected value.

    This helper function displays a slider widget in Streamlit with a fixed
    range from 1 to 20 and a default value of 10. It is intended to be used
    for selecting the number of items to display (e.g., top N currencies or
    products).

    Parameters
    ----------
    id : str
        Unique key for the Streamlit widget. Used to preserve the widget state.
    title : str
        Label displayed above the slider.

    Returns
    -------
    int
        The value selected by the user on the slider.

    Examples
    --------
    >>> # Dans une application Streamlit
    >>> value = slider("topCurrencySlider", "Nombre de devises à afficher")
    >>> # value est un int compris entre 1 et 20
    >>> 1 <= value <= 20
    True

    """
    slide: int = st.slider(title, min_value=1, max_value=20, value=10, key=id)
    return slide


def selectedYear(df: pd.DataFrame, id: str) -> int:
    """
    Display a Streamlit selectbox to choose a year from a DataFrame.

    This function extracts the unique years from the "year" column of the
    provided DataFrame, sorts them in descending order, and displays them in a
    Streamlit selectbox. The first (most recent) year is selected by default.

    Parameters
    ----------
    df : pandas.DataFrame
        Input DataFrame containing a "year" column.
    id : str
        Unique key for the Streamlit widget, used to preserve the widget state.

    Returns
    -------
    int
        The year selected by the user.

    Examples
    --------
    >>> import pandas as pd
    >>> df = pd.DataFrame({"year": [2021, 2022, 2023, 2023, None]})
    >>> # Dans une application Streamlit, la valeur par défaut sera la plus récente (2023)
    >>> selected_year = selectedYear(df, "year_select")
    >>> selected_year in [2021, 2022, 2023]
    True

    """
    years: np.ndarray = df["year"].dropna().sort_values(ascending=False).unique()
    selectedYears: int = st.selectbox("Sélectionnez une année", years, index=0, key=id)
    return selectedYears


def selectedCurrency(currency: pd.DataFrame, id: str) -> str:
    """
    Display a Streamlit selectbox to choose a currency.

    This function shows a Streamlit selectbox populated with the values from the
    provided currency list (or Series). If "EUR" is present, it is selected by
    default; otherwise, the first value is selected.

    Parameters
    ----------
    currency : pandas.DataFrame or pandas.Series
        List/Series of currency codes to display in the selectbox.
    id : str
        Unique key for the Streamlit widget to preserve its state.

    Returns
    -------
    str
        The currency selected by the user.

    Examples
    --------
    >>> import pandas as pd
    >>> currency = pd.Series(["USD", "EUR", "GBP"])
    >>> # "EUR" est présent → il est sélectionné par défaut
    >>> selected_currency = selectedCurrency(currency, "currency_select")
    >>> selected_currency in ["USD", "EUR", "GBP"]
    True

    """
    selectedCurrencies: str = st.selectbox(
        "Sélectionnez une devise",
        currency,
        index=list(currency).index("EUR") if "EUR" in list(currency) else 0,
        key=id,
    )
    return selectedCurrencies


def selectedAllYear(df: pd.DataFrame, id: str) -> int | None:
    """
    Display a Streamlit UI component to select either a specific year or all years.

    This function creates a two-column layout in Streamlit:
    - The first column contains a checkbox "Toutes les années".
    - The second column contains a selectbox with available years (descending order)
      only if the checkbox is unchecked.

    If the checkbox is checked, the function returns None to indicate that all
    years should be considered. Otherwise, it returns the selected year.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame containing a "year" column used to populate the selectbox.
    id : str
        Unique key for Streamlit widgets to preserve their state.

    Returns
    -------
    int | None
        The selected year, or None if "Toutes les années" is checked.

    Examples
    --------
    >>> import pandas as pd
    >>> df = pd.DataFrame({"year": [2021, 2022, 2023]})
    >>> # Cas 1 : checkbox non cochée → une année est retournée
    >>> selected_year = selectedAllYear(df, "year_selector")
    >>> selected_year in [2021, 2022, 2023, None]
    True

    >>> # Cas 2 : checkbox cochée → None est retourné
    >>> # (Dans une vraie app Streamlit, l'utilisateur coche la case)
    >>> # selected_year = None

    """
    col1, col2 = st.columns([1, 3])

    with col1:
        all_years: bool = st.checkbox("Toutes les années", value=False, key=f"{id}_all_years")
    with col2:
        if not all_years:
            years: np.ndarray = df["year"].dropna().sort_values(ascending=False).unique()
            selectedYears: int = st.selectbox("Sélectionnez une année", years, index=0, key=id)
            return selectedYears
        else:
            return None


def selectedCountry(country: pd.DataFrame, id: str) -> str:
    """
    Display a Streamlit selectbox to choose a country.

    This function shows a Streamlit `selectbox` populated with the values
    from the provided `country` DataFrame/Series. If "France" is present in
    the list, it will be selected by default; otherwise, the first element
    will be selected.

    Parameters
    ----------
    country : pandas.DataFrame
        DataFrame or Series containing the list of countries to display.
    id : str
        Unique key for the Streamlit widget to preserve its state.

    Returns
    -------
    str
        The selected country.

    Examples
    --------
    >>> import pandas as pd
    >>> countries = pd.Series(["France", "Germany", "Spain"])
    >>> # "France" est présent → il est sélectionné par défaut
    >>> selected_country = selectedCountry(countries, "country_selector")
    >>> selected_country in ["France", "Germany", "Spain"]
    True

    """
    selectedCountries: str = st.selectbox(
        "Sélectionnez un pays",
        country,
        index=list(country).index("France") if "France" in list(country) else 0,
        key=id,
    )
    return selectedCountries


def selectedItem(df: pd.DataFrame, columnName: str, id: str, label: str) -> str:
    """
    Display a Streamlit selectbox to choose an item from a DataFrame column.

    This function extracts the unique, non-null values from the specified
    column of the provided DataFrame, sorts them alphabetically, and then
    displays a Streamlit `selectbox` to allow the user to select one item.
    The first element is selected by default.

    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame containing the column to use for the selectbox.
    columnName : str
        Name of the column containing the items.
    id : str
        Unique key for the Streamlit widget to preserve its state.
    label : str
        Label displayed in the selectbox prompt.

    Returns
    -------
    str
        The selected item from the list.

    Examples
    --------
    >>> import pandas as pd
    >>> data = {"fruit": ["pomme", "banane", "pomme", None]}
    >>> df = pd.DataFrame(data)
    >>> # Les valeurs uniques non-null sont triées : ["banane", "pomme"]
    >>> selected = selectedItem(df, "fruit", "fruit_select", "un fruit")
    >>> selected in ["banane", "pomme"]
    True

    """
    items: np.ndarray = df[columnName].dropna().sort_values().unique()
    selectedItem: str = st.selectbox(f"Sélectionnez {label}", items, index=0, key=id)
    return selectedItem


def selectedMultipleItems(df: pd.DataFrame, columnName: str, id: str, label: str) -> list:
    """
    Display a Streamlit multiselect widget to choose one or several items.

    This function extracts the unique, non-null values from the specified
    DataFrame column, sorts them, and displays a Streamlit `multiselect`
    widget. If the column contains values, the first item is selected by default.
    Otherwise, the default selection is empty.

    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame containing the column to use for the multiselect.
    columnName : str
        Name of the column containing the items.
    id : str
        Unique key for the Streamlit widget to preserve its state.
    label : str
        Label displayed in the multiselect prompt.

    Returns
    -------
    list
        A list of selected items.

    Examples
    --------
    >>> import pandas as pd
    >>> data = {"fruit": ["pomme", "banane", "pomme", None]}
    >>> df = pd.DataFrame(data)
    >>> # Valeurs uniques non-null triées : ["banane", "pomme"]
    >>> selected = selectedMultipleItems(df, "fruit", "fruit_multi", "fruits")
    >>> all(item in ["banane", "pomme"] for item in selected)
    True

    """
    items: np.ndarray = df[columnName].dropna().sort_values().unique()
    selectedItems: list = st.multiselect(
        f"Sélectionnez un ou plusieurs {label}",
        items,
        default=[items[0]] if len(items) > 0 else [],
        key=id,
    )
    return selectedItems


def selectedCurrencyOrCountry(
    currencies: pd.Series, countries: pd.Series, id: str
) -> tuple[str, str]:
    """
    Display Streamlit widgets to select either a currency or a country.

    This function shows a two-column layout:
    - The first column contains a radio button to choose the filter type:
      either "Devise" (currency) or "Pays" (country).
    - The second column displays a selectbox with the corresponding list of
      values depending on the chosen filter type.

    If the user chooses "Devise", the function returns the filter column name
    "proof_currency" and the selected currency value.
    If the user chooses "Pays", the function returns the filter column name
    "location_osm_address_country" and the selected country value.

    Parameters
    ----------
    currencies : pandas.Series
        List/series of available currencies to display.
    countries : pandas.Series
        List/series of available countries to display.
    id : str
        Unique Streamlit key used to keep widget state.

    Returns
    -------
    tuple[str, str]
        A tuple containing:
        - the name of the filter column ("proof_currency" or "location_osm_address_country")
        - the selected value (currency or country)

    Examples
    --------
    >>> import pandas as pd
    >>> currencies = pd.Series(["EUR", "USD", "GBP"])
    >>> countries = pd.Series(["France", "Spain", "Germany"])
    >>> filter_column, selected_value = selectedCurrencyOrCountry(
        currencies, countries, "filter_1"
    )
    >>> filter_column in ["proof_currency", "location_osm_address_country"]
    True
    >>> selected_value in ["EUR", "USD", "GBP", "France", "Spain", "Germany"]
    True

    """
    col1, col2 = st.columns([1, 3])

    with col1:
        filterType: str = st.radio("Filtrer par", ["Devise", "Pays"], key=f"{id}_filter_type")
    with col2:
        if filterType == "Devise":
            selectedValue: str = st.selectbox(
                "Sélectionnez une devise",
                currencies,
                index=list(currencies).index("EUR") if "EUR" in list(currencies) else 0,
                key=f"{id}_currency",
            )
            return "proof_currency", selectedValue
        else:
            selectedValue = st.selectbox(
                "Sélectionnez un pays",
                countries,
                index=list(countries).index("France") if "France" in list(countries) else 0,
                key=f"{id}_country",
            )
            return "location_osm_address_country", selectedValue
