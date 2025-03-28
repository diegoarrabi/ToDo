from os import path

from sys import argv

import pandas as pd

from datetime import datetime
from datetime import timedelta

from config import log
from config import myLog
from config import csv_path
from config import path_dict
from config import getDialog
from config import copy2Clipboard

from makeTable import makeTable
############################################################################


def makeTasks(arg) -> None:
    # ENTRY POINT FROM INPUT-CONSOLE
    # THIS SCRIPT ADDS/REMOVES TASKS

    myLog('-[ TODO CONSOLE ]-')
    myLog('__makeTasks.py__'.upper())
    if len(arg) != 0:
        logAllTasks(arg)
        for _index, _item in enumerate(arg):
            myLog(f'Item {_index + 1}: {_item.upper()}')
            if "-" in _item:
                task_info = _item.split(" - ")
                duedate_value = (task_info[1].strip()).lower()
                if duedate_value != 'done':
                    taskAddEdit(task_info)
                elif duedate_value == 'done':
                    taskComplete(task_info)
            elif "update" in _item:
                print("UPDATE")
            else:
                myLog(f'UNKNOWN INPUT: {_item}', log.ERROR)
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
        myLog(f'{" "*3}ITEM {_count}: {_item.upper()}')
############################################################################


# def readTextFile(txtfile_name: str, basedir: str) -> list[str]:
#     """
#     Reads Assignment text file and returns a list of each line (stripped of whitespaces)

#     Args:
#         txtfile_name (str): name of text file
#         txtfile_path (str): path of parent folder

#     Returns:
#         list[str]: each line as a value 
#     """
#     myLog('method: readTextFile')
#     txtfile_path = path.join(basedir, txtfile_name)
#     with open(txtfile_path, "r+") as read_file:
#         txt_data = read_file.readlines()
#         txt_data = [x.strip() for x in txt_data]
#         read_file.truncate(0)
#         if len(txt_data) == 0:
#             txt_data = ["_skip"]
#     return txt_data
############################################################################


def taskAddEdit(assignment_info: list[str]) -> None:
    myLog('method: taskAddEdit')

    def invalidInput(item_info: list[str]) -> None:
        """
        If input is invalid, returns '05/25/1996' datetime. 
        That datetime will act as an 'Invalid Input' and will skip the current input

        """
        item_string = ' - '.join(item_info)
        copy2Clipboard(item_string)
        getDialog(f'{str(item_string)}\nis invalid\n\nItem Copied to Clipboard')
        myLog(f"{str(item_string)} NOT VALID")
        return datetime(year=1996, month=5, day=25)
    ############################################################################

    def getFullDate(item_info: list[str]) -> datetime:
        myLog('method: getFullDate')
        today_date = datetime.today().replace(minute=0, second=0, microsecond=0)
        today_str = str(today_date.day)
        if len(today_str) < 2:
            today_str = '0' + today_str
        today_month = str(today_date.month)
        today_compare = int(today_month + today_str)

        if item_info[1].isalpha():
            if item_info[1].lower() in ("today", "t"):
                return today_date
            if item_info[1].lower() == "tomorrow":
                return (today_date + timedelta(days=1))
            return invalidInput(item_info)
        elif "/" in item_info[1]:
            item_index = str(item_info[1]).split('/')
            item_day = item_index[1]
            if len(item_day) < 2:
                item_day = f'0{item_day}'
            item_month = item_index[0]
            item_compare = int(f'{item_month}{item_day}')

            if today_compare <= item_compare:
                item_year = today_date.year
            elif today_compare > item_compare:
                item_year = (today_date.year + 1)
            return datetime(int(item_year), int(item_month), int(item_day))
        else:
            return invalidInput(item_info)
        ############################################################################

    df_todo = pd.read_csv(csv_path, header=None)
    DATE_FORMAT = '%Y-%m-%d'
    ASSIGNMENT_COL = 0
    DATE_COL = 1
    all_assignments_count = len(df_todo.index)
    item_date = getFullDate(assignment_info).strftime(DATE_FORMAT)
    if item_date == "1996-05-25":
        return

    # USING AN INTEGER TO EDIT A TASK
    if assignment_info[0].isdigit():
        myLog('method: taskAddEdit -- EDIT TASK')
        task_label = df_todo.loc[(int(assignment_info[0]) - 1), ASSIGNMENT_COL]
        df_todo.loc[(int(assignment_info[0]) - 1), DATE_COL] = item_date
        saveCSV(df_todo, DATE_COL, DATE_FORMAT)
        return
    for _index in range(all_assignments_count):
        task_label = df_todo.loc[_index, ASSIGNMENT_COL].lower()
        if task_label == assignment_info[0].lower():
            myLog('method: taskAddEdit -- EDIT TASK')
            df_todo.loc[_index, DATE_COL] = item_date
            saveCSV(df_todo, DATE_COL, DATE_FORMAT)
            break
        elif _index == (all_assignments_count - 1):
            myLog('method: taskAddEdit -- ADD TASK')
            new_task = pd.DataFrame([[assignment_info[0], item_date]], columns=df_todo.columns)
            df_todo = pd.concat([new_task, df_todo], ignore_index=True)
            saveCSV(df_todo, DATE_COL, DATE_FORMAT)
            break
############################################################################


def taskComplete(assignment_info: list) -> None:
    myLog('method: taskComplete -- REMOVE TASK')
    df_todo = pd.read_csv(csv_path, header=None)
    DATE_FORMAT = '%Y-%m-%d'
    ASSIGNMENT_COL = 0
    DATE_COL = 1
    all_assignments_count = len(df_todo.index)

    try:
        assignment_info[0] = int(assignment_info[0])
    except ValueError:
        pass

    if isinstance(assignment_info[0], int):
        task_label = df_todo.loc[(assignment_info[0] - 1), ASSIGNMENT_COL]
        df_todo.drop(assignment_info[0] - 1, inplace=True)
        saveCSV(df_todo, DATE_COL, DATE_FORMAT)
        return

    for _index in range(all_assignments_count):
        task_label = df_todo.loc[_index, ASSIGNMENT_COL].lower()
        if task_label == assignment_info[0].lower():
            df_todo.drop(_index, inplace=True)
            saveCSV(df_todo, DATE_COL, DATE_FORMAT)
            break
############################################################################


def saveCSV(df_list, DATE_COL: int, DATE_FORMAT: str) -> None:
    myLog('method: saveCSV')
    df_list[DATE_COL] = pd.to_datetime(df_list[DATE_COL], format=DATE_FORMAT)
    df_list = df_list.sort_values(by=DATE_COL)
    df_list = df_list.reset_index(drop=True)
    df_list.to_csv(csv_path, index=False, header=False, date_format=DATE_FORMAT)
############################################################################


if __name__ == '__main__':
    makeTasks(argv[1:])
