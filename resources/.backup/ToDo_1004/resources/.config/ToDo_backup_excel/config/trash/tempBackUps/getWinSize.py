import subprocess

def runScript(script):
    p = subprocess.Popen(['osascript', '-'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    outResult, stdErr = p.communicate(script)
    outResult = outResult.split(',')
    desktopSize = []
    for i in range(len(outResult)): 
        print(i)
        if i > 1:
            outResult[i] = int(outResult[i])*2
            desktopSize.append(outResult[i])
        else:
            pass
    return desktopSize


script = 'tell application "Finder" to return (bounds of window of desktop)'
outResult = runScript(script)

print()
print(outResult)
print()
