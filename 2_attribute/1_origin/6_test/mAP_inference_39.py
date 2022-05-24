##############Import
import cv2
from tensorflow.keras.preprocessing.image import img_to_array
import tensorflow as tf
import argparse
import random
import cv2
import os
from tensorflow.keras.preprocessing.image import img_to_array
import numpy as np
from sklearn.preprocessing import MultiLabelBinarizer
from tensorflow.keras.models import Sequential
import pickle
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping
import argparse
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau, TensorBoard
from configparser import ConfigParser
from configparser import ConfigParser, ExtendedInterpolation

import UNI_47_v1_d
# class type 지정 -> arg 로 만들기
#Model
UNI_ATT = UNI_47_v1_d.Uni_47_v1()

os.environ["CUDA_DEVICE_ORDER"]="PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"]="0,1,2,3"
# 학습을 위해 에폭과 초기 학습률, 배치 사이즈, 그리고 이미지의 차원을 초기화합니다

################arg_pase로 바꿀 내용###########################
#MAIN_DIR = r'/data/attribute_data/0803_attribute_120K_lowercolor_9class_47'
#Config_File = r'/config.data'
#Classes_File = r'/9class.name'
#Config_DIR = MAIN_DIR + Config_File
#Classes_DIR = MAIN_DIR + Classes_File

Config_DIR = r'E:\dataset\attribute\0917_result\config.data'
Classes_DIR = r'E:\dataset\attribute\0917_result\39class.name'
###############Config.data 파싱##########################
parser = ConfigParser(interpolation=ExtendedInterpolation())
parser.read(Config_DIR)

EPOCHS = parser.getint('Settings','EPOCHS')			#EPOCHS
INIT_LR = parser.getfloat('Settings','INIT_LR')		#INIT_LR
BS = parser.getint('Settings','BS')					#BS
INPUT_x = parser.getint('Settings','INPUT_x')
INPUT_y = parser.getint('Settings','INPUT_y')
INPUT_c = parser.getint('Settings','INPUT_c')
IMAGE_DIMS = (INPUT_x,INPUT_y,INPUT_c)				#INPUT_DIMS
DECAY = parser.getfloat('Settings','DECAY')			#DECAY

TRAIN_MAIN = parser.get('Directory','TRAIN_DIR')		#TRAIN_DIR
VAL_MAIN = parser.get('Directory','VAL_DIR')			#VAL_DIR
SAVE_DIR = parser.get('Directory','SAVE_DIR')		#SAVE_DIR
###########################Init#################################

#Config_DIR = r'E:\dataset\attribute\0803_lowercolor_common\config.data'
#Classes_DIR = r'E:\dataset\attribute\0803_lowercolor_common\9class.name'

###########################Init#################################
classes_merge = []
for index in open(Classes_DIR):
	index = index.replace('\n',"")
	classes_merge.append(index)						#classes
SHAPE = len(classes_merge)

##########################GT_Load################################
def Read_Anno (annotation_label):
    labels = []
    for line in open(annotation_label):
        label = line.strip()
        labels.append(label)
#    for i,line in enumerate(labels):
#        if i < 10:
#            print(line)
#        else:
#            break
    return labels

##########################Model Load################################
TEST_DIR = r'E:\dataset\attribute 0329\market_1501\valid_dataset\39class_attribute_annotation\market1501_valid_common_img_list.txt'
WEIGHTS = r'weights_epoch-097_acc-0.9331_valloss-0.1363_valacc-0.9456.h5'
MLB = r'E:\dataset\attribute\0917_result\MLB'

#mlb
mlb = pickle.loads(open(MLB, "rb").read())
#Model
loaded_model = UNI_ATT.build(
	width=IMAGE_DIMS[1], height=IMAGE_DIMS[0],
	depth=IMAGE_DIMS[2], classes=SHAPE,
	finalAct="sigmoid")
opt = tf.keras.optimizers.Adam(learning_rate=INIT_LR, decay=DECAY )
loaded_model.compile(loss="binary_crossentropy", optimizer=opt,	metrics=["acc"])
#weights load
loaded_model.load_weights(WEIGHTS)

##########################Inference################################
#Load Classes
classes_proba_merge = {string : i for i,string in enumerate(classes_merge)}
print(classes_proba_merge)
#inference and save
# 저장할 장소
TXTFILE = r'E:\dataset\attribute\0917_result\result_val.txt'
#저장할 파일 열기
f = open(TXTFILE,'w')
#imagePaths = sorted(list(paths.list_images(TEST_DIR)))
#for imagePath in imagePaths:
for line in open(TEST_DIR):
    imagePath = line.strip()
    image = cv2.imread(imagePath)
    image = cv2.resize(image, (224, 224))
    image = image.astype("float") / 255.0
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)
    
    proba = loaded_model.predict(image)[0]
    idxs = np.argsort(proba)[::-1][:5]
    data = 'image : {}  type : {}\t'.format(imagePath,'merge')
    i=0
    for (label, p) in zip(mlb.classes_, proba):
        data = "index : {} label : {}: {:.2f}%\t".format(i , label, p * 100)
        #print(label)
        classes_proba_merge[label] = p * 100
        i = i+ 1
        #print(classes_proba_merge[label])
    #Inference data Annotation 만들기
    #List 초기화
    gender = []
    age = []
    bag = []
    hat = []
    hair = []
    upperbody = []
    uppercolor = []
    lowerbody = []
    lowercolor = []
    COLOR_PROB = 30
	
    for index, (classes, prob) in enumerate(classes_proba_merge.items()):
        if index < 2:
            gender.append(prob)
        elif index < 7:
            age.append(prob)
        elif index < 10:
            bag.append(prob)
        elif index < 13:
            hat.append(prob)
        elif index < 15:
            hair.append(prob)
        elif index < 17:
            upperbody.append(prob)
        elif index < 26:
            uppercolor.append(prob)
        elif index < 31:
            lowerbody.append(prob)
        elif index < 39:
            lowercolor.append(prob)
    #print(lowercolor)
    result= [0 for _ in range(39)]
    result[gender.index(max(gender))] = 1
    result[age.index(max(age))+2] = 1
    result[bag.index(max(bag))+7] = 1
    result[hat.index(max(hat))+10] = 1
    result[hair.index(max(hair))+13] = 1
    result[upperbody.index(max(upperbody))+15] = 1	
    result[uppercolor.index(max(uppercolor))+17] = 1	
    result[lowerbody.index(max(lowerbody))+26] = 1	
    result[lowercolor.index(max(lowercolor))+31] = 1
    #print(result)
    putNum = ''.join(str(result).replace(",",""))
    putNum = putNum.replace(" ","")
    putNum = putNum.replace("[","")
    putNum = putNum.replace("]","")
    putNum = putNum +'\n'
    #print(putNum)
    f.write(putNum)
f.close()

##########################GT_Load################################
##########################GT_Load################################
