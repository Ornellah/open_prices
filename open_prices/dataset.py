import pandas as pd


def noneSumCalc(df: pd.DataFrame):
    dfNone = pd.DataFrame({"columns": pd.Series(dtype='str'), "noneSum": pd.Series(dtype='float')})
    for i in df:
        colSum = df[f"{i}"].isna().sum()
        dfSize = df.shape[0]
        noneSum = colSum / dfSize
        new_row = pd.DataFrame([{"columns": i, "noneSum": noneSum}])
        dfNone = pd.concat([dfNone, new_row], ignore_index=True)
    return dfNone


def checkListTypeAndConvert(df: pd.DataFrame, convertColumnList: bool):
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
    for i in df:
        print(f"\n--- {i} ---")
        print(df[i].nunique())
        print(df[i].unique())
