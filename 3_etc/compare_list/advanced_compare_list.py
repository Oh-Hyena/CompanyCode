import os
import sys

ENCODING_FORMAT = 'utf-8'

Compare_One_FilePath = r"E:\39class_attribute_dataset\1st_version\total_imglist_annotation_imgsize\total_img_list\cvat_39Class_ImgList.txt"
Compare_Two_FilePath = r"E:\39class_attribute_dataset\1st_version\total_imglist_annotation_imgsize\total_img_list\origin_39Class_ImgList.txt"

CGREEN  = '\x1b[32m'
CYELLOW = '\x1b[33m'
CRESET  = '\x1b[0m'


def checkExistFile(FileName):
    if os.path.isfile(FileName) is False:
        print(f'{FileName} is Not Exist File! Program Quit.')
        sys.exit(-1)


def readFileToDict(filePath, encodingFormat=ENCODING_FORMAT):
    checkExistFile(filePath)
    rDict = {}
    with open(filePath, 'r', encoding=encodingFormat) as f:
        for idx, eachLine in enumerate(f):
            eachLine = eachLine.strip('\n')
            rDict[eachLine] = idx+1
    print(f'Read File To Dict Done << {filePath}')
    return rDict
    
    
def checkOverWrittenFromDicts(Dict_A:dict, Dict_B:dict):
    calcCountAtoB = 0
    
    print()
    # Compare A -> B
    print(f'Cmp Direction : {CGREEN}{Compare_One_FilePath}{CRESET} -> {CYELLOW}{Compare_Two_FilePath}{CRESET}')
    print('='*100)
    for eachElem in Dict_A.keys():
        if Dict_B.get(eachElem) is not None:
            print(f'[OverWritten] [ {CGREEN}{Dict_A[eachElem]:^5}{CRESET} ~ {CYELLOW}{Dict_B[eachElem]:^5}{CRESET} ] Msg : {eachElem}')
            calcCountAtoB += 1
    print()
    if calcCountAtoB == 0:
        print('Overwritten Nothing!')
    else:
        print(f'Overwitten : {calcCountAtoB}')
    print()
        
        
if __name__ == "__main__":
    cmp_one_dict = readFileToDict(Compare_One_FilePath)
    cmp_two_dict = readFileToDict(Compare_Two_FilePath)
    
    checkOverWrittenFromDicts(cmp_one_dict, cmp_two_dict)