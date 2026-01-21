"""
Analytics module for OpenPrices.

Provides functions to generate visualizations for sales trends and category
counts using Matplotlib and Plotly. The functions are designed to be used in
a Streamlit dashboard for displaying interactive charts.
"""

from typing import Tuple

import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def graphBar(
    productCategoryCounts: pd.Series,
    xlabel: str,
    ylabel: str,
    title: str,
    properties: fm.FontProperties,
) -> Tuple[plt.Figure, plt.Axes]:
    """
    Plot a horizontal bar chart for a Series of counts.

    This function creates a matplotlib figure with a horizontal bar chart
    representing the values of the input Series. The bars are plotted in a
    single color and the y-axis is inverted so that the highest value appears
    at the top. Axis labels and title are formatted using the provided font
    properties.

    Parameters
    ----------
    productCategoryCounts : pandas.Series
        Series where the index contains the category names and the values
        represent the counts for each category.
    xlabel : str
        Label for the x-axis.
    ylabel : str
        Label for the y-axis.
    title : str
        Title of the plot.
    properties : matplotlib.font_manager.FontProperties
        Font properties used for axis labels, title, and tick labels.

    Returns
    -------
    tuple[matplotlib.figure.Figure, matplotlib.axes.Axes]
        A tuple containing the created Figure and Axes objects.

    Examples
    --------
    >>> import pandas as pd
    >>> import matplotlib.font_manager as fm
    >>> from matplotlib import pyplot as plt
    >>> counts = pd.Series([5, 2, 8], index=["A", "B", "C"])
    >>> props = fm.FontProperties()
    >>> fig, ax = graphBar(counts, "Counts", "Category", "Test Title", props)
    >>> isinstance(fig, plt.Figure)
    True
    >>> isinstance(ax, plt.Axes)
    True

    """
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(productCategoryCounts.index, productCategoryCounts.values, color="skyblue")
    ax.invert_yaxis()
    ax.set_xlabel(f"{xlabel}", fontproperties=properties)
    ax.set_ylabel(f"{ylabel.capitalize()}", fontproperties=properties)
    ax.set_title(f"{title}", fontproperties=properties)
    ax.set_yticklabels(productCategoryCounts.index, fontproperties=properties)

    return fig, ax


def trendGraphLine(
    trendData: pd.DataFrame,
    selectCountryCurrency: str,
    selectedYears: int,
    type: str,
    properties: fm.FontProperties,
) -> Tuple[plt.Figure, plt.Axes]:
    """
    Plot a line chart showing monthly sales trends for selected items.

    This function creates a matplotlib line plot from a trend DataFrame.
    The DataFrame is expected to contain the columns "month", "count" and
    "item". Each unique item is plotted as a separate line over the 12 months.
    Missing months are assumed to be present in the input DataFrame with count
    values (e.g., 0), but the function itself does not fill missing months.

    Parameters
    ----------
    trendData : pandas.DataFrame
        DataFrame containing monthly sales counts for each item.
        Expected columns: "month", "count", "item".
    selectCountryCurrency : str
        Label used in the plot title to indicate the selected country/currency.
    selectedYears : int
        Year used in the plot title.
    type : str
        Label used in the plot title to indicate the dimension (e.g., "produits",
        "catégories").
    properties : matplotlib.font_manager.FontProperties
        Font properties used for axis labels, title, ticks, and legend.

    Returns
    -------
    tuple[matplotlib.figure.Figure, matplotlib.axes.Axes]
        A tuple containing the created Figure and Axes objects.

    Notes
    -----
    The legend is only displayed if there is at least one line plotted,
    preventing warnings when the input DataFrame is empty.

    Examples
    --------
    >>> import pandas as pd
    >>> import matplotlib.font_manager as fm
    >>> from matplotlib import pyplot as plt
    >>> trendData = pd.DataFrame({
    ...     "month": [1, 2, 1, 2],
    ...     "count": [5, 3, 2, 4],
    ...     "item": ["A", "A", "B", "B"]
    ... })
    >>> props = fm.FontProperties()
    >>> fig, ax = trendGraphLine(trendData, "EUR", 2023, "produits", props)
    >>> isinstance(fig, plt.Figure)
    True
    >>> isinstance(ax, plt.Axes)
    True

    """
    fig, ax = plt.subplots(figsize=(10, 6))

    monthNames: list = [
        "Jan",
        "Fév",
        "Mar",
        "Avr",
        "Mai",
        "Juin",
        "Juil",
        "Août",
        "Sep",
        "Oct",
        "Nov",
        "Déc",
    ]

    for item in trendData["item"].unique():
        itemData: pd.DataFrame = trendData[trendData["item"] == item]
        ax.plot(itemData["month"], itemData["count"], marker="o", label=item)

    ax.set_xlabel("Mois", fontproperties=properties)
    ax.set_ylabel("Nombre de ventes", fontproperties=properties)
    ax.set_title(
        f"Évolution mensuelle des ventes - {type} ({selectCountryCurrency}, {selectedYears})",
        fontproperties=properties,
    )
    ax.set_xticks(range(1, 13))
    ax.set_xticklabels(monthNames, fontproperties=properties)
    if ax.lines:
        ax.legend(prop=properties)
    ax.grid(True, alpha=0.3)

    return fig, ax


