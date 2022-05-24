import os
import xml.etree.ElementTree as ET
import shutil
import random
from xml.dom import minidom
import numpy
import glob
import cv2
import csv
import io
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
from data_aug.data_aug import *
from data_aug.bbox_util import *
import numpy as np
import matplotlib.pyplot as plt
import pickle as pkl
import os
from collections import deque
from lxml import etree


#img_augmentation할_xml
xmlRootpath = r"D:\HN_code\test\1_labeling\13_scale_plus\1_bus_img_xml\bus_xml"
#img_augmentation할_img
imageRootpath = r"D:\HN_code\test\1_labeling\13_scale_plus\1_bus_img_xml\bus_img"
#저장할폴더(txt파일)
rootpath=r"D:\HN_code\test\1_labeling\13_scale_plus\2_scale_plus_img_xml_txt"
# os.mkdir(rootpath)
targetpath=os.path.join(rootpath,'scale_plus_txt')
targetpath1=os.path.join(rootpath,'scale_plus_img')
save_xml=os.path.join(rootpath,'scale_plus_xml')
########txt저장
os.mkdir(targetpath)
os.mkdir(targetpath1)
os.mkdir(save_xml)

# videoclass = "UnitrainNightdataset_unknowncar_plus"
# bicycle, bus, motorbike
videoclass = "bus_scale_plus"
mode = "jpg"
videonumber = 1
fileCount = 1
labels = ['person','car',"bus", "truck" ,"unknown car", "bicycle", "motorbike"]
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
def csvread(fn):
    with open(fn, 'r') as csvfile:
        list_arr = []
        reader = csv.reader(csvfile, delimiter=' ')

        for row in reader:
            list_arr.append(row)
    return list_arr
global label
def convert_label(txt_file):
    global label
    for i in range(len(labels)):
        if txt_file[0] == str(i):
            label = labels[i]
            return label
    return label
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
def extract_coor(txt_file, img_width, img_height):
    x_rect_mid = float(txt_file[1])
    y_rect_mid = float(txt_file[2])
    width_rect = float(txt_file[3])
    height_rect = float(txt_file[4])
    x_min_rect = ((2 * x_rect_mid * img_width) - (width_rect * img_width)) / 2
    x_max_rect = ((2 * x_rect_mid * img_width) + (width_rect * img_width)) / 2
    y_min_rect = ((2 * y_rect_mid * img_height) -
                  (height_rect * img_height)) / 2
    y_max_rect = ((2 * y_rect_mid * img_height) +
                  (height_rect * img_height)) / 2

    return x_min_rect, x_max_rect, y_min_rect, y_max_rect
def imwrite(filename, img, params=None):
    try:
        ext = os.path.splitext(filename)[1]
        result, n = cv2.imencode(ext, img, params)

        if result:
             with open(filename, mode='w+b') as f:
                n.tofile(f)
             return True
        else:
             return False
    except Exception as e:
        print(e)
        return False
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


########################################dataaugmentation####################
for k,img in enumerate(total_images):
    cv_img = imread(img)[:,:,::-1]
    b1=cv_img.copy()
    img_, bboxes_ = Scale(0.3,0.3)(b1, a[k].copy())
    cv2.imwrite("temp1."+mode, img_[:,:,::-1])
    os.rename("temp1."+mode, os.path.join(videoclass +"_"+str(fileCount)+"."+mode))
    shutil.move(os.path.join(videoclass +"_"+str(fileCount)+"."+mode),(os.path.join(targetpath1)))
    a12=os.path.join(targetpath)
    file = open(a12+f"\\{videoclass}_{fileCount}.txt", "w")
    fileCount += 1
    width=img_width1[k]
    height=img_height1[k]
    for j in range(bboxes_.shape[0]):
        xmin=bboxes_[j][0]
        ymin=bboxes_[j][1]
        xmax=bboxes_[j][2]
        ymax=bboxes_[j][3]
        yolo_data = convert_xywh(width,height,xmin,xmax,ymin,ymax)
        #print(width,height)
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
file.close()

fw = os.listdir(targetpath)
for line in fw:
    root = etree.Element("annotation")
    img_style = targetpath1.split('\\')[-1]

    img_name = line
    image_info = targetpath1 + "\\" + line[:-4]+".jpg"
    img_txt_root = targetpath + "\\" + line[:-4]
    txt = ".txt"
    txt_path = img_txt_root + txt
    txt_file = csvread(txt_path)
    ######################################

    img_size = Image.open(image_info).size
    img_width = img_size[0]
    img_height = img_size[1]
    img_depth = 3
    ######################################
    folder = etree.Element("folder")
    folder.text = "%s" % (img_style)
    filename = etree.Element("filename")
    filename.text = "%s" % (img_name)
    path = etree.Element("path")
    path.text = "%s" % (img_txt_root)
    source = etree.Element("source")
    ##################source - element##################
    source_database = etree.SubElement(source, "database")
    source_database.text = "Unknown"
    ####################################################
    size = etree.Element("size")
    ####################size - element##################
    image_width = etree.SubElement(size, "width")
    image_width.text = "%d" % (img_width)
    image_height = etree.SubElement(size, "height")
    image_height.text = "%d" % (img_height)
    image_depth = etree.SubElement(size, "depth")
    image_depth.text = "%d" % (img_depth)
    ####################################################
    segmented = etree.Element("segmented")
    segmented.text = "0"
    root.append(folder)
    root.append(filename)
    root.append(path)
    root.append(source)
    root.append(size)
    root.append(segmented)
    for ii in range(len(txt_file)):
        label = convert_label(txt_file[ii][0])
        x_min_rect, x_max_rect, y_min_rect, y_max_rect = extract_coor(
            txt_file[ii], img_width, img_height)
        object = etree.Element("object")
        ####################object - element##################
        name = etree.SubElement(object, "name")
        name.text = "%s" % (label)
        pose = etree.SubElement(object, "pose")
        pose.text = "Unspecified"
        truncated = etree.SubElement(object, "truncated")
        truncated.text = "0"
        difficult = etree.SubElement(object, "difficult")
        difficult.text = "0"
        bndbox = etree.SubElement(object, "bndbox")
        #####sub_sub########
        xmin = etree.SubElement(bndbox, "xmin")
        xmin.text = "%d" % (x_min_rect)
        ymin = etree.SubElement(bndbox, "ymin")
        ymin.text = "%d" % (y_min_rect)
        xmax = etree.SubElement(bndbox, "xmax")
        xmax.text = "%d" % (x_max_rect)
        ymax = etree.SubElement(bndbox, "ymax")
        ymax.text = "%d" % (y_max_rect)
        #####sub_sub########
        root.append(object)
        ####################################################
    file_output = etree.tostring(root, pretty_print=True, encoding='UTF-8')
    ff = io.open(save_xml+f'\\%s.xml' % (img_name[:-4]), 'w', encoding="utf-8")
    ff.write(file_output.decode('utf-8'))
