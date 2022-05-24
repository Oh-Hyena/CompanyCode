import os
import cv2
import shutil
import time
import random
import json
import io
import csv
from PIL import Image
from lxml import etree
import xml.etree.ElementTree as ET
from xml.dom import minidom

global label

# cvatxml 폴더에는 다운받은 cvatxml 파일을 넣어놓고, img에는 원본 이미지 넣어놓고, img_Rootpath에는 img 폴더 경로 입력하기
img_Rootpath=r"D:\HN_code\test\1_labeling\6_make_7class_dataset\1_seongnamfalse1112_img"

# data_process 폴더 안에 cvatxmls 폴더 만들어서 다운받은 cvatxml 파일을 넣어놓고, rootpath에는 data_process 경로 입력하기
rootpath = r"D:\HN_code\test\1_labeling\6_make_7class_dataset\3_7class_data_process"

cvatxmlRootpath = os.path.join(rootpath, "cvatxmls")
xmlRootpath = os.path.join(rootpath, "original10_xml")
save_yolo = os.path.join(rootpath, "save_yolo")
os.mkdir(save_yolo)
save_xml=os.path.join(rootpath, "class7_xml")
os.mkdir(save_xml)
copy_img_Rootpath=os.path.join(rootpath,"copy_img")
os.mkdir(copy_img_Rootpath)

total_jpg_file_name=[]
total_jpg_file_path=[]
full_total_jpg_file_name=[]
copy_xmlname_list=[]
cls=[]
namelist=['person','car',"bus", "truck", "excavator", "forklift", "ladder truck", "unknown car" ,"bicycle", "motorbike"]
labels = ['person','car',"bus", "truck" ,"bicycle","unknown car", "motorbike"]


def some_process(x):
    return True

def convert_label(txt_file):
    global label
    for i in range(len(labels)):
        if txt_file[0] == str(i):
            label = labels[i]
            return label
    return label

def csvread(fn):
    with open(fn, 'r') as csvfile:
        list_arr = []
        reader = csv.reader(csvfile, delimiter=' ')

        for row in reader:
            list_arr.append(row)
    return list_arr

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

# xywh 변환 함수
def convert_xywh(width, height, xmin, xmax, ymin, ymax):
    dw = 1/width
    dy = 1/height
    # yolo의 영역 표시 방법을 계산식으로 써 놓은 코드
    xywh = [str(((xmin+xmax)/2.0)*dw), str(((ymin+ymax)/2.0)*dy), str((xmax-xmin)*dw), str((ymax-ymin)*dy)]
    return xywh

# 좌표 추출 함수
def extract_coor(txt_file, img_width, img_height):
    x_rect_mid  = float(txt_file[1])
    y_rect_mid  = float(txt_file[2])
    width_rect  = float(txt_file[3])
    height_rect = float(txt_file[4])

    x_min_rect = ((2 * x_rect_mid * img_width) - (width_rect * img_width)) / 2
    x_max_rect = ((2 * x_rect_mid * img_width) + (width_rect * img_width)) / 2
    y_min_rect = ((2 * y_rect_mid * img_height) - (height_rect * img_height)) / 2
    y_max_rect = ((2 * y_rect_mid * img_height) + (height_rect * img_height)) / 2

    return x_min_rect, x_max_rect, y_min_rect, y_max_rect

# cvatxml 파일로 xml 파일 만들기
def makeXmlByCvatxml():
    cvatxmllist = os.listdir(cvatxmlRootpath)
    if not os.path.isdir(xmlRootpath):
        os.mkdir(xmlRootpath)
    for cvatxml in cvatxmllist:
        if cvatxml.endswith(".xml"):
            tree = ET.parse(os.path.join(cvatxmlRootpath, cvatxml))
            note = tree.getroot()
            for image in note.findall("image"):
                name = image.get("name")
                width = image.get("width")
                height = image.get("height")
                annotation = ET.Element("annotation")
                ET.SubElement(annotation, "folder").text = ""
                ET.SubElement(annotation, "filename").text = name
                sourceTag = ET.SubElement(annotation, "source")
                ET.SubElement(sourceTag, "database").text = "Unknown"
                sizeTag = ET.SubElement(annotation, "size")
                ET.SubElement(sizeTag, "height").text = str(int(height))
                ET.SubElement(sizeTag, "width").text = str(int(width))
                ET.SubElement(sizeTag, "depth").text = "3"
                ET.SubElement(annotation, "segmented").text = "0"
                for box in image.findall("box"):
                    objectTag = ET.SubElement(annotation, "object")
                    label = box.get("label")
                    xtl = box.get("xtl")
                    ytl = box.get("ytl")
                    xbr = box.get("xbr")
                    ybr = box.get("ybr")
                    #------------------
                    xtl = str(int(float(xtl)))
                    ytl = str(int(float(ytl)))
                    xbr = str(int(float(xbr)))
                    ybr = str(int(float(ybr)))
                    #------------------
                    ET.SubElement(objectTag, "name").text = label
                    ET.SubElement(objectTag, "pose").text = "Unspecified"
                    ET.SubElement(objectTag, "difficult").text = "0"
                    ET.SubElement(objectTag, "truncated").text = "0"
                    bndboxTag = ET.SubElement(objectTag, "bndbox")
                    ET.SubElement(bndboxTag, "xmin").text = xtl
                    ET.SubElement(bndboxTag, "ymin").text = ytl
                    ET.SubElement(bndboxTag, "xmax").text = xbr
                    ET.SubElement(bndboxTag, "ymax").text = ybr
                pretty = minidom.parseString(ET.tostring(annotation)).toprettyxml(encoding="utf-8")
                with open(os.path.join(xmlRootpath, name[:-4]+".xml"), "wb") as f:
                    f.write(pretty)
    f.close()

