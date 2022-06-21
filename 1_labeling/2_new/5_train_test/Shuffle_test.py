# imglist.txt 파일 random 으로 섞기

import os
import sys
from random import shuffle


imgListPath     = r"E:\0610\dataset\total_dataset_list.txt"
resDir          = r"E:\0610\dataset"

ENCODING_FORMAT = "UTF-8"
resFileName     = "shuffle_total_dataset"


def checkInitDirValid():
    if os.path.isfile(imgListPath) is False:
        print(f'[Error] {imgListPath} is invalid')
        return False
    if os.path.isdir(resDir) is False:
        print(f'[Error] {resDir} is invalid')
        return False
    return True


def readImgList():
    print("[ 실행 ] Read ImgList")
    
    imgList = []
    
    with open(imgListPath, 'r', encoding=ENCODING_FORMAT) as f:
        for each in f:
            each = each.strip('\n')
            imgList.append(each)
        
    return imgList


def shuffleImgList(imgList):
    print("[ 실행 ] Shuffle ImgList")
    
    shuffle(imgList)
        
    with open(os.path.join(resDir, "shuffle_" + os.path.basename(imgListPath)), 'w') as f:
        for each in imgList:
            f.write(f"{each}\n")
    


if __name__ == "__main__":
    if checkInitDirValid() is False:
        sys.exit(-1)
    
    imgList = readImgList()
    shuffleImgList(imgList)