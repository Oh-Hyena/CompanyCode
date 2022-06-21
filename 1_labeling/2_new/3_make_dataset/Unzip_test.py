# zip 파일을 풀어서 yolo txt 파일만 추출해서 resDir 에 저장하기


import os
import sys
import zipfile
import shutil


zipDir          = r"E:\0610\zip"
unzipDir        = r"E:\0610\unzip"
resDir          = r"E:\0610\seongnamfalse0125_txt"

ENCODING_FORMAT = "UTF-8"


def checkInitDirValid():
    if os.path.isdir(zipDir) is False:
        print(f'[Error] {zipDir} is invalid')
        return False
    if os.path.isdir(unzipDir) is False:
        print(f'[Error] {unzipDir} is invalid')
        return False
    if os.path.isdir(resDir) is False:
        print(f'[Error] {resDir} is invalid')
        return False
    return True


def makeUnzipResDir(Dir):
    if not os.path.isdir(Dir):
        os.makedirs(Dir, exist_ok=True)


def writeZipList():
    zipList = []
    
    for path, dirs, files in os.walk(zipDir):
        for file in files:
            zipList.append(os.path.join(path, file))
    
    return zipList


def unzip(zipList):
    for zipFile in zipList:
        with zipfile.ZipFile(zipFile, 'r') as f:
            f.extractall(unzipDir)


def moveYoloTxtFile():
    for path, dirs, files in os.walk(unzipDir):
        for file in files:
            if file.endswith(".txt"):
                # os.remove(os.path.join(unzipDir, "train.txt"))
                shutil.move(os.path.join(path, file), os.path.join(resDir, file))
                

def deleteNothing():
    for path, dirs, files in os.walk(resDir):
        os.remove(os.path.join(path, "train.txt"))
                


if __name__ == "__main__":
    makeUnzipResDir(unzipDir)
    makeUnzipResDir(resDir)
    
    if checkInitDirValid() is False:
        sys.exit(-1)
    
    zipList = writeZipList()
    unzip(zipList)
    moveYoloTxtFile()
    deleteNothing()