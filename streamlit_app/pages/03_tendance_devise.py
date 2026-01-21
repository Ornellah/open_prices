"""
Streamlit page showing sales trends over time.

Provides four tabs:
- Single product
- Multiple products
- Single category
- Multiple categories

Each tab lets the user select year(s), currency, and item(s), then displays
either a line chart (matplotlib) or bar chart (plotly) with an optional data table.
"""

from pathlib import Path

import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

from open_prices.analytics import filterItemsByMinSales, makeDfTrendData
from open_prices.config import PROCESSED_DATA_FILE
from open_prices.plot import trendGraphBar, trendGraphLine
from open_prices.widgets import selectedCurrency, selectedItem, selectedMultipleItems, selectedYear

st.set_page_config(page_title="Tendances temporelles", layout="wide")

st.title("Tendances temporelles des ventes")

df: pd.DataFrame = pd.read_parquet(f"{PROCESSED_DATA_FILE}", engine="fastparquet")

df["date"] = pd.to_datetime(df["date"], errors="coerce")
df["year"] = df["date"].dt.year.astype("int")
df["month"] = df["date"].dt.month
df["product_name"].replace("", np.nan, inplace=True)
df["product_name"].replace(" ", np.nan, inplace=True)
dfProduct: pd.DataFrame = df.dropna(subset=["product_name", "price"], how="any")
df["category_tag"].replace("", np.nan, inplace=True)
df["category_tag"].replace(" ", np.nan, inplace=True)
dfCategory: pd.DataFrame = df.dropna(subset=["category_tag", "price"], how="any")

currenciesProduct: pd.DataFrame = dfProduct["proof_currency"].drop_duplicates().sort_values()
currenciesCategory: pd.DataFrame = dfCategory["proof_currency"].drop_duplicates().sort_values()

BASE_DIR: Path = Path(__file__).parent.parent
font_path: Path = BASE_DIR / "fonts" / "NotoSans-Regular.ttf"
properties: fm.FontProperties = fm.FontProperties(fname=str(font_path))

plt.rcParams['font.family'] = properties.get_name()
plt.rcParams['axes.unicode_minus'] = False

tabSingleProduct, tabMultipleProducts, tabSingleCategory, tabMultipleCategories = st.tabs(
    ["Un produit", "Plusieurs produits", "Une catégorie", "Plusieurs catégories"]
)

with tabSingleProduct:
    selectedYears = selectedYear(dfProduct, "singleProductYear")
    selectedCurrencies = selectedCurrency(currenciesProduct, "singleProductCurrency")

    dfFiltered = filterItemsByMinSales(
        dfProduct, "proof_currency", "product_name", selectedCurrencies, selectedYears
    )

    if len(dfFiltered) > 0:
        selectedProduct = selectedItem(dfFiltered, "product_name", "singleProduct", "un produit")

        graphType = st.radio(
            "Type de graphique", ["Ligne", "Barres"], key="singleProductGraphType", horizontal=True
        )

        trendData = makeDfTrendData(
            dfProduct,
            "proof_currency",
            "product_name",
            selectedCurrencies,
            selectedYears,
            [selectedProduct],
        )

        if graphType == "Ligne":
            fig, ax = trendGraphLine(
                trendData, selectedCurrencies, selectedYears, "Produit", properties
            )
            st.pyplot(fig)
        else:
            fig2 = trendGraphBar(trendData, selectedCurrencies, selectedYears, "Produit")
            st.plotly_chart(fig2)

        with st.expander("Voir les données"):
            displayData = trendData.pivot(index="month", columns="item", values="count")
            displayData.index.name = "Mois"
            st.dataframe(displayData)
    else:
        st.warning("Aucun produit ne répond aux critères (min. 10 ventes sur 2 mois différents)")

