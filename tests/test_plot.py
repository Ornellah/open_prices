"""
Unit tests for the OpenPrices plotting module.

Tests the functions:
- graphBar
- trendGraphLine
- trendGraphBar

Uses pytest as the test framework.
"""

import matplotlib.font_manager as fm
import pandas as pd

from open_prices.plot import graphBar, trendGraphBar, trendGraphLine


def testGraphBarEmptySeries() -> None:
    s: pd.Series = pd.Series(dtype=int)
    fig, ax = graphBar(s, "x", "y", "title", fm.FontProperties())

    assert fig is not None
    assert ax is not None


def testTrendGraphLineEmpty() -> None:
    df: pd.DataFrame = pd.DataFrame(columns=["item", "month", "count"])
    fig, ax = trendGraphLine(df, "EUR", 2024, "Type", fm.FontProperties())

    assert fig is not None
    assert ax is not None


def testTrendGraphBarEmpty() -> None:
    df: pd.DataFrame = pd.DataFrame(columns=["item", "month", "count"])
    fig = trendGraphBar(df, "EUR", 2024, "Type")

    assert len(fig.data) == 0
