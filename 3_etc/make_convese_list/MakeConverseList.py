import os


total_annotationTxtPath = r"E:\test\total_annotationlist.txt"
total_imgTxtPath = r"E:\test\total_imglist.txt"

test_annotationTxtPath = r"E:\test\test_annotationlist.txt"
test_imgTxtPath = r"E:\test\test_imglist.txt"

res = r"E:\test\res"

ENCODING_FORMAT = 'UTF-8'



def readFileToList(filePath, rList:list, encodingFormat=ENCODING_FORMAT):
    rList.clear()
    with open(filePath, 'r', encoding=encodingFormat) as f:
        for eachLine in f:
            eachLine = eachLine.strip('\n')
            rList.append(eachLine)


def readEntireList():    
    totalAnnotationList = []
    totalImgList = []
    readFileToList(total_annotationTxtPath, totalAnnotationList, encodingFormat=ENCODING_FORMAT)
    readFileToList(total_imgTxtPath, totalImgList, encodingFormat=ENCODING_FORMAT)
    
    testImgList = []
    readFileToList(test_imgTxtPath, testImgList, encodingFormat=ENCODING_FORMAT)
    
    print('[Done] Read Entire List')
    
    return totalImgList, testImgList, totalAnnotationList
    

def makeTrainList(totalImgList, testImgList, totalAnnotationList):
    trainAnnotationList = []
    trainImgList = []
    
    for idx, each in enumerate(totalImgList):
        if each not in testImgList:
            trainAnnotationList.append(totalAnnotationList[idx])
            trainImgList.append(totalImgList[idx])
            
    print('[Done] Make Converse AnnotationList.txt, Converse ImgList.txt')
            
    return trainAnnotationList, trainImgList

    
def writeListToFile(filePath, wList, encodingFormat=ENCODING_FORMAT):
    with open(filePath, 'w', encoding=encodingFormat) as f:
        for line in wList:
            f.write(f'{line}\n')
            

def writeTrainList(trainAnnotationList, trainImgList):
    trainAnnotationListPath = os.path.join(res, 'train_annotationList.txt')
    trainImgListPath = os.path.join(res, 'train_imglist.txt')
    
    writeListToFile(trainAnnotationListPath, trainAnnotationList, encodingFormat=ENCODING_FORMAT)
    writeListToFile(trainImgListPath, trainImgList, encodingFormat=ENCODING_FORMAT)
    
    print('[Done] Write Entire List')
    

if __name__ == "__main__":
    totalImgList, testImgList, totalAnnotationList = readEntireList()
    trainAnnotationList, trainImgList = makeTrainList(totalImgList, testImgList, totalAnnotationList)
    writeTrainList(trainAnnotationList, trainImgList)
