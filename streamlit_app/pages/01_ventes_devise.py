"""
Streamlit page displaying sales metrics by currency.

Provides four tabs:
- Top N currencies (products)
- All currencies (products)
- Top N currencies (categories)
- All currencies (categories)

Each tab shows either a horizontal bar chart or a data table based on the
selected year(s) and currency counts.
"""

from pathlib import Path

import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

from open_prices.analytics import computeSalesMetricsForYear, makeDfWithSomeMetrics
from open_prices.config import PROCESSED_DATA_FILE
from open_prices.plot import graphBar
from open_prices.widgets import selectedAllYear, slider

st.set_page_config(page_title="Ventes par devise", layout="wide")

st.title("Ventes par devise")

df: pd.DataFrame = pd.read_parquet(f"{PROCESSED_DATA_FILE}", engine="fastparquet")

df["date"] = pd.to_datetime(df["date"], errors="coerce")
df["year"] = df["date"].dt.year.astype("int")
df["product_name"].replace("", np.nan, inplace=True)
df["product_name"].replace(" ", np.nan, inplace=True)
df["proof_currency"].replace("", np.nan, inplace=True)
df["proof_currency"].replace(" ", np.nan, inplace=True)
dfProduct: pd.DataFrame = df.dropna(subset=["product_name", "proof_currency", "price"], how="any")
df["category_tag"].replace("", np.nan, inplace=True)
df["category_tag"].replace(" ", np.nan, inplace=True)
dfCategory: pd.DataFrame = df.dropna(subset=["category_tag", "proof_currency", "price"], how="any")

BASE_DIR: Path = Path(__file__).parent.parent
font_path: Path = BASE_DIR / "fonts" / "NotoSans-Regular.ttf"
properties: fm.FontProperties = fm.FontProperties(fname=str(font_path))

plt.rcParams['font.family'] = properties.get_name()
plt.rcParams['axes.unicode_minus'] = False

(
    tabTopNCurrenciesProducts,
    tabAllCurrenciesProducts,
    tabTopNCurrenciesCategories,
    tabAllCurrenciesCategories,
) = st.tabs(
    [
        "Top N devises (produits)",
        "Toutes les devises (produits)",
        "Top N devises (catégories)",
        "Toutes les devises (catégories)",
    ]
)

with tabTopNCurrenciesProducts:
    currencySlider = slider(id="topCurrencyProductSlider", title="Nombre de devises à afficher")
    selectedYears = selectedAllYear(dfProduct, "topCurrencyProductYear")
    (currencyCounts, salesKiloTop, salesUnitTop) = computeSalesMetricsForYear(
        dfProduct, "proof_currency", selectedYears, True, currencySlider
    )
    if selectedYears is not None:
        title = f"Top {currencySlider} devises avec le plus de ventes ({selectedYears})"
    else:
        title = f"Top {currencySlider} devises avec le plus de ventes (toutes années)"
    fig, ax = graphBar(currencyCounts, "nombre de ventes", "Devises", title, properties)
    st.pyplot(fig)
    with st.expander("Voir les données"):
        dfTop = makeDfWithSomeMetrics(currencyCounts, "devise", salesKiloTop, salesUnitTop)
        st.dataframe(dfTop)

with tabAllCurrenciesProducts:
    selectedYears = selectedAllYear(dfProduct, "allCurrencyProductYear")
    (currencyCounts, salesKiloTop, salesUnitTop) = computeSalesMetricsForYear(
        dfProduct, "proof_currency", selectedYears, False
    )
    dfTop = makeDfWithSomeMetrics(currencyCounts, "devise", salesKiloTop, salesUnitTop)
    st.dataframe(dfTop, height=597)

with tabTopNCurrenciesCategories:
    currencySlider = slider("topCurrencyCategorySlider", "Nombre de devises à afficher")
    selectedYears = selectedAllYear(dfCategory, "topCurrencyCategoryYear")
    (currencyCounts, salesKiloTop, salesUnitTop) = computeSalesMetricsForYear(
        dfCategory, "proof_currency", selectedYears, True, currencySlider
    )
    if selectedYears is not None:
        title = f"Top {currencySlider} devises avec le plus de ventes ({selectedYears})"
    else:
        title = f"Top {currencySlider} devises avec le plus de ventes (toutes années)"
    fig, ax = graphBar(currencyCounts, "nombre de ventes", "Devises", title, properties)
    st.pyplot(fig)
    with st.expander("Voir les données"):
        dfTop = makeDfWithSomeMetrics(currencyCounts, "devise", salesKiloTop, salesUnitTop)
        st.dataframe(dfTop)

with tabAllCurrenciesCategories:
    selectedYears = selectedAllYear(dfCategory, "allCurrencyCategoryYear")
    (currencyCounts, salesKiloTop, salesUnitTop) = computeSalesMetricsForYear(
        dfCategory, "proof_currency", selectedYears, False
    )
    dfTop = makeDfWithSomeMetrics(currencyCounts, "devise", salesKiloTop, salesUnitTop)
    st.dataframe(dfTop, height=597)
