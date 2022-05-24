import os
import cv2
import numpy as np
import imgaug as ia
import imgaug.augmenters as iaa
import numpy as np

IMAGE_EXT_LIST = ['.jpg', '.jpeg', '.png']
IMAGE_DIR_NAME = r'E:\test\aug_test\img'
saveDir = r'E:\test\aug_test\aug'

def GetImageFileList(DirName):
    _imageFileList = []
    _imageNameList = []

    if os.path.isdir(DirName) is False:
        print(f"{DirName} is Not Exist!")
        return None

    fileList = os.listdir(DirName)
    for eachFile in fileList:
        _, ext = os.path.splitext(eachFile)

        if ext in IMAGE_EXT_LIST:
            _imageFileList.append(os.path.join(DirName, eachFile))
            _imageNameList.append(eachFile)

    return _imageFileList, _imageNameList


def GetEachImageImReadList(FileList):
    _imReadList = []

    for eachFile in FileList:
        img = cv2.imread(eachFile)
        if img is not None:
            _imReadList.append(img)
    
    return _imReadList


def SaveAugImageList(AugImageList, imageNameList):
    savePath = os.path.join(saveDir, 'Res')

    if os.path.isdir(savePath) is False:
        os.makedirs(savePath, exist_ok=True)

    for idx, eachFile in enumerate(AugImageList):
        cv2.imwrite(os.path.join(savePath, imageNameList[idx]), eachFile)


def ImageListAugumentation(imReadList):
    # fliplr 좌우 반전
    seq = iaa.Sequential([iaa.Fliplr(1.0)])
    res = seq.augment_images(imReadList)

    # flipud 상하 반전
    # seq = iaa.Sequential([iaa.Flipud(1.0)])
    # res = seq.augment_images(imReadList)

    # rotation 각도 변경
    # seq = iaa.Sequential([iaa.Affine(rotate=(-10, -10))])
    # res = seq.augment_images(imReadList)

    # rotation 각도 변경
    # seq = iaa.Sequential([iaa.Affine(rotate=(20, 20))])
    # res = seq.augment_images(imReadList)

    # shearing
    # seq = iaa.Sequential([iaa.Affine(shear=(-15, 15))])
    # res = seq.augment_images(imReadList)

    return res


if __name__ == "__main__":
    imageFileList, imageNameList    = GetImageFileList(IMAGE_DIR_NAME)
    imReadList                      = GetEachImageImReadList(imageFileList)

    resultImgList                   = ImageListAugumentation(imReadList)
    SaveAugImageList(resultImgList, imageNameList)



