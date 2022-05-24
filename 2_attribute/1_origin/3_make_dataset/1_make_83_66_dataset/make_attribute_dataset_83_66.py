'''
python make83class_66class.py Alturk_1_48
python make83class_66class.py Asan_attribute_1_57
python make83class_66class.py Attribute_1_72
python make83class_66class.py Summer_1_32
python make83class_66class.py Summer16_1_162
python make83class_66class.py Summer17_1_94
python make83class_66class.py Summer18_1_108
python make83class_66class.py sungnamfalse_attribute_1_10
python make83class_66class.py unitrain8_1_22

'''
import random
import numpy as np
import os
import xml.etree.ElementTree as ET
from xml.dom import minidom
import cv2
import sys

ONLY_MAKE_DOCUMENTS=False
cvatxmlRootpath = r"E:\Attribute\market-1501\xml"
cvatxmllist = os.listdir(cvatxmlRootpath)
#attribute_img는 H:\ssd_1TB_blue\total_makeAttribute_dataset 에 들어있음
imageRootpath = r"E:\Attribute\market-1501\img"
#이거그대로
newImageRootpath = r"E:\Attribute\market-1501\market-1501_1_26"
os.makedirs(newImageRootpath,exist_ok=True)
print('cvatxml위치는 :{}'.format(cvatxmlRootpath))
print('newImageRootpath위치는 :{}'.format(newImageRootpath))
print('imageRootpath위치는 :{}'.format(imageRootpath))

##원하는 목록만 가져온 리스트
all_newImageRootpath = os.path.join(newImageRootpath, "common", "common_images")
head_newImageRootpath = os.path.join(newImageRootpath, "head","head_images")
upper_newImageRootpath = os.path.join(newImageRootpath, "upper","upper_images")
lower_newImageRootpath = os.path.join(newImageRootpath, "lower","lower_images")

os.makedirs(all_newImageRootpath,exist_ok=True)
os.makedirs(head_newImageRootpath,exist_ok=True)
os.makedirs(upper_newImageRootpath,exist_ok=True)
os.makedirs(lower_newImageRootpath,exist_ok=True)

cvatxmlNameList = []
cvatxmllist = os.listdir(cvatxmlRootpath)
for line in cvatxmllist:
    cvatxmlNameList.append(line[:-4])

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


def getImagePath(file):
    file= file.strip()
    for (path, dir, files) in os.walk(imageRootpath):
        for filename in files:
            filename = filename.strip()
            if filename == file:
                return os.path.join(path, filename)





