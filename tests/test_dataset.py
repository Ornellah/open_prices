"""
Unit tests for the OpenPrices dataset module.

Tests the functions:
- noneSumCalc
- checkListTypeAndConvert
- printColumnUnique

Uses pytest as the test framework.
"""

import numpy as np
import pandas as pd
import pytest

from open_prices.dataset import checkListTypeAndConvert, noneSumCalc, printColumnUnique


@pytest.fixture
def emptyDf() -> pd.DataFrame:
    return pd.DataFrame()


@pytest.fixture
def listOnlyDf() -> pd.DataFrame:
    df: pd.DataFrame = pd.DataFrame({"col1": [[1, 2], [3, 4]], "col2": [[5], [6]]})
    return df


@pytest.fixture
def allNanDf() -> pd.DataFrame:
    df: pd.DataFrame = pd.DataFrame(
        {
            "a": [np.nan, np.nan],
            "b": [np.nan, np.nan],
        }
    )
    return df


class TestNoneSumCalc:
    def testNoneSumLessEqualOne(self) -> None:
        df: pd.DataFrame = pd.DataFrame(
            {
                "a": [1, np.nan, 3],
                "b": [np.nan, np.nan, 2],
            }
        )
        result: pd.DataFrame = noneSumCalc(df)
        assert (result["noneSum"] <= 1).all()

    def testEmptyDataframe(self, emptyDf: pd.DataFrame) -> None:
        result: pd.DataFrame = noneSumCalc(emptyDf)
        assert result.empty

    def testDataframeWithoutNan(self) -> None:
        df: pd.DataFrame = pd.DataFrame(
            {
                "a": [1, 2, 3],
                "b": [4, 5, 6],
            }
        )
        result: pd.DataFrame = noneSumCalc(df)
        assert (result["noneSum"] == 0).all()

    def testDataframeFullNan(self, allNanDf: pd.DataFrame) -> None:
        result: pd.DataFrame = noneSumCalc(allNanDf)
        assert (result["noneSum"] == 1).all()


class TestCheckListTypeAndConvert:
    def testEmptyDataframe(self, emptyDf: pd.DataFrame) -> None:
        result: list = checkListTypeAndConvert(emptyDf, convertColumnList=False)
        assert result == []

    def testDataframeWithoutList(self) -> None:
        df: pd.DataFrame = pd.DataFrame(
            {
                "a": [1, 2, 3],
                "b": ["x", "y", "z"],
            }
        )
        result: list = checkListTypeAndConvert(df, convertColumnList=False)
        assert result == []

    def testOnlyLists(self, listOnlyDf: pd.DataFrame) -> None:
        result: list = checkListTypeAndConvert(listOnlyDf, convertColumnList=False)
        assert result == ["col1", "col2"]

    def testListsAndNonlists(self) -> None:
        df: pd.DataFrame = pd.DataFrame(
            {"col1": [[1, 2], [3, 4]], "col2": [10, 20], "col3": [["a"], ["b"]]}
        )
        result: list = checkListTypeAndConvert(df, convertColumnList=False)
        assert result == ["col1", "col3"]

    def testNoConversionIfFalse(self, listOnlyDf: pd.DataFrame) -> None:
        checkListTypeAndConvert(listOnlyDf, convertColumnList=False)
        assert isinstance(listOnlyDf["col1"].iloc[0], list)

    def testConversionIfTrue(self, listOnlyDf: pd.DataFrame) -> None:
        checkListTypeAndConvert(listOnlyDf, convertColumnList=True)
        assert isinstance(listOnlyDf["col1"].iloc[0], str)

    def testColumnAllNan(self, allNanDf: pd.DataFrame) -> None:
        result: list = checkListTypeAndConvert(allNanDf, convertColumnList=False)
        assert result == []

    def testColumnWithTuples(self) -> None:
        df: pd.DataFrame = pd.DataFrame({"col1": [(1, 2), (3, 4)], "col2": [10, 20]})
        result: list = checkListTypeAndConvert(df, convertColumnList=False)
        assert result == ["col1"]


class TestPrintColumnUnique:
    def testPrintColumnUniqueEmptyDf(
        self, capsys: pytest.CaptureFixture[str], emptyDf: pd.DataFrame
    ) -> None:
        printColumnUnique(emptyDf)
        captured = capsys.readouterr()
        assert captured.out == ""
