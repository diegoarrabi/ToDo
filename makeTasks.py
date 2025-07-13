#!/Users/diegoibarra/.config/pyenv/versions/3.13.0/envs/ToDo/bin/python

from datetime import datetime, timedelta
from sys import argv

import pandas as pd
from pandas import DataFrame

from config import copy2Clipboard, csv_path, getDialog, log, myLog
from makeTable import makeTable

from modules.objects import Task, AllTasks

############################################################################

def makeTasks(arg) -> None:
    # ENTRY POINT FROM INPUT-CONSOLE
    # THIS SCRIPT ADDS/REMOVES TASKS

    myLog("-[ TODO CONSOLE ]-")
    myLog("__makeTasks.py__".upper())
    all_tasks = AllTasks()

    todos_list = pd.read_csv(csv_path, header=None)
    for index, row in todos_list.iterrows():
        task_name = row[0]
        task_date = row[1]
        all_tasks.addTask(Task(name=task_name, duedate=task_date))
    all_tasks.printTasks()
    exit()



    if len(arg) != 0:
        logAllTasks(arg)

        for _index, _item in enumerate(arg):
            myLog(f"Item {_index + 1}: {_item.upper()}")
            if "-" in _item:
                task_info = _item.split(" - ")
                if task_info[0].isdigit():
                    task_info[0] = todos_list.iloc[int(task_info[0])-1, 0]
                if "i" in task_info:
                    taskImportance(task_info)
                    continue
                if "r" in task_info:
                    taskRename(task_info)
                    continue
                duedate_value = (task_info[1].strip()).lower()
                if duedate_value != "done":
                    taskAddEdit(task_info)
                elif duedate_value == "done":
                    taskComplete(task_info)
            else:
                myLog(f"UNKNOWN INPUT: {_item}", log.ERROR)
    else:
        myLog("NO ITEMS PROVIDED")
        saveCSV(todos_list)
    makeTable()


############################################################################
############################################################################
############################################################################


def logAllTasks(task_list: list) -> None:
    """
    Logs all tasks at the beginning of the log message

    Args:
        task_list: (list): raw task info
    """
    for _count, _item in enumerate(task_list):
        myLog(f"{' ' * 3}ITEM {_count}: {_item.upper()}")


############################################################################


def taskImportance(assignment_info: list[str]) -> None:
    myLog("method: taskImportance")
    df_todo: DataFrame = pd.read_csv(csv_path, header=None)
    all_assignments_count = len(df_todo.index)

    # USING AN INTEGER TO EDIT A TASK
    for _index in range(all_assignments_count):

        task_label = df_todo.loc[_index, ASSIGNMENT_COL].lower()
        if task_label == assignment_info[0].lower():
            if task_label[-1] == "!":
                myLog("method: taskImportance - NOT IMPORTANT")
                task_label = task_label[:-1]
            else:
                task_label = f"{task_label}!"
                myLog("method: taskImportance - IMPORTANT")
            myLog("method: taskImportance -- IMPORTANT TASK")
            df_todo.loc[_index, ASSIGNMENT_COL] = task_label
            saveCSV(df_todo)
            break


############################################################################


def taskRename(assignment_info: list[str]) -> None:
    myLog("method: taskRename")
    df_todo = pd.read_csv(csv_path, header=None)
    all_assignments_count = len(df_todo.index)

    # USING AN INTEGER TO EDIT A TASK
    if assignment_info[0].isdigit():
        myLog("INTEGERINTEGER-SHOULDNOLONGERRUN - method: taskRename -- RENAME TASK")
        task_label = df_todo.loc[(int(assignment_info[0]) - 1), ASSIGNMENT_COL]
        df_todo.loc[(int(assignment_info[0]) - 1), ASSIGNMENT_COL] = assignment_info[ASSIGNMENT_NEW_NAME]
        saveCSV(df_todo)
        return
    for _index in range(all_assignments_count):
        task_label = df_todo.loc[_index, ASSIGNMENT_COL].lower()
        if task_label == assignment_info[0].lower():
            myLog("method: taskRename -- RENAME TASK")
            df_todo.loc[_index, ASSIGNMENT_COL] = assignment_info[ASSIGNMENT_NEW_NAME]
            saveCSV(df_todo)
            break


############################################################################


