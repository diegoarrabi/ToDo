from subprocess import call, run #, Popen, PIPE
from os import path, listdir, remove
from collections import defaultdict
from sys import exit as _exit
from datetime import datetime
from pathlib import Path
import logging as log

# TEST

def myLog(msg: str) -> None:
    """
    logs data to file

    Args:
        msg (str): any string to be logged
    """
    log_name = 'diegoibarra.todo.log'
    log_file = path.join(path_dict['resources'], 'cache', log_name)
    
    log.basicConfig(
        filename=log_file,
        level=log.INFO,
        datefmt='%m.%d[%H:%M:%S]',
        format=f'%(asctime)s: %(message)s'
    )
    if msg.startswith('module'):
        msg = f'    {msg}'
    elif 'DONE' in msg:
        msg = f'{msg}\n\n'
    log.info(msg)


def copy2Clipboard(_text) -> None:
    """
    Copies the given text to the clipboard using the pbcopy command.

    Args:
        _text (str): The text to be copied to the clipboard.
    """
    run("pbcopy", text=True, input=str(_text))


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
    

def getDialog(msg='mew mew', stop=False) -> None:

    def testDialog(message):
        message = runfromTerm(message)
        dIcon = "/Users/diegoibarra/Pictures/2. Icons/0. Icons/Python/pyLogo.png"
        s1 = '-e set dText to "%s"' % (message)
        s2 = '-e set dTitle to ("ToDo")'
        s3 = '-e set dIcon to POSIX file ("%s")' % (Path(dIcon))
        s4 = '-e display dialog dText with title dTitle with icon dIcon buttons {"Ok"} default button 1'
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

    def padNumbers(raw_time) -> list[str]:
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
    cStyle['head_font'] = 'SF Pro Rounded'
    cStyle['body_font'] = 'SF Mono'
    cStyle['head_font_size'] = 1.2
    cStyle['body_font_size'] = 1.3
    cStyle['border_width'] = 4

    # BOX COLOR
    cStyle['box_color'] = '353535'

    cStyle['head_font_color'] = '8E8E8E'
    cStyle['body_font_color'] = 'E0E0E0'
    cStyle['header_line_color'] = 'E2E2E2'

    cStyle['rowCoE'] = '424242'  # / Dark
    cStyle['rowCoO'] = '353535'  # / Light
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

