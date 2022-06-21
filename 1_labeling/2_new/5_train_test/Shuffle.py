# total_dataset_imglist.txt 파일을 random 으로 섞기

import os
import sys
from random import shuffle


imgListPath     = r"E:\0610\dataset2\total_dataset_list.txt"
resDir          = r"E:\0610\dataset2"

ENCODING_FORMAT = "UTF-8"
resFileName     = "shuffle_total_dataset"


def readFileToList(fileName:str):
    fList = []
    
    if os.path.isfile(fileName) is False:
        print(f'[Error] {fileName} is invalid')
        return fList
        
    with open(fileName, 'r', encoding=ENCODING_FORMAT) as rf:
        for eachLine in rf:
            fList.append(eachLine.strip('\n'))

    print(f'[Done] File Read Done : {fileName}')
    
    return fList


def writeListToFile(fileName:str, writeList:list):
    fileDir = os.path.dirname(fileName)
    
    if os.path.isdir(fileDir) is False:
        print(f'[Error] {fileDir} is invalid')
        return False
    
    with open(fileName, 'w', encoding=ENCODING_FORMAT) as wf:
        for eachLine in writeList:
            wf.write(f'{eachLine}\n')
            
    print(f'[Done] File Write Done : {fileName}')
    
    return True


def checkInitDirValid():
    if os.path.isfile(imgListPath) is False:
        print(f'[Error] {imgListPath} is invalid')
        return False
    if os.path.isdir(resDir) is False:
        print(f'[Error] {resDir} is invalid')
        return False
    return True


def readImgList():
    print("[play] Read ImgList")
    imgList = readFileToList(imgListPath)
        
    return imgList


def shuffleImgList(imgList):
    print("[play] Shuffle ImgList")
    shuffle(imgList)
    
    writeListToFile(os.path.join(resDir, "shuffle_" + os.path.basename(imgListPath)), imgList)
     


if __name__ == "__main__":
    if checkInitDirValid() is False:
        sys.exit(-1)
    
    imgList = readImgList()
    shuffleImgList(imgList)