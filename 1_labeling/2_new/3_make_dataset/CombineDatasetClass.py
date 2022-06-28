import os
import sys
import shutil

from numpy import save


# destination
originDatasetDir = r"D:\dataset3"
# source
newDatasetDir    = r"D:\0628\dataset"

ENCODING_FORMAT = "UTF-8"


class CombineDataset:
    def __init__(self):
        self.newList      = []
        
        self.trainList    = []
        self.validList    = []
        self.testList     = []
        
        self.TxtList      = []
        
        self.trainTxtList = []
        self.validTxtList = []
        self.testTxtList  = []
        
        
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
                elif 'list' in file:
                    self.TxtList.append(file)


    def makeEachCopyList(self):
        for each in self.newList:
            if 'train' in each:
                self.trainList.append(each)
            elif 'valid' in each:
                self.validList.append(each)
            elif 'test' in each:
                self.testList.append(each)
                
    
    def makeEachTxtList(self):
        for each in self.TxtList:
            if 'train_list.txt' in each:
                self.readTxtFiles(each, self.trainTxtList)
            elif 'valid_list.txt' in each:
                self.readTxtFiles(each, self.validTxtList)
            elif 'test_list.txt' in each:
                self.readTxtFiles(each, self.testTxtList)
                        
                        
    def readTxtFiles(self, each, txtList):
        with open(os.path.join(newDatasetDir, each), 'r', encoding=ENCODING_FORMAT) as f:
            for eachLine in f:
                eachLine = eachLine.strip('\n')
                txtList.append(eachLine)
    
    
    def makeTotalTxtList(self):
        for each in self.TxtList:
            if 'train_list.txt' in each:
                self.writeTxtList(each, self.trainTxtList)
            elif 'valid_list.txt' in each:
                self.writeTxtList(each, self.validTxtList)
            elif 'test_list.txt' in each:
                self.writeTxtList(each, self.testTxtList)
    
    
    def writeTxtList(self, each, txtList):
        with open(os.path.join(originDatasetDir, each), 'a') as f:
            for eachLine in txtList:
                f.write(f'{eachLine}\n')
    
    
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
        self.makeEachCopyList()
        self.makeEachTxtList()
        self.makeTotalTxtList()
        
        self.CopyFiles()

        
if __name__ == "__main__":
    program = CombineDataset()
    program.run()