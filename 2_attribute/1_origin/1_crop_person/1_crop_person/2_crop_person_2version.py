# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 09:42:37 2020

@author: kth

어노테이션(xml for cvat) 1개의 파일을 읽고, 150개의 이미지 경로를 참조하여, 작업폴더에 사람이미지만 크롭해주는 프로그램.

"""

import os
import xml.etree.ElementTree as ET
import cv2
import numpy as np

cvatxmlrootpath = r"F:\ai_hub\K-Fashion_이미지\K-Fashion_1\kfashion1_xml\k_fashion1_1_30"
imagesrootpath =  r"F:\ai_hub\K-Fashion_이미지\K-Fashion_1\kfashion1_img"
cropedrootpath =  r"E:\test\sport1"

def naming(length, name):
    name = str(name)
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


def imread(filename, flags=cv2.IMREAD_COLOR, dtype=np.uint8):
    try:
        n = np.fromfile(filename, dtype)
        img = cv2.imdecode(n, flags)

        return img
    except Exception as e:
        print(e)
        return None


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


def cropPersonByXmlForCvat(cvatxmlpath, imagespath, cropedpath,count):
    cropCount = 0
    if not os.path.isfile(cvatxmlpath):
        print("xml없음.")
        return
    if not os.path.isdir(cropedpath):
        print("디렉토리 생성")
        os.mkdir(cropedpath)
    tree = ET.parse(cvatxmlpath)
    note = tree.getroot()
    for image in note.findall("image"):
        dets = []
        name = image.get("name")
        for box in image.findall("box"):
            label = box.get("label")
            if label == "person":
                attribute = box.find("attribute").text
                xtl = int(float(box.get("xtl")))  ##일단 10base로 만드려고 float캐스팅 한번 넣어준거.
                ytl = int(float(box.get("ytl")))
                xbr = int(float(box.get("xbr")))
                ybr = int(float(box.get("ybr")))

                xlen = abs(xtl-xbr)
                ylen = abs(ytl-ybr)

                dets.append([xtl, ytl, xbr, ybr, 1.])

            if label == "person" and attribute == "pure" and  xlen > 25 and ylen > 25 :
                img = imread(os.path.join(imagespath,name), cv2.IMREAD_COLOR)
                # print(imagespath)
                src = img.copy()

                # while True:
                #     img = cv2.imread(os.path.join(imagespath,name), cv2.IMREAD_COLOR)
                #     if img is None:
                #         break
                #     src = img.copy()                
                
                croped = src[ytl:ybr, xtl:xbr]
                cropCount += 1
                # if not os.path.isdir(os.path.join(cropedpath,name[:-5])):
                #     os.mkdir(os.path.join(cropedpath,name[:-5]))
                # imwrite(os.path.join(cropedpath,name[:-5],name[:-5]+"_"+naming(6,cropCount))+".jpg", croped)
                if not os.path.isdir(os.path.join(cropedpath,str(count))):
                    os.mkdir(os.path.join(cropedpath,str(count)))
                #if not os.path.isdir(os.path.join(cropedpath,name[:-10])):
                    #os.mkdir(os.path.join(cropedpath,name[:-10]))
                #imwrite(os.path.join(cropedpath,name[:-10],name[:-10]+"_"+naming(6,cropCount))+".jpg", croped)
                imwrite(os.path.join(cropedpath,str(count),name[:-4]+"_"+naming(6,cropCount))+".jpg", croped)

    # print(name[:-5] + " : "+str(cropCount) + " crop")
    return

def cropPersonByXmlsDirectory(cvatxmlrootpath, imagesrootpath, cropedrootpath):
    cvatxmlpathlist = []
    for (path, dir, files) in os.walk(cvatxmlrootpath):
        for filename in files:
            if filename.endswith(".xml"):
                cvatxmlpathlist.append(os.path.join(path,filename))
    cvatxmlpathlist.sort()
    count = 0
    for file in cvatxmlpathlist:
        cropPersonByXmlForCvat(file, os.path.join(imagesrootpath, file.split("\\")[-1].strip()[:-4]), cropedrootpath ,count)
        count+=1

# cropPersonByXmlForCvat(cvatxmlrootpath, imagesrootpath, cropedrootpath)
cropPersonByXmlsDirectory(cvatxmlrootpath, imagesrootpath, cropedrootpath)
