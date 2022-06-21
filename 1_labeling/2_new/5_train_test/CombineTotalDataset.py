# img 파일과 txt 파일을 totaol_dataset 폴더로 복사하기

import os
import sys
import shutil


imgDir          = r"E:\0610\seongnamfalse0125_img"
txtDir          = r"E:\0610\seongnamfalse0125_txt"
resDir          = r"E:\0610\dataset2\total_dataset"

ENCODING_FORMAT = "UTF-8"


def checkInitDirValid():
    if os.path.isdir(imgDir) is False:
        print(f'[Error] {imgDir} is invalid')
        return False
    if os.path.isdir(txtDir) is False:
        print(f'[Error] {txtDir} is invalid')
        return False
    if os.path.isdir(resDir) is False:
        print(f'[Error] {resDir} is invalid')
        return False
    return True


def makeDatasetResDir(Dir):
    if not os.path.isdir(Dir):
        os.makedirs(Dir, exist_ok=True)
        

def copyImgFiles():
    print("[ 실행 ] Copy Img Files")
    for path, dirs, files in os.walk(imgDir):
        for file in files:
            shutil.copy(os.path.join(path, file), os.path.join(resDir, file))

def copyTxtFiles():
    print("[ 실행 ] Copy Yolo Txt Files")
    for txt in os.listdir(txtDir):
        shutil.copy(os.path.join(txtDir, txt), os.path.join(resDir, txt))  
    
        
def writeImgList():
    print("[ 실행 ] Write ImgList")
    upperDir = os.path.join(resDir, "../") 
    with open(os.path.join(upperDir, os.path.basename(resDir) + "_list.txt"), 'w', encoding=ENCODING_FORMAT) as f:
        for each in os.listdir(resDir):
            if each.endswith(".jpg"):
                imgListPath = os.path.join(resDir, each)
                f.write(f'{imgListPath}\n')
    
        
if __name__ == "__main__":
    makeDatasetResDir(resDir)
    
    if checkInitDirValid() is False:
        sys.exit(-1)
        
    copyImgFiles()
    copyTxtFiles()
    writeImgList()