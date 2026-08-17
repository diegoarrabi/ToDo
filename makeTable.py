#!/Users/diegoibarra/.config/pyenv/versions/3.13.0/envs/ToDo/bin/python
# required env for launchdaemon execution

from datetime import datetime, timedelta
from os import listdir, path
from subprocess import run
from sys import argv

import dataframe_image as dfi
import pandas as pd
from pandas import DataFrame

from config import clearScreen, csv_path, day_limit, log, myLog, path_dict, tableStyle
from makeWallpaper import makeWallpaper

############################################################################


# region MAKETABLE
def makeTable(_from="") -> None:
    # ENTRY POINT FOR LAUNCHDAEMON
    # CALLING THIS SCRIPT FROM LAUNCH DAEMON ALLOWS FOR TABLE TO BE UPDATED
    clearScreen()

    myLog("__makeTable.py__".upper())

    make_image: bool = True
    images_directory = path_dict["images"]
    table_exists = deletePreviousTable(images_directory)

    if _from == "toggle":
        myLog("toggle argument")
        if table_exists:
            make_image = False
            myLog("TURN DESKTOP OFF")

    HEADER = ["TASKS", "DUE DATE", "DAYS", "_Days"]
    TASK_COL = HEADER[0]
    DATE_COL = HEADER[1]
    DAYS_COL = HEADER[3]
    DAY_STR_COL = HEADER[2]
    DATE_FORMAT = "%Y-%m-%d"

    dt_day_limit = timedelta(days=day_limit)
    time_now = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
    df_todo = pd.read_csv(csv_path, header=None)
    df_todo.rename(columns={0: HEADER[0], 1: HEADER[1]}, inplace=True)
    df_todo[DATE_COL] = pd.to_datetime(df_todo[DATE_COL], format=DATE_FORMAT)
    df_todo[DAY_STR_COL] = ""
    df_todo[DAYS_COL] = df_todo[DATE_COL] - time_now
    df_todo[DATE_COL] = df_todo[DATE_COL].dt.strftime("%m/%d")
    df_soon: DataFrame = df_todo[(df_todo[DAYS_COL] < dt_day_limit) | (df_todo[TASK_COL].str.endswith("!"))]
    if not df_soon.empty:
        for index, row in df_soon.iterrows():
            days_left = row[DAYS_COL].days
            if days_left == 0:
                df_soon.loc[index, TASK_COL] = row[TASK_COL].upper()
                df_soon.loc[index, DAY_STR_COL] = "TODAY!"
            elif days_left == -1:
                df_soon.loc[index, TASK_COL] = row[TASK_COL].upper()
                df_soon.loc[index, DAY_STR_COL] = "YESTERDAY!"
            elif days_left < -1:
                df_soon.loc[index, TASK_COL] = row[TASK_COL].upper()
                df_soon.loc[index, DAY_STR_COL] = f"{days_left} DAYS AGO!"
            elif days_left == 1:
                df_soon.loc[index, DAY_STR_COL] = "Tomorrow"
            elif days_left > 1:
                df_soon.loc[index, DAY_STR_COL] = f"{days_left} Days"
        df_styled = df_soon.style.set_table_styles(styleTable(df_soon, HEADER)).hide()
        try:
            if make_image:
                if not table_exists:
                    myLog("TURN DESKTOP ON")
                dfi.export(df_styled, path.join(images_directory, "table.png"), dpi=300) # type: ignore
        except Exception as e:
            myLog(f"DataFrame_Image Module Error: {e}", log.ERROR)
    makeWallpaper()


###########################################################################
###########################################################################
###########################################################################


def deletePreviousTable(images_directory: str) -> bool:
    myLog("method: deletePreviousTable")
    previous_table = [x for x in listdir(images_directory) if x.startswith("table")]
    if len(previous_table) == 0:
        myLog("NO TABLE TO DELETE")
        return False
    previous_path = path.join(images_directory, previous_table[0])
    run(["rm", "-f", previous_path])
    myLog("DELETING PREVIOUS TABLE")
    return True


###########################################################################