with tabMultipleProducts:
    selectedYears = selectedYear(dfProduct, "multipleProductsYear")
    selectedCurrencies = selectedCurrency(currenciesProduct, "multipleProductsCurrency")

    dfFiltered = filterItemsByMinSales(
        dfProduct, "proof_currency", "product_name", selectedCurrencies, selectedYears
    )

    if len(dfFiltered) > 0:
        selectedProducts = selectedMultipleItems(
            dfFiltered, "product_name", "multipleProducts", "produits"
        )

        if selectedProducts:
            graphType = st.radio(
                "Type de graphique",
                ["Ligne", "Barres"],
                key="multipleProductsGraphType",
                horizontal=True,
            )

            trendData = makeDfTrendData(
                dfProduct,
                "proof_currency",
                "product_name",
                selectedCurrencies,
                selectedYears,
                selectedProducts,
            )

            if graphType == "Ligne":
                fig, ax = trendGraphLine(
                    trendData, selectedCurrencies, selectedYears, "Produits", properties
                )
                st.pyplot(fig)
            else:
                fig2 = trendGraphBar(trendData, selectedCurrencies, selectedYears, "Produits")
                st.plotly_chart(fig2)

            with st.expander("Voir les données"):
                displayData = trendData.pivot(index="month", columns="item", values="count")
                displayData.index.name = "Mois"
                st.dataframe(displayData)
        else:
            st.info("Veuillez sélectionner au moins un produit")
    else:
        st.warning("Aucun produit ne répond aux critères (min. 10 ventes sur 2 mois différents)")

with tabSingleCategory:
    selectedYears = selectedYear(dfCategory, "singleCategoryYear")
    selectedCurrencies = selectedCurrency(currenciesCategory, "singleCategoryCurrency")

    dfFiltered = filterItemsByMinSales(
        dfCategory, "proof_currency", "category_tag", selectedCurrencies, selectedYears
    )

    if len(dfFiltered) > 0:
        selectedCategory = selectedItem(
            dfFiltered, "category_tag", "singleCategory", "une catégorie"
        )

        graphType = st.radio(
            "Type de graphique",
            ["Ligne", "Barres"],
            key="singleCategoryGraphType",
            horizontal=True,
        )

        trendData = makeDfTrendData(
            dfCategory,
            "proof_currency",
            "category_tag",
            selectedCurrencies,
            selectedYears,
            [selectedCategory],
        )

        if graphType == "Ligne":
            fig, ax = trendGraphLine(
                trendData, selectedCurrencies, selectedYears, "Catégorie", properties
            )
            st.pyplot(fig)
        else:
            fig2 = trendGraphBar(trendData, selectedCurrencies, selectedYears, "Catégorie")
            st.plotly_chart(fig2)

        with st.expander("Voir les données"):
            displayData = trendData.pivot(index="month", columns="item", values="count")
            displayData.index.name = "Mois"
            st.dataframe(displayData)
    else:
        st.warning(
            "Aucune catégorie ne répond aux critères (min. 10 ventes sur 2 mois différents)"
        )

with tabMultipleCategories:
    selectedYears = selectedYear(dfCategory, "multipleCategoriesYear")
    selectedCurrencies = selectedCurrency(currenciesCategory, "multipleCategoriesCurrency")

    dfFiltered = filterItemsByMinSales(
        dfCategory, "proof_currency", "category_tag", selectedCurrencies, selectedYears
    )

    if len(dfFiltered) > 0:
        selectedCategories = selectedMultipleItems(
            dfFiltered, "category_tag", "multipleCategories", "catégories"
        )

        if selectedCategories:
            graphType = st.radio(
                "Type de graphique",
                ["Ligne", "Barres"],
                key="multipleCategoriesGraphType",
                horizontal=True,
            )

            trendData = makeDfTrendData(
                dfCategory,
                "proof_currency",
                "category_tag",
                selectedCurrencies,
                selectedYears,
                selectedCategories,
            )

            if graphType == "Ligne":
                fig, ax = trendGraphLine(
                    trendData, selectedCurrencies, selectedYears, "Catégories", properties
                )
                st.pyplot(fig)
            else:
                fig2 = trendGraphBar(trendData, selectedCurrencies, selectedYears, "Catégories")
                st.plotly_chart(fig2)

            with st.expander("Voir les données"):
                displayData = trendData.pivot(index="month", columns="item", values="count")
                displayData.index.name = "Mois"
                st.dataframe(displayData)
        else:
            st.info("Veuillez sélectionner au moins une catégorie")
    else:
        st.warning(
            "Aucune catégorie ne répond aux critères (min. 10 ventes sur 2 mois différents)"
        )
