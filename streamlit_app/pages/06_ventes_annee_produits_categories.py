"""
Streamlit page displaying annual sales by product and category.

Provides four tabs:
- Top N products
- All products
- Top N categories
- All categories

Each tab shows either a horizontal bar chart or a data table based on the
selected year(s), filter (currency or country), and top N selection.
"""

from pathlib import Path

import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

from open_prices.analytics import computeSalesMetrics, makeDfWithAllMetrics
from open_prices.config import PROCESSED_DATA_FILE
from open_prices.plot import graphBar
from open_prices.widgets import selectedCurrencyOrCountry, selectedYear, slider

st.set_page_config(page_title="Ventes annuelles par produit et catégorie", layout="wide")

st.title("Ventes annuelles par produit et catégorie")

df: pd.DataFrame = pd.read_parquet(
    f"{PROCESSED_DATA_FILE}",
    engine="fastparquet",
)

df["date"] = pd.to_datetime(df["date"], errors="coerce")
df["year"] = df["date"].dt.year.astype("int")
df["product_name"].replace("", np.nan, inplace=True)
df["product_name"].replace(" ", np.nan, inplace=True)
dfProduct: pd.DataFrame = df.dropna(subset=["product_name", "price"], how="any")
df["category_tag"].replace("", np.nan, inplace=True)
df["category_tag"].replace(" ", np.nan, inplace=True)
dfCategory: pd.DataFrame = df.dropna(subset=["category_tag", "price"], how="any")

currenciesProduct: pd.DataFrame = dfProduct["proof_currency"].drop_duplicates().sort_values()
currenciesCategory: pd.DataFrame = dfCategory["proof_currency"].drop_duplicates().sort_values()
countryProduct: pd.DataFrame = (
    dfProduct["location_osm_address_country"].drop_duplicates().sort_values()
)
countryCategory: pd.DataFrame = (
    dfCategory["location_osm_address_country"].drop_duplicates().sort_values()
)

BASE_DIR: Path = Path(__file__).parent.parent
font_path: Path = BASE_DIR / "fonts" / "NotoSans-Regular.ttf"
properties: fm.FontProperties = fm.FontProperties(fname=str(font_path))

plt.rcParams['font.family'] = properties.get_name()
plt.rcParams['axes.unicode_minus'] = False

tabTopNProducts, tabAllProducts, tabTopNCategories, tabAllCategories = st.tabs(
    [
        "Top N produits",
        "Tous les produits",
        "Top N catégories",
        "Toutes les catégories",
    ]
)

with tabTopNProducts:
    productSlider = slider(id="topProductSlider", title="Nombre de produits à afficher")
    filterColumn, filterValue = selectedCurrencyOrCountry(
        currenciesProduct, countryProduct, "topProductCurrency"
    )
    selectedYears = selectedYear(dfProduct, "topProductYear")
    (productCounts, salesKiloTop, priceKiloTop, salesUnitTop, priceUnitTop, totalPrices) = (
        computeSalesMetrics(
            dfProduct,
            "product_name",
            filterColumn,
            filterValue,
            selectedYears,
            True,
            productSlider,
        )
    )
    fig, ax = graphBar(
        xlabel="Nombre de ventes",
        ylabel="Produits",
        title=f"top {productSlider} produits les plus vendus",
        productCategoryCounts=productCounts,
        properties=properties,
    )
    st.pyplot(fig)
    with st.expander("Voir les données"):
        dfTop = makeDfWithAllMetrics(
            productCounts, salesKiloTop, priceKiloTop, salesUnitTop, priceUnitTop, totalPrices
        )
        st.dataframe(dfTop)

with tabAllProducts:
    filterColumn, filterValue = selectedCurrencyOrCountry(
        currenciesProduct, countryProduct, "allProductCurrency"
    )
    selectedYears = selectedYear(dfProduct, "allProductYear")
    (productCounts, salesKiloTop, priceKiloTop, salesUnitTop, priceUnitTop, totalPrices) = (
        computeSalesMetrics(
            dfProduct, "product_name", filterColumn, filterValue, selectedYears, False
        )
    )
    dfTop = makeDfWithAllMetrics(
        productCounts, salesKiloTop, priceKiloTop, salesUnitTop, priceUnitTop, totalPrices
    )
    st.dataframe(dfTop, height=597)

with tabTopNCategories:
    categorySlider = slider(id="topCategorySlider", title="Nombre de catégories à afficher")
    filterColumn, filterValue = selectedCurrencyOrCountry(
        currenciesCategory, countryCategory, "topCategoryCurrency"
    )
    selectedYears = selectedYear(dfCategory, "topCategoryYear")
    (categoryCounts, salesKiloTop, priceKiloTop, salesUnitTop, priceUnitTop, totalPrices) = (
        computeSalesMetrics(
            dfCategory,
            "category_tag",
            filterColumn,
            filterValue,
            selectedYears,
            True,
            categorySlider,
        )
    )
    fig, ax = graphBar(
        xlabel="Nombre de ventes",
        ylabel="Catégories",
        title=f"top {categorySlider} catégories les plus vendus",
        productCategoryCounts=categoryCounts,
        properties=properties,
    )
    st.pyplot(fig)
    with st.expander("Voir les données"):
        dfTop = makeDfWithAllMetrics(
            categoryCounts, salesKiloTop, priceKiloTop, salesUnitTop, priceUnitTop, totalPrices
        )
        st.dataframe(dfTop)

with tabAllCategories:
    filterColumn, filterValue = selectedCurrencyOrCountry(
        currenciesCategory, countryCategory, "allCategoryCurrency"
    )
    selectedYears = selectedYear(dfCategory, "allCategoryYear")
    (categoryCounts, salesKiloTop, priceKiloTop, salesUnitTop, priceUnitTop, totalPrices) = (
        computeSalesMetrics(
            dfCategory, "category_tag", filterColumn, filterValue, selectedYears, False
        )
    )
    dfTop = makeDfWithAllMetrics(
        categoryCounts, salesKiloTop, priceKiloTop, salesUnitTop, priceUnitTop, totalPrices
    )
    st.dataframe(dfTop, height=597)
