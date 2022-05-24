import os
import sys

SRC_PATH        = r"E:\hyena\7_git\test\test_dataset"
DST_PATH        = r"E:\hyena\7_git\test\res_txt_dataset"
ENCODING_FORMAT = "utf-8"

VALID_VALUE     = '1'


def readFileToList(fileName:str):
    fList = []
    
    if os.path.isfile(fileName) is False:
        print(f'[Error] {fileName} is invalid')
        return fList
        
    with open(fileName, 'r', encoding=ENCODING_FORMAT) as rf:
        for eachLine in rf:
            fList.append(eachLine.strip('\n'))

    print(f'[Done] File Read Done : {fileName} - {len(fList)} 개')
    return fList


def writeListToFile(fileName:str, writeList:list):
    fileDir = os.path.dirname(fileName)
    
    if os.path.isdir(fileDir) is False:
        print(f'[Error] {fileDir} is invalid')
        return False
    
    if not writeList:
        with open(fileName, 'w', encoding=ENCODING_FORMAT) as wf:
            wf.write('')
        return True
    
    with open(fileName, 'w', encoding=ENCODING_FORMAT) as wf:
        for eachLine in writeList:
            wf.write(f'{eachLine}\n')
    return True


def writeEmptyToFile(fileName:str):
    fileDir = os.path.dirname(fileName)
    
    if os.path.isdir(fileDir) is False:
        print(f'[Error] {fileDir} is invalid')
        return
    
    with open(fileName, 'w', encoding=ENCODING_FORMAT) as wf:
        wf.write('')


def checkInitDirValid():
    if os.path.isdir(SRC_PATH) is False:
        print(f'[Error] {SRC_PATH} is invalid')
        return False
    if os.path.isdir(DST_PATH) is False:
        print(f'[Error] {DST_PATH} is invalid')
        return False
    return True


def makeEachDestDir(srcDir:str):
    DestDir = srcDir.replace(SRC_PATH, DST_PATH)
    os.makedirs(DestDir, exist_ok=True)
    
    return DestDir 


def searchRecursiveDir():
    print()
    for srcPath, _, files in os.walk(SRC_PATH):
        print('=============================================')
        # 결과 폴더 각각 만들어주기
        dstPath = makeEachDestDir(srcPath)
        
        if files:
            print(f'* {srcPath} -> {dstPath}')
        
        # os.makedirs(os.path.join)
        for file in files:
            if file.endswith('.txt'):
                totalSrcFilePath = os.path.join(srcPath, file)
                totalDstFilePath = os.path.join(dstPath, file)
                
                # [ '1', '3', ... ]
                readList = readFileToList(totalSrcFilePath)
                
                print(f'  - {file} : {readList} : ', end="")
                
                if VALID_VALUE in readList:
                    writeListToFile(totalDstFilePath, readList)
                    print('is Vaild')
                else:
                    writeEmptyToFile(totalDstFilePath)
                    print('Empty Write')

        print('=============================================')
        print()
        


if __name__ == "__main__":
    if checkInitDirValid() is False:
        sys.exit(-1)
    
    searchRecursiveDir()