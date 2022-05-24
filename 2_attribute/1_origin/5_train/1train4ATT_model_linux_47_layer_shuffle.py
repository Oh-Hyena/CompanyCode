# -*- coding: utf-8 -*-
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
from result_graph import plot_history, save_history

#import UNI_16_v1
import UNI_47_v1_d
#Test 폴더 이름
TEST_NO = '1104_1_All_47_d'
#Model load
#UNI_ATT = UNI_16_v1_d_m.Uni_16_v1()
#Model
UNI_ATT = UNI_47_v1_d.Uni_47_v1()

os.environ["CUDA_DEVICE_ORDER"]="PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"]="0,1,2,3"
# 학습을 위해 에폭과 초기 학습률, 배치 사이즈, 그리고 이미지의 차원을 초기화합니다

################arg_pase로 바꿀 내용###########################
MAIN_DIR = r'/home/keti/attribute_data/1104_attribute_common_PA100K_market1501_2class'
# MAIN_DIR = r'/data/attribute_data/0916_attribute_common_PA100K_market1501_39class'
Config_File = r'/config.data'
Classes_File = r'/2class.name'
Config_DIR = MAIN_DIR + Config_File
Classes_DIR = MAIN_DIR + Classes_File

print(Config_DIR)
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
#############ATT_name읽기###################################
classes_merge = []
for index in open(Classes_DIR):
	index = index.replace('\n',"")
	classes_merge.append(index)						#classes

SHAPE = len(classes_merge)
# EPOCHS = 100000
# INIT_LR = 1e-3
# BS = 256
# IMAGE_DIMS = (224, 224, 3)
# DECAY = 0.0005
# MOMENTUM = 0.9 #Adam 에서 사용하지 않음
#DATANUM = 290325
#/home/keti/attribute_data/img_list/train
#Init DIR
# TRAIN_MAIN_DIR = r'/data/attribute_data/0521_attribute_290K/img_list/train'
# VAL_MAIN_DIR = r'/data/attribute_data/0521_attribute_290K/img_list/val_0524'
#TEST_MAIN_DIR = r'/data/attribute_data/0521_attribute_290K/img_list/test'


TRAIN_IMG_DIR = r'/train_common_img_list.txt'
TRAIN_MERGE_ATT = r'/train_merge_annotation.txt'
VAL_IMG_DIR = r'/val_common_img_list.txt'
VAL_MERGE_ATT = r'/val_merge_annotation.txt'


#실제 사용할 DIR
TRAIN_DIR = TRAIN_MAIN + TRAIN_IMG_DIR
VAL_DIR = VAL_MAIN + VAL_IMG_DIR
TRAIN_ATT = TRAIN_MAIN + TRAIN_MERGE_ATT
VAL_ATT = VAL_MAIN + VAL_MERGE_ATT

#SAVE DIR
#SAVE_MAIN = r'/data/attribute_data/0521_attribute_290K/result/{}'.format(TEST_NO)
MODEL_DIR = r'/model.json'
BEST_DIR = r'/weights/'
MLB_DIR = r'/MLB'

MODEL_DIR = SAVE_DIR + MODEL_DIR
WEIGHTS_DIR = SAVE_DIR + BEST_DIR
MLB_DIR = SAVE_DIR + MLB_DIR

if not os.path.isdir(SAVE_DIR):
    try:
        os.makedirs(SAVE_DIR)
    except OSError:
        print('Error : Creating dir' + SAVE_DIR)

if not os.path.isdir(WEIGHTS_DIR):
    try:
        os.makedirs(WEIGHTS_DIR)
    except OSError:
        print('Error : Creating dir' + WEIGHTS_DIR)

if not os.path.isdir(MLB_DIR):
    try:
        os.makedirs(MLB_DIR)
    except OSError:
        print('Error : Creating dir' + MLB_DIR)


#Image Processing Load Dataset
def get_img_data(path,mlb_label):
    for i, line in enumerate(open(path)):
        img_path = line.strip()
        image = cv2.imread(img_path)
        image = cv2.resize(image, (IMAGE_DIMS[1], IMAGE_DIMS[0]))
        image = img_to_array(image)
        image = np.array(image, dtype="float") / 255.0
        label = mlb_label[i]
        label = np.array(label)
        #print(label)
        yield(image, label)

#Callback
# Save Every epoch
#callback 에서 호출될 save 함수
class save(tf.keras.callbacks.Callback):
    def __init__(self, model):
        self.count = 0
        self.model = model
    def on_epoch_end(self, bath, logs={}):
        self.count = self.count + 1
        if self.count % 1 == 0:
            model.save(WEIGHTS_DIR + "mymodel_epoch_{0:04d}.h5".format(self.count))
#earlyStopping Point
es = EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=40)
#best model choice
mc = ModelCheckpoint(WEIGHTS_DIR+'weights_epoch-{epoch:03d}_acc-{acc:.4f}_valloss-{val_loss:.4f}_valacc-{val_acc:.4f}.h5', monitor='val_loss', mode='min', save_best_only=True,verbose=1)
########################################################################################


#MLB Init, SAVE
#path_label = r'E:\Seach\crop_Attribute\merge_attribute_annotation.txt'
path_label = TRAIN_ATT
mlb_labels = []
labels = []

for line in open(path_label):
    label = line.strip()
    for i in range(len(label)):
        if label[i] == '1':
            labels.append(classes_merge[i])
    mlb_labels.append(labels)
    labels = []
