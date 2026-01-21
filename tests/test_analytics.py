"""
Unit tests for the OpenPrices analytics module.

Tests the functions:
- computeSalesMetrics
- computeSalesMetricsForYear
- filterItemsByMinSales
- makeDfTrendData

Uses pytest as the test framework.
"""

import pandas as pd

from open_prices.analytics import (
    computeSalesMetrics,
    computeSalesMetricsForYear,
    filterItemsByMinSales,
    makeDfTrendData,
)


class TestComputeSalesMetrics:
    def testComputeSalesMetricsHeadTrue(self) -> None:
        df: pd.DataFrame = pd.DataFrame(
            {
                "category": ["A", "A", "B", "B", "C"],
                "country": ["FR", "FR", "FR", "FR", "FR"],
                "year": [2024, 2024, 2024, 2024, 2024],
                "price_per": ["UNIT", "UNIT", "KILOGRAM", "KILOGRAM", "UNIT"],
                "price": [10, 20, 2, 3, 5],
            }
        )
        res: pd.Series = computeSalesMetrics(df, "category", "country", "FR", 2024, head=True, n=2)

        assert res[0].index.tolist() == ["A", "B"]

    def testComputeSalesMetricsHeadFalse(self) -> None:
        df: pd.DataFrame = pd.DataFrame(
            {
                "category": ["A", "A", "B", "B", "C"],
                "country": ["FR", "FR", "FR", "FR", "FR"],
                "year": [2024, 2024, 2024, 2024, 2024],
                "price_per": ["UNIT", "UNIT", "KILOGRAM", "KILOGRAM", "UNIT"],
                "price": [10, 20, 2, 3, 5],
            }
        )
        res: pd.Series = computeSalesMetrics(df, "category", "country", "FR", 2024, head=False)

        assert res[0].index.tolist() == ["A", "B", "C"]

    def testComputeSalesMetricsPriceAverageAndCounts(self) -> None:
        df: pd.DataFrame = pd.DataFrame(
            {
                "category": ["A", "A", "B", "B"],
                "country": ["FR", "FR", "FR", "FR"],
                "year": [2024, 2024, 2024, 2024],
                "price_per": ["UNIT", "UNIT", "KILOGRAM", "KILOGRAM"],
                "price": [10, 20, 2, 4],
            }
        )
        (
            productCategoryCounts,
            salesKiloTop,
            priceKiloTop,
            salesUnitTop,
            priceUnitTop,
            totalPrices,
        ) = computeSalesMetrics(df, "category", "country", "FR", 2024, head=False)

        assert priceUnitTop["A"] == 15
        assert priceKiloTop["B"] == 3
        assert salesUnitTop["A"] == 2
        assert salesKiloTop["B"] == 2

    def testComputeSalesMetricsTotalPricesSum(self) -> None:
        df: pd.DataFrame = pd.DataFrame(
            {
                "category": ["A", "A", "B", "B"],
                "country": ["FR", "FR", "FR", "FR"],
                "year": [2024, 2024, 2024, 2024],
                "price_per": ["UNIT", "UNIT", "KILOGRAM", "KILOGRAM"],
                "price": [10, 20, 2, 4],
            }
        )
        (
            productCategoryCounts,
            salesKiloTop,
            priceKiloTop,
            salesUnitTop,
            priceUnitTop,
            totalPrices,
        ) = computeSalesMetrics(df, "category", "country", "FR", 2024, head=False)
        expected_total: int = 2 * 15 + 2 * 3

        assert totalPrices.sum() == expected_total


