from subprocess import run
from os import path, listdir, remove
from collections import defaultdict
from sys import exit as _exit
from datetime import datetime
from pathlib import Path
import logging as log


# GLOBALS
# CONFIG ONLY
table_name = 'TaskList.csv'
code_wrap = 150
half_tab = 2

# MAKETASKS.PY
txt_doc_name = "TasksToDo.txt"

# MAKETABLE.PY
day_limit = 8


class CustomLogFormatter(log.Formatter):
    # DEBUG     -> 10
    # INFO      -> 20
    # ERROR     -> 40
    # CRITICAL  -> 50

    def __init__(self, fmt=None, datefmt="%m.%d[%H:%M:%S]", style="%", validate=True, *, defaults=None):
        super().__init__(fmt, datefmt, style, validate, defaults=defaults)

    def format(self, record):
        # CODE START
        if record.levelno == log.CRITICAL:
            self._style._fmt = f'\n\n%(asctime)s: %(message)s'
        # METHOD START
        elif record.levelno == log.INFO:
            self._style._fmt = f'%(asctime)s:\t└── %(message)s'
        # ERROR DETECTED
        elif record.levelno == log.ERROR:
            self._style._fmt = f'%(message)s'
        # ALL OTHER MESSAGES
        else:
            self._style._fmt = f'%(asctime)s: %(message)s'
        return super().format(record)

    def formatException(self, exception_info):
        global code_wrap
        global half_tab

        result = (super().formatException(exception_info)).splitlines()
        result_formatted_list = [f"{half_tab*' '}│{half_tab*' '}{strline}" for strline in result]
        result_formatted_string = f"{' '*half_tab}{'─'*(code_wrap-half_tab)}\n{'\n'.join(result_formatted_list)}"
        return result_formatted_string

def myLog(message: str, log_level=log.DEBUG):
    """
    logs data to file

    Args:
        message (str): any string to be logged
    """
    log_name = 'diegoibarra.todo.log'
    log_file = path.join(path_dict['resources'], 'cache', log_name)

    my_handler = log.FileHandler(log_file)
    my_handler.setFormatter(CustomLogFormatter())

    my_logger = log.getLogger('myLogger')
    my_logger.setLevel(log.DEBUG)
    my_logger.addHandler(my_handler)

    # CODE START
    if message.lower().startswith('-') and (not "done" in message.lower()):
        message = message.center(35, '-')
        my_logger.critical(message)
    # METHOD START
    elif message.lower().startswith('method'):
        my_logger.info(message)
    # ERROR DETECTED
    elif log_level == log.ERROR:
        log_message = f"ERROR: {message}"
        my_logger.error(log_message, exc_info=True)
        getDialog(log_file, message)
    # SCRIPT END
    elif "done" in message.lower():
        message = message.center(35, '-')
        my_logger.debug(message)
    # ALL OTHER MESSAGES
    else:
        my_logger.debug(message)

    my_logger.removeHandler(my_handler)
    my_handler.close()

def clearScreen() -> None:
    print("\x1b[H\x1b[J")

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
    path_dict[key_list[0]] = base_directory  # Project Directory
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
    global table_name

    wb_path = path.join(project_directory, table_name)
    if path.isfile(wb_path):
        return wb_path
    else:
        _exit()

def getDialog(log_file: str, message='') -> None:

    def runScript(applescript: str) -> str:

        std_outerr = run(['osascript', '-e', applescript], capture_output=True, text=True)
        stdout = std_outerr.stdout.strip()
        return stdout
    
    applescript = """
    set dialog_message to "%s\n\n\tOpen ToDo.log in VSCode?"
    set buttons_list to {"Open", "Nah"}
    set default_button to (item 2 of buttons_list)
    set title_message to "ToDo [ ERROR ]"
    set dialog_icon to POSIX file "/Users/diegoibarra/Pictures/1. Icons/0. Icons/MyApps/ToDo/AppIcon.icns"
    set time_out to 4

    display dialog dialog_message ¬
    	with title title_message ¬
	    buttons buttons_list ¬
	    default button default_button ¬
	    with icon dialog_icon ¬
	    giving up after time_out
    
    """ % (message)

    stdout = runScript(applescript)
    # button returned:Nah, gave up:false
    stdout_parse = stdout.split(', ')
    user_response = stdout_parse[0].split(':')
    if user_response[1].lower() == 'open':
        run(['code', path_dict['Project'], log_file])
    exit()


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


# MakeAssignments & MakeTable
path_dict = pathDict()
csv_path = csvTable(path_dict['Project'])
