import os
import numpy as np
import matplotlib.pyplot as plt
import cv2
from PIL import Image
import shutil
import xml.etree.ElementTree as ET
from xml.dom import minidom
import io
from data_aug.data_aug import *
from data_aug.bbox_util import *
import pickle as pkl
from collections import deque



cvatxmlDir = r"E:\0610\seongnamfalse0125_cvatxml"
imgDir     = r"E:\0610\seongnamfalse0125_img"
resDir     = r"E:\0610\seongnamfalse0125_flipping"

ENCODING_FORMAT = "UTF-8"


def checkInitDirValid():
    if os.path.isdir(cvatxmlDir) is False:
        print(f'[Error] {cvatxmlDir} is invalid')
        return False
    if os.path.isdir(imgDir) is False:
        print(f'[Error] {imgDir} is invalid')
        return False
    if os.path.isdir(resDir) is False:
        print(f'[Error] {resDir} is invalid')
        return False
    return True


def makeFlippingResDir(Dir):
    if not os.path.isdir(Dir):
        os.makedirs(Dir, exist_ok=True)


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


def numCount(length, num):
    rotate = length - len(num)
    if rotate > 0:
        for i in range(rotate):
            num = "0" + num
    return num


def flip(image, bbox, x, y):
    image = np.fliplr(image).copy()
    w = image.shape[1]
    x_min, y_min, x_max, y_max = bbox
    bbox = np.array([w - x_max, y_min, w - x_min, y_max])
    x = w - x
    x, y = Transformer.swap_joints(x, y)
    return image, bbox, x, y




if __name__ == "__main__":
    makeFlippingResDir(resDir)
    
    if checkInitDirValid() is False:
        sys.exit(-1)
