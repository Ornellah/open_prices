"""
Analytics module for OpenPrices.

Provides functions to compute sales metrics and prepare dataframes for
visualization.
"""

import pandas as pd


def computeSalesMetrics(
    df: pd.DataFrame,
    columnName: str,
    filterColumn: str,
    filterValue: str,
    selectedYears: int,
    head: bool,
    n: int | None = None,
) -> pd.Series:
    """
    Compute sales metrics for a specific dimension and filter.

    This function filters the input DataFrame based on a given column value
    and a selected year. It then computes counts and average prices for the
    specified dimension (columnName), separated by unit type ("KILOGRAM" and
    "UNIT"). The function returns several pandas Series aligned on the same
    index (the top dimension values if `head` is True).

    Parameters
    ----------
    df : pandas.DataFrame
        Input DataFrame containing sales data.
        Expected columns: "year", "price_per", "price", and the specified
        `columnName` and `filterColumn`.
    columnName : str
        Name of the dimension column to analyze (e.g., "product_name",
        "category_tag", "proof_currency").
    filterColumn : str
        Column used to filter the dataset (e.g., "proof_currency").
    filterValue : str
        Value to filter on in `filterColumn`.
    selectedYears : int
        Year to filter the dataset on.
    head : bool
        If True, returns only the top `n` results based on total counts.
    n : int | None, optional
        Number of top rows to return when `head` is True. If None, returns all.

    Returns
    -------
    tuple[pandas.Series, pandas.Series, pandas.Series, pandas.Series, pandas.Series, pandas.Series]
        A tuple containing:
        - productCategoryCounts: total counts for each value in `columnName`
        - salesKiloTop: counts of sales priced per kilogram
        - priceKiloTop: average price per kilogram
        - salesUnitTop: counts of sales priced per unit
        - priceUnitTop: average price per unit
        - totalPrices: estimated total price per dimension value,
          computed as (salesKiloTop * priceKiloTop + salesUnitTop * priceUnitTop)

    Examples
    --------
    >>> import pandas as pd
    >>> df = pd.DataFrame({
    ...     "year": [2023, 2023, 2023, 2023],
    ...     "proof_currency": ["EUR", "EUR", "EUR", "EUR"],
    ...     "product_name": ["A", "A", "B", "B"],
    ...     "price_per": ["UNIT", "KILOGRAM", "UNIT", "KILOGRAM"],
    ...     "price": [10, 20, 15, 30],
    ... })
    >>> computeSalesMetrics(df, "product_name", "proof_currency", "EUR", 2023, head=True, n=2)
    (product_name
     A    2
     B    2
     dtype: int64,
     product_name
     A    1
     B    1
     dtype: int64,
     product_name
     A    20.0
     B    30.0
     dtype: float64,
     product_name
     A    1
     B    1
     dtype: int64,
     product_name
     A    10.0
     B    15.0
     dtype: float64,
     product_name
     A    30.0
     B    45.0
     dtype: float64)

    """
    dfFiltered: pd.DataFrame = df[
        (df[f"{filterColumn}"] == filterValue) & (df["year"] == selectedYears)
    ]
    if head:
        productCategoryCounts: pd.Series = dfFiltered[f"{columnName}"].value_counts().head(n)
    else:
        productCategoryCounts = dfFiltered[f"{columnName}"].value_counts()

    unitPriceKilo: pd.Series = (
        dfFiltered[dfFiltered["price_per"] == "KILOGRAM"].groupby(f"{columnName}")["price"].mean()
    )
    priceKiloTop: pd.Series = unitPriceKilo.reindex(productCategoryCounts.index, fill_value=0)
    unitPriceUnit: pd.Series = (
        dfFiltered[dfFiltered["price_per"] == "UNIT"].groupby(f"{columnName}")["price"].mean()
    )
    priceUnitTop: pd.Series = unitPriceUnit.reindex(productCategoryCounts.index, fill_value=0)
    salesKilo: pd.Series = dfFiltered[dfFiltered["price_per"] == "KILOGRAM"][
        f"{columnName}"
    ].value_counts()
    salesKiloTop: pd.Series = salesKilo.reindex(productCategoryCounts.index, fill_value=0)
    salesUnit: pd.Series = dfFiltered[dfFiltered["price_per"] == "UNIT"][
        f"{columnName}"
    ].value_counts()
    salesUnitTop: pd.Series = salesUnit.reindex(productCategoryCounts.index, fill_value=0)
    totalPrices: pd.Series = salesKiloTop * priceKiloTop + salesUnitTop * priceUnitTop

    return (
        productCategoryCounts,
        salesKiloTop,
        priceKiloTop,
        salesUnitTop,
        priceUnitTop,
        totalPrices,
    )


