import os
import xml.etree.ElementTree as ET
import shutil
import random
from xml.dom import minidom
import numpy
import glob
import cv2
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
from data_aug.data_aug import *
from data_aug.bbox_util import *
import numpy as np
import cv2
import matplotlib.pyplot as plt
import pickle as pkl
import os
from collections import deque

#img_augmentation할_xml
xmlRootpath = r"D:\HN_code\test\1_labeling\12_rotation\1_bus_img_xml\bus_xml"
#img_augmentation할_img
imageRootpath = r"D:\HN_code\test\1_labeling\12_rotation\1_bus_img_xml\bus_img"
########txt저장
rootpath=r"D:\HN_code\test\1_labeling\12_rotation\2_rotation_img_xml_txt"
rotation_count=1
rotation_angle=30
# os.mkdir(rootpath)
targetpath=os.path.join(rootpath,'rotation_txt')
targetpath1=os.path.join(rootpath,'rotation_img')
os.mkdir(targetpath)
os.mkdir(targetpath1)
videoclass = "bus_rotation"
mode = "jpg"
videonumber = 1
fileCount = 1

cvatxmllist = os.listdir(xmlRootpath)
xmin1=[]
cls=[]
total_list=[]
list1=[]
bndbox_1=[]
b=[]
y2=[]
path_list=[]
bndbox_count_shape=[]
img=[]
images=[]
total_images=[]
img2=[]
img_width1=[]
img_height1=[]
yolo_data_list=[]
yolo_data_list_1=[]

total_xml = 0
count=0
n = 4
count1=0

def imread(filename, flags=cv2.IMREAD_COLOR, dtype=np.uint8):
    try:
        n = np.fromfile(filename, dtype)
        img = cv2.imdecode(n, flags)
        return img
    except Exception as e:
        print(e)
        return None


def divide_list(l, n):
    # 리스트 l의 길이가 n이면 계속 반복
    for i in range(0, len(bndbox_1),4):
        yield l[i:i + n]

def convert_xywh(width,height,xmin,xmax,ymin,ymax):
    dw = 1/width
    dy = 1/height
    #[x,y,w,h]
    xywh = [str(((xmin+xmax)/2.0)*dw),str(((ymin+ymax)/2.0)*dy),str((xmax-xmin)*dw),str((ymax-ymin)*dy)] #YOLO의 영역 표시방법을 계산식으로 써놓은 모습.

    return xywh

def naming(length, name):
    if int(length) == 5:
        if len(name) == 1:
            return "0000"+name
        elif len(name) == 2:
            return "000"+name
        elif len(name) == 3:
            return "00" + name
        elif len(name) == 4:
            return "0" + name
        else:
            return name
    else:
        if len(name) == 1:
            return "00000"+name
        elif len(name) == 2:
            return "0000"+name
        elif len(name) == 3:
            return "000" + name
        elif len(name) == 4:
            return "00" + name
        elif len(name) == 5:
            return "0" + name
        else:
            return name

###############################1번째 xml 읽기######################################
for (path, dir, files) in os.walk(xmlRootpath):
    for file in files:
        if file.endswith(".xml"):
            empty = os.path.join(xmlRootpath,path)
            path_list.append(empty)
            total_xml += 1
            parser = ET.XMLParser(encoding="utf-8")
            tree = ET.parse(os.path.join(empty, file),parser=parser)
            note = tree.getroot()
            for child in note.findall('object'):
                ob=child.find('object')

                name = child.find('name').text #객체의 카테고리 이름
                #print(name)
                if(name == 'person'):
                    cls.append('11')

                elif (name=='car'):
                    cls.append('22')

                elif (name=='bus'):
                    cls.append('33')

                elif (name=='truck'):
                    cls.append('44')

                elif (name=='unknown car' or name =="excavator" or name == "forklift" or name =="ladder truck"):
                    cls.append('55')

                elif (name=='bicycle'):
                    cls.append('66')

                elif (name=='motorbike'):
                    cls.append('77')

                for bndbox in child.find('bndbox'):
                    bndbox_1.append(bndbox.text)
                    #print(bndbox.text)
                    count +=1
            box_count=count/4
            bndbox_count_shape.append(int(box_count))

            count=0
#################xmin,ymin,xmax,ymax로 나누기##################
result = list(divide_list(bndbox_1, n))
data=np.array(result)
y = data.astype(np.float)
####################빈행렬나누기##########################
a = numpy.zeros(shape=(len(bndbox_count_shape)+500,1000,4))

for j,name in enumerate(bndbox_count_shape):
    for k in range(1000):
##여기다가 빈행렬에다가 y를 집어넣어준다
        if k < name :
            a[j][k]=y[count1]
            count1+= 1
############### 이미지읽어오는부분 #################
for (path, dir, files) in os.walk(imageRootpath):
    for file in files:
        if file.endswith(".jpg"):
            img1 = os.path.join(imageRootpath,path)
            total_image1=os.path.join(img1,file)
            total_images.append(total_image1)
            img_style = total_image1.split('\\')[-1]
            img_name = file
            image_info = total_image1
            img_size = Image.open(image_info).size
            img_width = img_size[0]
            img_height = img_size[1]
            img_width1.append(img_width)
            img_height1.append(img_height)

############class나누기###############################
data1=np.array(cls)
y1 = data1.astype(np.float)
####################빈행렬나누기##########################
a1 = numpy.zeros(shape=(len(bndbox_count_shape)+500,1000,1))
#########################################

count2=0
for j,name in enumerate(bndbox_count_shape):
    for k in range(1000):
        if k < name :

            a1[j][k]=y1[count2]
            count2+= 1
