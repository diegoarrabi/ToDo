from os import path, listdir, remove
from collections import defaultdict
from sys import exit as exitCode
from datetime import datetime
from subprocess import call
from pathlib import Path
from time import sleep
import logging as log

'''
def checkRunner() -> None:
    """
    Checks */.config/RUNNER.txt for 0 or 1.

    When TextDocument is launched from Assignments.app on Desktop two things happen:
        1. It writes "0" to runner.txt file by launching */.config/runnerReset.py.
        2. The LaunchAgent recognizes a change to the file so it runs the program.

    The checkRunner module stops the code from running when the LaunchAgent recognizes the 
        document opening. When the document closes, the runner.txt file now contains a "1"
        which allows the code to fully run.
    """

    file_name = 'RUNNER.txt'
    runner_path = path.join(path_dict['configPATH'], file_name)

    with open(runner_path, "r+") as runner_txtfile:
        run_value = int(runner_txtfile.read())
        runner_txtfile.seek(0)
        if run_value == 0:
            runner_txtfile.write('1')
            exitCode()
        elif run_value == 1:
            runner_txtfile.write('0')
            sleep(1)
        else:
            exitCode()
'''

def getPaths() -> dict:
    """
    Using the main file as the source of the Project Directory, 
        returns a dict of all of the paths used throughout the project

    Returns:
        dict:   Project = '*';
                configPATH = '*/.config';
                resources = '*/resources';
                images = '*/resources/images';
                makeColor = '*/resources/images/makeColor';
                tableIMG = '*/resources/images/tableIMG';
                wallpaperIMG = '*/resources/images/wallpaperIMG';
    """
    base_directory = path.dirname(__file__)
    images_main_directory = path.join(base_directory, 'resources/images')
    pathKey = ['Project', 'resources', 'makeColor',
               'images', 'tableIMG', 'wallpaperIMG', 'configPATH']

    path_dict = defaultdict(str)
    path_dict[pathKey[0]] = base_directory
    path_dict[pathKey[1]] = path.join(base_directory, 'resources')
    path_dict[pathKey[2]] = path.join(images_main_directory, 'makeColor')
    path_dict[pathKey[3]] = images_main_directory
    path_dict[pathKey[4]] = path.join(images_main_directory, 'tableIMG')
    path_dict[pathKey[5]] = path.join(images_main_directory, 'wallpaperIMG')
    path_dict[pathKey[6]] = base_directory + '/.config'
    return path_dict


def excelPath(project_directory: str) -> str:
    """
    Checks to see if excel file exists and returns path

    Args:
        project_directory (str)

    Returns:
        str: path of excel file
    """
    wb_path = path.join(project_directory, wb_name)
    excelfile_exists = path.isfile(wb_path)
    if excelfile_exists:
        return wb_path
    else:
        dialog_icon = "/Users/diegoibarra/Pictures/2. Icons/14. ToDo/pToDo.png"
        s1 = '-e set dText to ("                   File Not Found\nFile: \n%s \n\nDirectory: \n%s ")' % (
            wb_name.upper(), wb_path)
        s2 = '-e set dTitle to ("To Do")'
        s3 = '-e set dIcon to POSIX file ("%s")' % (Path(dialog_icon))
        s4 = '-e display dialog dText with title dTitle with icon dIcon buttons {"Cancel", "Go To %s Folder"} default button 2' % (
            (project_directory))
        run_output = call(['osascript', s1, s2, s3, s4])
        if run_output == 0:
            call(["open", '-R', project_directory])
        else:
            exitCode()
    return ""


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
            message = 'mew mew'
        return message

    testDialog(msg)

    if stop == True:
        exitCode()


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


notifications_on = False

resize_ratio = 0.20
lego_x = 0.97
lego_y = 0.89
rotation = 15
add_legominifigure = True

day_limit = 8
wb_name = 'ExcelList.xlsx'
path_dict = getPaths()
lego_config = {
    'resize_ratio': resize_ratio,
    'x_percent': lego_x,
    'y_percent': lego_y,
    'rotation': rotation
}
