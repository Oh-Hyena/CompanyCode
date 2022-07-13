# change new version cvatxml's form 
# try new version cvatxml's environment

import os
import sys
import zipfile
import shutil



# extract 'yolo txt' zipfile at cvatxml server ('not image')
zipDir          = r"D:\hyena\3_dataset\seongnam\2020\0330\seongnam\231_300\zip"
resDir          = r"D:\hyena\3_dataset\seongnam\2020\0330\seongnam\231_300\seongnam20200330_falldown_txt"

ENCODING_FORMAT = "UTF-8"
deleteFileList  = ["obj.data", "obj.names"]  # 고정값


class UnzipClass:
    def __init__(self):
        self.zipList = []
        
        
    def checkInitDirValid(self):
        if os.path.isdir(zipDir) is False:
            print(f'[Error] {zipDir} is invalid')
            return False
        if os.path.isdir(resDir) is False:
            print(f'[Error] {resDir} is invalid')
            return False
        return True


    def makeUnzipResDir(self, Dir):
        if not os.path.isdir(Dir):
            os.makedirs(Dir, exist_ok=True)
    
    
    def writeZipList(self):
        for path, dirs, files in os.walk(zipDir):
            for file in files:
                self.zipList.append(os.path.join(path, file))

    
    def unzip(self):
        print("[ play ] Unzip")
    
        self.writeZipList()
        
        for zipFile in self.zipList:
            with zipfile.ZipFile(zipFile, 'r') as f:
                f.extractall(resDir)   
        
    
    def moveYoloTxtFile():
        print("[ play ] Move Yolo Txt")
        
        for path, dirs, files in os.walk(resDir):
            for file in files:
                if file.endswith(".txt") and file != "train.txt":
                    shutil.move(os.path.join(path, file), os.path.join(resDir, file))
        
    
    # 폴더 안에 파일이 없어야 폴더 삭제 가능!
    def deleteNothing():
        print("[ play ] Delete Nothing Dir")
    
        # zip 파일 삭제
        for each in os.listdir(zipDir):
            os.remove(os.path.join(zipDir, each))
        
        # 빈 폴더 삭제
        os.rmdir(zipDir)
        os.rmdir(os.path.join(resDir, "obj_train_data"))
        
        # 파일 삭제
        for each in deleteFileList:
            os.remove(os.path.join(resDir, each))
    
    
    def run(self):
        if self.checkInitDirValid() is False:
            sys.exit(-1)
        self.makeUnzipResDir(resDir)
        
        self.unzip()
        self.moveYoloTxtFile()
        self.deleteNothing()
    
    
if __name__ == "__main__":
    program = UnzipClass()
    program.run()
