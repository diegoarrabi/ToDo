from subprocess import run

from config import log
from config import myLog
############################################################################


def runscript(script):
    process = run(['osascript', '-e', script], capture_output=True, text=True)
    stdout = (process.stdout).strip()
    stderr = (process.stderr).strip()
    return (stdout, stderr)
############################################################################


def console2Background():
    applescript_string = """
    on run {}
        set app_name to "Terminal"
        set console_name to "todoConsole"

        -- Checks to see if Terminal was already open prior to running script
        tell application "System Events" to set is_running to (name of processes) contains app_name

        if is_running then
            set quit_terminal to false
        else
            set quit_terminal to true
        end if

        tell application app_name

            set window_list to every window

            repeat with i from 1 to (count window_list)
                set window_object to item i of window_list
                set window_title to (name of window_object)

                if window_title contains (word 1 of console_name) then
                    --delay 1
                    close window_object
                end if
            end repeat
            
            if quit_terminal then
                delay 1
                quit
            end if
        end tell
    end run
    """
    stdout, stderr = runscript(applescript_string)
    myLog('__console2Background.py__'.upper())
    if len(stdout) != 0:
        myLog(f"Output: \n{stdout}")
    if len(stderr) != 0:
        myLog(f"Output: \n{stderr}", log.ERROR)
############################################################################
############################################################################
############################################################################


if __name__ == '__main__':
    console2Background()