def taskAddEdit(assignment_info: list[str]) -> None:
    myLog("method: taskAddEdit")

    def invalidInput(item_info: list[str]) -> None:
        """
        If input is invalid, returns '05/25/1996' datetime.
        That datetime will act as an 'Invalid Input' and will skip the current input

        """
        item_string = " - ".join(item_info)
        copy2Clipboard(item_string)
        getDialog(f"{str(item_string)}\nis invalid\n\nItem Copied to Clipboard")
        myLog(f"{str(item_string)} NOT VALID")
        return datetime(year=1996, month=5, day=25)

    ############################################################################

    def getFullDate(item_info: list[str]) -> datetime:
        myLog("method: getFullDate")
        today_date = datetime.today().replace(minute=0, second=0, microsecond=0)
        today_str = str(today_date.day)
        if len(today_str) < 2:
            today_str = "0" + today_str
        today_month = str(today_date.month)
        today_compare = int(today_month + today_str)

        if item_info[1].isalpha():
            if item_info[1].lower() in ("today", "t"):
                return today_date
            if item_info[1].lower() == "tomorrow":
                return today_date + timedelta(days=1)
            return invalidInput(item_info)
        elif "/" in item_info[1]:
            item_index = str(item_info[1]).split("/")
            item_day = item_index[1]
            if len(item_day) < 2:
                item_day = f"0{item_day}"
            item_month = item_index[0]
            item_compare = int(f"{item_month}{item_day}")

            if today_compare <= item_compare:
                item_year = today_date.year
            elif today_compare > item_compare:
                item_year = today_date.year + 1
            return datetime(int(item_year), int(item_month), int(item_day))
        else:
            return invalidInput(item_info)
        ############################################################################

    df_todo = pd.read_csv(csv_path, header=None)
    all_assignments_count = len(df_todo.index)
    item_date = getFullDate(assignment_info).strftime(DATE_FORMAT)
    if item_date == "1996-05-25":
        return

    # USING AN INTEGER TO EDIT A TASK
    if assignment_info[0].isdigit():
        myLog("INTEGERINTEGER-SHOULDNOLONGERRUN - method: taskAddEdit -- EDIT TASK")
        task_label = df_todo.loc[(int(assignment_info[0]) - 1), ASSIGNMENT_COL]
        df_todo.loc[(int(assignment_info[0]) - 1), DATE_COL] = item_date
        saveCSV(df_todo)
        return
    for _index in range(all_assignments_count):
        task_label = df_todo.loc[_index, ASSIGNMENT_COL].lower()
        if task_label == assignment_info[0].lower():
            myLog("method: taskAddEdit -- EDIT TASK")
            df_todo.loc[_index, DATE_COL] = item_date
            saveCSV(df_todo)
            break
        elif _index == (all_assignments_count - 1):
            myLog("method: taskAddEdit -- ADD TASK")
            new_task = pd.DataFrame([[assignment_info[0], item_date]], columns=df_todo.columns)
            df_todo = pd.concat([new_task, df_todo], ignore_index=True)
            saveCSV(df_todo)
            break


############################################################################


def taskComplete(assignment_info: list) -> None:
    myLog("method: taskComplete -- REMOVE TASK")
    df_todo = pd.read_csv(csv_path, header=None)
    all_assignments_count = len(df_todo.index)

    try:
        assignment_info[0] = int(assignment_info[0])
    except ValueError:
        pass

    if isinstance(assignment_info[0], int):
        task_label = df_todo.loc[(assignment_info[0] - 1), ASSIGNMENT_COL]
        df_todo.drop(assignment_info[0] - 1, inplace=True)
        saveCSV(df_todo)
        return

    for _index in range(all_assignments_count):
        task_label = df_todo.loc[_index, ASSIGNMENT_COL].lower()
        if task_label == assignment_info[0].lower():
            df_todo.drop(_index, inplace=True)
            saveCSV(df_todo)
            break


############################################################################


def sortTasks(df_list):
    df_list[DATE_COL] = pd.to_datetime(df_list[DATE_COL], format=DATE_FORMAT)
    df_list = df_list.sort_values(by=DATE_COL).reset_index(drop=True)
    _location = 0
    for _idx, _row in df_list.iterrows():
        if "!" in _row[ASSIGNMENT_COL]:
            row_obj = df_list.loc[[_idx]]

            df_list = df_list.drop(df_list.index[_idx])

            df_top = df_list.iloc[:_location]
            df_bottom = df_list.iloc[_location:]
            df_list = pd.concat([df_top, row_obj, df_bottom])
            _location += 1
    return df_list


def saveCSV(df_list) -> None:
    myLog("method: saveCSV")
    sorted_df = sortTasks(df_list).reset_index(drop=True)
    sorted_df.to_csv(csv_path, index=False, header=False, date_format=DATE_FORMAT)

############################################################################


if __name__ == "__main__":
    ASSIGNMENT_COL = 0
    DATE_COL = 1
    ASSIGNMENT_NEW_NAME = 2
    DATE_FORMAT = "%Y-%m-%d"
    makeTasks(argv[1:])
