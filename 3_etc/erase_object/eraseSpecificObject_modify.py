# txt 파일을 읽어서 조건에 해당하는 것만 가져오기

import os
import sys

SRC_PATH        = r"D:\hyena\7_git\CompanyCode\3_etc\erase_object\txt"
DST_PATH        = r"D:\hyena\7_git\CompanyCode\3_etc\erase_object\res"
ENCODING_FORMAT = "utf-8"

imgXlen         = 40
imgYlen         = 30


def readFileToList(fileName:str):
    fList = []
    
    if os.path.isfile(fileName) is False:
        print(f'[Error] {fileName} is invalid')
        return fList
        
    with open(fileName, 'r', encoding=ENCODING_FORMAT) as rf:
        for eachLine in rf:
            fList.append(eachLine.strip('\n'))

    print()
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
                
                
                imgWidth  = 1920
                imgHeight = 1080
                
                tmpValidValueList = []
                
                for each in readList:
                    eachSplit = each.split(" ")
                    
                    x_mid  = float(eachSplit[1])
                    y_mid  = float(eachSplit[2])
                    width  = float(eachSplit[3])
                    height = float(eachSplit[4])
                
                    ytl = ((2 * y_mid * imgHeight) + (height * imgHeight)) / 2
                    ybr = ((2 * y_mid * imgHeight) - (height * imgHeight)) / 2
                    xtl = ((2 * x_mid * imgWidth)  + (width  * imgWidth))  / 2
                    xbr = ((2 * x_mid * imgWidth)  - (width  * imgWidth))  / 2
                    
                    xlen = abs(float(xtl)-float(xbr))
                    ylen = abs(float(ytl)-float(ybr))
                    
                    # 큰 사이즈 객체만 남기기
                    if float(xlen) > imgXlen and float(ylen) > imgYlen:
                        tmpValidValueList.append(each)
                        print('is Vaild')
                    else:
                        print('Empty Write')
                        
                writeListToFile(totalDstFilePath, tmpValidValueList)
                

        print('=============================================')
        print()
        


if __name__ == "__main__":
    if checkInitDirValid() is False:
        sys.exit(-1)
    
    searchRecursiveDir()