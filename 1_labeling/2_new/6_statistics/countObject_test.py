# txt 파일을 읽어서, 전체 이미지 장수, 객체(person, car) 개수, 전체 객체 개수 write 

import os
import sys


txtDir = r"E:\0610\dataset\total_dataset"
resDir = r"F:\재작업\done\res"


ENCODING_FORMAT     = "UTF-8"
resAnalysisFileName = "res"


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
    
    with open(fileName, 'w', encoding=ENCODING_FORMAT) as wf:
        for eachLine in writeList:
            wf.write(f'{eachLine}\n')
    return True


def checkInitDirValid():
    if os.path.isdir(txtDir) is False:
        print(f'[Error] {txtDir} is invalid')
        return False
    if os.path.isdir(resDir) is False:
        print(f'[Error] {resDir} is invalid')
        return False
    return True


def makeCountResDir(resDir):
    if not os.path.isdir(resDir):
        os.makedirs(resDir, exist_ok=True)


def countObject():
    imgTotal   = 0
    
    txtList    = os.listdir(txtDir)
    imgTotal   = len(txtList)  # 이미지 장수
    
    lenTotal    = 0
    personTotal = 0
    carTotal    = 0
    
    print()   
    print('=============================================')
    print()
    
    if txtList.endswith(".txt"):
        for txtfile in txtList:
            print("75 : ", txtfile)
            totalSrcFilePath = os.path.join(txtDir, txtfile)
            
            readList = readFileToList(totalSrcFilePath)
            print(f'  - {txtfile} : {readList} ', end="\n")
            print()
            
            lenTotal += len(readList)  # 전체 객체 개수
            
            for each in readList:
                eachSplit = each.split(" ")
                classes   = eachSplit[0]
                            
                if classes == '0':
                    personTotal += 1  # person 객체 개수
                else:
                    carTotal += 1     # car 객체 개수
                
            resFileName = resAnalysisFileName + "_analysis.txt"
            with open(os.path.join(resDir, resFileName), 'w', encoding='utf-8') as f:
                f.write(f"전체 이미지 장수 : {imgTotal}\n")
                f.write(f"person : {personTotal}\n")
                f.write(f"car : {carTotal}\n")  
                f.write(f"전체 객체 개수 : {lenTotal}\n")              
                        
    print('=============================================')
    print()
    


if __name__ == "__main__":
    makeCountResDir(resDir)
    
    if checkInitDirValid() is False:
        sys.exit(-1)
    
    countObject()