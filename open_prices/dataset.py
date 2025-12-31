"""
Dataset module for OpenPrices.

Provides functions for processing and analyzing dataframes.
"""

import pandas as pd


def noneSumCalc(df: pd.DataFrame):
    """
    Calculate the proportion of missing values for each column in a DataFrame.

    This function iterates over all columns of the input DataFrame and computes
    the fraction of missing values (`NaN`) for each column. It returns a new
    DataFrame summarizing these proportions.

    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame to analyze.

    Returns
    -------
    pandas.DataFrame
        A DataFrame with two columns:
        - 'columns': the column names from the input DataFrame
        - 'noneSum': the proportion of missing values in each column

    Examples
    --------
    >>> import pandas as pd
    >>> data = {'A': [1, None, 3], 'B': [None, None, 3]}
    >>> df = pd.DataFrame(data)
    >>> noneSumCalc(df)
      columns  noneSum
    0       A  0.33
    1       B  0.66

    """
    dfNone = pd.DataFrame({"columns": pd.Series(dtype='str'), "noneSum": pd.Series(dtype='float')})
    for i in df:
        colSum = df[f"{i}"].isna().sum()
        dfSize = df.shape[0]
        noneSum = colSum / dfSize
        new_row = pd.DataFrame([{"columns": i, "noneSum": noneSum}])
        dfNone = pd.concat([dfNone, new_row], ignore_index=True)
    return dfNone


def checkListTypeAndConvert(df: pd.DataFrame, convertColumnList: bool):
    """
    Identify columns containing list or tuple elements and optionally convert them to strings.

    This function inspects each column of the input DataFrame. If the first
    non-null value in a column is of type `list` or `tuple`, the column name
    is added to the result list. If `convertColumnList` is True, the identified
    columns are converted to strings in-place in the DataFrame.

    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame to analyze.
    convertColumnList : bool
        If True, convert columns containing lists or tuples to strings in-place.

    Returns
    -------
    list
        List of column names that contained lists or tuples. If `convertColumnList`
        is True, this list is cleared after conversion, and the returned list
        will be empty.

    Notes
    -----
    - The function only checks the first non-null value in each column.
    - Conversion to string modifies the original DataFrame in-place.

    Examples
    --------
    >>> import pandas as pd
    >>> df = pd.DataFrame({'A': [[1,2], [3,4]], 'B': ['x', 'y']})
    >>> checkListTypeAndConvert(df, convertColumnList=False)
    ['A']
    >>> checkListTypeAndConvert(df, convertColumnList=True)
    []
    >>> df['A'].dtype
    dtype('O')

    """
    result = []
    columnList = []
    for i in df:
        listCheck = df[i][df[f"{i}"].notnull()]
        if len(listCheck) != 0:
            elementList = listCheck.values[0]
            if type(elementList).__name__ in ["list", "tuple"]:
                result.append(i)
    if len(result) != 0 and convertColumnList:
        columnList.extend(result)
        for i in columnList:
            df[f"{i}"] = df[f'{i}'].astype(str)
        result.clear()
    return result


def printColumnUnique(df: pd.DataFrame):
    """
    Print the unique values and their counts for each column in a DataFrame.

    This function iterates over all columns of the input DataFrame and prints,
    for each column, its name, the number of unique values, and the array of
    unique values. It doesn't return any value.

    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame to inspect.

    Returns
    -------
    None
        The function prints the output to the console and doesn't modify the DataFrame.

    Notes
    -----
    - Useful for quickly checking the distribution of values in each column.
    - Output is printed to standard output; no return value.

    Examples
    --------
    >>> import pandas as pd
    >>> df = pd.DataFrame({'A': [1, 2, 2], 'B': ['x', 'y', 'x']})
    >>> printColumnUnique(df)

    --- A ---
    2
    [1 2]

    --- B ---
    2
    ['x' 'y']

    """
    for i in df:
        print(f"\n--- {i} ---")
        print(df[i].nunique())
        print(df[i].unique())
