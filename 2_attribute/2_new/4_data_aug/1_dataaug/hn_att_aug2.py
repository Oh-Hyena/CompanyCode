import os
import cv2
import numpy as np
import imgaug as ia
import imgaug.augmenters as iaa


IMAGE_EXT_LIST = ['.jpg', '.jpeg', '.png']
IMAGE_DIR_NAME = r'C:\attribute_3rd_dataset\aug_age_man_woman\child_6450\woman_1654\data_aug\fliplr'
imgListPath = r''
savePath = r'C:\attribute_3rd_dataset\aug_age_man_woman\child_6450\woman_1654\data_aug\shearing\fliplr_-15_15'


def GetImageTxtList(ImgList):
    _imgTxtList = []

    with open(ImgList, "r", encoding="utf8") as f:
        for each in f:
            each = each.strip('\n')
            _imgTxtList.append(each)

    return _imgTxtList


def GetImageFileList(DirName):
    _imageFileList = []
    _imageNameList = []

    if os.path.isdir(DirName) is False:
        print(f"{DirName} is Not Exist!")
        return None

    for root, dirs, files in os.walk(DirName):
        for file in files:
            _, ext = os.path.splitext(file)

            if ext in IMAGE_EXT_LIST:
                _imageFileList.append(os.path.join(DirName, file))
                _imageNameList.append(file)

    return _imageFileList, _imageNameList


def GetEachImageImReadList(FileList):
    _imReadList = []

    for eachFile in FileList:
        img_array = np.fromfile(eachFile, np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

        if img is not None:
            _imReadList.append(img)

    return _imReadList


def imwrite(fileName, img, params=None):
    try:
        ext         = os.path.splitext(fileName)[1]
        result, n   = cv2.imencode(ext, img, params)

        if result:
            with open(fileName, mode='w+b') as f:
                 n.tofile(f)
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False


def SaveAugImageList(AugImageList, imageNameList):
    if os.path.isdir(savePath) is False:
        os.makedirs(savePath, exist_ok=True)

    for idx, eachFile in enumerate(AugImageList):
        imwrite(os.path.join(savePath, imageNameList[idx]), eachFile)


def ImageListAugumentation(imReadList):
    # fliplr 좌우 반전
    seq = iaa.Sequential([iaa.Fliplr(1.0)])
    res = seq.augment_images(imReadList)

    # flipud 상하 반전
    # seq = iaa.Sequential([iaa.Flipud(1.0)])
    # res = seq.augment_images(imReadList)

    # rotation 각도 변경
    # seq = iaa.Sequential([iaa.Affine(rotate=(-5, -5))])
    # res = seq.augment_images(imReadList)

    # rotation 각도 변경
    # seq = iaa.Sequential([iaa.Affine(rotate=(5, 5))])
    # res = seq.augment_images(imReadList)

    # shearing
    # seq = iaa.Sequential([iaa.Affine(shear=(-15, 15))])
    # res = seq.augment_images(imReadList)

    # gaussianblur 가우시안 블러
    # seq = iaa.Sequential([iaa.GaussianBlur(sigma=(0.2, 0.2))])
    # res = seq.augment_images(imReadList)

    # up 이미지 확대 (아직 코드 못 짬)
    # contrast

    return res


if __name__ == "__main__":
    imageTxtList                    = GetImageTxtList(imgListPath)
    imageFileList, imageNameList    = GetImageFileList(IMAGE_DIR_NAME)
    imReadList                      = GetEachImageImReadList(imageFileList)

    resultImgList                   = ImageListAugumentation(imReadList)
    SaveAugImageList(resultImgList, imageNameList)



