
'''
python 1_attribute_low_mid_high_statistics.py Alturk_1_48
python 1_attribute_low_mid_high_statistics.py Asan_attribute_1_57
python 1_attribute_low_mid_high_statistics.py Attribute_1_72
python 1_attribute_low_mid_high_statistics.py Summer_1_32
python 1_attribute_low_mid_high_statistics.py Summer16_1_162
python 1_attribute_low_mid_high_statistics.py Summer17_1_941
python 1_attribute_low_mid_high_statistics.py Summer18_1_108
python 1_attribute_low_mid_high_statistics.py sungnamfalse_attribute_1_10
python 1_attribute_low_mid_high_statistics.py unitrain8_1_22

'''

import numpy as np
import os
import xml.etree.ElementTree as ET
from xml.dom import minidom
import pandas as pd
import cv2
import sys

head_xlen1=[]
head_ylen1=[]
common_xlen1=[]
common_ylen1=[]
lower_xlen1=[]
lower_ylen1=[]
upper_xlen1=[]
upper_ylen1=[]
common_condition_xlen1=[]
common_condition_ylen1=[]
lower_condition_xlen1=[]
lower_condition_ylen1=[]
upper_condition_xlen1=[]
upper_condition_ylen1=[]
head_condition_xlen1=[]
head_condition_ylen1=[]
imageName_path=[]
imageName_path2=[]
imageName_path3=[]
imageName_path4=[]
imageName_path5=[]
imageName_path6=[]
imageName_path7=[]
imageName_path8=[]
originalimageName_path=[]

condition_low_width=[]
condition_low_height=[]
condition_mid_high_width=[]
condition_mid_high_height=[]


ONLY_MAKE_DOCUMENTS = False
Temp = "cvatxml"
cvatxmlRootpath = r"D:\HN_code\search\make_attribute_88_66_dataset\refine_attribute_dataset_practice\{}".format(Temp)
cvatxmllist = os.listdir(cvatxmlRootpath)

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

def readBoodreturnInt(Bool):
    if Bool == "false":
        return 0
    else:
        return 1


def statistic():
    #common
    global common_low_width_count,common_low_height_count,common_mid_high_width_count,common_mid_high_height_count
    common_low_width_count=0
    common_low_height_count=0
    common_mid_high_width_count=0
    common_mid_high_height_count=0

    #head
    global head_low_width_count,head_low_height_count,head_mid_high_width_count,head_mid_high_height_count
    head_low_width_count=0
    head_low_height_count=0
    head_mid_high_width_count=0
    head_mid_high_height_count=0

    #lower
    global lower_low_width_count,lower_low_height_count,lower_mid_high_width_count,lower_mid_high_height_count
    lower_low_width_count=0
    lower_low_height_count=0
    lower_mid_high_width_count=0
    lower_mid_high_height_count=0


    #upper
    global upper_low_width_count,upper_low_height_count,upper_mid_high_width_count,upper_mid_high_height_count
    upper_low_width_count=0
    upper_low_height_count=0
    upper_mid_high_width_count=0
    upper_mid_high_height_count=0


    for i in range(len(common_xlen1)):
        #common
        if(common_xlen1[i]<=23):
            common_low_width_count+=1
        elif(common_xlen1[i]>23):
            common_mid_high_width_count+=1
        if(common_ylen1[i]<=23):
            common_low_height_count+=1
        elif(common_ylen1[i]>23):
            common_mid_high_height_count+=1
        #head
        if(head_xlen1[i]<=23):
            head_low_width_count+=1
        elif(head_xlen1[i]>23):
            head_mid_high_width_count+=1
        if(head_ylen1[i]<=23):
            head_low_height_count+=1
        elif(head_ylen1[i]>23):
            head_mid_high_height_count+=1

        #upper
        if(upper_xlen1[i]<=23):
            upper_low_width_count+=1
        elif(upper_xlen1[i]>23):
            upper_mid_high_width_count+=1
        if(upper_ylen1[i]<=23):
            upper_low_height_count+=1
        elif(upper_ylen1[i]>23):
            upper_mid_high_height_count+=1

        #lower
        if(lower_xlen1[i]<=23):
            lower_low_width_count+=1
        elif(lower_xlen1[i]>23):
            lower_mid_high_width_count+=1
        if(lower_ylen1[i]<=23):
            lower_low_height_count+=1
        elif(lower_ylen1[i]>23):
            lower_mid_high_height_count+=1
    print('-------------------common--------------------')
    print('common_low_width_count:',common_low_width_count)
    print('common_low_height_count:',common_low_height_count)
    print('common_mid_high_width_count:',common_mid_high_width_count)
    print('common_mid_high_height_count:',common_mid_high_height_count)

    print('-------------------head--------------------')
    print('head_low_width_count:',head_low_width_count)
    print('head_low_height_count:',head_low_height_count)
    print('head_mid_high_width_count:',head_mid_high_width_count)
    print('head_mid_high_height_count:',head_mid_high_height_count)

    print('-------------------upper--------------------')
    print('upper_low_width_count:',upper_low_width_count)
    print('upper_low_height_count:',upper_low_height_count)
    print('upper_mid_high_width_count:',upper_mid_high_width_count)
    print('upper_mid_high_height_count:',upper_mid_high_height_count)

    print('-------------------lower--------------------')
    print('lower_low_width_count:',lower_low_width_count)
    print('lower_low_height_count:',lower_low_height_count)
    print('lower_mid_high_width_count:',lower_mid_high_width_count)
    print('lower_mid_high_height_count:',lower_mid_high_height_count)