def convert_yolo():
    file_list = os.listdir(xmlRootpath)
    for file in file_list:
        if file.endswith(".xml"): #확장자가 xml이라면 작업 시행
            parser = ET.XMLParser(encoding="utf-8")
            tree = ET.parse(os.path.join(xmlRootpath,str(file)),parser=parser)
            note = tree.getroot()
            fname = note.find('filename').text
            size = note.find('size')
            #2K이미지를 넣고 싶을때
            height = int(size.find('height').text) #이미지의 height
            width = int(size.find('width').text) #이미지의 width
            result = open(os.path.join(save_yolo, file[:-4]+".txt"),"w")
            for child in note.findall('object'): #모든 객체에 대한 작업 실행
                name = child.find('name').text #객체의 카테고리 이름
                if name == "excavator" or name == "forklift" or name == "ladder truck" or name == "unknown car" :
                     name = "unknown car"

                if name in namelist: #category list에 해당하는 카테고리의 이름이 있다면 작업 실행
    #               name = child.find('name').text
                    bndbox = child.find('bndbox')
                    xmin = int(float(bndbox.find('xmin').text))
                    ymin = int(float(bndbox.find('ymin').text))
                    xmax = int(float(bndbox.find('xmax').text))
                    ymax = int(float(bndbox.find('ymax').text))
                    yolo_data = convert_xywh(width,height,xmin,xmax,ymin,ymax)
                    #print(yolo_data)
                    if name =='person':
                        cls.append(0)
                        result.write("0"+" "+yolo_data[0]+" "+yolo_data[1]+" "+yolo_data[2]+" "+yolo_data[3]+"\n")
                    elif name=='car' or name=='unknown car':
                        cls.append(1)
                        result.write("1"+" "+yolo_data[0]+" "+yolo_data[1]+" "+yolo_data[2]+" "+yolo_data[3]+"\n")
                    elif name=='bus':
                        cls.append(2)
                        result.write("2"+" "+yolo_data[0]+" "+yolo_data[1]+" "+yolo_data[2]+" "+yolo_data[3]+"\n")
                    elif name=='truck':
                        cls.append(3)
                        result.write("3"+" "+yolo_data[0]+" "+yolo_data[1]+" "+yolo_data[2]+" "+yolo_data[3]+"\n")
                    elif name=='bicycle':
                        cls.append(4)
                        result.write("4"+" "+yolo_data[0]+" "+yolo_data[1]+" "+yolo_data[2]+" "+yolo_data[3]+"\n")
                    elif name=='unknown car':
                        cls.append(5)
                        result.write("4"+" "+yolo_data[0]+" "+yolo_data[1]+" "+yolo_data[2]+" "+yolo_data[3]+"\n")
                    elif name=='motorbike':
                        cls.append(6)
                        result.write("5"+" "+yolo_data[0]+" "+yolo_data[1]+" "+yolo_data[2]+" "+yolo_data[3]+"\n")
        result.close()




def copyimg():
    xmlname=os.listdir(save_yolo)
    for i in xmlname:
        copy_xmlname_list.append(i[:-4])

    for (path, dir, files) in os.walk(img_Rootpath):
        for j,file in enumerate(files):
            if file.endswith(".jpg"):
                total_jpg_file_name.append(file[:-4])
                total_jpg_file_path.append(path)
                full_total_jpg_file_name.append(file)

    total = len(full_total_jpg_file_name)
    start = time.time()
    for i in range(len(total_jpg_file_name)):
        some_process(i)
        now=time.time()
        print(f'\r{i+1}/{total} runtime: {now - start:.2f}', end='')
        for j in range(len(copy_xmlname_list)):
            if(total_jpg_file_name[i]==copy_xmlname_list[j]):
                path=os.path.join(total_jpg_file_path[i],full_total_jpg_file_name[i])
                path1=os.path.join(copy_img_Rootpath,full_total_jpg_file_name[i])
                shutil.copy(path,path1)
    time.sleep(0.5)

def txttopascalvoc():
    fw = os.listdir(save_yolo)
    for line in fw:
        root = etree.Element("annotation")
        img_style = copy_img_Rootpath.split('\\')[-1]
        img_name = line
        image_info = copy_img_Rootpath + "\\" + line[:-4]+".jpg"
        img_txt_root = save_yolo + "\\" + line[:-4]
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
        path.text = "%s" % (save_yolo)
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


makeXmlByCvatxml();
convert_yolo();
copyimg();
txttopascalvoc();
