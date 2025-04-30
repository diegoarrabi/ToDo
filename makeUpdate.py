from datetime import date, timedelta

import pandas as pd

from config import csv_path, myLog
from makeTable import makeTable

############################################################################


def makeUpdate() -> None:
    # THIS SCRIPT UPDATES ALL TASKS

    myLog("-[ TODO CONSOLE ]-")
    myLog("__makeUpdate.py__".upper())
    today = date.today()
    df_todo = pd.read_csv(csv_path, header=None)
    DATE_FORMAT = "%Y-%m-%d"
    DATE_COL = 1
    max_day = None
    for row, _ in df_todo.iterrows():
        task_date = date.fromisoformat(df_todo.at[row, DATE_COL])
        days_between = (task_date - today).days

        # filters out tasks not overdue
        if days_between > -1:
            continue

        if max_day is None:
            max_day = abs(days_between)
        new_duedate = today + timedelta(days=(days_between + max_day))
        df_todo.at[row, DATE_COL] = new_duedate

    saveCSV(df_todo, DATE_COL, DATE_FORMAT)
    makeTable()


############################################################################
############################################################################
############################################################################


def saveCSV(df_list: pd.DataFrame, date_column: int, date_format: str) -> None:
    myLog("method: saveCSV")
    df_list[date_column] = pd.to_datetime(df_list[date_column], format=date_format)
    df_list = df_list.sort_values(by=date_column)
    df_list = df_list.reset_index(drop=True)
    df_list.to_csv(csv_path, index=False, header=False, date_format=date_format)


############################################################################


if __name__ == "__main__":
    makeUpdate()
