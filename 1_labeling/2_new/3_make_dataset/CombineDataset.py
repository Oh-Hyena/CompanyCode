import os
import sys
import shutil


originDatasetDir = r"C:\Users\ohhye\VisionProject\1_labeling\dataset"
newDatasetDir    = r"D:\hyena\3_dataset\seongnam\2020\0330\seongnam\231_300\dataset"

ENCODING_FORMAT = "UTF-8"


class CombineDataset:
    def __init__(self):
        self.newList   = []
        
        self.trainList = []
        self.validList = []
        self.testList  = []
        
        
    def checkInitDirValid(self):
        if os.path.isdir(originDatasetDir) is False:
            print(f'[Error] {originDatasetDir} is invalid')
            return False
        if os.path.isdir(newDatasetDir) is False:
            print(f'[Error] {newDatasetDir} is invalid')
            return False
        return True
    
    
    def makeTotalCopyList(self):
        for path, dir, files in os.walk(newDatasetDir):
            for file in files:
                if 'list' not in file:
                    self.newList.append(f'{os.path.basename(file)},{os.path.join(path, file)}')


    def makeTypeCopyList(self):
        for each in self.newList:
            if 'train' in each:
                self.trainList.append(each)
            elif 'valid' in each:
                self.validList.append(each)
            elif 'test' in each:
                self.testList.append(each)
     
    
    def getDirectoryList(self, rootDir:str) -> list:
        resList = []
        for _, dirs, _ in os.walk(rootDir):
            resList = dirs
            break
        return [ os.path.join(rootDir, each) for each in resList]
           
                
    def CopyFiles(self):
        for eachPath in self.getDirectoryList(originDatasetDir):
            
            curRelativeDirName = os.path.basename(eachPath)
            
            if curRelativeDirName == 'train_dataset':
                selectList = self.trainList.copy()
            elif curRelativeDirName == 'valid_dataset':
                selectList = self.validList.copy()
            elif curRelativeDirName == 'test_dataset':
                selectList = self.testList.copy()
                
            for each in selectList:
                each = each.split(',')
                eachFileName = each[0]
                srcFilePath  = each[1]
                dstFilePath  = os.path.join(eachPath, eachFileName)
                shutil.copy(srcFilePath, dstFilePath)
            
            
    def run(self):
        if self.checkInitDirValid() is False:
            sys.exit(-1)
        
        self.makeTotalCopyList()
        self.makeTypeCopyList()
        self.CopyFiles()


if __name__ == "__main__":
    program = CombineDataset()
    program.run()