mlb = MultiLabelBinarizer()
mlb_label = mlb.fit_transform(mlb_labels)
#for i in mlb_label:
#    label.append(i)
#print(mlb_label)
for (i, label) in enumerate(mlb.classes_):
	print("{}. {}".format(i+1 , label))
#load 된 image 개수 확인
print(len(mlb_label))
d_train = len(mlb_label)
# MLB SAVE
f = open(MLB_DIR+'/MLB', "wb")
f.write(pickle.dumps(mlb))
f.close()
#####################################################################
val_label = VAL_ATT
val_labels = []
labels = []
#val_set Annotation 만들기
for line in open(val_label):
    label = line.strip()
    #print(label, len(label))
    for i in range(len(label)):
        if label[i] == '1':
            labels.append(classes_merge[i])
    #print(labels)
    val_labels.append(labels)
    labels = []

val_mlb = MultiLabelBinarizer()
val_mlb_label = val_mlb.fit_transform(val_labels)
##############################################################################
mirrored_strategy = tf.distribute.MirroredStrategy()
#with mirrored_strategy.scope():
dataset = tf.data.Dataset.from_generator(get_img_data,(tf.float32, tf.int16), (tf.TensorShape([224,224,3]), tf.TensorShape([SHAPE])),args=(TRAIN_DIR,mlb_label))
#print(len(mlb_label))

dataset = dataset.shuffle(buffer_size=20000)

d_train = len(mlb_label)


with mirrored_strategy.scope():
	dataset = dataset.repeat()
	dataset = dataset.batch(BS)


print('TrainSet : ',dataset)

#Val
valset = tf.data.Dataset.from_generator(get_img_data,(tf.float32, tf.int16), (tf.TensorShape([224,224,3]), tf.TensorShape([SHAPE])),args=(VAL_DIR,val_mlb_label))
#valset repeat 필요한가

valset = dataset.shuffle(buffer_size=1000)

#valset = valset.repeat()
valset = valset.batch(BS)
print('ValSet :',valset)
#val_label = r'E:\Seach\test\merge_attribute_annotation.txt'

label =[]
for i in val_mlb_label:
   label.append(i)
#valSet 이미지 장수
d_val = len(val_mlb_label)
#valset 확인 Classes
for (i, label) in enumerate(val_mlb.classes_):
	print("{}. {}".format(i+1 , label))

######################################################################
reduceLROnPlat = ReduceLROnPlateau(monitor='val_loss',
                                        factor=0.1,
                                        patience=15,
                                        verbose=1,
                                        mode='auto',
                                        min_delta=0.0001,
                                        cooldown=2,
                                        min_lr=1e-6)
######################################################################
######################################################################
#Model Load
#from keras.models import model_from_json
#json_file = open(MODEL_DIR, "r")
#loaded_model_json = json_file.read()
#json_file.close()
#loaded_model = model_from_json(loaded_model_json)
# muli GPU
#mirrored_strategy = tf.distribute.MirroredStrategy()
#mirrored_strategy = tf.distribute.MirroredStrategy(devices=["/gpu:0", "/gpu:1"])
print('bs = ', BS)

with mirrored_strategy.scope():
	model = UNI_ATT.build(
	width=IMAGE_DIMS[1], height=IMAGE_DIMS[0],
	depth=IMAGE_DIMS[2], classes=len(mlb.classes_),
	finalAct="sigmoid")
	opt = tf.keras.optimizers.Adam(learning_rate=INIT_LR, decay=DECAY )
	model.compile(loss="binary_crossentropy", optimizer=opt,	metrics=["acc"])

print( model.summary())

train_steps = d_train//BS
val_steps = d_val//BS
print(train_steps, val_steps)
print(dataset, valset)
s = save(model)
		# history = model.fit(dataset,steps_per_epoch=train_steps, epochs = EPOCHS ,batch_size = BS, validation_data=valset,validation_steps=val_steps, callbacks = [s,es,reduceLROnPlat,mc], verbose=1, max_queue_size=10,workers=10,use_multiprocessing=True)
# history = model.fit(dataset,steps_per_epoch=train_steps, epochs = EPOCHS ,batch_size = BS, callbacks = [s,es,reduceLROnPlat,mc], verbose=1, max_queue_size=10,workers=10,use_multiprocessing=True)

#history = model.fit(dataset,steps_per_epoch=train_steps, epochs = EPOCHS ,batch_size = BS, validation_data=valset,validation_steps=val_steps, callbacks = [s,es,mc], verbose=1, max_queue_size=10,workers=10,use_multiprocessing=True)

history = model.fit(dataset,steps_per_epoch=train_steps, epochs = EPOCHS , validation_data=valset,validation_steps=val_steps, callbacks = [s,es,mc], verbose=1, max_queue_size=10,workers=10,use_multiprocessing=True)



result_path = SAVE_DIR
plot_history(history, result_path)

model.evaluate(valset)
#########################################################################
#  model = tf.keras.Sequential([tf.keras.layers.Dense(1, input_shape=(1,))])
#  model.compile(loss='mse', optimizer='sgd')

#dataset = tf.data.Dataset.from_tensors(([1.], [1.])).repeat(100).batch(10)
#model.fit(dataset, epochs=2)
#model.evaluate(dataset)
#########################################################################
#Model Train
