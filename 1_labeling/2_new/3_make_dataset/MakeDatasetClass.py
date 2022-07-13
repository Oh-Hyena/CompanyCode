# totalImgList.txt 만들기
# shuffle 해서 shuffleImgList.txt 만들기
# splitPercent 만큼 train/valid/test 로 나누어 splitImgList.txt splitTxtList.txt 만들기
# splitTxtList.txt 만큼 train/valid/test_dataset 폴더에 img, txt 파일 복사하기 

import os
import sys
from random import shuffle
import shutil


imgDir = r"D:\hyena\3_dataset\seongnam\2020\0330\seongnam\231_300\seongnam20200330_falldown_img"
txtDir = r"D:\hyena\3_dataset\seongnam\2020\0330\seongnam\231_300\seongnam20200330_falldown_txt"
resDir = r"D:\hyena\3_dataset\seongnam\2020\0330\seongnam\231_300\dataset"

ENCODING_FORMAT = "UTF-8"
splitPercent     = [80, 10, 10]  # [train, valid, test]


class makeDataset:
    def __init__(self):
        self.trainPath = None
        self.validPath = None
        self.testPath  = None
        
        self.TotalImgList     = []
        self.TotalTxtList     = []
        
        self.shuffleZipList   = []
        self.ShuffleImgList   = []
        self.ShuffleTxtList   = []
       
        
        self.TotalAmount      = 0
        self.TrainSplitAmount = 0
        self.ValidSplitAmount = 0
        self.TestSplitAmount  = 0
        
        self.trainImgList     = []
        self.trainTxtList     = []
        self.remnantImgList   = []
        self.remnantTxtList   = []
        
        self.validImgList     = []
        self.validTxtList     = []
        self.testImgList      = []
        self.testTxtList      = []
        
    
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
    
    
    def makeDatasetResDir(self, Dir):
        if not os.path.isdir(Dir):
            os.makedirs(Dir, exist_ok=True)
        if not os.path.isfile(os.path.join(Dir, "train_dataset")):
            self.trainPath = os.path.join(Dir, "train_dataset")
            os.makedirs(self.trainPath, exist_ok=True)
        if not os.path.isfile(os.path.join(Dir, "valid_dataset")):
            self.validPath = os.path.join(Dir, "valid_dataset")
            os.makedirs(self.validPath, exist_ok=True)
        if not os.path.isfile(os.path.join(Dir, "test_dataset")):
            self.testPath = os.path.join(Dir, "test_dataset")
            os.makedirs(self.testPath, exist_ok=True)
    
    
    def makeTotalImgList(self):
        print("[ Play ] Make Total ImgList")
    
        for path, dir, files in os.walk(imgDir):
            for file in files:
                totalImgPathList = os.path.join(path, file)
                self.TotalImgList.append(f'{totalImgPathList}\n')
                self.TotalImgList.sort()
        

    def makeTotalTxtList(self):
        print("[ Play ] Make Total TxtList")
    
        for path, dir, files in os.walk(txtDir):
            for file in files:
                totalTxtPathList = os.path.join(path, file)
                self.TotalTxtList.append(f'{totalTxtPathList}\n')
                self.TotalTxtList.sort()
        
    
    def shuffleImgList(self):
        print("[ play ] Shuffle ImgList")
        self.shuffleZipList = list(zip(self.TotalImgList, self.TotalTxtList))
        shuffle(self.shuffleZipList) 
        
    
    def makeShuffleList(self):
        for each in self.shuffleZipList:
            self.ShuffleImgList.append(each[0])
            self.ShuffleTxtList.append(each[1])

        
    def SplitAmount(self):
        self.TotalAmount      = int(len(self.ShuffleImgList))
        self.TrainSplitAmount = int(len(self.ShuffleImgList)*splitPercent[0]/100)
        self.ValidSplitAmount = int(len(self.ShuffleImgList)*splitPercent[1]/100)
        self.TestSplitAmount  = int(len(self.ShuffleImgList)*splitPercent[2]/100)
        
       
    def makeSplitList(self):
        print("[ Play ] Make Train/Valid/Test ImgList and TxtList")   
        
        for idx, each in enumerate(self.ShuffleImgList):
            if idx < self.TrainSplitAmount:
                self.trainImgList.append(each)
                self.trainTxtList.append(self.ShuffleTxtList[idx])
            else:
                self.remnantImgList.append(each)
                self.remnantTxtList.append(self.ShuffleTxtList[idx])
        
        for idx, each in enumerate(self.remnantImgList):
            if idx < self.ValidSplitAmount:
                self.validImgList.append(each)
                self.validTxtList.append(self.remnantTxtList[idx])
            else:
                self.testImgList.append(each)
                self.testTxtList.append(self.remnantTxtList[idx])
        
    
    def eachCopyImg(self, list, path):
        for each in list:
            eachLine = each.strip('\n')
            eachBase = os.path.basename(eachLine)
            shutil.copy(eachLine, os.path.join(path, eachBase))
            

    def eachCopyTxt(self, list, path):
        for each in list:
            eachLine = each.strip('\n')
            eachBase = os.path.basename(eachLine)
            shutil.copy(eachLine, os.path.join(path, eachBase))


    # 다시 만들어야 함
    def eachResList(self, list, path):
        type = os.path.basename(path.split("_")[0])
        with open(os.path.join(resDir, type + "_list.txt"), 'w', encoding=ENCODING_FORMAT) as f:
            for each in os.listdir(path):
                if each.endswith('.jpg'):
                    imgListPath = os.path.join(path, each)
                    f.write(f'{imgListPath}\n')
    
    
    def CopyImgAndTxt(self):
        print(f'[ Play ] Copy Train Img and Txt')
        self.eachCopyImg(self.trainImgList, self.trainPath)
        self.eachCopyTxt(self.trainTxtList, self.trainPath)
        self.eachResList(self.trainTxtList, self.trainPath)
        
        print(f'[ Play ] Copy Valid Img and Txt')
        self.eachCopyImg(self.validImgList, self.validPath)
        self.eachCopyTxt(self.validTxtList, self.validPath)
        self.eachResList(self.validTxtList, self.validPath)
        
        print(f'[ Play ] Copy Test Img and Txt')
        self.eachCopyImg(self.testImgList, self.testPath)
        self.eachCopyTxt(self.testTxtList, self.testPath)
        self.eachResList(self.testTxtList, self.testPath)
                     

    def run(self):
        if self.checkInitDirValid() is False:
            sys.exit(-1)
        self.makeDatasetResDir(resDir)
        
        self.makeTotalImgList()
        self.makeTotalTxtList()
        
        self.shuffleImgList()
        self.makeShuffleList()
        
        self.SplitAmount()
        self.makeSplitList()
        
        self.CopyImgAndTxt()
        

if __name__ == "__main__":
    program = makeDataset()
    program.run()