def computeSalesMetricsForYear(
    df: pd.DataFrame,
    columnName: str,
    selectedYears: int | None,
    head: bool,
    n: int | None = None,
) -> pd.Series:
    """
    Compute sales counts by dimension for a given year (or all years).

    This function filters the input DataFrame by the selected year (if provided)
    and computes the total counts for the specified dimension (`columnName`).
    It also computes counts separately for sales priced per kilogram and per unit.
    The results are aligned to the same index (top values if `head` is True).

    Parameters
    ----------
    df : pandas.DataFrame
        Input DataFrame containing sales data.
        Expected columns: "year", "price_per", and the specified `columnName`.
    columnName : str
        Name of the dimension column to analyze (e.g., "proof_currency",
        "product_name", "category_tag").
    selectedYears : int | None
        Year to filter the dataset on. If None, no year filter is applied.
    head : bool
        If True, returns only the top `n` results based on total counts.
    n : int | None, optional
        Number of top rows to return when `head` is True. If None, returns all.

    Returns
    -------
    tuple[pandas.Series, pandas.Series, pandas.Series]
        A tuple containing:
        - dimensionCounts: total counts for each value in `columnName`
        - salesKiloTop: counts of sales priced per kilogram
        - salesUnitTop: counts of sales priced per unit

    Examples
    --------
    >>> import pandas as pd
    >>> df = pd.DataFrame({
    ...     "year": [2023, 2023, 2022, 2023],
    ...     "proof_currency": ["EUR", "EUR", "EUR", "USD"],
    ...     "price_per": ["UNIT", "KILOGRAM", "UNIT", "UNIT"],
    ...     "price": [10, 20, 15, 30],
    ... })
    >>> computeSalesMetricsForYear(df, "proof_currency", 2023, head=True, n=2)
    (proof_currency
     EUR    2
     USD    1
     dtype: int64,
     proof_currency
     EUR    1
     USD    0
     dtype: int64,
     proof_currency
     EUR    1
     USD    1
     dtype: int64)

    """
    if selectedYears is not None:
        dfFiltered: pd.DataFrame = df[df["year"] == selectedYears]
    else:
        dfFiltered = df

    if head:
        dimensionCounts: pd.Series = dfFiltered[f"{columnName}"].value_counts().head(n)
    else:
        dimensionCounts = dfFiltered[f"{columnName}"].value_counts()
    salesKilo: pd.Series = dfFiltered[dfFiltered["price_per"] == "KILOGRAM"][
        f"{columnName}"
    ].value_counts()
    salesKiloTop: pd.Series = salesKilo.reindex(dimensionCounts.index, fill_value=0)
    salesUnit: pd.Series = dfFiltered[dfFiltered["price_per"] == "UNIT"][
        f"{columnName}"
    ].value_counts()
    salesUnitTop: pd.Series = salesUnit.reindex(dimensionCounts.index, fill_value=0)

    return dimensionCounts, salesKiloTop, salesUnitTop