def styleTable(df: pd.DataFrame, headerCol: list) -> list:
    myLog("method: styleTable")
    cStyle = tableStyle()
    border_width = cStyle["border_width"]

    background_color = cStyle["background_color"]

    head_font = cStyle["head_font"]
    header_line_color = cStyle["header_line_color"]
    head_fontsize = cStyle["head_font_size"]
    body_font = cStyle["body_font"]
    body_fontsize = cStyle["body_font_size"]
    head_font_color = cStyle["head_font_color"]
    body_font_color = cStyle["body_font_color"]
    row_even_color = cStyle["row_even_color"]
    row_odd_color = cStyle["row_odd_color"]

    # HEADER
    pad_head = "padding-top: 0em; padding-bottom: 0em;"
    properties_head = f"font-weight:600; background-color:#{background_color}; font-family: {head_font}; color: #{head_font_color}; font-size: {head_fontsize}em;"

    pad_body = "padding-top: 0.4em; padding-bottom: 0.4em;"
    pad_body_left = "padding-left: 0.5em; padding-top: 0.4em; padding-bottom: 0.4em;"
    properties_even = f"font-weight:normal; background-color: #{row_even_color}; font-family: {body_font}; color: #{body_font_color}; font-size: {body_fontsize}em;"
    properties_odd = f"font-weight:normal; background-color: #{row_odd_color}; font-family: {body_font}; color: #{body_font_color}; font-size: {body_fontsize}em;"

    header_border = f"border-bottom: {border_width - 2}px solid #{header_line_color};"
    border_top = f"border-top: {border_width}px solid #{background_color};"
    border_right = f"border-right: {border_width}px solid #{background_color};"
    border_bottom = f"border-bottom: {border_width}px solid #{background_color};"
    border_left = f"border-left: {border_width}px solid #{background_color};"

    styleList = [
        # COLOR
        # ##### HEADER
        {"selector": "th.col_heading", "props": f"{properties_head}; {pad_head}; {border_top}; {header_border};"},
        # ##### EVEN
        {"selector": "tbody tr:nth-child(even)", "props": f"{properties_even};"},
        # ##### ODD
        {"selector": "tbody tr:nth-child(odd)", "props": f"{properties_odd};"},
        # ALIGNMENT
        # ##### 1ST COLUMN "TASKS"
        {"selector": "th.col0", "props": f"text-align: left;{border_left}; {pad_body_left}; min-width: 440px;"},
        {"selector": "td.col0", "props": f"text-align: left; {pad_body_left}; {border_left};"},
        # ##### 2ND COLUMN "DUE DATE"
        {"selector": "th.col1", "props": "text-align: center;"},
        {"selector": "td.col1", "props": f"text-align: center; {pad_body}"},
        # ##### 3RD COLUMN "DAYS"
        {"selector": "th.col2", "props": f"text-align: center; {border_right}"},
        {"selector": "td.col2", "props": f"text-align: right; {pad_body}; {border_right}"},
        # ##### REMOVES DAY COUNTER
        {"selector": "td.col3", "props": "display: none"},
        {"selector": "th.col3", "props": "display: none"},
        # ##### LAST ROW
        {"selector": "tbody tr:nth-last-child(1)", "props": f"text-align: right; {pad_body}; {border_bottom}"},
    ]

    count = 0
    for index, row in df.iterrows():
        tempToday = {}
        dict_keys = ["selector", "props"]
        tempToday[dict_keys[0]] = ""
        # Priority Tasks
        if "!" in row["TASKS"]:
            tempToday[dict_keys[1]] = (
                "\
                text-decoration: underline solid 0.15em #%s; \
                font-weight: bold; \
                color: #%s;"
                % (cStyle["priority_color"], cStyle["priority_color"])
            )
        elif "!" in row["DAYS"]:
            tempToday[dict_keys[1]] = "font-weight: bold; color: #%s;" % (cStyle["pastdue_color"])
        else:
            break
        tempToday["selector"] = f"tbody tr:nth-child({count + 1})"
        count += 1
        styleList.append(tempToday)
        del tempToday

    return styleList


###########################################################################


if __name__ == "__main__":
    if len(argv) == 1:
        argv.append("vscode")
    makeTable(argv[1])