def condition_after(width,height,imageName):
    if(width <=23 or height <=23):
        imageName_path.append(imageName)
        #print('width/height',width,height)
    if(width >23 and height >23):
        imageName_path2.append(imageName)

def condition_after2(width,height,imageName):
    if(width <=23 or height <=23):
        imageName_path3.append(imageName)
        #print('width/height',width,height)
    if(width >23 and height >23):
        imageName_path4.append(imageName)

def condition_after3(width,height,imageName):
    if(width <=23 or height <=23):
        imageName_path5.append(imageName)
        #print('width/height',width,height)
    if(width >23 and height >23):
        imageName_path6.append(imageName)

def condition_after4(width,height,imageName):
    if(width <=23 or height <=23):
        imageName_path7.append(imageName)
        #print('width/height',width,height)
    if(width >23 and height >23):
        imageName_path8.append(imageName)
for cvatxml in cvatxmllist:
    if cvatxml.endswith(".xml"):
        tree = ET.parse(os.path.join(cvatxmlRootpath, cvatxml))
        note = tree.getroot()
        #print(os.path.join(cvatxmlRootpath, cvatxml))
        for image in note.findall("image"):
            imageName= image.get("name")
            ## 기본적으로 한개도 안쳐져있는 경우 cvatxmls에 기록이 안됨.

            ### 가방이 두개 있는 경우 버림.
            MOREBAG = False
            bagdk = 0
            plasticbag = 0
            shoulderbag = 0
            totebag = 0
            backpack = 0
            for box in image.findall("box"):
                label = box.get("label")
                if label == "all":
                    for attribute in box.findall("attribute"):
                        if attribute.get("name") == "unknown_bag":
                            unknown_bag = attribute.text
                            unknown_bag = readBoodreturnInt(unknown_bag)
                            bagdk = unknown_bag
                        elif attribute.get("name") == "plasticbag":
                            plasticbag = attribute.text
                            plasticbag = readBoodreturnInt(plasticbag)
                        elif attribute.get("name") == "shoulderbag":
                            shoulderbag = attribute.text
                            shoulderbag = readBoodreturnInt(shoulderbag)
                        elif attribute.get("name") == "handbag":
                            handbag = attribute.text
                            handbag = readBoodreturnInt(handbag)
                            totebag = handbag
                        elif attribute.get("name") == "backpack":
                            backpack = attribute.text
                            backpack = readBoodreturnInt(backpack)
                        if plasticbag + shoulderbag + totebag + backpack + bagdk >= 2 :
                            MOREBAG = True
            if MOREBAG == True:
                continue
            #---------------------


            ### 라벨 개수 4개 아니면 버림.
            if not (len(image.findall("box")) == 4):
