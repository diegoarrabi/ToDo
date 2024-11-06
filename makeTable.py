#!/Users/diegoibarra/.config/pyenv/versions/3.13.0/envs/ToDo/bin/python

import pandas as pd
from subprocess import run
from os import path, listdir
import dataframe_image as dfi
from datetime import datetime, timedelta
from config import path_dict, csv_path, day_limit, tableStyle, myLog

from makeWallpaper import makeWallpaper


def makeTable() -> None:
    myLog('\n\nmakeTable.py: ')
        
    project_directory = path_dict['Project']
    images_directory = path_dict['images']

    deletePreviousTable(images_directory)

    HEADER = ['Tasks', 'Due Date', 'Days', '_Days']
    TASK_COL = HEADER[0]
    DATE_COL = HEADER[1]
    DAYS_COL = HEADER[3]
    DAY_STR_COL = HEADER[2]
    DATE_FORMAT = '%Y-%m-%d'

    dt_day_limit = timedelta(days=day_limit)
    time_now = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)

    df_todo = pd.read_csv(csv_path, header=None)
    df_todo.rename(columns={0: HEADER[0], 1: HEADER[1]}, inplace=True)
    df_todo[DATE_COL] = pd.to_datetime(df_todo[DATE_COL], format=DATE_FORMAT)
    df_todo[DAY_STR_COL] = ""
    df_todo[DAYS_COL] = (df_todo[DATE_COL] - time_now)
    df_todo[DATE_COL] = df_todo[DATE_COL].dt.strftime('%m/%d')
    
    df_soon = df_todo[df_todo[DAYS_COL] < dt_day_limit]
    
    if not df_soon.empty:
        for _row in range(len(df_soon.index)):
            days_left = df_soon.loc[_row, DAYS_COL].days
            if days_left == 0:
                df_soon.loc[_row, TASK_COL] = df_soon.loc[_row, TASK_COL].upper()
                df_soon.loc[_row, DAY_STR_COL] = 'TODAY!'
            elif days_left == -1:
                df_soon.loc[_row, TASK_COL] = df_soon.loc[_row, TASK_COL].upper()
                df_soon.loc[_row, DAY_STR_COL] = 'YESTERDAY!'
            elif days_left < -1:
                df_soon.loc[_row, TASK_COL] = df_soon.loc[_row, TASK_COL].upper()
                df_soon.loc[_row, DAY_STR_COL] = f'{days_left} DAYS AGO!'
            elif days_left == 1:
                df_soon.loc[_row, DAY_STR_COL] = 'Tomorrow'
            elif days_left > 1:
                df_soon.loc[_row, DAY_STR_COL] = f'{days_left} Days'
    
        df_styled = df_soon.style.set_table_styles(styleTable(df_soon, HEADER)).hide()
        dfi.export(df_styled, path.join(images_directory, 'table.png'), dpi=300)
    
    makeWallpaper()
    '''
    python_script = "makeWallpaper.py"
    script = path.join(project_directory, python_script)
    run(['python3', script])
    '''
###########################################################################



def deletePreviousTable(images_directory: str) -> None:
    
    previous_table = [x for x in listdir(images_directory) if x.startswith("table")]
    if len(previous_table) == 0:
        return
    previous_path = path.join(images_directory, previous_table[0])
    run(["rm", "-f", previous_path])
###########################################################################


def styleTable(df, headerCol):
    cStyle = tableStyle()
    bPx = cStyle['brWidth']
    bCo = cStyle['brColor']
    hFnt = cStyle['fontHead']
    hSFnt = cStyle['fontHsize']
    bFnt = cStyle['fontBody']
    bSFnt = cStyle['fontBsize']
    hCo = cStyle['HeadColor']
    hFntCo = cStyle['hFntColor']
    bFntCo = cStyle['bFntColor']
    rECo = cStyle['rowCoE']
    rOCo = cStyle['rowCoO']

    paddingHead = 'padding-top: %sem; padding-bottom: %sem;' % (0, 0)
    propsHead = 'font-weight:normal; background-color: #%s; font-family: %s; color: #%s; font-size: %sem;' % (hCo, hFnt, hFntCo, hSFnt)

    paddingBody = 'padding-top: %sem; padding-bottom: %sem;' % (0.3, 0.3)
    paddingBodyL = 'padding-left: %sem; padding-top: %sem; padding-bottom: %sem;' % (1, 0.3, 0.3)
    propsBodyE = 'font-weight:normal; background-color: #%s; font-family: %s; color: #%s; font-size: %sem;' % (rECo, bFnt, bFntCo, bSFnt)
    propsBodyO = 'font-weight:normal; background-color: #%s; font-family: %s; color: #%s; font-size: %sem;' % (rOCo, bFnt, bFntCo, bSFnt)

    bhBottom = 'border-bottom: %spx solid #%s;' % ((bPx-2), rECo)
    bTop = 'border-top: %spx solid #%s;' % (bPx, bCo)
    bRight = 'border-right: %spx solid #%s;' % (bPx, bCo)
    bBottom = 'border-bottom: %spx solid #%s;' % (bPx, bCo)
    bLeft = 'border-left: %spx solid #%s;' % (bPx, bCo)

    styleList = [
        # COLOR
        {"selector": "th.col_heading",
            "props": f'{propsHead}; {paddingHead}; {bTop}; {bhBottom};'},

        {"selector": "tbody tr:nth-child(even)",
            "props": f'{propsBodyE};'},

        {"selector": "tbody tr:nth-child(odd)",
            "props": f'{propsBodyO};'},
        # ALIGNMENT
        {"selector": "th.col0",
            "props": f"text-align: left;{bLeft}; {paddingBodyL};"},

        {"selector": "td.col0",
            "props": f"text-align: left; {paddingBodyL}; {bLeft};"},

        {"selector": "th.col1",
            "props": "text-align: center;"},

        {"selector": "td.col1",
            "props": f"text-align: center; {paddingBody}"},

        {"selector": "th.col2",
            "props": f"text-align: center; {bRight}"},

        {"selector": "td.col2",
            "props": f"text-align: right; {paddingBody}; {bRight}"},

        {"selector": "td.col3",
            "props": f"display: none"},

        {"selector": "th.col3",
            "props": f"display: none"},

        {"selector": "tbody tr:nth-last-child(1)",
            "props": f"text-align: right; {paddingBody}; {bBottom}"},
    ]
    
    lengthofToday = len(df[df[headerCol[2]].str.contains("!")])

    if lengthofToday > 0:
        for i in range(lengthofToday):
            tempToday = {}
            dict_keys = ['selector', 'props']
            tempToday[dict_keys[0]] = ""
            tempToday[dict_keys[1]
                      ] = 'font-weight: bold; color: #%s;' % (cStyle['pastCo'])
            tempToday['selector'] = (f"tbody tr:nth-child({i+1})")
            styleList.append(tempToday)
            del tempToday
    
    return styleList

if __name__ == '__main__':
    makeTable()