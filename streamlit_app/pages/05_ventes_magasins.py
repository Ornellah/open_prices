"""
Streamlit page displaying sales metrics by store.

Provides four tabs:
- Top N stores (products)
- All stores (products)
- Top N stores (categories)
- All stores (categories)

Each tab shows either a horizontal bar chart or a data table based on the
selected year(s) and store sales counts.
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

st.set_page_config(page_title="Ventes par magasin", layout="wide")

st.title("Ventes par magasin")

df: pd.DataFrame = pd.read_parquet(f"{PROCESSED_DATA_FILE}", engine="fastparquet")

df["date"] = pd.to_datetime(df["date"], errors="coerce")
df["year"] = df["date"].dt.year.astype("int")
df["product_name"].replace("", np.nan, inplace=True)
df["product_name"].replace(" ", np.nan, inplace=True)
df["store_name"].replace("", np.nan, inplace=True)
df["store_name"].replace(" ", np.nan, inplace=True)
dfProduct: pd.DataFrame = df.dropna(subset=["product_name", "store_name", "price"], how="any")
df["category_tag"].replace("", np.nan, inplace=True)
df["category_tag"].replace(" ", np.nan, inplace=True)
dfCategory: pd.DataFrame = df.dropna(subset=["category_tag", "store_name", "price"], how="any")

BASE_DIR: Path = Path(__file__).parent.parent
font_path: Path = BASE_DIR / "fonts" / "NotoSans-Regular.ttf"
properties: fm.FontProperties = fm.FontProperties(fname=str(font_path))

plt.rcParams['font.family'] = properties.get_name()
plt.rcParams['axes.unicode_minus'] = False

tabTopNStoresProducts, tabAllStoresProducts, tabTopNStoresCategories, tabAllStoresCategories = (
    st.tabs(
        [
            "Top N magasins (produits)",
            "Tous les magasins (produits)",
            "Top N magasins (catégories)",
            "Tous les magasins (catégories)",
        ]
    )
)

with tabTopNStoresProducts:
    storeSlider = slider("topStoreProductSlider", "Nombre de magasins à afficher")
    selectedYears = selectedAllYear(dfProduct, "topStoreProductYear")
    (storeCounts, salesKiloTop, salesUnitTop) = computeSalesMetricsForYear(
        dfProduct, "store_name", selectedYears, True, storeSlider
    )
    if selectedYears is not None:
        title = f"Top {storeSlider} magasins avec le plus de ventes ({selectedYears})"
    else:
        title = f"Top {storeSlider} magasins avec le plus de ventes (toutes années)"
    fig, ax = graphBar(
        storeCounts,
        "nombre de ventes",
        "Magasin",
        title=f"top {storeSlider} magasins avec le plus de ventes",
        properties=properties,
    )
    st.pyplot(fig)
    with st.expander("Voir les données"):
        dfTop = makeDfWithSomeMetrics(storeCounts, "magasin", salesKiloTop, salesUnitTop)
        st.dataframe(dfTop)

with tabAllStoresProducts:
    selectedYears = selectedAllYear(dfProduct, "allStoreProductYear")
    (storeCounts, salesKiloTop, salesUnitTop) = computeSalesMetricsForYear(
        dfProduct, "store_name", selectedYears, False
    )
    dfTop = makeDfWithSomeMetrics(storeCounts, "magasin", salesKiloTop, salesUnitTop)
    st.dataframe(dfTop, height=597)

with tabTopNStoresCategories:
    storeSlider = slider("topStoreCategorySlider", "Nombre de magasins à afficher")
    selectedYears = selectedAllYear(dfCategory, "topStoreCategoryYear")
    (storeCounts, salesKiloTop, salesUnitTop) = computeSalesMetricsForYear(
        dfCategory, "store_name", selectedYears, True, storeSlider
    )
    if selectedYears is not None:
        title = f"Top {storeSlider} magasins avec le plus de ventes ({selectedYears})"
    else:
        title = f"Top {storeSlider} magasins avec le plus de ventes (toutes années)"
    fig, ax = graphBar(
        storeCounts,
        "nombre de ventes",
        "Magasin",
        title=f"top {storeSlider} magasins avec le plus de ventes",
        properties=properties,
    )
    st.pyplot(fig)
    with st.expander("Voir les données"):
        dfTop = makeDfWithSomeMetrics(storeCounts, "magasin", salesKiloTop, salesUnitTop)
        st.dataframe(dfTop)

with tabAllStoresCategories:
    selectedYears = selectedAllYear(dfCategory, "allStoreCategoryYear")
    (storeCounts, salesKiloTop, salesUnitTop) = computeSalesMetricsForYear(
        dfCategory, "store_name", selectedYears, False
    )
    dfTop = makeDfWithSomeMetrics(storeCounts, "magasin", salesKiloTop, salesUnitTop)
    st.dataframe(dfTop, height=597)
