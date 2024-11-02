import os
import sys
from pathlib import Path
import subprocess

from subprocess import Popen, PIPE

def runPYScript(pyScript):
    print(pyScript)
    p = Popen(['python3', pyScript], stdin=PIPE, stdout=PIPE, stderr=PIPE, universal_newlines=True)
    outResult, stdErr = p.communicate('plsRun')
    outResult = outResult.strip()
    return outResult


script_path = (Path(__file__).parents[1])
fileName = 'scriptRuntest.py'
fullPath = os.path.join(script_path, fileName)

returnResult = runPYScript(fullPath)
print(returnResult+"GOTPRINT")

