# txt 파일을 읽어서, 전체 이미지 장수, 객체(person, car) 개수, 전체 객체 개수 write 

import os
import sys


txtDir = r"E:\0610\seongnamfalse0125_txt"
resDir = r"E:\0610"

ENCODING_FORMAT     = "UTF-8"


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
    
    for txtfile in txtList:
        if txtfile.endswith(".txt"):
            totalSrcFilePath = os.path.join(txtDir, txtfile)
            
            readList = readFileToList(totalSrcFilePath)
            
            lenTotal += len(readList)  # 전체 객체 개수
            
            for each in readList:
                eachSplit = each.split(" ")
                classes   = eachSplit[0]
                            
                if classes == '0':
                    personTotal += 1   # person 객체 개수
                else:
                    carTotal    += 1   # car 객체 개수
                
            with open(os.path.join(resDir, "analysis_" + os.path.basename(txtDir) + ".txt"), 'w', encoding='utf-8') as f:
                f.write(f"[ img count ]\n")
                f.write(f"* 전체 : {str(imgTotal).rjust(5)}\n")
                f.write(f"\n[ obj count ]\n")
                f.write(f"* 사람 : {str(personTotal).rjust(5)}\n")
                f.write(f"* 차량 : {str(carTotal).rjust(5)}\n")  
                f.write(f"* 전체 : {str(lenTotal).rjust(5)}\n")              
                        


if __name__ == "__main__":
    makeCountResDir(resDir)
    
    if checkInitDirValid() is False:
        sys.exit(-1)
    
    countObject()