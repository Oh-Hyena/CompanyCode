# img 파일과 txt 파일을 totaol_dataset 폴더로 복사하기

import os
import sys
import shutil


imgDir          = r"D:\0626\seongnam20200330_falldown_img"
txtDir          = r"D:\0626\seongnam20200330_falldown_txt"
resDir          = r"D:\0626\dataset\total_dataset"

ENCODING_FORMAT = "UTF-8"


class CombineTotalDataset:
    def __init__(self):
        self.copyTxtList = []
        
    
    def checkInitDirValid(self):
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
    
    
    def makeTotalResDir(self, Dir):
        if not os.path.isdir(Dir):
            os.makedirs(Dir, exist_ok=True)
    
    
    def copyTxtFiles(self):
        print("[ Play ] Copy Yolo Txt Files")
        for txt in os.listdir(txtDir):
            self.copyTxtList.append(txt.replace(".txt", ".jpg"))
            shutil.copy(os.path.join(txtDir, txt), os.path.join(resDir, txt)) 
            

    def copyImgFiles(self):
        print("[ Play ] Copy Img Files")
        for path, dirs, files in os.walk(imgDir):
            for file in files:
                if file in self.copyTxtList:
                    shutil.copy(os.path.join(path, file), os.path.join(resDir, file))

       
    def writeImgList(self):
        print("[ Play ] Write ImgList.txt")
        upperDir = os.path.join(resDir, "../") 
        with open(os.path.join(upperDir, os.path.basename(resDir) + "_list.txt"), 'w', encoding=ENCODING_FORMAT) as f:
            for each in os.listdir(resDir):
                if each.endswith(".jpg"):
                    imgListPath = os.path.join(resDir, each)
                    f.write(f'{imgListPath}\n')
    

    def run(self):
        if self.checkInitDirValid() is False:
            sys.exit(-1)
        self.makeTotalResDir(resDir)
        
        self.copyTxtFiles()
        self.copyImgFiles()
        self.writeImgList()


if __name__ == "__main__":
    program = CombineTotalDataset()
    program.run()