class TestComputeSalesMetricsForYear:
    def testComputeSalesMetricsForYearFilterYear(self) -> None:
        df: pd.DataFrame = pd.DataFrame(
            {
                "category": ["A", "B", "C", "B"],
                "year": [2024, 2024, 2024, 2023],
                "price_per": ["UNIT", "UNIT", "UNIT", "UNIT"],
            }
        )
        dimensionCounts, salesKiloTop, salesUnitTop = computeSalesMetricsForYear(
            df, "category", 2024, head=False
        )

        assert dimensionCounts.index.tolist() == ["A", "B", "C"]

    def testComputeSalesMetricsForYearNoFilterYear(self) -> None:
        df: pd.DataFrame = pd.DataFrame(
            {
                "category": ["A", "B", "C"],
                "year": [2024, 2023, 2022],
                "price_per": ["UNIT", "UNIT", "UNIT"],
            }
        )
        dimensionCounts, salesKiloTop, salesUnitTop = computeSalesMetricsForYear(
            df, "category", None, head=False
        )

        assert dimensionCounts.index.tolist() == ["A", "B", "C"]

    def testComputeSalesMetricsForYearHeadTrue(self) -> None:
        df: pd.DataFrame = pd.DataFrame(
            {
                "category": ["A", "A", "B", "B", "C"],
                "year": [2024, 2024, 2024, 2024, 2024],
                "price_per": ["UNIT", "UNIT", "KILOGRAM", "KILOGRAM", "UNIT"],
                "price": [10, 20, 2, 3, 5],
            }
        )
        dimensionCounts, salesKiloTop, salesUnitTop = computeSalesMetricsForYear(
            df, "category", 2024, head=True, n=2
        )

        assert dimensionCounts.index.tolist() == ["A", "B"]

    def testComputeSalesMetricsForYearHeadFalse(self) -> None:
        df: pd.DataFrame = pd.DataFrame(
            {
                "category": ["A", "A", "B", "B", "C"],
                "year": [2024, 2024, 2024, 2024, 2024],
                "price_per": ["UNIT", "UNIT", "KILOGRAM", "KILOGRAM", "UNIT"],
                "price": [10, 20, 2, 3, 5],
            }
        )
        dimensionCounts, salesKiloTop, salesUnitTop = computeSalesMetricsForYear(
            df, "category", 2024, head=False
        )

        assert dimensionCounts.index.tolist() == ["A", "B", "C"]

    def testComputeSalesMetricsForYearSalesKiloUnit(self) -> None:
        df: pd.DataFrame = pd.DataFrame(
            {
                "category": ["A", "A", "A", "B"],
                "year": [2024, 2024, 2024, 2024],
                "price_per": ["KILOGRAM", "KILOGRAM", "UNIT", "UNIT"],
                "price": [2, 2, 10, 20],
            }
        )
        dimensionCounts, salesKiloTop, salesUnitTop = computeSalesMetricsForYear(
            df, "category", 2024, head=False
        )

        assert salesKiloTop["A"] == 2
        assert salesUnitTop["B"] == 1


class TestFilterItemsByMinSales:
    def testFilterItemsByMinSalesMinSales(self) -> None:
        df: pd.DataFrame = pd.DataFrame(
            {
                "country": ["FR", "FR", "FR", "FR", "FR"],
                "year": [2024, 2024, 2024, 2024, 2024],
                "item": ["A", "A", "B", "B", "B"],
                "month": [1, 1, 1, 2, 2],
            }
        )
        result: pd.DataFrame = filterItemsByMinSales(
            df,
            filterOn="country",
            columnName="item",
            selectCountryCurrency="FR",
            selectedYears=2024,
            minSales=3,
            minMonths=1,
        )

        assert set(result["item"]) == {"B"}

    def testFilterItemsByMinSalesMinMonths(self) -> None:
        df: pd.DataFrame = pd.DataFrame(
            {
                "country": ["FR", "FR", "FR", "FR"],
                "year": [2024, 2024, 2024, 2024],
                "item": ["A", "A", "B", "B"],
                "month": [1, 2, 1, 1],
            }
        )
        result: pd.DataFrame = filterItemsByMinSales(
            df,
            filterOn="country",
            columnName="item",
            selectCountryCurrency="FR",
            selectedYears=2024,
            minSales=1,
            minMonths=2,
        )

        assert set(result["item"]) == {"A"}

    def testFilterItemsByMinSalesIntersection(self) -> None:
        df: pd.DataFrame = pd.DataFrame(
            {
                "country": ["FR", "FR", "FR", "FR", "FR", "FR"],
                "year": [2024, 2024, 2024, 2024, 2024, 2024],
                "item": ["A", "A", "B", "B", "C", "C"],
                "month": [1, 2, 1, 1, 1, 2],
            }
        )
        result: pd.DataFrame = filterItemsByMinSales(
            df,
            filterOn="country",
            columnName="item",
            selectCountryCurrency="FR",
            selectedYears=2024,
            minSales=2,
            minMonths=2,
        )

        assert set(result["item"]) == {"A", "C"}

    def testFilterItemsByMinSalesEmpty(self) -> None:
        df = pd.DataFrame(columns=["country", "year", "item", "month"])
        result: pd.DataFrame = filterItemsByMinSales(
            df,
            filterOn="country",
            columnName="item",
            selectCountryCurrency="FR",
            selectedYears=2024,
        )

        assert result.empty

    class TestMakeDfTrendData:
        def testMakeDfTrendDataEmpty(self) -> None:
            df: pd.DataFrame = pd.DataFrame(columns=["country", "year", "item", "month"])
            result: pd.DataFrame = makeDfTrendData(
                df,
                filterOn="country",
                columnName="item",
                selectCountryCurrency="FR",
                selectedYears=2024,
                selectedItems=["A"],
            )

            assert len(result) == 12
            assert result["count"].sum() == 0
