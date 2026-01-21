"""
Streamlit page displaying sales metrics by country.

Provides four tabs:
- Top N countries (products)
- All countries (products)
- Top N countries (categories)
- All countries (categories)

Each tab shows either a horizontal bar chart or a data table based on the
selected year(s) and country counts.
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

st.set_page_config(page_title="Ventes par pays", layout="wide")

st.title("Ventes par pays")

df: pd.DataFrame = pd.read_parquet(f"{PROCESSED_DATA_FILE}", engine="fastparquet")

df["date"] = pd.to_datetime(df["date"], errors="coerce")
df["year"] = df["date"].dt.year.astype("int")
df["product_name"].replace("", np.nan, inplace=True)
df["product_name"].replace(" ", np.nan, inplace=True)
df["location_osm_address_country"].replace("", np.nan, inplace=True)
df["location_osm_address_country"].replace(" ", np.nan, inplace=True)
dfProduct: pd.DataFrame = df.dropna(
    subset=["product_name", "location_osm_address_country", "price"], how="any"
)
df["category_tag"].replace("", np.nan, inplace=True)
df["category_tag"].replace(" ", np.nan, inplace=True)
dfCategory: pd.DataFrame = df.dropna(
    subset=["category_tag", "location_osm_address_country", "price"], how="any"
)

BASE_DIR: Path = Path(__file__).parent.parent
font_path: Path = BASE_DIR / "fonts" / "NotoSans-Regular.ttf"
properties: fm.FontProperties = fm.FontProperties(fname=str(font_path))

plt.rcParams['font.family'] = properties.get_name()
plt.rcParams['axes.unicode_minus'] = False

(
    tabTopNCountriesProducts,
    tabAllCountriesProducts,
    tabTopNCountriesCategories,
    tabAllCountriesCategories,
) = st.tabs(
    [
        "Top N pays (produits)",
        "Tous les pays (produits)",
        "Top N pays (catégories)",
        "Tous les pays (catégories)",
    ]
)

with tabTopNCountriesProducts:
    countrySlider = slider("topCountryProductSlider", title="Nombre de pays à afficher")
    selectedYears = selectedAllYear(dfProduct, "topCountryProductYear")
    (countryCounts, salesKiloTop, salesUnitTop) = computeSalesMetricsForYear(
        dfProduct, "location_osm_address_country", selectedYears, True, countrySlider
    )
    if selectedYears is not None:
        title = f"Top {countrySlider} pays avec le plus de ventes ({selectedYears})"
    else:
        title = f"Top {countrySlider} pays avec le plus de ventes (toutes années)"
    fig, ax = graphBar(countryCounts, "nombre de ventes", "Pays", title, properties)
    st.pyplot(fig)
    with st.expander("Voir les données"):
        dfTop = makeDfWithSomeMetrics(countryCounts, "pays", salesKiloTop, salesUnitTop)
        st.dataframe(dfTop)

with tabAllCountriesProducts:
    selectedYears = selectedAllYear(dfProduct, "allCountryProductYear")
    (countryCounts, salesKiloTop, salesUnitTop) = computeSalesMetricsForYear(
        dfProduct, "location_osm_address_country", selectedYears, False
    )
    dfTop = makeDfWithSomeMetrics(countryCounts, "pays", salesKiloTop, salesUnitTop)
    st.dataframe(dfTop, height=597)

with tabTopNCountriesCategories:
    countrySlider = slider("topCountryCategorySlider", title="Nombre de pays à afficher")
    selectedYears = selectedAllYear(dfCategory, "topCountryCategoryYear")
    (countryCounts, salesKiloTop, salesUnitTop) = computeSalesMetricsForYear(
        dfCategory, "location_osm_address_country", selectedYears, True, countrySlider
    )
    if selectedYears is not None:
        title = f"Top {countrySlider} pays avec le plus de ventes ({selectedYears})"
    else:
        title = f"Top {countrySlider} pays avec le plus de ventes (toutes années)"
    fig, ax = graphBar(countryCounts, "nombre de ventes", "Pays", title, properties)
    st.pyplot(fig)
    with st.expander("Voir les données"):
        dfTop = makeDfWithSomeMetrics(countryCounts, "pays", salesKiloTop, salesUnitTop)
        st.dataframe(dfTop)

with tabAllCountriesCategories:
    selectedYears = selectedAllYear(dfCategory, "allCountryCategoryYear")
    (countryCounts, salesKiloTop, salesUnitTop) = computeSalesMetricsForYear(
        dfCategory, "location_osm_address_country", selectedYears, False
    )
    dfTop = makeDfWithSomeMetrics(countryCounts, "pays", salesKiloTop, salesUnitTop)
    st.dataframe(dfTop, height=597)
