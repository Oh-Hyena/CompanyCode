# zip 파일을 풀어서 yolo txt 파일만 추출해서 resDir 에 저장하기

import os
import sys
import zipfile
import shutil


zipDir          = r"D:\hyena\3_dataset\seongnam\2020\0330\seongnam\231_300\zip"
resDir          = r"D:\hyena\3_dataset\seongnam\2020\0330\seongnam\231_300\seongnam20200330_falldown_txt"

ENCODING_FORMAT = "UTF-8"
deleteFileList  = ["obj.data", "obj.names", "train.txt"]


def checkInitDirValid():
    if os.path.isdir(zipDir) is False:
        print(f'[Error] {zipDir} is invalid')
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


def unzip():
    print("[ 실행 ] Unzip")
    
    zipList = writeZipList()
    
    for zipFile in zipList:
        with zipfile.ZipFile(zipFile, 'r') as f:
            f.extractall(resDir)
            

def moveYoloTxtFile():
    print("[ 실행 ] Move Yolo Txt")
    for path, dirs, files in os.walk(resDir):
        for file in files:
            if file.endswith(".txt"):
                shutil.move(os.path.join(path, file), os.path.join(resDir, file))
                
                
def deleteNothing():
    print("[ 실행 ] Delete Nothing Dir")
    
    # zip 파일 삭제
    for each in os.listdir(zipDir):
        os.remove(os.path.join(zipDir, each))
    
    # 빈 폴더 삭제
    os.rmdir(zipDir)
    os.rmdir(os.path.join(resDir, "obj_train_data"))
    
    # 파일 삭제
    for each in deleteFileList:
        os.remove(os.path.join(resDir, each))


if __name__ == "__main__":
    makeUnzipResDir(resDir)
    
    if checkInitDirValid() is False:
        sys.exit(-1)
    
    unzip()
    moveYoloTxtFile()
    deleteNothing()