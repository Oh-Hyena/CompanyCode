import os
from lxml import etree
from PIL import Image
import xml.etree.ElementTree as ET
import shutil
import random
from xml.dom import minidom
import json
import cv2
import io
import csv

# 이미지 경로
imgRootpath=r"D:\HN_code\test\1_labeling\7_txttopascalvoc_6class\1_seongnamfalse1112_7class_img_txt"
# xml 저장 경로
save_xml=r"D:\HN_code\test\1_labeling\7_txttopascalvoc_6class\2_seongnamfalse1112_change_6class_xml"
#os.mkdir(save_xml)
# txt 경로
save_yolo=r"D:\HN_code\test\1_labeling\7_txttopascalvoc_6class\1_seongnamfalse1112_7class_img_txt"

# unknown car 추가하기
labels = ['person','car',"bus", "truck","bicycle", "motorbike"]


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


def convert_label(txt_file):
    global label
    for i in range(len(labels)):
        if txt_file[0] == str(i):
            label = labels[i]
            return label
    return label


fw = os.listdir(save_yolo)
for line in fw:
    root = etree.Element("annotation")
    img_style = imgRootpath.split('\\')[-1]
    img_name = line
    image_info = imgRootpath + "\\" + line[:-4]+".jpg"
    img_txt_root = save_yolo + "\\" + line[:-4]
    print(img_txt_root)
    txt = ".txt"
    txt_path = img_txt_root + txt
    print(txt_path)
    txt_file = csvread(txt_path)
    #####################################
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