def make83class():

    allAttributeFile = open(os.path.join(all_newImageRootpath, "..", "83_common_attribute_annotation.txt"), "w")
    headAttributeFile = open(os.path.join(head_newImageRootpath, "..", "83_head_attribute_annotation.txt"), "w")
    upperAttributeFile = open(os.path.join(upper_newImageRootpath, "..", "83_upper_attribute_annotation.txt"), "w")
    lowerAttributeFile = open(os.path.join(lower_newImageRootpath, "..", "83_lower_attribute_annotation.txt"), "w")

    head_hair_short = 0
    head_hair_long = 0
    head_hair_bald = 0
    head_hair_unknown = 0

    head_hat_red = 0
    head_hat_yellow = 0
    head_hat_green = 0
    head_hat_blue = 0
    head_hat_brown = 0
    head_hat_pink = 0
    head_hat_grey = 0
    head_hat_black = 0
    head_hat_white = 0
    head_hat_color_unknown = 0

    head_hat_hatless = 0
    head_hat_cap = 0
    head_hat_brimmed = 0
    head_hat_brimless = 0
    head_hat_helmat= 0
    head_hat_hood = 0
    head_hat_unknown = 0


    all_gender_male = 0
    all_gender_female = 0
    all_gender_unknown = 0

    all_age_infant = 0
    all_age_child = 0
    all_age_teenager = 0
    all_age_adult = 0
    all_age_oldperson = 0

    all_bag_red = 0
    all_bag_yellow = 0
    all_bag_green = 0
    all_bag_blue = 0
    all_bag_brown = 0
    all_bag_pink = 0
    all_bag_grey = 0
    all_bag_black = 0
    all_bag_white = 0
    all_bag_color_unknown = 0

    all_unknown_bag = 0
    all_plasticbag = 0
    all_shoulderbag = 0
    all_handbag = 0
    all_backpack = 0
    all_bagless = 0

    upper_top_long_sleeve = 0
    upper_top_short_sleeve = 0
    upper_top_unknown_sleeve = 0

    upper_top_red = 0
    upper_top_yellow = 0
    upper_top_green = 0
    upper_top_blue = 0
    upper_top_brown = 0
    upper_top_pink = 0
    upper_top_grey = 0
    upper_top_black = 0
    upper_top_white = 0
    upper_top_color_unknown = 0


    lower_bottom_long_pants = 0
    lower_bottom_short_pants = 0
    lower_bottom_long_skirt = 0
    lower_bottom_short_skirt = 0
    lower_bottom_unknown_bottom = 0

    lower_shoes_red = 0
    lower_shoes_yellow = 0
    lower_shoes_green = 0
    lower_shoes_blue = 0
    lower_shoes_brown = 0
    lower_shoes_pink = 0
    lower_shoes_grey = 0
    lower_shoes_black = 0
    lower_shoes_white = 0
    lower_shoes_color_unknown = 0


    lower_bottom_red = 0
    lower_bottom_yellow = 0
    lower_bottom_green = 0
    lower_bottom_blue = 0
    lower_bottom_brown = 0
    lower_bottom_pink = 0
    lower_bottom_grey = 0
    lower_bottom_black = 0
    lower_bottom_white = 0
    lower_bottom_color_unknown = 0



    img_list=[]


    for cvatxml in cvatxmllist:
        if cvatxml.endswith(".xml"):
            tree = ET.parse(os.path.join(cvatxmlRootpath, cvatxml))
            note = tree.getroot()
            for image in note.findall("image"):
                imageName= image.get("name")
                img_list.append(imageName)
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

                    continue
                #--------------------


                ### 4개여도 같은 박스중첩이 있을 경우 버림.
                labelList = []
                for box in image.findall("box"):
                    labelList.append(box.get("label"))
                if not (len(set(labelList)) == 4):

                    continue
                #-------------------


                for box in image.findall("box"):
                    label = box.get("label")

                    if label == "head":
                        xtl = int(float(box.get("xtl")))
                        ytl = int(float(box.get("ytl")))
                        xbr = int(float(box.get("xbr")))
                        ybr = int(float(box.get("ybr")))
                        xlen = abs(xtl-xbr)
                        ylen = abs(ytl-ybr)

                        if ONLY_MAKE_DOCUMENTS == False:
                            img = imread(os.path.join(getImagePath(imageName)))
                            src = img.copy()
                            croped = src[ytl:ybr, xtl:xbr]
                            imwrite(os.path.join(head_newImageRootpath,imageName), croped)
                            #img2 = imread(os.path.join(getImagePath(imageName)))
                            #headAttributeFile1_img.write(img2+"\n")
                        for attribute in box.findall("attribute"):

                            if attribute.get("name") == "hair":
                                hair = attribute.text
                                if hair == "short":
                                    short, long, bald, hairdk = 1,0,0,0
                                    head_hair_short += 1

                                elif hair == "long":
                                    short, long, bald, hairdk = 0,1,0,0
                                    head_hair_long  += 1

                                elif hair == "bald":
                                    short, long, bald, hairdk = 0,0,1,0
                                    head_hair_bald += 1

                                elif hair == "unknown":
                                    short, long, bald, hairdk = 0,0,0,1
                                    head_hair_unknown += 1




                            elif attribute.get("name") == "hat_red":
                                hat_red = attribute.text
                                hat_red = readBoodreturnInt(hat_red)
                                head_hat_red += hat_red


                            elif attribute.get("name") == "hat_yellow":
                                hat_yellow = attribute.text
                                hat_yellow = readBoodreturnInt(hat_yellow)
                                head_hat_yellow += hat_yellow

                            elif attribute.get("name") == "hat_green":
                                hat_green = attribute.text
                                hat_green = readBoodreturnInt(hat_green)
                                head_hat_green += hat_green


                            elif attribute.get("name") == "hat_blue":
                                hat_blue = attribute.text
                                hat_blue = readBoodreturnInt(hat_blue)
                                head_hat_blue += hat_blue



                            elif attribute.get("name") == "hat_brown":
                                hat_brown = attribute.text
                                hat_brown = readBoodreturnInt(hat_brown)
                                head_hat_brown += hat_brown


                            elif attribute.get("name") == "hat_pink":
                                hat_pink = attribute.text
                                hat_pink = readBoodreturnInt(hat_pink)
                                head_hat_pink += hat_pink


                            elif attribute.get("name") == "hat_grey":
                                hat_grey = attribute.text
                                hat_grey = readBoodreturnInt(hat_grey)
                                head_hat_grey += hat_grey


                            elif attribute.get("name") == "hat_black":
                                hat_black = attribute.text
                                hat_black = readBoodreturnInt(hat_black)
                                head_hat_black += hat_black


                            elif attribute.get("name") == "hat_white":
                                hat_white = attribute.text
                                hat_white = readBoodreturnInt(hat_white)
                                head_hat_white += hat_white


                            elif attribute.get("name") == "hat_color_unknown":
                                hat_color_unknown = attribute.text
                                hat_color_unknown = readBoodreturnInt(hat_color_unknown)
                                head_hat_color_unknown += hat_color_unknown



                            elif attribute.get("name") == "hat":
                                hat = attribute.text
                                if hat == "hatless":
                                    cap, visor, novisor, helmat, hood, nohat, hatdk = 0,0,0,0,0,1,0
                                    head_hat_hatless += 1


                                    #어노테이터 실수 제거 코드.
                                    hat_red, hat_yellow, hat_green, hat_blue, hat_brown, hat_pink, hat_grey, hat_black, hat_white, hat_color_unknown = 0,0,0,0,0, 0,0,0,0,0


                                elif hat == "cap":
                                    cap, visor, novisor, helmat, hood, nohat, hatdk = 1,0,0,0,0,0,0
                                    head_hat_cap += 1


                                elif hat == "brimmed":
                                    cap, visor, novisor, helmat, hood, nohat, hatdk = 0,1,0,0,0,0,0
                                    head_hat_brimmed += 1


                                elif hat == "brimless":
                                    cap, visor, novisor, helmat, hood, nohat, hatdk = 0,0,1,0,0,0,0
                                    head_hat_brimless += 1

                                elif hat == "helmat":
                                    cap, visor, novisor, helmat, hood, nohat, hatdk = 0,0,0,1,0,0,0
                                    head_hat_helmat += 1

                                elif hat == "hood":
                                    cap, visor, novisor, helmat, hood, nohat, hatdk = 0,0,0,0,1,0,0
                                    head_hat_hood += 1

                                elif hat == "unknown":
                                    cap, visor, novisor, helmat, hood, nohat, hatdk = 0,0,0,0,0,0,1
                                    head_hat_unknown += 1



                        HEAD_classes = "{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}".format(cap, visor, novisor, helmat, hood, nohat, hatdk,hat_red,hat_yellow,hat_green,hat_blue,hat_brown,hat_pink,hat_grey,hat_black,hat_white,hat_color_unknown, short, long, bald, hairdk)
                        #classesHEad =                                                 ['cap','visor','nonvisor','helmat','hood','nohat','hatdk','hatred','hatyellow','hatgreen','hatblue','hatbrown','hatpink','hatgray','hatblack','hatwhite','hatcolordk','shot','long','bald','hairdk']
                        headAttributeFile.write(HEAD_classes+"\n")


                    elif label == "all":
                        xtl = int(float(box.get("xtl")))
                        ytl = int(float(box.get("ytl")))
                        xbr = int(float(box.get("xbr")))
                        ybr = int(float(box.get("ybr")))
                        xlen = abs(xtl-xbr)
                        ylen = abs(ytl-ybr)

                        if ONLY_MAKE_DOCUMENTS == False:
                            img = imread(os.path.join(getImagePath(imageName)))
                            #print(img)
                            src = img.copy()
                            croped = src[ytl:ybr, xtl:xbr]
                            imwrite(os.path.join(all_newImageRootpath,imageName), croped)
                                    #img2 = imread(os.path.join(getImagePath(imageName)))
                            #allAttributeFile1_img.write(img2+"\n")
                        for attribute in box.findall("attribute"):
                            if attribute.get("name") == "gender":
                                gender = attribute.text
                                if gender == "male":
                                    man, woman, unknown_gender = 1,0,0
                                    all_gender_male += 1

                                elif gender == "female":
                                    man, woman, unknown_gender = 0,1,0
                                    all_gender_female += 1

                                else: ##unknown gender
                                    man, woman, unknown_gender = 0,0,1
                                    all_gender_unknown += 1



                            elif attribute.get("name") == "age":
                                age = attribute.text
                                if age == "20~70":
                                    infant,child,teenager,adult,oldperson = 0,0,0,1,0
                                    all_age_adult += 1

                                elif age == "0~7":
                                    infant,child,teenager,adult,oldperson = 1,0,0,0,0
                                    all_age_infant += 1

                                elif age == "8~13":
                                    infant,child,teenager,adult,oldperson = 0,1,0,0,0
                                    all_age_child += 1

                                elif age == "14~19":
                                    infant,child,teenager,adult,oldperson = 0,0,1,0,0
                                    all_age_teenager += 1

                                else: ## 70~
                                    infant,child,teenager,adult,oldperson = 0,0,0,0,1
                                    all_age_oldperson += 1



                            elif attribute.get("name") == "bag_color_unknown":
                                bag_color_unknown = attribute.text
                                bag_color_unknown = readBoodreturnInt(bag_color_unknown)
                                all_bag_color_unknown += bag_color_unknown


                            elif attribute.get("name") == "bag_white":
                                bag_white = attribute.text
                                bag_white = readBoodreturnInt(bag_white)
                                all_bag_white += bag_white


                            elif attribute.get("name") == "bag_black":
                                bag_black = attribute.text
                                bag_black = readBoodreturnInt(bag_black)
                                all_bag_black += bag_black


                            elif attribute.get("name") == "bag_grey":
                                bag_grey = attribute.text
                                bag_grey = readBoodreturnInt(bag_grey)
                                all_bag_grey += bag_grey


                            elif attribute.get("name") == "bag_pink":
                                bag_pink = attribute.text
                                bag_pink = readBoodreturnInt(bag_pink)
                                all_bag_pink += bag_pink


                            elif attribute.get("name") == "bag_brown":
                                bag_brown = attribute.text
                                bag_brown = readBoodreturnInt(bag_brown)
                                all_bag_brown += bag_brown


                            elif attribute.get("name") == "bag_blue":
                                bag_blue = attribute.text
                                bag_blue = readBoodreturnInt(bag_blue)
                                all_bag_blue += bag_blue


                            elif attribute.get("name") == "bag_green":
                                bag_green = attribute.text
                                bag_green = readBoodreturnInt(bag_green)
                                all_bag_green += bag_green


                            elif attribute.get("name") == "bag_yellow":
                                bag_yellow = attribute.text
                                bag_yellow = readBoodreturnInt(bag_yellow)
                                all_bag_yellow += bag_yellow


                            elif attribute.get("name") == "bag_red":
                                bag_red = attribute.text
                                bag_red = readBoodreturnInt(bag_red)
                                all_bag_red += bag_red


                            elif attribute.get("name") == "unknown_bag":
                                unknown_bag = attribute.text
                                unknown_bag = readBoodreturnInt(unknown_bag)
                                bagdk = unknown_bag
                                all_unknown_bag += unknown_bag


                            elif attribute.get("name") == "plasticbag":
                                plasticbag = attribute.text
                                plasticbag = readBoodreturnInt(plasticbag)
                                all_plasticbag += plasticbag


                            elif attribute.get("name") == "shoulderbag":
                                shoulderbag = attribute.text
                                shoulderbag = readBoodreturnInt(shoulderbag)
                                all_shoulderbag += shoulderbag


                            elif attribute.get("name") == "handbag":
                                handbag = attribute.text
                                handbag = readBoodreturnInt(handbag)
                                totebag = handbag
                                all_handbag += handbag


                            elif attribute.get("name") == "backpack":
                                backpack = attribute.text
                                backpack = readBoodreturnInt(backpack)
                                all_backpack += backpack


                            elif attribute.get("name") == "bagless":
                                bagless = attribute.text
                                bagless = readBoodreturnInt(bagless)
                                bagnone = bagless
                                all_bagless += bagless



                        ALL_classes = "{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}".format(man,woman,unknown_gender,infant,child,teenager,adult,oldperson,backpack,totebag,shoulderbag,plasticbag,bagdk,bagnone, bag_red, bag_yellow, bag_green, bag_blue, bag_brown, bag_pink, bag_grey, bag_black, bag_white, bag_color_unknown)
                        #classesCOMmon = ['man','woman','genderdk','infant','child','teenager','adult','oldperson','backpack','totebag','shoulderbag','plasticbag','bagdk','bagnone','begred','begyellow','beggreen','begblue','begbrown','begpink','beggray','begblack','begwhite','begcolordk']

                        allAttributeFile.write(ALL_classes+"\n")

                    elif label == "upper":
                        xtl = int(float(box.get("xtl")))
                        ytl = int(float(box.get("ytl")))
                        xbr = int(float(box.get("xbr")))
                        ybr = int(float(box.get("ybr")))
                        xlen = abs(xtl-xbr)
                        ylen = abs(ytl-ybr)

                        if ONLY_MAKE_DOCUMENTS == False:
                            img = imread(os.path.join(getImagePath(imageName)))
                            src = img.copy()
                            croped = src[ytl:ybr, xtl:xbr]
                            imwrite(os.path.join(upper_newImageRootpath,imageName), croped)
                            #img2 = imread(os.path.join(getImagePath(imageName)))
                            #upperAttributeFile1_img.write(img2+"\n")
                        for attribute in box.findall("attribute"):


                            if attribute.get("name") == "top_white":
                                top_white = attribute.text
                                top_white = readBoodreturnInt(top_white)
                                upper_top_white += top_white


                            elif attribute.get("name") == "top_color_unknown":
                                top_color_unknown = attribute.text
                                top_color_unknown = readBoodreturnInt(top_color_unknown)
                                upper_top_color_unknown += top_color_unknown


                            elif attribute.get("name") == "top_black":
                                top_black = attribute.text
                                top_black = readBoodreturnInt(top_black)
                                upper_top_black += top_black


                            elif attribute.get("name") == "top_grey":
                                top_grey = attribute.text
                                top_grey = readBoodreturnInt(top_grey)
                                upper_top_grey += top_grey


                            elif attribute.get("name") == "top_pink":
                                top_pink = attribute.text
                                top_pink = readBoodreturnInt(top_pink)
                                upper_top_pink += top_pink

                            elif attribute.get("name") == "top_brown":
                                top_brown = attribute.text
                                top_brown = readBoodreturnInt(top_brown)
                                upper_top_brown += top_brown

                            elif attribute.get("name") == "top_blue":
                                top_blue = attribute.text
                                top_blue = readBoodreturnInt(top_blue)
                                upper_top_blue += top_blue


                            elif attribute.get("name") == "top_green":
                                top_green = attribute.text
                                top_green = readBoodreturnInt(top_green)
                                upper_top_green += top_green


                            elif attribute.get("name") == "top_yellow":
                                top_yellow = attribute.text
                                top_yellow = readBoodreturnInt(top_yellow)
                                upper_top_yellow += top_yellow


                            elif attribute.get("name") == "top_red":
                                top_red = attribute.text
                                top_red = readBoodreturnInt(top_red)
                                upper_top_red += top_red


                            elif attribute.get("name") == "top":
                                top = attribute.text
                                if top == "long_sleeve":
                                    long_sleeve, short_sleeve, unknown_sleeve = 1,0,0
                                    upper_top_long_sleeve += 1

                                elif top == "short_sleeve":
                                    long_sleeve, short_sleeve, unknown_sleeve = 0,1,0
                                    upper_top_short_sleeve += 1

                                else: ##unknown sleeve
                                    long_sleeve, short_sleeve, unknown_sleeve = 0,0,1
                                    upper_top_unknown_sleeve += 1


                                longshirt = long_sleeve
                                shortshirt = short_sleeve

                        UPPER_classes = "{}{}{}{}{}{}{}{}{}{}{}{}{}".format(longshirt,shortshirt, unknown_sleeve, top_red,top_yellow,top_green,top_blue,top_brown,top_pink,top_grey,top_black,top_white,top_color_unknown)
                        upperAttributeFile.write(UPPER_classes+"\n")

                    elif label == "lower":
                        xtl = int(float(box.get("xtl")))
                        ytl = int(float(box.get("ytl")))
                        xbr = int(float(box.get("xbr")))
                        ybr = int(float(box.get("ybr")))
                        xlen = abs(xtl-xbr)
                        ylen = abs(ytl-ybr)

                        if ONLY_MAKE_DOCUMENTS == False:
                            img = imread(os.path.join(getImagePath(imageName)))
                            src = img.copy()
                            croped = src[ytl:ybr, xtl:xbr]
                            imwrite(os.path.join(lower_newImageRootpath,imageName), croped)

                        for attribute in box.findall("attribute"):

                            if attribute.get("name") == "bottom_color_unknown":
                                bottom_color_unknown = attribute.text
                                bottom_color_unknown = readBoodreturnInt(bottom_color_unknown)
                                lower_bottom_color_unknown += bottom_color_unknown


                            elif attribute.get("name") == "bottom_white":
                                bottom_white = attribute.text
                                bottom_white = readBoodreturnInt(bottom_white)
                                lower_bottom_white += bottom_white


                            elif attribute.get("name") == "bottom_black":
                                bottom_black = attribute.text
                                bottom_black = readBoodreturnInt(bottom_black)
                                lower_bottom_black += bottom_black


                            elif attribute.get("name") == "bottom_grey":
                                bottom_grey = attribute.text
                                bottom_grey = readBoodreturnInt(bottom_grey)
                                lower_bottom_grey += bottom_grey


                            elif attribute.get("name") == "bottom_pink":
                                bottom_pink = attribute.text
                                bottom_pink = readBoodreturnInt(bottom_pink)
                                lower_bottom_pink += bottom_pink

                            elif attribute.get("name") == "bottom_brown":
                                bottom_brown = attribute.text
                                bottom_brown = readBoodreturnInt(bottom_brown)
                                lower_bottom_brown += bottom_brown


                            elif attribute.get("name") == "bottom_blue":
                                bottom_blue = attribute.text
                                bottom_blue = readBoodreturnInt(bottom_blue)
                                lower_bottom_blue += bottom_blue


                            elif attribute.get("name") == "bottom_green":
                                bottom_green = attribute.text
                                bottom_green = readBoodreturnInt(bottom_green)
                                lower_bottom_green += bottom_green


                            elif attribute.get("name") == "bottom_yellow":
                                bottom_yellow = attribute.text
                                bottom_yellow = readBoodreturnInt(bottom_yellow)
                                lower_bottom_yellow += bottom_yellow


                            elif attribute.get("name") == "bottom_red":
                                bottom_red = attribute.text
                                bottom_red = readBoodreturnInt(bottom_red)
                                lower_bottom_red += bottom_red


                            elif attribute.get("name") == "bottom":
                                bottom = attribute.text
                                if bottom == "long_pants":
                                    long_pants, short_pants, long_skirt, short_skirt, unknown_bottom = 1,0,0,0,0
                                    lower_bottom_long_pants += 1

                                elif bottom == "short_pants":
                                    long_pants, short_pants, long_skirt, short_skirt, unknown_bottom = 0,1,0,0,0
                                    lower_bottom_short_pants += 1

                                elif bottom == "long_skirt":
                                    long_pants, short_pants, long_skirt, short_skirt, unknown_bottom = 0,0,1,0,0
                                    lower_bottom_long_skirt += 1

                                elif bottom == "short_skirt":
                                    long_pants, short_pants, long_skirt, short_skirt, unknown_bottom = 0,0,0,1,0
                                    lower_bottom_short_skirt += 1

                                else: # unknown bottom
                                    long_pants, short_pants, long_skirt, short_skirt, unknown_bottom = 0,0,0,0,1
                                    lower_bottom_unknown_bottom += 1

                            elif attribute.get("name") == "shoes_color":
                                shoes_color = attribute.text
                                if shoes_color == "shoes_red":
                                    shoes_red, shoes_yellow, shoes_green, shoes_blue, shoes_brown, shoes_pink, shoes_grey, shoes_black, shoes_white,  shoes_unknown = 1,0,0,0,0,0,0,0,0,0
                                    lower_shoes_red += 1

                                elif shoes_color == "shoes_yellow":
                                    shoes_red, shoes_yellow, shoes_green, shoes_blue, shoes_brown, shoes_pink, shoes_grey, shoes_black, shoes_white,  shoes_unknown = 0,1,0,0,0,0,0,0,0,0
                                    lower_shoes_yellow += 1

                                elif shoes_color == "shoes_green":
                                    shoes_red, shoes_yellow, shoes_green, shoes_blue, shoes_brown, shoes_pink, shoes_grey, shoes_black, shoes_white,  shoes_unknown = 0,0,1,0,0,0,0,0,0,0
                                    lower_shoes_green += 1

                                elif shoes_color == "shoes_blue":
                                    shoes_red, shoes_yellow, shoes_green, shoes_blue, shoes_brown, shoes_pink, shoes_grey, shoes_black, shoes_white,  shoes_unknown = 0,0,0,1,0,0,0,0,0,0
                                    lower_shoes_blue += 1

                                elif shoes_color == "shoes_brown":
                                    shoes_red, shoes_yellow, shoes_green, shoes_blue, shoes_brown, shoes_pink, shoes_grey, shoes_black, shoes_white,  shoes_unknown = 0,0,0,0,1,0,0,0,0,0
                                    lower_shoes_brown += 1

                                elif shoes_color == "shoes_pink":
                                    shoes_red, shoes_yellow, shoes_green, shoes_blue, shoes_brown, shoes_pink, shoes_grey, shoes_black, shoes_white,  shoes_unknown = 0,0,0,0,0,1,0,0,0,0
                                    lower_shoes_pink += 1

                                elif shoes_color == "shoes_grey":
                                    shoes_red, shoes_yellow, shoes_green, shoes_blue, shoes_brown, shoes_pink, shoes_grey, shoes_black, shoes_white,  shoes_unknown = 0,0,0,0,0,0,1,0,0,0
                                    lower_shoes_grey += 1

                                elif shoes_color == "shoes_black":
                                    shoes_red, shoes_yellow, shoes_green, shoes_blue, shoes_brown, shoes_pink, shoes_grey, shoes_black, shoes_white,  shoes_unknown = 0,0,0,0,0,0,0,1,0,0
                                    lower_shoes_black += 1

                                elif shoes_color == "shoes_white":
                                    shoes_red, shoes_yellow, shoes_green, shoes_blue, shoes_brown, shoes_pink, shoes_grey, shoes_black, shoes_white,  shoes_unknown = 0,0,0,0,0,0,0,0,1,0
                                    lower_shoes_white += 1

                                else: #shoes_color_unknown
                                    shoes_red, shoes_yellow, shoes_green, shoes_blue, shoes_brown, shoes_pink, shoes_grey, shoes_black, shoes_white,  shoes_unknown = 0,0,0,0,0,0,0,0,0,1
                                    lower_shoes_color_unknown += 1



                        LOWER_classes = "{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}".format(long_pants, short_pants, long_skirt, short_skirt, unknown_bottom, bottom_red, bottom_yellow, bottom_green, bottom_blue, bottom_brown, bottom_pink, bottom_grey, bottom_black, bottom_white, bottom_color_unknown,shoes_red, shoes_yellow, shoes_green, shoes_blue, shoes_brown, shoes_pink, shoes_grey, shoes_black, shoes_white,  shoes_unknown)
                        lowerAttributeFile.write(LOWER_classes+"\n")
                    else:
                        if ONLY_MAKE_DOCUMENTS == False:
                            print(label)

    print('총이미지개수는',len(img_list))


