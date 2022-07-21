from configparser import ConfigParser, ExtendedInterpolation
import os
# import sys
# import cv2
# import numpy as np
# import matplotlib
# import pickle
# import argparse

# import tensorflow as tf
# from tensorflow.keras.preprocessing.image import img_to_array
# from tensorflow.keras.callbacks import EarlyStopping
# from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau
from configparser import ConfigParser, ExtendedInterpolation
from re import L
# from sklearn.preprocessing import MultiLabelBinarizer


import UNI_47_v1_d
uniAttributeClass = UNI_47_v1_d.Uni_47_v1()


AttTrainDir = r'E:\attTest\0630_att_train'


# 환경변수 읽어오기
#  *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
os.environ["CUDA_DEVICE_ORDER"]    = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = "0"


# 각종 파일 경로 저장하기
#  *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
classList = []
txtList   = []
for path, dirs, files in os.walk(AttTrainDir):
    for file in files:
        if '.data' in file:
            configPath = os.path.join(path, file)
        elif '.name' in file:
            classPath = os.path.join(path, file)
            classList.append(os.path.join(path, file))
        elif '.txt' in file:
            txtList.append(os.path.join(path, file))


# .data 파일
#  *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
parser     = ConfigParser(interpolation=ExtendedInterpolation())
parser.read(configPath)

# [Settings]
EPOCHS     = parser.getint('Settings', 'EPOCHS')
INIT_LR    = parser.getfloat('Settings', 'INIT_LR')
BS         = parser.getint('Settings', 'BS')
INPUT_x    = parser.getint('Settings', 'INPUT_x')
INPUT_y    = parser.getint('Settings', 'INPUT_y')
INPUT_c    = parser.getint('Settings', 'INPUT_c')
IMAGE_DIMS = (INPUT_x, INPUT_y, INPUT_c)		
DECAY      = parser.getfloat('Settings', 'DECAY')

# [Directory]
TRAIN_DIR  = parser.get('Directory', 'TRAIN_DIR')
VAL_DIR    = parser.get('Directory', 'VAL_DIR')
SAVE_DIR   = parser.get('Directory', 'SAVE_DIR')

classMergeList = []
for each in classList:
    with open(each, 'r', encoding='utf-8') as f:
        for eachLine in f:
            eachLine = eachLine.strip('\n')
            classMergeList.append(eachLine)

# classLenth
classLenth = len(classMergeList)


# 학습 후 저장할 파일 경로 설정하기
#  *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
JSON_DIR    = os.path.join(SAVE_DIR, 'model.json')
WEIGHTS_DIR = os.path.join(SAVE_DIR, 'weights')
MLB_DIR     = os.path.join(SAVE_DIR, 'MLB')


# 저장 폴더 만들기
#  *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
def makeDir(dir):
    if not os.path.isdir(dir):
        os.makedirs(dir, exist_ok=True)

makeDir(SAVE_DIR)
makeDir(WEIGHTS_DIR)
makeDir(MLB_DIR)


