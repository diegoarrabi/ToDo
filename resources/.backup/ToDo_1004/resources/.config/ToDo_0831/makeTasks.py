import pandas as pd
from os import path
from subprocess import run
from datetime import datetime

from config import csv_path, path_dict, txt_doc_name, myLog


def main() -> None:
    project_directory = path_dict['Project']

    for item in readTextFile(txt_doc_name, project_directory):
        if item == "_skip":
            myLog("No Assignment Changes")
            break

        task_info = item.split(" - ")
        duedate_value = (task_info[1].strip()).lower()
        myLog(f'Task: {task_info}')

        if duedate_value != 'done':
            taskAddEdit(task_info)
        elif duedate_value == 'done':
            taskComplete(task_info)

    py_script = "makeTable.py"
    script = path.join(project_directory, py_script)

    run(['python3', script])
    myLog(script)

    myLog('----------------------------DONE----------------------------\n\n')
# ? ###########################################################################
# ? ###########################################################################
# ? ###########################################################################


def readTextFile(txtfile_name: str, basedir: str) -> list[str]:
    """
    Reads Assignment text file and returns a list of each line (stripped of whitespaces)

    Args:
        txtfile_name (str): name of text file
        txtfile_path (str): path of parent folder

    Returns:
        list[str]: each line as a value 
    """

    txtfile_path = path.join(basedir, txtfile_name)
    with open(txtfile_path, "r+") as read_file:
        txt_data = read_file.readlines()
        txt_data = [x.strip() for x in txt_data]
        # read_file.truncate(0)
        if len(txt_data) == 0:
            txt_data = ["_skip"]
    return txt_data
# ? ###########################################################################


def taskAddEdit(assignment_info: list) -> None:

    def getFullDate(item_info: list) -> datetime:
        today_date = datetime.today()
        today_str = str(today_date.day)
        if len(today_str) < 2:
            today_str = '0' + today_str
        today_month = str(today_date.month)
        today_compare = int(today_month + today_str)

        item_index = str(item_info[1]).split('/')
        item_day = item_index[1]
        if len(item_day) < 2:
            item_day = '0' + item_day
        item_month = item_index[0]
        item_compare = int(item_month + item_day)

        if today_compare <= item_compare:
            item_year = today_date.year
        elif today_compare > item_compare:
            item_year = (today_date.year + 1)
        return datetime(int(item_year), int(item_month), int(item_day))

    df_todo = pd.read_csv(csv_path, header=None)
    DATE_FORMAT = '%Y-%m-%d'
    ASSIGNMENT_COL = 0
    DATE_COL = 1
    assignment_length = len(df_todo.index)
    item_date = getFullDate(assignment_info).strftime(DATE_FORMAT)

    try:
        assignment_info[0] = int(assignment_info[0])
    except ValueError:
        pass

    if isinstance(assignment_info[0], int):
        task_label = df_todo.loc[(assignment_info[0] - 1), ASSIGNMENT_COL]
        myLog(f'EDIT: {task_label}')
        df_todo.loc[(assignment_info[0] - 1), DATE_COL] = item_date
        saveCSV(df_todo, DATE_COL, DATE_FORMAT)
        return

    for _index in range(assignment_length):
        task_label = df_todo.loc[_index, ASSIGNMENT_COL].lower()
        if task_label == assignment_info[0].lower():
            myLog(f'EDIT: {task_label}')
            df_todo.loc[_index, DATE_COL] = item_date
            saveCSV(df_todo, DATE_COL, DATE_FORMAT)
            break
        elif _index == (assignment_length - 1):
            myLog(f'ADD: {task_label}')
            new_task = pd.DataFrame([[assignment_info[0], item_date]], columns=df_todo.columns)
            df_todo = pd.concat([new_task, df_todo], ignore_index=True)
            saveCSV(df_todo, DATE_COL, DATE_FORMAT)
            break
# ? ###########################################################################


def taskComplete(assignment_info: list) -> None:

    df_todo = pd.read_csv(csv_path, header=None)
    DATE_FORMAT = '%Y-%m-%d'
    ASSIGNMENT_COL = 0
    DATE_COL = 1
    assignment_length = len(df_todo.index)

    try:
        assignment_info[0] = int(assignment_info[0])
    except ValueError:
        pass

    if isinstance(assignment_info[0], int):
        task_label = df_todo.loc[(assignment_info[0] - 1), ASSIGNMENT_COL]
        df_todo.drop(assignment_info[0] - 1, inplace=True)
        myLog(f'DONE: {task_label}')
        saveCSV(df_todo, DATE_COL, DATE_FORMAT)
        return

    for _index in range(assignment_length):
        task_label = df_todo.loc[_index, ASSIGNMENT_COL].lower()
        if task_label == assignment_info[0].lower():
            myLog(f'DONE: {task_label}')
            df_todo.drop(_index, inplace=True)
            saveCSV(df_todo, DATE_COL, DATE_FORMAT)
            break
# ? ###########################################################################


def saveCSV(df_list, DATE_COL: int, DATE_FORMAT: str) -> None:
    # print('Before:')
    # print(df_list.to_string(header=['Tasks', 'Due Date'], index=True), end="\n\n")
    df_list[DATE_COL] = pd.to_datetime(df_list[DATE_COL], format=DATE_FORMAT)
    df_list = df_list.sort_values(by=DATE_COL)
    df_list = df_list.reset_index(drop=True)
    df_list.to_csv(csv_path, index=False, header=False, date_format=DATE_FORMAT)
    # print('After:')
    # print(df_list.to_string(header=['Tasks', 'Due Date'], index=True))
# ? ###########################################################################


if __name__ == '__main__':
    main()
