from subprocess import call
from pathlib import Path
import sys

def main(msg):
    # call(['echo', str(msg)])

    msg = runfromTerm(msg[1:])

    dIcon = "/Users/diegoibarra/Pictures/2. Icons/0. Icons/Python/pyLogo.png"
    s1 = '-e set dText to "Code Run was Succesful \n\n%s"' % (msg)
    s2 = '-e set dTitle to ("Python Test")'
    s3 = '-e set dIcon to POSIX file ("%s")' % (Path(dIcon))
    s4 = '-e display dialog dText with title dTitle with icon dIcon buttons {"Awesome"} default button 1 giving up after 2'
    call(['osascript', s1, s2, s3, s4])

def runfromTerm(msg):
    if len(msg) == 0:
        msg = 'mew mew'
    else:
        msg = str(msg)
    return msg

if __name__ == '__main__':
    main(sys.argv)