def makeDfWithAllMetrics(
    productCategoryCounts: pd.Series,
    salesKiloTop: pd.Series,
    priceKiloTop: pd.Series,
    salesUnitTop: pd.Series,
    priceUnitTop: pd.Series,
    totalPrices: pd.Series,
) -> pd.DataFrame:
    """
    Create a summary DataFrame combining sales counts and prices.

    This function takes multiple pandas Series containing sales counts and
    average prices for a given dimension (e.g., product, category, currency)
    and returns a single DataFrame summarizing these metrics.

    The Series are expected to have the same index (dimension values). The
    resulting DataFrame contains one row per dimension value with the
    corresponding metrics.

    Parameters
    ----------
    productCategoryCounts : pandas.Series
        Total number of sales for each dimension value.
    salesKiloTop : pandas.Series
        Number of sales priced per kilogram for each dimension value.
    priceKiloTop : pandas.Series
        Average price per kilogram for each dimension value.
    salesUnitTop : pandas.Series
        Number of sales priced per unit for each dimension value.
    priceUnitTop : pandas.Series
        Average price per unit for each dimension value.
    totalPrices : pandas.Series
        Estimated total sales value per dimension value.

    Returns
    -------
    pandas.DataFrame
        A DataFrame with columns:
        - "nom": dimension values
        - "nombre_de_ventes_total"
        - "nombre_ventes_kilo"
        - "prix_unitaire_moyen_kilo"
        - "nombre_ventes_unit"
        - "prix_unitaire_moyen_unit"
        - "prix_total"

    Examples
    --------
    >>> import pandas as pd
    >>> productCategoryCounts = pd.Series([10, 5], index=["A", "B"])
    >>> salesKiloTop = pd.Series([4, 2], index=["A", "B"])
    >>> priceKiloTop = pd.Series([20.0, 30.0], index=["A", "B"])
    >>> salesUnitTop = pd.Series([6, 3], index=["A", "B"])
    >>> priceUnitTop = pd.Series([10.0, 15.0], index=["A", "B"])
    >>> totalPrices = salesKiloTop * priceKiloTop + salesUnitTop * priceUnitTop
    >>> makeDfWithAllMetrics(
    ...     productCategoryCounts,
    ...     salesKiloTop,
    ...     priceKiloTop,
    ...     salesUnitTop,
    ...     priceUnitTop,
    ...     totalPrices
    ... )
      nom  nombre_de_ventes_total  nombre_ventes_kilo  prix_unitaire_moyen_kilo  \
    0   A                      10                  4                      20.0   
    1   B                       5                  2                      30.0   

       nombre_ventes_unit  prix_unitaire_moyen_unit  prix_total  
    0                  6                      10.0       140.0  
    1                  3                      15.0        90.0  

    """
    dfTop: pd.DataFrame = pd.DataFrame(
        {
            "nom": productCategoryCounts.index,
            "nombre_de_ventes_total": productCategoryCounts.values,
            "nombre_ventes_kilo": salesKiloTop.values,
            "prix_unitaire_moyen_kilo": priceKiloTop.values,
            "nombre_ventes_unit": salesUnitTop.values,
            "prix_unitaire_moyen_unit": priceUnitTop.values,
            "prix_total": totalPrices.values,
        }
    )
    return dfTop


def makeDfWithSomeMetrics(
    currencyCountryCounts: pd.Series, name: str, salesKiloTop: pd.Series, salesUnitTop: pd.Series
) -> pd.DataFrame:
    """
    Create a summary DataFrame with selected sales metrics.

    This function takes multiple pandas Series containing sales counts for a
    given dimension (e.g., currency or country) and returns a DataFrame
    summarizing these metrics. The Series are expected to share the same index
    (dimension values).

    Parameters
    ----------
    currencyCountryCounts : pandas.Series
        Total number of sales for each dimension value.
    name : str
        Name of the dimension (not used in the DataFrame construction,
        kept for compatibility with other functions).
    salesKiloTop : pandas.Series
        Number of sales priced per kilogram for each dimension value.
    salesUnitTop : pandas.Series
        Number of sales priced per unit for each dimension value.

    Returns
    -------
    pandas.DataFrame
        A DataFrame with columns:
        - "devise": dimension values
        - "nombre_de_ventes_total"
        - "nombre_ventes_kilo"
        - "nombre_ventes_unit"

    Examples
    --------
    >>> import pandas as pd
    >>> currencyCountryCounts = pd.Series([10, 5], index=["EUR", "USD"])
    >>> salesKiloTop = pd.Series([4, 2], index=["EUR", "USD"])
    >>> salesUnitTop = pd.Series([6, 3], index=["EUR", "USD"])
    >>> makeDfWithSomeMetrics(currencyCountryCounts, "devise", salesKiloTop, salesUnitTop)
      devise  nombre_de_ventes_total  nombre_ventes_kilo  nombre_ventes_unit
    0    EUR                      10                  4                  6
    1    USD                       5                  2                  3

    """
    dfTop: pd.DataFrame = pd.DataFrame(
        {
            "devise": currencyCountryCounts.index,
            "nombre_de_ventes_total": currencyCountryCounts.values,
            "nombre_ventes_kilo": salesKiloTop.values,
            "nombre_ventes_unit": salesUnitTop.values,
        }
    )
    return dfTop


