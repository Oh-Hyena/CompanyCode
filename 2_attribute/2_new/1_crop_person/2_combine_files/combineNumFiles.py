# 이미지 파일을 xx개씩 파일 묶기

import os
import sys
import shutil


imgDir = r"D:\hyena\3_dataset\0531\origin"
resDir = r"D:\hyena\3_dataset\0531\img"


ENCODING_FORMAT = "UTF-8"
resFolderName   = "seongnam0530"
fileNum         = 150


def checkInitDirValid():
    if os.path.isdir(imgDir) is False:
        print(f'[Error] {imgDir} is invalid')
        return False
    if os.path.isdir(resDir) is False:
        print(f'[Error] {resDir} is invalid')
        return False
    
    return True


def makeCombineResDir(resDir):
    if not os.path.isdir(resDir):
        os.makedirs(resDir, exist_ok=True)


def numCount(length, num):
    rotate = length - len(num)
    if rotate > 0:
        for i in range(rotate):
            num = "0" + num
    return num


def makeEachDestDir(Count):  
    folderName = resFolderName + "_" + numCount(6, str(Count))
    DestDir = os.path.join(resDir, folderName)
    os.makedirs(DestDir, exist_ok=True)
    
    return DestDir


def combineFiles(imgDir):
    folderCount = 1
    fileCount   = 1
    
    for path, dir, files in os.walk(imgDir):
        for file in files:
            if file.endswith(".jpg"):
                shutil.copy(os.path.join(imgDir, file), os.path.join(resDir, makeEachDestDir(folderCount)))
                
                fileCount += 1
                
                if fileCount == fileNum + 1:
                    folderCount += 1
                    fileCount    = 1



if __name__ == "__main__":
    makeCombineResDir(resDir)
    
    if checkInitDirValid() is False:
        sys.exit(-1)
    
    combineFiles(imgDir)

