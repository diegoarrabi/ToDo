import sys
import subprocess
import os
import time
import openpyxl

from PIL import Image
from PIL import ImageColor

from datetime import datetime
from pathlib import Path 

addLegoFigure = True

def main(mainVar):

    basedirColor = os.path.dirname(__file__)
    basedirExcelToDo = basedirColor.rsplit('/', 1)
    imagesPath = basedirExcelToDo[0] + '/images'
    tablePath = imagesPath + '/table'
    newwallpaperPath = imagesPath + '/wallpaper'

    print(imagesPath)
    print(tablePath)
    print(newwallpaperPath)

    if addLegoFigure:
        legoFigure = "legominifigure.png"
        legoFigurePath = basedirColor + '/' + legoFigure

        imgToDo = Image.open(legoFigurePath)
        orig_imgH = imgToDo.height
        orig_imgW = imgToDo.width

        print(legoFigure)
    
    sys.exit()
    

    rgbVar = getValues(mainVar)
    setColorxslx(rgbVar)

    imgOne = "/Users/diegoibarra/Coding/1_Python/Projects/0_PlayProjects/color/legominifigure.png"
    foldPath = "/Users/diegoibarra/Coding/1_Python/Projects/0_PlayProjects/color"
    xtraPath = "/Users/diegoibarra/Coding/2_AppleScripts/1. Projects/ToDo Excel/Images"
    saveExt = ".png"
    dirPath = Path(foldPath)
    savePath = foldPath + '/' + getDateTime() + saveExt
    extraPath = xtraPath + '/' + "Wallpaper" + saveExt

    selectFiletoDelete(dirPath)
    time.sleep(0.5)

    imgToDo = Image.open(imgOne)
    orig_imgH = imgToDo.height
    orig_imgW = imgToDo.width
    imgBackH = 1964
    imgBackW = 3024

    resizeRatio = 0.20
    imgXr = 0.96
    imgYr = 0.87

    imgW = round(orig_imgW * resizeRatio, None)
    imgH = round(orig_imgH * resizeRatio, None)
    imgX = round(imgBackW*imgXr)
    imgY = round(imgBackH*imgYr)

    imgRS = imgToDo.resize([imgW, imgH])
    imgRS = imgRS.rotate(20)
    _,_,_, mask = imgRS.split()

    newWall = Image.new("RGBA", [imgBackW, imgBackH], rgbVar)
    newWall.paste(imgRS, [imgX, imgY], mask)
    newWall.save(savePath, "png")
    newWall.save(extraPath, "png")
    imgToDo.close

    updateWallpaper(savePath)
    sys.exit()


def getValues(varL):
    argVar = varL[0]
    colorCode = "#" + argVar
    rgbIndex = ImageColor.getcolor(colorCode, "RGB")
    return rgbIndex

def setColorxslx(colorRGBVar):
    txtPath = "/Users/diegoibarra/Coding/1_Python/Projects/0_PlayProjects/color/colorRGB.txt"
    with open(txtPath, "w") as txtFile:
        for i in range(len(colorRGBVar)):
            if i == 2:
                txtFile.write(str('%s') % colorRGBVar[i])
            else:
                txtFile.write(str('%s\n') % colorRGBVar[i])

def getDateTime():
    def getTime():
        tdHour = datetime.today().hour
        tdMin = datetime.today().minute
        tdSec = datetime.today().second
        timeList = [tdHour, tdMin, tdSec]
        return padNum(timeList)
    
    def padNum(var):
        for i in range(len(var)):
            timeVar = str(var[i])
            if len(timeVar) < 2:
                timeVar = "0" + timeVar
            var[i] = timeVar
        return comboTime(var)
    
    def comboTime(var):
        timeStr = ""
        for i in range(len(var)):
            timeStr = timeStr + var[i]
        return timeStr
    
    return getTime()

def updateWallpaper(savePath):
    script = ('tell application "Finder" to set desktop picture to POSIX file "%s"' % (savePath))
    meow = subprocess.call(['osascript', '-e', script])
    return "meow"

def selectFiletoDelete(dirPath):
    filedirList = dirPath.iterdir()
    for item in filedirList:
        itemName = str(item.name)
        itemName = itemName.split(".")
        if len(itemName[0]) == 6 and itemName[1].endswith("png"):
            deleteFiles(item)

def warningTooManyFiles(dirPath):
    messageDisplayed = "Shouldn't be more then 4 files in this folder"
    script = 'Display Dialog "%s"' % messageDisplayed
    subprocess.call(['osascript', '-e', script])
    subprocess.call(['open', '-R', dirPath])
    sys.exit()

def deleteFiles(filePath):
    cmd = "rm"
    pM = "-I"
    subprocess.call([cmd, pM, filePath])
    print(filePath)

if __name__ == '__main__':
    main(sys.argv[1:])