import os
import sys
import shutil


totalDatasetDir = r"E:\0610\dataset2\total_dataset"
imgListPath     = r"E:\0610\dataset2\shuffle_total_dataset_list.txt"
resDir          = r"E:\0610\dataset2"

ENCODING_FORMAT = "UTF-8"
splitPecent     = [80, 10, 10]  # [train, valid, test]


def checkInitDirValid():
    if os.path.isdir(totalDatasetDir) is False:
        print(f'[Error] {totalDatasetDir} is invalid')
        return False
    if os.path.isdir(resDir) is False:
        print(f'[Error] {resDir} is invalid')
        return False
    
    return True


def makeSplitResDir(Dir):
    if not os.path.isdir(Dir):
        os.makedirs(Dir, exist_ok=True)
    if not os.path.isfile(os.path.join(Dir, "train_dataset")):
        trainPath = os.path.join(Dir, "train_dataset")
        os.makedirs(trainPath, exist_ok=True)
    if not os.path.isfile(os.path.join(Dir, "valid_dataset")):
        validPath = os.path.join(Dir, "valid_dataset")
        os.makedirs(validPath, exist_ok=True)
    if not os.path.isfile(os.path.join(Dir, "test_dataset")):
        testPath = os.path.join(Dir, "test_dataset")
        os.makedirs(testPath, exist_ok=True)

    print('[Done] Make Train, Valid, Test Directory')
    
    return trainPath, validPath, testPath


def readShuffleTotalDataset():
    shuffleTotalDatasetImgList = []
    shuffleTotalDatasetTxtList = []
    
    with open(imgListPath, 'r', encoding=ENCODING_FORMAT) as f:
        for eachLine in f:
            eachLine = eachLine.strip('\n')
            imgName  = eachLine.split('\\')[-1]
            txtName  = imgName.replace(".jpg", ".txt")
            shuffleTotalDatasetImgList.append(imgName)
            shuffleTotalDatasetTxtList.append(txtName)
            
    print('[Done] Read Shuffle Total Dataset ImgList.txt')
    
    return shuffleTotalDatasetImgList, shuffleTotalDatasetTxtList


def splitTotalDataset(shuffleTotalDatasetImgList, shuffleTotalDatasetTxtList, trainPath, validPath, testPath):
    trainImgList   = []
    trainTxtList   = []
    remnantImgList = []
    remnantTxtList = []
    
    validImgList   = []
    validTxtList   = []
    testImgList    = []
    testTxtList    = []
    
    TotalAmount      = int(len(shuffleTotalDatasetImgList))
    TrainSplitAmount = int(len(shuffleTotalDatasetImgList)*splitPecent[0]/100)
    ValidSplitAmount = int(len(shuffleTotalDatasetImgList)*splitPecent[1]/100)
    TestSplitAmount  = int(len(shuffleTotalDatasetImgList)*splitPecent[2]/100)
    
    for idx, each in enumerate(shuffleTotalDatasetImgList):
        if idx < TrainSplitAmount:
            trainImgList.append(each)
            trainTxtList.append(shuffleTotalDatasetTxtList[idx])
        else:
            remnantImgList.append(each)
            remnantTxtList.append(each.replace(".jpg", ".txt"))
    
    for idx, each in enumerate(remnantImgList):
        if idx < ValidSplitAmount:
            validImgList.append(each)
            validTxtList.append(remnantTxtList[idx])
        else:
            testImgList.append(each)
            testTxtList.append(remnantTxtList[idx])
            
    eachCopyImg(trainImgList, trainPath)
    eachCopyTxt(trainTxtList, trainPath)
    print(f'[Done] Copy Train Img and Txt')
    
    eachCopyImg(validImgList, validPath)
    eachCopyTxt(validTxtList, validPath)
    print(f'[Done] Copy Valid Img and Txt')
    
    eachCopyImg(testImgList, testPath)
    eachCopyTxt(testTxtList, testPath)
    print(f'[Done] Copy Test Img and Txt')
    
    
    print(f'[Done] Divide Total Dataset\n')
    print(f'[Output]')
    print(f'Total : 100% | {TotalAmount}장')
    print(f'Train : {str(splitPecent[0]).rjust(3)}% | {str(TrainSplitAmount).rjust(3)}장')
    print(f'Valid : {str(splitPecent[1]).rjust(3)}% | {str(ValidSplitAmount).rjust(3)}장')
    print(f'Test  : {str(splitPecent[2]).rjust(3)}% | {str(TestSplitAmount).rjust(3)}장')
    
    return TotalAmount, TrainSplitAmount, ValidSplitAmount, TestSplitAmount
            

def eachCopyImg(list, path):
    for each in list:
        shutil.copy(os.path.join(totalDatasetDir, each), os.path.join(path, each))


def eachCopyTxt(list, path):
    for each in list:
        shutil.copy(os.path.join(totalDatasetDir, each), os.path.join(path, each))
        

def writeSplitDataset(TotalAmount, TrainSplitAmount, ValidSplitAmount, TestSplitAmount):
    with open(os.path.join(resDir, "split_total_dataset.txt"), 'w', encoding=ENCODING_FORMAT) as f:
        f.write(f"[ total Dataset - 100% ]\n")
        f.write(f"* Total : 100%, {TotalAmount}장\n")
        f.write(f"\n[ split Dataset - {str(splitPecent[0]).rjust(3)}% : {str(splitPecent[1]).rjust(3)}% : {str(splitPecent[2]).rjust(3)}% ]\n")
        f.write(f'* Train : {str(TrainSplitAmount).rjust(3)}장\n')
        f.write(f'* Valid : {str(ValidSplitAmount).rjust(3)}장\n')
        f.write(f'* Test  : {str(TestSplitAmount).rjust(3)}장\n')
            
    
if __name__ == "__main__":
    trainPath, validPath, testPath = makeSplitResDir(resDir)
    
    if checkInitDirValid() is False:
        sys.exit(-1)
        
    shuffleTotalDatasetImgList, shuffleTotalDatasetTxtList = readShuffleTotalDataset()
    TotalAmount, TrainSplitAmount, ValidSplitAmount, TestSplitAmount = splitTotalDataset(shuffleTotalDatasetImgList, shuffleTotalDatasetTxtList, trainPath, validPath, testPath)
    writeSplitDataset(TotalAmount, TrainSplitAmount, ValidSplitAmount, TestSplitAmount)
    
    
