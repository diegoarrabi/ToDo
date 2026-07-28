from config import *
import sys
import subprocess
import os
from PIL import Image

def main():

	tableBorderize()



	pDict = getPaths()
	wallpaperIMGdir = pDict['wallpaperIMG']
	tableIMGdir = pDict['tableIMG']
	imagesDir = pDict['images']

	clearFolder(wallpaperIMGdir)
	
	wallpaperpathList = getImagePath(imagesDir)
	stockWallpaper = wallpaperpathList[2]

	tableIMGpathList = getImagePath(tableIMGdir)
	tableIMGpath = tableIMGpathList[2]
	newWallFULLpathExt = wallpaperIMGdir + "/" + tableIMGpathList[1]
	
	imageMerge_Save(tableIMGpath, stockWallpaper, newWallFULLpathExt)
	updateWallpaper(newWallFULLpathExt)

def getImagePath(imgPath):
	imgName = os.listdir(imgPath)
	for i in imgName:
		if str(i).startswith("."):
			pass
		elif str(i).endswith('png'):
			imgNameExt = i
			imgPath = imgPath + "/"
			imgName = imgNameExt.split(".")
			imgName = imgName[0]
			fullimgPath = imgPath + imgNameExt
			imgList = [imgName, imgNameExt, fullimgPath]
		else:
			pass
	return imgList

def tableBorderize():

	pDict = getPaths()
	dirmakeColor = pDict['makeColor']
	tableDir = pDict['tableIMG']
	saveExt = ".png"

	tablePath = getImagePath(tableDir)
	tableImg = Image.open(tablePath[2])

	borderName = "border.png"
	borderPath = os.path.join(dirmakeColor + '/' + borderName)
	borderImage = Image.open(borderPath)

	tblW = tableImg.width
	tblH = tableImg.height
	rR = (1+(4.75/100))
	frmToprR = (20.5/100)
	
	newW = round(tblW*rR)
	newH = round(tblH*rR)

	tblX = round((newW-tblW)/2)
	diffY = round((newH-tblH))
	tblY = round(diffY*frmToprR)

	borderImg = borderImage.resize([newW, newH])

	borderImg.paste(tableImg, [tblX, tblY])
	
	newName = timeLabel()
	newimageName = newName + saveExt
	saveP = '/Users/diegoibarra/Downloads'
	savePath = os.path.join(saveP + '/' + newimageName)

	borderImg.save(savePath)

	borderImg.close()
	tableImg.close()
	sys.exit()
	return

def imageMerge_Save(imgTablefile, blankWallpaper, savePath):
	imgTable = Image.open(imgTablefile)
	imgWall = Image.open(blankWallpaper)

	resizeRatio = 0.5
	imgTableWidth = round((imgTable.width) * resizeRatio, None)
	imgTableHeight = round((imgTable.height) * resizeRatio, None)
	
	imgTableRS = imgTable.resize([imgTableWidth, imgTableHeight])
	
	imgWall.paste(imgTableRS,(60,130))
	imgWall.save(savePath, "png")
	imgWall.close()

def updateWallpaper(item_path):
   script = ('tell application "Finder" to set desktop picture to POSIX file "%s"' % (item_path))
   subprocess.call(['osascript', '-e', script])

if __name__ == '__main__':
    main()