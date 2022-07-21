import os
import cv2
import numpy as np

imgDir = r'E:\test\img'
txtDir = r'E:\test\txt'
resDir = r'E:\test\res'

saveFolderName = "att_seongnamfalse0311"
saveFileNum    = 150

# s나중
# class 선택 (default == person)
# xlen, ylen 설정 (default == (xlen>25 and ylen>25))


# *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
def listDir(Dir):
    dirList = []
    for root, _, files in os.walk(Dir):
        for file in files:
            dirPath = os.path.join(root, file)
            dirList.append(dirPath)
    
    return dirList


# *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
def makeImgSizeList(imgDirList):
    imgSizeList = []
    for each in imgDirList:
        imgFolderName = os.path.basename(each.split('\\')[-2])
        imgFileName = os.path.basename(each.split('.')[0])
        img         = cv2.imread(each, cv2.IMREAD_COLOR)
        h, w, c     = img.shape
        imgSizeList.append(f'{imgFolderName} {imgFileName} {w} {h}')

    return imgSizeList


# *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
def makeTxtList(txtDirList):
    txtList = []
    for each in txtDirList:
        txtFileName = os.path.basename(each.split('.')[0])
        with open(each, 'r', encoding='utf-8') as f:
            for eachLine in f:
                if eachLine[0] == '0':  # 0 == person
                    eachLine = eachLine.strip('\n')
                    txtList.append(f'{txtFileName} {eachLine}')

    return txtList


# *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
def makeImgInfoList(txtList, imgSizeList):
    imgInfoList = []
    for eachTxt in txtList:
        eachTxtSplit = eachTxt.split(" ")
        txtFilename  = eachTxtSplit[0]
        for eachImg in imgSizeList:
            eachImgSplit = eachImg.split(" ")
            imgFoldername = eachImgSplit[0]
            if txtFilename in eachImg:
                imgInfoList.append(f'{imgFoldername} {txtFilename} {eachTxtSplit[2]} {eachTxtSplit[3]} {eachTxtSplit[4]} {eachTxtSplit[5]} {eachImgSplit[2]} {eachImgSplit[3]}')

    return imgInfoList


# *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
def makeXyInfoList(imgInfoList):
    xyInfoList = []
    for each in imgInfoList:
        eachSplit      = each.split(" ")
        cropfolderName = eachSplit[0]
        cropfileName   = eachSplit[1]

        box_x_mid  = float(eachSplit[2])
        box_y_mid  = float(eachSplit[3])
        box_width  = float(eachSplit[4])
        box_height = float(eachSplit[5])

        img_width  = int(eachSplit[6])
        img_height = int(eachSplit[7])

        xtl  = ((2 * box_x_mid * img_width)  - (box_width  * img_width))  / 2
        ytl  = ((2 * box_y_mid * img_height) - (box_height * img_height)) / 2
        xbr  = ((2 * box_x_mid * img_width)  + (box_width  * img_width))  / 2
        ybr  = ((2 * box_y_mid * img_height) + (box_height * img_height)) / 2

        xlen = abs(int(float(xtl)) - int(float(xbr)))
        ylen = abs(int(float(ytl)) - int(float(ybr)))

        if (xlen > 10) and (ylen > 10):
            xyInfoList.append(f'{cropfolderName} {cropfileName} {xtl} {ytl} {xbr} {ybr}')
    
    return xyInfoList
    

# *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
def imread(filename, flags=cv2.IMREAD_COLOR, dtype=np.uint8):
    try:
        n   = np.fromfile(filename, dtype)
        img = cv2.imdecode(n, flags)
        return img
    
    except Exception as e:
        print(f"imread error : {e}")
        return None
    
    
def imwrite(filename, img, params=None):
    try:
        ext       = os.path.splitext(filename)[1]
        result, n = cv2.imencode(ext, img, params)

        if result:
             with open(filename, mode='w+b') as f:
                 n.tofile(f)
             return True
        else:
             return False
         
    except Exception as e:
        print(f"imwrite error : {e}")
        return False


# *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
def makeEachDestDir(Count):  
    folderName = saveFolderName + "_" + str(Count).zfill(6)
    DestDir    = os.path.join(resDir, folderName)
    os.makedirs(DestDir, exist_ok=True)

    return DestDir


# *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
def cropPerson(xyInfoList):
    folderCount = 1
    fileCount   = 1

    for eachXy in xyInfoList:
        DestDir = makeEachDestDir(folderCount)

        eachXySplit    = eachXy.split(" ")
        cropFolderName = eachXySplit[0]
        cropFileName   = eachXySplit[1]
        imgPath        = os.path.join(imgDir, cropFolderName)
        img            = imread(os.path.join(imgPath, cropFileName + '.jpg'), cv2.IMREAD_COLOR)

        if img is None: break

        src     = img.copy()
        cropXtl = eachXySplit[2]
        cropYtl = eachXySplit[3]
        cropXbr = eachXySplit[4]
        cropYbr = eachXySplit[5]

        cropImg = src[int(float(cropYtl)):int(float(cropYbr)), int(float(cropXtl)):int(float(cropXbr))]

        DestFileName = cropFolderName + "_" + str(fileCount).zfill(6) + '.jpg'
        imwrite(os.path.join(DestDir, DestFileName), cropImg)

        fileCount += 1

        if fileCount == saveFileNum + 1:
            folderCount += 1
            fileCount    = 1
    

if __name__ == "__main__":
    imgDirList  = listDir(imgDir)
    imgSizeList = makeImgSizeList(imgDirList)
    txtDirList  = listDir(txtDir)
    txtList     = makeTxtList(txtDirList)
    imgInfoList = makeImgInfoList(txtList, imgSizeList)
    xyInfoList  = makeXyInfoList(imgInfoList)
    cropPerson(xyInfoList)