def make66class():

    global short_pants
    global long_skirt
    global short_skirt
    global bagnone
    global long_sleeve
    global short_sleeve
    global long_sleeve
    global short
    global long
    global shoes_red
    global shoes_yellow
    global shoes_green
    global shoes_blue
    global shoes_brown
    global shoes_pink
    global shoes_grey
    global shoes_black
    global shoes_white
    global cap
    global nocap
    global nohat
    global hat_red
    global hat_yellow
    global hat_green
    global hat_blue
    global hat_brown
    global hat_pink
    global hat_grey
    global hat_black
    global hat_white
    global nobackpack
    nobackpack=0
    global all_plasticbag
    all_plasticbag=0
    global all_shoulderbag
    global all_handbag
    global all_backpack
    global all_bagless
    global gender
    global hair_bald_imagename
    hair_bald_imagename=0
    gender=0
    all_shoulderbag=0
    all_handbag=0
    all_backpack=0
    all_bagless=0

    one_all_backpack=0
    zero_all_backpack=0
    cap=0
    nocap=0
    nohat=0
    hat_red=0
    hat_yellow=0
    hat_green=0
    hat_blue=0
    hat_brown=0
    hat_pink=0
    hat_grey=0
    hat_black=0
    hat_white=0

    long_pants=0
    short_pants=0
    long_skirt=0
    short_skirt=0
    shoes_yellow=0
    shoes_green=0
    shoes_blue=0
    shoes_brown=0
    shoes_pink=0
    shoes_grey=0
    shoes_black=0
    shoes_white=0
    shoes_red=0
    long=0
    short=0
    long_sleeve=0
    short_sleeve=0
    long_sleeve=0
    bagnone=0
    head_hair_short = 0
    head_hair_long = 0
    head_hair_bald=0
    head_hat_red = 0
    head_hat_yellow = 0
    head_hat_green = 0
    head_hat_blue = 0
    head_hat_brown = 0
    head_hat_pink = 0
    head_hat_grey = 0
    head_hat_black = 0
    head_hat_white = 0


    head_hat_hatless = 0
    head_hat_cap = 0
    head_hat_nocap=0


    all_gender_male = 0
    all_gender_female = 0

    all_age_infant = 0
    all_age_child = 0
    all_age_teenager = 0
    all_age_adult = 0
    all_age_oldperson = 0

    all_bag_red = 0
    all_bag_yellow = 0
    all_bag_green = 0
    all_bag_blue = 0
    all_bag_brown = 0
    all_bag_pink = 0
    all_bag_grey = 0
    all_bag_black = 0
    all_bag_white = 0
    all_nobackpack=0
    all_backpack = 0
    all_bagless = 0

    upper_top_long_sleeve = 0
    upper_top_short_sleeve = 0

    upper_top_red = 0
    upper_top_yellow = 0
    upper_top_green = 0
    upper_top_blue = 0
    upper_top_brown = 0
    upper_top_pink = 0
    upper_top_grey = 0
    upper_top_black = 0
    upper_top_white = 0


    lower_bottom_long_pants = 0
    lower_bottom_short_pants = 0
    lower_bottom_long_skirt = 0
    lower_bottom_short_skirt = 0

    lower_shoes_red = 0
    lower_shoes_yellow = 0
    lower_shoes_green = 0
    lower_shoes_blue = 0
    lower_shoes_brown = 0
    lower_shoes_pink = 0
    lower_shoes_grey = 0
    lower_shoes_black = 0
    lower_shoes_white = 0

    lower_bottom_red = 0
    lower_bottom_yellow = 0
    lower_bottom_green = 0
    lower_bottom_blue = 0
    lower_bottom_brown = 0
    lower_bottom_pink = 0
    lower_bottom_grey = 0
    lower_bottom_black = 0
    lower_bottom_white = 0

    hair_unknown_imagename=[]
    hat_colorunknown_imagename=[]
    hatunknown_imagename=[]
    genderunknown_imagename=[]
    bag_colorunknown_imagename=[]
    bagunknown_imagename=[]
    top_colorunknown_imagename=[]
    m_top_longsleeve_imagename=[]
    m_top_shortsleeve_imagename=[]
    top_unknownsleeve_imagename=[]
    bottom_colorunknown_imagename=[]
    m_long_pants_imagename=[]
    m_short_pants_imagename=[]
    m_long_skirt_imagename=[]
    m_short_skirt_imagename=[]
    bottomunknown_imagename=[]
    m_shoes_red_imagename=[]
    m_shoes_yellow_imagename=[]
    m_shoes_green_imagename=[]
    m_shoes_blue_imagename=[]
    m_shoes_brown_imagename=[]
    m_shoes_pink_imagename=[]
    m_shoes_grey_imagename=[]
    m_shoes_black_imagename=[]
    m_shoes_white_imagename=[]
    shoes_colorunknown_imagename=[]
    hairbald_imagename=[]
    MOREBAG1=[]
    img_list=[]
    for cvatxml in cvatxmllist:
        if cvatxml.endswith(".xml"):
            tree = ET.parse(os.path.join(cvatxmlRootpath, cvatxml))
            note = tree.getroot()
            for image in note.findall("image"):
                imageName= image.get("name")
                img_list.append(imageName)
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
                                MOREBAG1.append(MOREBAG)
                if MOREBAG == True:
                    continue
                #---------------------


                ### 라벨 개수 4개 아니면 버림.
                if not (len(image.findall("box")) == 4):

                    continue
                #--------------------


                ### 4개여도 같은 박스중첩이 있을 경우 버림.
                labelList = []
                for box in image.findall("box"):
                    labelList.append(box.get("label"))
                if not (len(set(labelList)) == 4):

                    continue
                #-------------------


                for box in image.findall("box"):
                    label = box.get("label")
                    if label == "head":
                        for attribute in box.findall("attribute"):
                            if attribute.get("name") == "hair":
                                hair = attribute.text
                                if hair == "unknown":
                                    hair_unknown_imagename.append(imageName)
                                elif hair == "bald":
                                    hairbald_imagename.append(imageName)

                            elif attribute.get("name") == "hat_color_unknown":
                                hat_color_unknown=attribute.text
                                if(hat_color_unknown=='true'):
                                    hat_colorunknown_imagename.append(imageName)

                            elif attribute.get("name") == "hat":
                                hat = attribute.text
                                if hat == "unknown":
                                    hatunknown_imagename.append(imageName)

                    elif label == "all":
                        for attribute in box.findall("attribute"):
                            if attribute.get("name") == "gender":
                                gender=attribute.text
                                if(gender=='unknown'):
                                    genderunknown_imagename.append(imageName)

                            elif attribute.get("name") == "bag_color_unknown":
                                bag_color_unknown=attribute.text
                                if(bag_color_unknown=='true'):
                                    bag_colorunknown_imagename.append(imageName)

                            elif attribute.get("name") == "unknown_bag":
                                unknown_bag=attribute.text
                                if(unknown_bag=='true'):
                                    bagunknown_imagename.append(imageName)


                    elif label == "upper":
                        for attribute in box.findall("attribute"):
                            if attribute.get("name") == "top_color_unknown":
                                top_color_unknown=attribute.text
                                if(top_color_unknown=='true'):
                                    top_colorunknown_imagename.append(imageName)


                            elif attribute.get("name") == "top":
                                top = attribute.text
                                if top == "long_sleeve":
                                    m_top_longsleeve_imagename.append(imageName)
                                elif top == "short_sleeve":
                                    m_top_shortsleeve_imagename.append(imageName)
                                else:
                                    top_unknownsleeve_imagename.append(imageName)


                    elif label == "lower":
                        for attribute in box.findall("attribute"):
                            if attribute.get("name") == "bottom_color_unknown":
                                bottom_color_unknown=attribute.text
                                if(bottom_color_unknown=="true"):
                                    bottom_colorunknown_imagename.append(imageName)

                            elif attribute.get("name") == "bottom":
                                bottom = attribute.text
                                if bottom == "long_pants":
                                    m_long_pants_imagename.append(imageName)
                                elif bottom == "short_pants":
                                    m_short_pants_imagename.append(imageName)
                                elif bottom == "long_skirt":
                                    m_long_skirt_imagename.append(imageName)
                                elif bottom == "short_skirt":
                                    m_short_skirt_imagename.append(imageName)
                                else:
                                    bottomunknown_imagename.append(imageName)

                            elif attribute.get("name") == "shoes_color":
                                shoes_color = attribute.text
                                if shoes_color == "shoes_red":
                                    m_shoes_red_imagename.append(imageName)
                                elif shoes_color == "shoes_yellow":
                                    m_shoes_yellow_imagename.append(imageName)
                                elif shoes_color == "shoes_green":
                                    m_shoes_green_imagename.append(imageName)
                                elif shoes_color == "shoes_blue":
                                    m_shoes_blue_imagename.append(imageName)
                                elif shoes_color == "shoes_brown":
                                    m_shoes_brown_imagename.append(imageName)
                                elif shoes_color == "shoes_pink":
                                    m_shoes_pink_imagename.append(imageName)
                                elif shoes_color == "shoes_grey":
                                    m_shoes_grey_imagename.append(imageName)
                                elif shoes_color == "shoes_black":
                                    m_shoes_black_imagename.append(imageName)
                                elif shoes_color == "shoes_white":
                                    m_shoes_white_imagename.append(imageName)
                                else:
                                    shoes_colorunknown_imagename.append(imageName)


    unknown=genderunknown_imagename+bagunknown_imagename+bag_colorunknown_imagename+hair_unknown_imagename+hat_colorunknown_imagename+hatunknown_imagename+hairbald_imagename+top_colorunknown_imagename+top_unknownsleeve_imagename+bottom_colorunknown_imagename+bottomunknown_imagename+shoes_colorunknown_imagename
    ex_unknown=(list(set(unknown)))
    print('총unknown이미지개수는',len(ex_unknown))
    ex_list = []
    for i in img_list:
        if i not in ex_unknown:
            ex_list.append(i)

    allAttributeFile2 = open(os.path.join(all_newImageRootpath, "..", "66_common_attribute_annotation.txt"), "w")
    headAttributeFile2 = open(os.path.join(head_newImageRootpath, "..", "66_head_attribute_annotation.txt"), "w")
    upperAttributeFile2 = open(os.path.join(upper_newImageRootpath, "..", "66_upper_attribute_annotation.txt"), "w")
    lowerAttributeFile2 = open(os.path.join(lower_newImageRootpath, "..", "66_lower_attribute_annotation.txt"), "w")
    allAttributeFile2_img = open(os.path.join(all_newImageRootpath, "..", "66_common_attribute_annotation_img.txt"), "w")
    headAttributeFile2_img = open(os.path.join(head_newImageRootpath, "..", "66_head_attribute_annotation_img.txt"), "w")
    upperAttributeFile2_img = open(os.path.join(upper_newImageRootpath, "..", "66_upper_attribute_annotation_img.txt"), "w")
    lowerAttributeFile2_img = open(os.path.join(lower_newImageRootpath, "..", "66_lower_attribute_annotation_img.txt"), "w")

    for cvatxml in cvatxmllist:
        if cvatxml.endswith(".xml"):
            tree = ET.parse(os.path.join(cvatxmlRootpath, cvatxml))
            note = tree.getroot()

            for image in note.findall("image"):
                imageName= image.get("name")
                for i in range(len(ex_list)):
                    if(imageName==ex_list[i]):
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

                            continue
                        #--------------------


                        ### 4개여도 같은 박스중첩이 있을 경우 버림.
                        labelList = []
                        for box in image.findall("box"):
                            labelList.append(box.get("label"))
                        if not (len(set(labelList)) == 4):

                            continue
                        #-------------------



                        for box in image.findall("box"):
                            label = box.get("label")

                            if label == "head":
                                xtl = int(float(box.get("xtl")))
                                ytl = int(float(box.get("ytl")))
                                xbr = int(float(box.get("xbr")))
                                ybr = int(float(box.get("ybr")))
                                xlen = abs(xtl-xbr)
                                ylen = abs(ytl-ybr)

                                img =(os.path.join(getImagePath(imageName)))
                                headAttributeFile2_img.write(imageName+"\n")

                                for attribute in box.findall("attribute"):

                                    if attribute.get("name") == "hair":
                                        hair = attribute.text
                                        if hair == "short":
                                            short, long = 1,0
                                            head_hair_short += 1

                                        elif hair == "long":
                                            short, long = 0,1
                                            head_hair_long  += 1


                                    elif attribute.get("name") == "hat_red":
                                        hat_red = attribute.text
                                        hat_red = readBoodreturnInt(hat_red)
                                        head_hat_red += hat_red


                                    elif attribute.get("name") == "hat_yellow":
                                        hat_yellow = attribute.text
                                        hat_yellow = readBoodreturnInt(hat_yellow)
                                        head_hat_yellow += hat_yellow

                                    elif attribute.get("name") == "hat_green":
                                        hat_green = attribute.text
                                        hat_green = readBoodreturnInt(hat_green)
                                        head_hat_green += hat_green


                                    elif attribute.get("name") == "hat_blue":
                                        hat_blue = attribute.text
                                        hat_blue = readBoodreturnInt(hat_blue)
                                        head_hat_blue += hat_blue



                                    elif attribute.get("name") == "hat_brown":
                                        hat_brown = attribute.text
                                        hat_brown = readBoodreturnInt(hat_brown)
                                        head_hat_brown += hat_brown


                                    elif attribute.get("name") == "hat_pink":
                                        hat_pink = attribute.text
                                        hat_pink = readBoodreturnInt(hat_pink)
                                        head_hat_pink += hat_pink


                                    elif attribute.get("name") == "hat_grey":
                                        hat_grey = attribute.text
                                        hat_grey = readBoodreturnInt(hat_grey)
                                        head_hat_grey += hat_grey


                                    elif attribute.get("name") == "hat_black":
                                        hat_black = attribute.text
                                        hat_black = readBoodreturnInt(hat_black)
                                        head_hat_black += hat_black


                                    elif attribute.get("name") == "hat_white":
                                        hat_white = attribute.text
                                        hat_white = readBoodreturnInt(hat_white)
                                        head_hat_white += hat_white


                                    elif attribute.get("name") == "hat":
                                        hat = attribute.text
                                        if hat == "hatless":
                                            cap, nocap, nohat = 0,0,1
                                            head_hat_hatless += 1
                                            #어노테이터 실수 제거 코드.
                                            hat_red, hat_yellow, hat_green, hat_blue, hat_brown, hat_pink, hat_grey, hat_black, hat_white= 0,0,0,0,0,0,0,0,0

                                        elif hat == "cap":
                                            cap, nocap, nohat = 1,0,0
                                            head_hat_cap += 1


                                        elif hat == "brimmed" or  hat =="brimless" or hat == "helmat"or  hat == "hood" :
                                            cap, nocap, nohat = 0,1,0
                                            head_hat_nocap += 1

                                HEAD_classes = "{}{}{}{}{}{}{}{}{}{}{}{}{}{}".format(cap, nocap, nohat ,hat_red,hat_yellow,hat_green,hat_blue,hat_brown,hat_pink,hat_grey,hat_black,hat_white, short, long)
                                #classesHEad =                                                ['cap','visor','nonvisor','helmat','hood','nohat','hatdk','hatred','hatyellow','hatgreen','hatblue','hatbrown','hatpink','hatgray','hatblack','hatwhite','hatcolordk','shot','long','bald','hairdk']
                                headAttributeFile2.write(HEAD_classes+"\n")

                            elif label == "all":
                                xtl = int(float(box.get("xtl")))
                                ytl = int(float(box.get("ytl")))
                                xbr = int(float(box.get("xbr")))
                                ybr = int(float(box.get("ybr")))
                                xlen = abs(xtl-xbr)
                                ylen = abs(ytl-ybr)

                                img = (os.path.join(getImagePath(imageName)))
                                allAttributeFile2_img.write(imageName+"\n")

                                for attribute in box.findall("attribute"):
                                    if attribute.get("name") == "gender":
                                        gender = attribute.text
                                        if gender == "male":
                                            man, woman= 1,0
                                            all_gender_male += 1

                                        elif gender == "female":
                                            man, woman = 0,1
                                            all_gender_female += 1

                                    elif attribute.get("name") == "age":
                                        age = attribute.text
                                        if age == "20~70":
                                            infant,child,teenager,adult,oldperson = 0,0,0,1,0
                                            all_age_adult += 1


                                        elif age == "0~7":
                                            infant,child,teenager,adult,oldperson = 1,0,0,0,0
                                            all_age_infant += 1

                                        elif age == "8~13":
                                            infant,child,teenager,adult,oldperson = 0,1,0,0,0
                                            all_age_child += 1

                                        elif age == "14~19":
                                            infant,child,teenager,adult,oldperson = 0,0,1,0,0
                                            all_age_teenager += 1

                                        else: ## 70~
                                            infant,child,teenager,adult,oldperson = 0,0,0,0,1
                                            all_age_oldperson += 1


                                    elif attribute.get("name") == "bag_white":
                                        bag_white = attribute.text
                                        bag_white = readBoodreturnInt(bag_white)
                                        all_bag_white += bag_white


                                    elif attribute.get("name") == "bag_black":
                                        bag_black = attribute.text
                                        bag_black = readBoodreturnInt(bag_black)
                                        all_bag_black += bag_black


                                    elif attribute.get("name") == "bag_grey":
                                        bag_grey = attribute.text
                                        bag_grey = readBoodreturnInt(bag_grey)
                                        all_bag_grey += bag_grey


                                    elif attribute.get("name") == "bag_pink":
                                        bag_pink = attribute.text
                                        bag_pink = readBoodreturnInt(bag_pink)
                                        all_bag_pink += bag_pink


                                    elif attribute.get("name") == "bag_brown":
                                        bag_brown = attribute.text
                                        bag_brown = readBoodreturnInt(bag_brown)
                                        all_bag_brown += bag_brown


                                    elif attribute.get("name") == "bag_blue":
                                        bag_blue = attribute.text
                                        bag_blue = readBoodreturnInt(bag_blue)
                                        all_bag_blue += bag_blue


                                    elif attribute.get("name") == "bag_green":
                                        bag_green = attribute.text
                                        bag_green = readBoodreturnInt(bag_green)
                                        all_bag_green += bag_green


                                    elif attribute.get("name") == "bag_yellow":
                                        bag_yellow = attribute.text
                                        bag_yellow = readBoodreturnInt(bag_yellow)
                                        all_bag_yellow += bag_yellow


                                    elif attribute.get("name") == "bag_red":
                                        bag_red = attribute.text
                                        bag_red = readBoodreturnInt(bag_red)
                                        all_bag_red += bag_red

                                    elif attribute.get("name") == "plasticbag":
                                        plasticbag = attribute.text
                                        plasticbag = readBoodreturnInt(plasticbag)
                                        plasticbag=plasticbag

                                        all_plasticbag += plasticbag


                                    elif attribute.get("name") == "shoulderbag":
                                        shoulderbag = attribute.text
                                        shoulderbag = readBoodreturnInt(shoulderbag)
                                        shoulderbag=shoulderbag
                                        all_shoulderbag += shoulderbag

                                    elif attribute.get("name") == "handbag":
                                        handbag = attribute.text
                                        handbag = readBoodreturnInt(handbag)
                                        totebag = handbag
                                        all_handbag += handbag


                                    elif attribute.get("name") == "backpack":
                                        backpack = attribute.text
                                        backpack = readBoodreturnInt(backpack)
                                        all_backpack += backpack


                                    elif attribute.get("name") == "bagless":
                                        bagless = attribute.text
                                        bagless = readBoodreturnInt(bagless)
                                        bagnone = bagless
                                        all_bagless += bagless

                                    if (plasticbag or shoulderbag or totebag) ==1:
                                        nobackpack = 1
                                    else:
                                        nobackpack = 0


                                ALL_classes = "{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}".format(man,woman,infant,child,teenager,adult,oldperson,backpack,nobackpack,bagnone, bag_red, bag_yellow, bag_green, bag_blue, bag_brown, bag_pink, bag_grey, bag_black, bag_white)
                                allAttributeFile2.write(ALL_classes+"\n")

                            elif label == "upper":
                                xtl = int(float(box.get("xtl")))
                                ytl = int(float(box.get("ytl")))
                                xbr = int(float(box.get("xbr")))
                                ybr = int(float(box.get("ybr")))
                                xlen = abs(xtl-xbr)
                                ylen = abs(ytl-ybr)

                                img = (os.path.join(getImagePath(imageName)))

                                upperAttributeFile2_img.write(imageName+"\n")
                                for attribute in box.findall("attribute"):


                                    if attribute.get("name") == "top_white":
                                        top_white = attribute.text
                                        top_white = readBoodreturnInt(top_white)
                                        upper_top_white += top_white

                                    elif attribute.get("name") == "top_black":
                                        top_black = attribute.text
                                        top_black = readBoodreturnInt(top_black)
                                        upper_top_black += top_black


                                    elif attribute.get("name") == "top_grey":
                                        top_grey = attribute.text
                                        top_grey = readBoodreturnInt(top_grey)
                                        upper_top_grey += top_grey


                                    elif attribute.get("name") == "top_pink":
                                        top_pink = attribute.text
                                        top_pink = readBoodreturnInt(top_pink)
                                        upper_top_pink += top_pink

                                    elif attribute.get("name") == "top_brown":
                                        top_brown = attribute.text
                                        top_brown = readBoodreturnInt(top_brown)
                                        upper_top_brown += top_brown

                                    elif attribute.get("name") == "top_blue":
                                        top_blue = attribute.text
                                        top_blue = readBoodreturnInt(top_blue)
                                        upper_top_blue += top_blue


                                    elif attribute.get("name") == "top_green":
                                        top_green = attribute.text
                                        top_green = readBoodreturnInt(top_green)
                                        upper_top_green += top_green


                                    elif attribute.get("name") == "top_yellow":
                                        top_yellow = attribute.text
                                        top_yellow = readBoodreturnInt(top_yellow)
                                        upper_top_yellow += top_yellow


                                    elif attribute.get("name") == "top_red":
                                        top_red = attribute.text
                                        top_red = readBoodreturnInt(top_red)
                                        upper_top_red += top_red


                                    elif attribute.get("name") == "top":
                                        top = attribute.text
                                        if top == "long_sleeve":
                                            long_sleeve, short_sleeve = 1,0
                                            upper_top_long_sleeve += 1

                                        elif top == "short_sleeve":
                                            long_sleeve, short_sleeve= 0,1
                                            upper_top_short_sleeve += 1

                                        longshirt = long_sleeve
                                        shortshirt = short_sleeve

                                UPPER_classes = "{}{}{}{}{}{}{}{}{}{}{}".format(longshirt,shortshirt, top_red,top_yellow,top_green,top_blue,top_brown,top_pink,top_grey,top_black,top_white)
                                upperAttributeFile2.write(UPPER_classes+"\n")

                            elif label == "lower":
                                xtl = int(float(box.get("xtl")))
                                ytl = int(float(box.get("ytl")))
                                xbr = int(float(box.get("xbr")))
                                ybr = int(float(box.get("ybr")))
                                xlen = abs(xtl-xbr)
                                ylen = abs(ytl-ybr)

                                img = (os.path.join(getImagePath(imageName)))
                                lowerAttributeFile2_img.write(imageName+"\n")

                                for attribute in box.findall("attribute"):

                                    if attribute.get("name") == "bottom_white":
                                        bottom_white = attribute.text
                                        bottom_white = readBoodreturnInt(bottom_white)
                                        lower_bottom_white += bottom_white


                                    elif attribute.get("name") == "bottom_black":
                                        bottom_black = attribute.text
                                        bottom_black = readBoodreturnInt(bottom_black)
                                        lower_bottom_black += bottom_black


                                    elif attribute.get("name") == "bottom_grey":
                                        bottom_grey = attribute.text
                                        bottom_grey = readBoodreturnInt(bottom_grey)
                                        lower_bottom_grey += bottom_grey


                                    elif attribute.get("name") == "bottom_pink":
                                        bottom_pink = attribute.text
                                        bottom_pink = readBoodreturnInt(bottom_pink)
                                        lower_bottom_pink += bottom_pink

                                    elif attribute.get("name") == "bottom_brown":
                                        bottom_brown = attribute.text
                                        bottom_brown = readBoodreturnInt(bottom_brown)
                                        lower_bottom_brown += bottom_brown


                                    elif attribute.get("name") == "bottom_blue":
                                        bottom_blue = attribute.text
                                        bottom_blue = readBoodreturnInt(bottom_blue)
                                        lower_bottom_blue += bottom_blue


                                    elif attribute.get("name") == "bottom_green":
                                        bottom_green = attribute.text
                                        bottom_green = readBoodreturnInt(bottom_green)
                                        lower_bottom_green += bottom_green


                                    elif attribute.get("name") == "bottom_yellow":
                                        bottom_yellow = attribute.text
                                        bottom_yellow = readBoodreturnInt(bottom_yellow)
                                        lower_bottom_yellow += bottom_yellow


                                    elif attribute.get("name") == "bottom_red":
                                        bottom_red = attribute.text
                                        bottom_red = readBoodreturnInt(bottom_red)
                                        lower_bottom_red += bottom_red


                                    elif attribute.get("name") == "bottom":
                                        bottom = attribute.text
                                        if bottom == "long_pants":
                                            long_pants, short_pants, long_skirt, short_skirt = 1,0,0,0
                                            lower_bottom_long_pants += 1

                                        elif bottom == "short_pants":
                                            long_pants, short_pants, long_skirt, short_skirt = 0,1,0,0
                                            lower_bottom_short_pants += 1

                                        elif bottom == "long_skirt":
                                            long_pants, short_pants, long_skirt, short_skirt= 0,0,1,0
                                            lower_bottom_long_skirt += 1

                                        elif bottom == "short_skirt":
                                            long_pants, short_pants, long_skirt, short_skirt = 0,0,0,1
                                            lower_bottom_short_skirt += 1



                                    elif attribute.get("name") == "shoes_color":
                                        shoes_color = attribute.text
                                        if shoes_color == "shoes_red":
                                            shoes_red, shoes_yellow, shoes_green, shoes_blue, shoes_brown, shoes_pink, shoes_grey, shoes_black, shoes_white = 1,0,0,0,0,0,0,0,0
                                            lower_shoes_red += 1

                                        elif shoes_color == "shoes_yellow":
                                            shoes_red, shoes_yellow, shoes_green, shoes_blue, shoes_brown, shoes_pink, shoes_grey, shoes_black, shoes_white= 0,1,0,0,0,0,0,0,0
                                            lower_shoes_yellow += 1

                                        elif shoes_color == "shoes_green":
                                            shoes_red, shoes_yellow, shoes_green, shoes_blue, shoes_brown, shoes_pink, shoes_grey, shoes_black, shoes_white= 0,0,1,0,0,0,0,0,0
                                            lower_shoes_green += 1

                                        elif shoes_color == "shoes_blue":
                                            shoes_red, shoes_yellow, shoes_green, shoes_blue, shoes_brown, shoes_pink, shoes_grey, shoes_black, shoes_white = 0,0,0,1,0,0,0,0,0
                                            lower_shoes_blue += 1

                                        elif shoes_color == "shoes_brown":
                                            shoes_red, shoes_yellow, shoes_green, shoes_blue, shoes_brown, shoes_pink, shoes_grey, shoes_black, shoes_white = 0,0,0,0,1,0,0,0,0
                                            lower_shoes_brown += 1

                                        elif shoes_color == "shoes_pink":
                                            shoes_red, shoes_yellow, shoes_green, shoes_blue, shoes_brown, shoes_pink, shoes_grey, shoes_black, shoes_white = 0,0,0,0,0,1,0,0,0
                                            lower_shoes_pink += 1

                                        elif shoes_color == "shoes_grey":
                                            shoes_red, shoes_yellow, shoes_green, shoes_blue, shoes_brown, shoes_pink, shoes_grey, shoes_black, shoes_white = 0,0,0,0,0,0,1,0,0
                                            lower_shoes_grey += 1

                                        elif shoes_color == "shoes_black":
                                            shoes_red, shoes_yellow, shoes_green, shoes_blue, shoes_brown, shoes_pink, shoes_grey, shoes_black, shoes_white = 0,0,0,0,0,0,0,1,0
                                            lower_shoes_black += 1

                                        elif shoes_color == "shoes_white":
                                            shoes_red, shoes_yellow, shoes_green, shoes_blue, shoes_brown, shoes_pink, shoes_grey, shoes_black, shoes_white = 0,0,0,0,0,0,0,0,1
                                            lower_shoes_white += 1


                                LOWER_classes = "{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}".format(long_pants, short_pants, long_skirt, short_skirt, bottom_red, bottom_yellow, bottom_green, bottom_blue, bottom_brown, bottom_pink, bottom_grey, bottom_black, bottom_white,shoes_red, shoes_yellow, shoes_green, shoes_blue, shoes_brown, shoes_pink, shoes_grey, shoes_black, shoes_white)
                                lowerAttributeFile2.write(LOWER_classes+"\n")

                            else:
                                if ONLY_MAKE_DOCUMENTS == False:
                                    print(label)


make83class()
make66class()
