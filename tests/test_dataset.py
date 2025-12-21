import pytest
import pandas as pd
import numpy as np
from open_prices.dataset import noneSumCalc, checkListTypeAndConvert, printColumnUnique

@pytest.fixture
def emptyDf():
    return pd.DataFrame()

@pytest.fixture
def listOnlyDf():
    df = pd.DataFrame({
            "col1": [[1, 2], [3, 4]],
            "col2": [[5], [6]]
    })
    return df

@pytest.fixture
def allNanDf():
    df = pd.DataFrame({
            "a": [np.nan, np.nan],
            "b": [np.nan, np.nan],
    })
    return df

class TestnoneSumCalc:
    def testNoneSumLessEqualOne(self):
        df = pd.DataFrame(
            {
                "a": [1, np.nan, 3],
                "b": [np.nan, np.nan, 2],
            }
        )
        result = noneSumCalc(df)
        assert (result["noneSum"] <= 1).all()

    def testEmptyDataframe(self,emptyDf):
        result = noneSumCalc(emptyDf)
        assert result.empty

    def testDataframeWithoutNan(self):
        df = pd.DataFrame(
            {
                "a": [1, 2, 3],
                "b": [4, 5, 6],
            }
        )
        result = noneSumCalc(df)
        assert (result["noneSum"] == 0).all()

    def testDataframeFullNan(self,allNanDf):
        result = noneSumCalc(allNanDf)
        assert (result["noneSum"] == 1).all()


class TestcheckListTypeAndConvert:
    def testEmptyDataframe(self,emptyDf):
        result = checkListTypeAndConvert(emptyDf, convertColumnList=False)
        assert result == []

    def testDataframeWithoutList(self):
        df = pd.DataFrame(
            {
                "a": [1, 2, 3],
                "b": ["x", "y", "z"],
            }
        )
        result = checkListTypeAndConvert(df, convertColumnList=False)
        assert result == []

    def testOnlyLists(self,listOnlyDf):
        result = checkListTypeAndConvert(listOnlyDf, convertColumnList=False)
        assert result == ["col1", "col2"]

    def testListsAndNonlists(self):
        df = pd.DataFrame({
            "col1": [[1, 2], [3, 4]],
            "col2": [10, 20],
            "col3": [["a"], ["b"]]
        })
        result = checkListTypeAndConvert(df, convertColumnList=False)
        assert result == ["col1", "col3"]

    def testNoConversionIfFalse(self,listOnlyDf):
        checkListTypeAndConvert(listOnlyDf, convertColumnList=False)
        assert isinstance(listOnlyDf["col1"].iloc[0], list)

    def testConversionIfTrue(self,listOnlyDf):
        checkListTypeAndConvert(listOnlyDf, convertColumnList=True)
        assert isinstance(listOnlyDf["col1"].iloc[0], str)

    def testColumnAllNan(self,allNanDf):
        result = checkListTypeAndConvert(allNanDf, convertColumnList=False)
        assert result == []

    def testColumnWithTuples(self):
        df = pd.DataFrame({
            "col1": [(1, 2), (3, 4)],
            "col2": [10, 20]
        })
        result = checkListTypeAndConvert(df, convertColumnList=False)
        assert result == ["col1"]

class TestPrintColumnUnique:
    def testPrintColumnUniqueEmptyDf(self,capsys,emptyDf):
        printColumnUnique(emptyDf)
        captured = capsys.readouterr()
        assert captured.out == "" 