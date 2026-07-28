from os import path, listdir, remove
from collections import defaultdict
from sys import exit as _exit
from datetime import datetime
from subprocess import call
from pathlib import Path
import logging as log

def pathDict() -> dict:
    """
    Using the main file as the source of the Project Directory, 
        returns a dict of all of the paths used throughout the project

    Returns:
        dict:   Project = '*';
                resources = '*/resources';
                configPATH = '*/.config';
    """

    base_directory = path.dirname(__file__)
    key_list = ['Project', 'resources', 'images']
    path_dict = defaultdict(str)
    path_dict[key_list[0]] = base_directory # Project Directory
    path_dict[key_list[1]] = path.join(base_directory, 'resources')
    path_dict[key_list[2]] = path.join(path_dict[key_list[1]], 'images')
    return path_dict


def csvTable(project_directory: str) -> str:
    """
    Checks to see if csv file exists and returns path

    Args:
        project_directory (str)

    Returns:
        str: path of csv file
    """
    wb_path = path.join(project_directory, table_name)
    if path.isfile(wb_path):
        return wb_path
    else:
        _exit()
    


def myLog(msg: str) -> None:
    """
    logs data to file

    Args:
        msg (str): any string to be logged
    """
    log_name = 'todo_log'
    log_file = path.join(path_dict['resources'], log_name)
    log.basicConfig(
        filename=log_file,
        level=log.DEBUG,
        datefmt='%m.%d[%H:%M:%S]',
        format=f'%(asctime)s:       %(message)s'
    )
    log.debug(msg)


def getDialog(msg='mew mew', stop=False) -> None:

    def testDialog(message):
        message = runfromTerm(message)
        dIcon = "/Users/diegoibarra/Pictures/2. Icons/0. Icons/Python/pyLogo.png"
        s1 = '-e set dText to "Code Run was Succesful \n\n%s"' % (message)
        s2 = '-e set dTitle to ("Python Test")'
        s3 = '-e set dIcon to POSIX file ("%s")' % (Path(dIcon))
        s4 = '-e display dialog dText with title dTitle with icon dIcon buttons {"Awesome"} default button 1'
        call(['osascript', s1, s2, s3, s4])

    def runfromTerm(message):
        if len(message) == 0:
            message = 'mew'
        return message

    testDialog(msg)

    if stop == True:
        _exit()


def clearFolder(directory: str) -> None:
    """
    Removes all files within a directory, preserving the directory itself.

    Args:
        directory (str): Full path of directory
    """
    folder_files = listdir(directory)
    for i in folder_files:
        path_to_remove = directory + '/' + i
        remove(path_to_remove)


def timeLabel(prefix="") -> str:
    """
    Returns time string as *HHMMSS
    accepting a prefix represented by the asterisk

    Args:
        prefix (str, optional): Any string to precede the time. Defaults to "".

    Returns:
        str: "052501"
    """

    def getTime() -> list[str]:
        current_hour = datetime.today().hour
        current_min = datetime.today().minute
        current_sec = datetime.today().second
        current_list = [current_hour, current_min, current_sec]
        return padNumbers(current_list)

    def padNumbers(raw_time: list[int]) -> list[str]:
        for i in range(len(raw_time)):
            time_component = str(raw_time[i])
            if len(time_component) < 2:
                time_component = "0" + time_component
            raw_time[i] = time_component
        return raw_time

    return f'{prefix}{''.join(getTime())}'


def tableStyle():

    cautionColor = "F86702"
    cStyle = {}
    cStyle['fontHead'] = 'Manrope-SemiBold'
    # cStyle['fontHead'] = 'JetBrainsMono-Light'
    cStyle['fontBody'] = 'Mona Sans'
    cStyle['fontHsize'] = 1.4
    cStyle['fontBsize'] = 1.3
    cStyle['brWidth'] = 4

    cStyle['brColor'] = '202020'
    # cStyle['brColor'] = '505658'

    cStyle['HeadColor'] = '202020'
    # cStyle['HeadColor'] = '505658'

    cStyle['hFntColor'] = 'E3E3E3'
    cStyle['bFntColor'] = '272727'

    cStyle['rowCoE'] = 'D7D7D8'  # / Dark
    cStyle['rowCoO'] = 'F5F5F5'  # / Light
    cStyle['pastCo'] = cautionColor  # / PastDue Color
    return cStyle


## Config ONLY
table_name = 'TaskList.csv'


## MakeAssignments
txt_doc_name = "TasksToDo.txt"
#// notifications_on = False


## MakeTable
day_limit = 8


## MakeWallpaper


## MakeAssignments & MakeTable
path_dict = pathDict()
csv_path = csvTable(path_dict['Project'])