for i in range(int(rotation_count)):
    makepath=os.path.join(targetpath1,str((i+1)*int(rotation_angle)))
    makepath1=os.path.join(targetpath,str((i+1)*int(rotation_angle)))
    os.mkdir(makepath)
    os.mkdir(makepath1)
    makepath2=os.path.join(targetpath1,str((i+1)*-int(rotation_angle)))
    makepath3=os.path.join(targetpath,str((i+1)*-int(rotation_angle)))
    os.mkdir(makepath2)
    os.mkdir(makepath3)
########################################dataaugmentation####################

for k,img in enumerate(total_images):
    cv_img = imread(img)[:,:,::-1]
    b1=cv_img.copy()
    width = img_width1[k]
    height = img_height1[k]
    for i in range(int(rotation_count)):
        img_, bboxes_  = Rotate((i+1)*int(rotation_angle))(b1, a[k].copy())
        cv2.imwrite("temp5."+mode, img_[:,:,::-1])
        os.rename("temp5."+mode, os.path.join(videoclass+"_"+str(fileCount)+"."+mode))
        shutil.move(os.path.join(videoclass +"_"+str(fileCount)+"."+mode),(os.path.join(targetpath1,str((i+1)*int(rotation_angle)))))
        a12=os.path.join(targetpath,str((i+1)*int(rotation_angle)))
        file = open(a12+f"\\{videoclass}_{fileCount}.txt", "w")
        fileCount += 1
        for j in range(bboxes_.shape[0]):
            xmin=bboxes_[j][0]
            ymin=bboxes_[j][1]
            xmax=bboxes_[j][2]
            ymax=bboxes_[j][3]
            yolo_data = convert_xywh(width,height,xmin,xmax,ymin,ymax)

            if (a1[k][j]==11):
                file.write("0"+" "+yolo_data[0]+" "+yolo_data[1]+" "+yolo_data[2]+" "+yolo_data[3]+"\n") # 결과를 .txt에 삽입
            elif (a1[k][j]==22):
                file.write("1"+" "+yolo_data[0]+" "+yolo_data[1]+" "+yolo_data[2]+" "+yolo_data[3]+"\n") # 결과를 .txt에 삽입
            elif (a1[k][j]==33):
                file.write("2"+" "+yolo_data[0]+" "+yolo_data[1]+" "+yolo_data[2]+" "+yolo_data[3]+"\n") # 결과를 .txt에 삽입
            elif (a1[k][j]==44):
                file.write("3"+" "+yolo_data[0]+" "+yolo_data[1]+" "+yolo_data[2]+" "+yolo_data[3]+"\n") # 결과를 .txt에 삽입
            elif (a1[k][j]==55):
                file.write("4"+" "+yolo_data[0]+" "+yolo_data[1]+" "+yolo_data[2]+" "+yolo_data[3]+"\n") # 결과를 .txt에 삽입
            elif (a1[k][j]==66):
                file.write("5"+" "+yolo_data[0]+" "+yolo_data[1]+" "+yolo_data[2]+" "+yolo_data[3]+"\n") # 결과를 .txt에 삽입
            elif (a1[k][j]==77):
                file.write("6"+" "+yolo_data[0]+" "+yolo_data[1]+" "+yolo_data[2]+" "+yolo_data[3]+"\n") # 결과를 .txt에 삽입

    for f in range(int(rotation_count)):
        img_, bboxes_  = Rotate((f+1)*-int(rotation_angle))(b1, a[k].copy())
        cv2.imwrite("temp5."+mode, img_[:,:,::-1])
        os.rename("temp5."+mode, os.path.join(videoclass +"_"+str(fileCount)+"."+mode))
        shutil.move(os.path.join(videoclass +"_"+str(fileCount)+"."+mode),(os.path.join(targetpath1,str((f+1)*-int(rotation_angle)))))
        b12=os.path.join(targetpath,str((f+1)*-int(rotation_angle)))
        file = open(b12+f"\\{videoclass}_{fileCount}.txt", "w")
        fileCount += 1
        for j in range(bboxes_.shape[0]):
            xmin=bboxes_[j][0]
            ymin=bboxes_[j][1]
            xmax=bboxes_[j][2]
            ymax=bboxes_[j][3]
            yolo_data = convert_xywh(width,height,xmin,xmax,ymin,ymax)

            if (a1[k][j]==11):
                file.write("0"+" "+yolo_data[0]+" "+yolo_data[1]+" "+yolo_data[2]+" "+yolo_data[3]+"\n") # 결과를 .txt에 삽입
            elif (a1[k][j]==22):
                file.write("1"+" "+yolo_data[0]+" "+yolo_data[1]+" "+yolo_data[2]+" "+yolo_data[3]+"\n") # 결과를 .txt에 삽입
            elif (a1[k][j]==33):
                file.write("2"+" "+yolo_data[0]+" "+yolo_data[1]+" "+yolo_data[2]+" "+yolo_data[3]+"\n") # 결과를 .txt에 삽입
            elif (a1[k][j]==44):
                file.write("3"+" "+yolo_data[0]+" "+yolo_data[1]+" "+yolo_data[2]+" "+yolo_data[3]+"\n") # 결과를 .txt에 삽입
            elif (a1[k][j]==55):
                file.write("4"+" "+yolo_data[0]+" "+yolo_data[1]+" "+yolo_data[2]+" "+yolo_data[3]+"\n") # 결과를 .txt에 삽입
            elif (a1[k][j]==66):
                file.write("5"+" "+yolo_data[0]+" "+yolo_data[1]+" "+yolo_data[2]+" "+yolo_data[3]+"\n") # 결과를 .txt에 삽입
            elif (a1[k][j]==77):
                file.write("6"+" "+yolo_data[0]+" "+yolo_data[1]+" "+yolo_data[2]+" "+yolo_data[3]+"\n")

file.close()