#                 if ONLY_MAKE_DOCUMENTS == False:
#                     print(imageName)
                continue
            #--------------------


            ### 4개여도 같은 박스중첩이 있을 경우 버림.
            labelList = []
            for box in image.findall("box"):
                labelList.append(box.get("label"))
            if not (len(set(labelList)) == 4):
#                 if ONLY_MAKE_DOCUMENTS == False:
#                     print(imageName)
                continue
            #-------------------
            for box in image.findall("box"):
                label = box.get("label")
                if label == "all":
                    xtl = int(float(box.get("xtl")))
                    ytl = int(float(box.get("ytl")))
                    xbr = int(float(box.get("xbr")))
                    ybr = int(float(box.get("ybr")))
                    xlen = abs(xtl-xbr)
                    ylen = abs(ytl-ybr)
                    common_xlen1.append(xlen)
                    common_ylen1.append(ylen)
                    condition_after(xlen,ylen,imageName)
                    #print('common_width,common_height',xlen,ylen)
                if label == "head":
                    xtl = int(float(box.get("xtl")))
                    ytl = int(float(box.get("ytl")))
                    xbr = int(float(box.get("xbr")))
                    ybr = int(float(box.get("ybr")))
                    xlen = abs(xtl-xbr)
                    ylen = abs(ytl-ybr)
                    head_xlen1.append(xlen)
                    head_ylen1.append(ylen)
                    condition_after2(xlen,ylen,imageName)

                if label == "lower":
                    xtl = int(float(box.get("xtl")))
                    ytl = int(float(box.get("ytl")))
                    xbr = int(float(box.get("xbr")))
                    ybr = int(float(box.get("ybr")))
                    xlen = abs(xtl-xbr)
                    ylen = abs(ytl-ybr)
                    lower_xlen1.append(xlen)
                    lower_ylen1.append(ylen)
                    condition_after3(xlen,ylen,imageName)
                    #print('lower_width,lower_height',xlen,ylen)
                if label == "upper":
                    xtl = int(float(box.get("xtl")))
                    ytl = int(float(box.get("ytl")))
                    xbr = int(float(box.get("xbr")))
                    ybr = int(float(box.get("ybr")))
                    xlen = abs(xtl-xbr)
                    ylen = abs(ytl-ybr)
                    upper_xlen1.append(xlen)
                    upper_ylen1.append(ylen)
                    condition_after4(xlen,ylen,imageName)

statistic()
print('----------------------------------------------------')
ex_list=list(set(imageName_path))
ex_list2=list(set(imageName_path2))
ex_list3=list(set(imageName_path3))
ex_list4=list(set(imageName_path4))
ex_list5=list(set(imageName_path5))
ex_list6=list(set(imageName_path6))
ex_list7=list(set(imageName_path7))
ex_list8=list(set(imageName_path8))


print('[common-low] width,height 조건에 해당하는 객체수:',len(ex_list))
print('[common-mid-high] width,height 조건에 해당하는 객체수:',len(ex_list2))
print('[head-low] width,height 조건에 해당하는 객체수:',len(ex_list3))
print('[head-mid-high] width,height 조건에 해당하는 객체수:',len(ex_list4))
print('[upper-low] width,height 조건에 해당하는 객체수:',len(ex_list7))
print('[upper-mid-high] width,height 조건에 해당하는 객체수:',len(ex_list8))
print('[lower-low] width,height 조건에 해당하는 객체수:',len(ex_list5))
print('[lower-mid-high] width,height 조건에 해당하는 객체수:',len(ex_list6))