def filterItemsByMinSales(
    df: pd.DataFrame,
    filterOn: str,
    columnName: str,
    selectCountryCurrency: str,
    selectedYears: int,
    minSales: int = 10,
    minMonths: int = 2,
) -> pd.DataFrame:
    """
    Filter items that meet minimum sales and minimum active months criteria.

    This function filters a DataFrame for a specific country/currency and year,
    then keeps only the items (defined by `columnName`) that satisfy both:
    - having at least `minSales` total sales, and
    - being sold in at least `minMonths` different months.

    The returned DataFrame contains only rows corresponding to items that
    satisfy both conditions.

    Parameters
    ----------
    df : pandas.DataFrame
        Input DataFrame containing sales data.
        Expected columns: `filterOn`, `year`, `month`, and `columnName`.
    filterOn : str
        Column name used to filter the dataset (e.g., "proof_currency").
    columnName : str
        Column name defining the item dimension (e.g., "product_name" or "category_tag").
    selectCountryCurrency : str
        Value to filter on in `filterOn`.
    selectedYears : int
        Year to filter the dataset on.
    minSales : int, optional (default=10)
        Minimum number of sales required for an item to be kept.
    minMonths : int, optional (default=2)
        Minimum number of distinct months in which the item must appear.

    Returns
    -------
    pandas.DataFrame
        Filtered DataFrame containing only items that meet both criteria.

    Examples
    --------
    >>> import pandas as pd
    >>> df = pd.DataFrame({
    ...     "year": [2023, 2023, 2023, 2023, 2023],
    ...     "proof_currency": ["EUR", "EUR", "EUR", "EUR", "EUR"],
    ...     "product_name": ["A", "A", "A", "B", "B"],
    ...     "month": [1, 1, 2, 1, 2],
    ... })
    >>> filterItemsByMinSales(
        df, "proof_currency", "product_name",
        "EUR", 2023, minSales=3, minMonths=2
    )
      year proof_currency product_name  month
    0  2023           EUR            A      1
    1  2023           EUR            A      1
    2  2023           EUR            A      2

    """
    dfFiltered: pd.DataFrame = df[
        (df[f"{filterOn}"] == selectCountryCurrency) & (df["year"] == selectedYears)
    ]
    itemCounts: pd.Series = dfFiltered.groupby(columnName).size()
    validItemsBySales: pd.Index = itemCounts[itemCounts >= minSales].index
    monthCounts: pd.Series = dfFiltered.groupby(columnName)["month"].nunique()
    validItemsByMonths: pd.Index = monthCounts[monthCounts >= minMonths].index
    validItems: pd.Index = validItemsBySales.intersection(validItemsByMonths)
    filterItems: pd.DataFrame = dfFiltered[dfFiltered[columnName].isin(validItems)]

    return filterItems


def makeDfTrendData(
    df: pd.DataFrame,
    filterOn: str,
    columnName: str,
    selectCountryCurrency: str,
    selectedYears: int,
    selectedItems: list,
) -> pd.DataFrame:
    """
    Build a monthly trend DataFrame for selected items.

    This function filters the input DataFrame by country/currency and year,
    then for each selected item computes the number of sales per month.
    It ensures that all months from 1 to 12 are present by filling missing
    months with zero sales.

    The resulting DataFrame is suitable for plotting time series charts,
    with one row per item per month.

    Parameters
    ----------
    df : pandas.DataFrame
        Input DataFrame containing sales data.
        Expected columns: `filterOn`, `year`, `month`, and `columnName`.
    filterOn : str
        Column name used to filter the dataset (e.g., "proof_currency").
    columnName : str
        Column name defining the item dimension (e.g., "product_name").
    selectCountryCurrency : str
        Value to filter on in `filterOn`.
    selectedYears : int
        Year to filter the dataset on.
    selectedItems : list
        List of items (values from `columnName`) to include in the trend.

    Returns
    -------
    pandas.DataFrame
        A DataFrame with columns:
        - "month": month number (1–12)
        - "count": number of sales for the item in that month
        - "item": item name

    Examples
    --------
    >>> import pandas as pd
    >>> df = pd.DataFrame({
    ...     "year": [2023, 2023, 2023, 2023],
    ...     "proof_currency": ["EUR", "EUR", "EUR", "EUR"],
    ...     "product_name": ["A", "A", "B", "B"],
    ...     "month": [1, 2, 1, 3],
    ... })
    >>> makeDfTrendData(df, "proof_currency", "product_name", "EUR", 2023, ["A", "B"])
       month  count item
    0      1    1.0    A
    1      2    1.0    A
    2      3    0.0    A
    3      4    0.0    A
    ...
    12     1    1.0    B
    13     2    0.0    B
    14     3    1.0    B
    15     4    0.0    B
    ...

    """
    dfFiltered: pd.DataFrame = df[
        (df[f"{filterOn}"] == selectCountryCurrency) & (df["year"] == selectedYears)
    ]

    results: list = []
    for item in selectedItems:
        dfItem: pd.DataFrame = dfFiltered[dfFiltered[columnName] == item]
        monthlyCounts: pd.Series = dfItem.groupby("month").size()
        allMonths: pd.DataFrame = pd.DataFrame({"month": range(1, 13)})
        monthlyData: pd.DataFrame = allMonths.merge(
            monthlyCounts.reset_index(name="count"), on="month", how="left"
        ).fillna(0)
        monthlyData["item"] = item
        results.append(monthlyData)
    dfTrendData: pd.DataFrame = pd.concat(results, ignore_index=True)

    return dfTrendData