def trendGraphBar(
    trendData: pd.DataFrame,
    selectCountryCurrency: str,
    selectedYears: int,
    chartType: str,
) -> go.Figure:
    """
    Plot a grouped bar chart showing monthly sales trends for selected items using Plotly.

    This function creates a Plotly bar chart from a trend DataFrame. The DataFrame
    must contain the columns "month", "count" and "item". Each unique item is
    plotted as a separate bar group for each month. The function also formats
    axis labels, title, legend, and colors to ensure good readability on a
    Streamlit page.

    Parameters
    ----------
    trendData : pandas.DataFrame
        DataFrame containing monthly sales counts for each item.
        Expected columns: "month", "count", "item".
    selectCountryCurrency : str
        Label used in the plot title to indicate the selected country/currency.
    selectedYears : int
        Year used in the plot title.
    chartType : str
        Label used for the legend title and in the plot title (e.g., "produits",
        "catégories").

    Returns
    -------
    plotly.graph_objects.Figure
        A Plotly Figure object representing the grouped bar chart.

    Notes
    -----
    - The x-axis is fixed to 12 months (1–12) with French month names.
    - The legend and text colors are forced to black to avoid visibility issues
      on Streamlit.

    Examples
    --------
    >>> import pandas as pd
    >>> import plotly.graph_objects as go
    >>> trendData = pd.DataFrame({
    ...     "month": [1, 1, 2, 2],
    ...     "count": [5, 2, 3, 4],
    ...     "item": ["A", "B", "A", "B"]
    ... })
    >>> fig = trendGraphBar(trendData, "EUR", 2023, "produits")
    >>> isinstance(fig, go.Figure)
    True

    """
    fig = px.bar(
        trendData,
        x="month",
        y="count",
        color="item",
        color_discrete_sequence=px.colors.qualitative.D3,
        barmode="group",
        labels={
            "month": "Mois",
            "count": "Nombre de ventes",
            "item": chartType,
        },
        title=(
            f"Évolution mensuelle des ventes - {chartType}"
            f"({selectCountryCurrency}, {selectedYears})"
        ),
    )

    fig.update_xaxes(
        tickmode="array",
        tickvals=list(range(1, 13)),
        ticktext=[
            "Jan",
            "Fév",
            "Mar",
            "Avr",
            "Mai",
            "Juin",
            "Juil",
            "Août",
            "Sep",
            "Oct",
            "Nov",
            "Déc",
        ],
        title_font=dict(color="black"),
        tickfont=dict(color="black"),
    )

    fig.update_layout(
        bargap=0.2,
        bargroupgap=0.05,
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(color="black"),
        legend=dict(
            title=dict(font=dict(color="black")),
            font=dict(color="black"),
        ),
    )

    fig.update_yaxes(
        title_font=dict(color="black"),
        tickfont=dict(color="black"),
    )

    return fig
