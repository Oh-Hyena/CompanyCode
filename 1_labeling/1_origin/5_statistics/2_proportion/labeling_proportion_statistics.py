import numpy as np
import os
import xml.etree.ElementTree as ET
from xml.dom import minidom
import pandas as pd
import cv2
import time
import random
import shutil

start_time = time.time()
#originalxml
cvatxmlRootpath=r"D:\HN_code\test\1_labeling\16_7class_object_proportion_statistics\1_6class_data_process\class6_xml"
classes=['person','car','bus','truck','unknown car','bicycle','motorbike']
condition=['low','mid','high']
shape=['width','height']

# 무슨 경로인지 모르겠음
move_xml_path=r"D:\HN_code\test\1_labeling\16_7class_object_proportion_statistics\2_move_xml"

###############조건 지정 부분####################################
class_list = [] # 조건 지정 ex) bus, mid , height , count
result_list = [] # class_list의 토탈

#bicycle
class_list.append([classes[5],condition[0],shape[0],0])
class_list.append([classes[5],condition[1],shape[0],0])
class_list.append([classes[5],condition[2],shape[0],0])

# # # # #motorbike
class_list.append([classes[6],condition[0],shape[1],0])
class_list.append([classes[6],condition[1],shape[1],0])
class_list.append([classes[6],condition[2],shape[1],0])

# # # # #bus
class_list.append([classes[2],condition[0],shape[0],0])
class_list.append([classes[2],condition[1],shape[0],0])
class_list.append([classes[2],condition[2],shape[0],0])

# # #unknowncar
class_list.append([classes[4],condition[0],shape[0],0])
class_list.append([classes[4],condition[1],shape[0],0])
class_list.append([classes[4],condition[2],shape[0],0])


# # #truck-width-mid-3만
class_list.append([classes[3],condition[0],shape[0],0])
class_list.append([classes[3],condition[1],shape[0],0])
class_list.append([classes[3],condition[2],shape[0],0])

##person-height-hight-25만
class_list.append([classes[0],condition[0],shape[1],0])
class_list.append([classes[0],condition[1],shape[1],0])
class_list.append([classes[0],condition[2],shape[1],0])

##car -width-mid-30만
class_list.append([classes[1],condition[0],shape[0],0])
class_list.append([classes[1],condition[1],shape[0],0])
class_list.append([classes[1],condition[2],shape[0],0])


for i in range (len(class_list)):
    result_list.append(class_list[i])
#print(total_list)

############################init##########################################
path=[]
bus_result=0
car_result=0
person_result=0
truck_result=0
unknown_result=0
bicycle_result=0
motorbike_result=0

condition_car_width=[]
condition_car_height=[]
condition_person_width=[]
condition_person_height=[]
condition_bus_width=[]
condition_bus_height=[]
condition_truck_width=[]
condition_truck_height=[]
condition_unknown_width=[]
condition_unknown_height=[]
condition_bicycle_width=[]
condition_bicycle_height=[]
condition_motorbike_width=[]
condition_motorbike_height=[]

person_count=0
car_count=0
bus_count=0
truck_count=0
unknown_count=0
bicycle_count=0
motorbike_count=0
bicycle_confirm=[]
total_car=0
total_person=0
total_bus=0
total_truck=0
total_unknown=0
total_bicycle=0
total_motorbike=0
bus_Height=[]
bicycle_result_confirm=[]
bicycle_result_path=[]
person_result_path=[]
car_result_path=[]
bus_result_path=[]
truck_result_path=[]
motorbike_result_path=[]
unknown_result_path=[]
pathname=[]
result_path=[]
result_name=[]
result_only_path=[]

#xml list를 읽어서 통계
def statistics(result_final):
    #global person_height_100_count,person_height_100_200_count,person_height_200_300_count,person_height_300_400_count,person_height_400_600_count,person_height_600_count
    person_height_100_count=0
    person_height_100_200_count=0
    person_height_200_300_count=0
    person_height_300_400_count=0
    person_height_400_600_count=0
    person_height_600_count=0

    global person_width_100_count,person_width_100_150_count,person_width_150_200_count,person_width_200_300_count,person_width_300_600_count,person_width_600_count
    person_width_100_count=0
    person_width_100_150_count=0
    person_width_150_200_count=0
    person_width_200_300_count=0
    person_width_300_600_count=0
    person_width_600_count=0

    global car_height_100_count,car_height_100_200_count,car_height_200_300_count,car_height_300_400_count,car_height_400_600_count,car_height_600_count
    car_height_100_count=0
    car_height_100_200_count=0
    car_height_200_300_count=0
    car_height_300_400_count=0
    car_height_400_600_count=0
    car_height_600_count=0

    global car_width_100_count,car_width_100_150_count,car_width_150_200_count,car_width_200_300_count,car_width_300_600_count,car_width_600_count
    car_width_100_count=0
    car_width_100_150_count=0
    car_width_150_200_count=0
    car_width_200_300_count=0
    car_width_300_600_count=0
    car_width_600_count=0

    global bus_height_100_count,bus_height_100_200_count,bus_height_200_300_count,bus_height_300_400_count,bus_height_400_600_count,bus_height_600_count
    bus_height_100_count=0
    bus_height_100_200_count=0
    bus_height_200_300_count=0
    bus_height_300_400_count=0
    bus_height_400_600_count=0
    bus_height_600_count=0

    global bus_width_100_count,bus_width_100_150_count,bus_width_150_200_count,bus_width_200_300_count,bus_width_300_600_count,bus_width_600_count
    bus_width_100_count=0
    bus_width_100_150_count=0
    bus_width_150_200_count=0
    bus_width_200_300_count=0
    bus_width_300_600_count=0
    bus_width_600_count=0

    global truck_height_100_count,truck_height_100_200_count,truck_height_200_300_count,truck_height_300_400_count,truck_height_400_600_count,truck_height_600_count
    truck_height_100_count=0
    truck_height_100_200_count=0
    truck_height_200_300_count=0
    truck_height_300_400_count=0
    truck_height_400_600_count=0
    truck_height_600_count=0

    global truck_width_100_count,truck_width_100_150_count,truck_width_150_200_count,truck_width_200_300_count,truck_width_300_600_count,truck_width_600_count
    truck_width_100_count=0
    truck_width_100_150_count=0
    truck_width_150_200_count=0
    truck_width_200_300_count=0
    truck_width_300_600_count=0
    truck_width_600_count=0

    global unknowncar_height_100_count,unknowncar_height_100_200_count,unknowncar_height_200_300_count,unknowncar_height_300_400_count,unknowncar_height_400_600_count,unknowncar_height_600_count
    unknowncar_height_100_count=0
    unknowncar_height_100_200_count=0
    unknowncar_height_200_300_count=0
    unknowncar_height_300_400_count=0
    unknowncar_height_400_600_count=0
    unknowncar_height_600_count=0

    global unknowncar_width_100_count,unknowncar_width_100_150_count,unknowncar_width_150_200_count,unknowncar_width_200_300_count,unknowncar_width_300_600_count,unknowncar_width_600_count
    unknowncar_width_100_count=0
    unknowncar_width_100_150_count=0
    unknowncar_width_150_200_count=0
    unknowncar_width_200_300_count=0
    unknowncar_width_300_600_count=0
    unknowncar_width_600_count=0

    global bicycle_height_100_count,bicycle_height_100_200_count,bicycle_height_200_300_count,bicycle_height_300_400_count,bicycle_height_400_600_count,bicycle_height_600_count
    bicycle_height_100_count=0
    bicycle_height_100_200_count=0
    bicycle_height_200_300_count=0
    bicycle_height_300_400_count=0
    bicycle_height_400_600_count=0
    bicycle_height_600_count=0

    global bicycle_width_100_count,bicycle_width_100_150_count,bicycle_width_150_200_count,bicycle_width_200_300_count,bicycle_width_300_600_count,bicycle_width_600_count
    bicycle_width_100_count=0
    bicycle_width_100_150_count=0
    bicycle_width_150_200_count=0
    bicycle_width_200_300_count=0
    bicycle_width_300_600_count=0
    bicycle_width_600_count=0

    global motorbike_height_100_count,motorbike_height_100_200_count,motorbike_height_200_300_count,motorbike_height_300_400_count,motorbike_height_400_600_count,motorbike_height_600_count
    motorbike_height_100_count=0
    motorbike_height_100_200_count=0
    motorbike_height_200_300_count=0
    motorbike_height_300_400_count=0
    motorbike_height_400_600_count=0
    motorbike_height_600_count=0

    global motorbike_width_100_count,motorbike_width_100_150_count,motorbike_width_150_200_count,motorbike_width_200_300_count,motorbike_width_300_600_count,motorbike_width_600_count
    motorbike_width_100_count=0
    motorbike_width_100_150_count=0
    motorbike_width_150_200_count=0
    motorbike_width_200_300_count=0
    motorbike_width_300_600_count=0
    motorbike_width_600_count=0

    ex_list=list(set(result_final))
    #print("xml_count",len(ex_list))
    for cvatxml in ex_list:
        if cvatxml.endswith(".xml"):
            #print(cvatxml)
            tree = ET.parse(cvatxml)
            note = tree.getroot()
            for child in note.findall('object'):
                name = child.find('name').text
                if name  == "car":

                    name = child.find('name').text
                    bndbox = child.find('bndbox')
                    xmin = int(float(bndbox.find('xmin').text))
                    ymin = int(float(bndbox.find('ymin').text))
                    xmax = int(float(bndbox.find('xmax').text))
                    ymax = int(float(bndbox.find('ymax').text))
                    car_width = (abs(xmin-xmax))
                    car_height = (abs(ymin-ymax))

                    condition_car_width.append(car_width)
                    condition_car_height.append(car_height)
                if name  == "person":

                    name = child.find('name').text
                    bndbox = child.find('bndbox')
                    xmin = int(float(bndbox.find('xmin').text))
                    ymin = int(float(bndbox.find('ymin').text))
                    xmax = int(float(bndbox.find('xmax').text))
                    ymax = int(float(bndbox.find('ymax').text))
                    person_width = abs(xmin-xmax)
                    person_height = abs(ymin-ymax)
                    condition_person_width.append(person_width)
                    condition_person_height.append(person_height)

                if name  == "truck":

                    name = child.find('name').text
                    bndbox = child.find('bndbox')
                    xmin = int(float(bndbox.find('xmin').text))
                    ymin = int(float(bndbox.find('ymin').text))
                    xmax = int(float(bndbox.find('xmax').text))
                    ymax = int(float(bndbox.find('ymax').text))
                    truck_width = abs(xmin-xmax)
                    truck_height = abs(ymin-ymax)
                    condition_truck_width.append(truck_width)
                    condition_truck_height.append(truck_height)

                if name  == "bus":

                    name = child.find('name').text
                    bndbox = child.find('bndbox')
                    xmin = int(float(bndbox.find('xmin').text))
                    ymin = int(float(bndbox.find('ymin').text))
                    xmax = int(float(bndbox.find('xmax').text))
                    ymax = int(float(bndbox.find('ymax').text))
                    bus_width = abs(xmin-xmax)
                    bus_height = abs(ymin-ymax)
                    condition_bus_width.append(bus_width)
                    condition_bus_height.append(bus_height)

                if name  == "unknown car" or name == "excavator" or name == "forklift" or name == "ladder truck":

                    name = child.find('name').text
                    bndbox = child.find('bndbox')
                    xmin = int(float(bndbox.find('xmin').text))
                    ymin = int(float(bndbox.find('ymin').text))
                    xmax = int(float(bndbox.find('xmax').text))
                    ymax = int(float(bndbox.find('ymax').text))
                    unknown_width = abs(xmin-xmax)
                    unknown_height = abs(ymin-ymax)
                    condition_unknown_width.append(unknown_width)
                    condition_unknown_height.append(unknown_height)

                if name  == "bicycle":

                    name = child.find('name').text
                    bndbox = child.find('bndbox')
                    xmin = int(float(bndbox.find('xmin').text))
                    ymin = int(float(bndbox.find('ymin').text))
                    xmax = int(float(bndbox.find('xmax').text))
                    ymax = int(float(bndbox.find('ymax').text))
                    bicycle_width = abs(xmin-xmax)
                    bicycle_height = abs(ymin-ymax)
                    condition_bicycle_width.append(bicycle_width)
                    condition_bicycle_height.append(bicycle_height)

                if name  == "motorbike":

                    name = child.find('name').text
                    bndbox = child.find('bndbox')
                    xmin = int(float(bndbox.find('xmin').text))
                    ymin = int(float(bndbox.find('ymin').text))
                    xmax = int(float(bndbox.find('xmax').text))
                    ymax = int(float(bndbox.find('ymax').text))
                    motorbike_width = abs(xmin-xmax)
                    motorbike_height = abs(ymin-ymax)
                    condition_motorbike_width.append(motorbike_width)
                    condition_motorbike_height.append(motorbike_height)
    for i in range(len(condition_person_height)):
        if (condition_person_height[i] <100):
            person_height_100_count+=1
        elif ((condition_person_height[i]>=100) & (condition_person_height[i]<200)):
            person_height_100_200_count+=1
        elif ((condition_person_height[i]>=200) & (condition_person_height[i]<300)):
            person_height_200_300_count+=1
        elif ((condition_person_height[i]>=300) & (condition_person_height[i]<400)):
            person_height_300_400_count+=1
        elif ((condition_person_height[i]>=400) & (condition_person_height[i]<=600)):
            person_height_400_600_count+=1
        elif (condition_person_height[i]>600):
            person_height_600_count+=1


        if (condition_person_width[i]<100):
            person_width_100_count+=1
        elif ((condition_person_width[i]>=100) & (condition_person_width[i]<150)):
            person_width_100_150_count+=1
        elif ((condition_person_width[i]>=150) & (condition_person_width[i]<200)):
            person_width_150_200_count+=1
        elif ((condition_person_width[i]>=200) & (condition_person_width[i]<300)):
            person_width_200_300_count+=1
        elif ((condition_person_width[i]>=300) & (condition_person_width[i]<600)):
            person_width_300_600_count+=1
        elif (condition_person_width[i]>=600):
            person_width_600_count+=1

    for i in range(len(condition_car_height)):
        if (condition_car_height[i] <100):
            car_height_100_count+=1
        elif ((condition_car_height[i]>=100) & (condition_car_height[i]<200)):
            car_height_100_200_count+=1
        elif ((condition_car_height[i]>=200) & (condition_car_height[i]<300)):
            car_height_200_300_count+=1
        elif ((condition_car_height[i]>=300) & (condition_car_height[i]<400)):
            car_height_300_400_count+=1
        elif ((condition_car_height[i]>=400) & (condition_car_height[i]<=600)):
            car_height_400_600_count+=1
        elif (condition_car_height[i]>600):
            car_height_600_count+=1


        if (condition_car_width[i]<100):
            car_width_100_count+=1
        elif ((condition_car_width[i]>=100) & (condition_car_width[i]<150)):
            car_width_100_150_count+=1
        elif ((condition_car_width[i]>=150) & (condition_car_width[i]<200)):
            car_width_150_200_count+=1
        elif ((condition_car_width[i]>=200) & (condition_car_width[i]<300)):
            car_width_200_300_count+=1
        elif ((condition_car_width[i]>=300) & (condition_car_width[i]<=600)):
            car_width_300_600_count+=1
        elif (condition_car_width[i]>600):
            car_width_600_count+=1


    for i in range(len(condition_bus_height)):
        if (condition_bus_height[i] <100):
            bus_height_100_count+=1
        elif ((condition_bus_height[i]>=100) & (condition_bus_height[i]<200)):
            bus_height_100_200_count+=1
        elif ((condition_bus_height[i]>=200) & (condition_bus_height[i]<300)):
            bus_height_200_300_count+=1
        elif ((condition_bus_height[i]>=300) & (condition_bus_height[i]<400)):
            bus_height_300_400_count+=1
        elif ((condition_bus_height[i]>=400) & (condition_bus_height[i]<=600)):
            bus_height_400_600_count+=1
        elif (condition_bus_height[i]>600):
            bus_height_600_count+=1


        if (condition_bus_width[i]<100):
            bus_width_100_count+=1
        elif ((condition_bus_width[i]>=100) & (condition_bus_width[i]<150)):
            bus_width_100_150_count+=1
        elif ((condition_bus_width[i]>=150) & (condition_bus_width[i]<200)):
            bus_width_150_200_count+=1
        elif ((condition_bus_width[i]>=200) & (condition_bus_width[i]<300)):
            bus_width_200_300_count+=1
        elif ((condition_bus_width[i]>=300) & (condition_bus_width[i]<=600)):
            bus_width_300_600_count+=1
        elif (condition_bus_width[i]>600):
            bus_width_600_count+=1

    for i in range(len(condition_truck_height)):
        if (condition_truck_height[i] <100):
            truck_height_100_count+=1
        elif ((condition_truck_height[i]>=100) & (condition_truck_height[i]<200)):
            truck_height_100_200_count+=1
        elif ((condition_truck_height[i]>=200) & (condition_truck_height[i]<300)):
            truck_height_200_300_count+=1
        elif ((condition_truck_height[i]>=300) & (condition_truck_height[i]<400)):
            truck_height_300_400_count+=1
        elif ((condition_truck_height[i]>=400) & (condition_truck_height[i]<=600)):
            truck_height_400_600_count+=1
        elif (condition_truck_height[i]>600):
            truck_height_600_count+=1


        if (condition_truck_width[i]<100):
            truck_width_100_count+=1
        elif ((condition_truck_width[i]>=100) & (condition_truck_width[i]<150)):
            truck_width_100_150_count+=1
        elif ((condition_truck_width[i]>=150) & (condition_truck_width[i]<200)):
            truck_width_150_200_count+=1
        elif ((condition_truck_width[i]>=200) & (condition_truck_width[i]<300)):
            truck_width_200_300_count+=1
        elif ((condition_truck_width[i]>=300) & (condition_truck_width[i]<=600)):
            truck_width_300_600_count+=1
        elif (condition_truck_width[i]>600):
            truck_width_600_count+=1

    for i in range(len(condition_unknown_height)):
        if (condition_unknown_height[i] <100):
            unknowncar_height_100_count+=1
        elif ((condition_unknown_height[i]>=100) & (condition_unknown_height[i]<200)):
            unknowncar_height_100_200_count+=1
        elif ((condition_unknown_height[i]>=200) & (condition_unknown_height[i]<300)):
            unknowncar_height_200_300_count+=1
        elif ((condition_unknown_height[i]>=300) & (condition_unknown_height[i]<400)):
            unknowncar_height_300_400_count+=1
        elif ((condition_unknown_height[i]>=400) & (condition_unknown_height[i]<=600)):
            unknowncar_height_400_600_count+=1
        elif (condition_unknown_height[i]>600):
            unknowncar_height_600_count+=1


        if (condition_unknown_width[i]<100):
            unknowncar_width_100_count+=1
        elif ((condition_unknown_width[i]>=100) & (condition_unknown_width[i]<150)):
            unknowncar_width_100_150_count+=1
        elif ((condition_unknown_width[i]>=150) & (condition_unknown_width[i]<200)):
            unknowncar_width_150_200_count+=1
        elif ((condition_unknown_width[i]>=200) & (condition_unknown_width[i]<300)):
            unknowncar_width_200_300_count+=1
        elif ((condition_unknown_width[i]>=300) & (condition_unknown_width[i]<=600)):
            unknowncar_width_300_600_count+=1
        elif (condition_unknown_width[i]>600):
            unknowncar_width_600_count+=1

    for i in range(len(condition_bicycle_height)):
        if (condition_bicycle_height[i] <100):
            bicycle_height_100_count+=1
        elif ((condition_bicycle_height[i]>=100) & (condition_bicycle_height[i]<200)):
            bicycle_height_100_200_count+=1
        elif ((condition_bicycle_height[i]>=200) & (condition_bicycle_height[i]<300)):
            bicycle_height_200_300_count+=1
        elif ((condition_bicycle_height[i]>=300) & (condition_bicycle_height[i]<400)):
            bicycle_height_300_400_count+=1
        elif ((condition_bicycle_height[i]>=400) & (condition_bicycle_height[i]<=600)):
            bicycle_height_400_600_count+=1
        elif (condition_bicycle_height[i]>600):
            bicycle_height_600_count+=1


        if (condition_bicycle_width[i]<100):
            bicycle_width_100_count+=1
        elif ((condition_bicycle_width[i]>=100) & (condition_bicycle_width[i]<150)):
            bicycle_width_100_150_count+=1
        elif ((condition_bicycle_width[i]>=150) & (condition_bicycle_width[i]<200)):
            bicycle_width_150_200_count+=1
        elif ((condition_bicycle_width[i]>=200) & (condition_bicycle_width[i]<300)):
            bicycle_width_200_300_count+=1
        elif ((condition_bicycle_width[i]>=300) & (condition_bicycle_width[i]<=600)):
            bicycle_width_300_600_count+=1
        elif (condition_bicycle_width[i]>600):
            bicycle_width_600_count+=1

    for i in range(len(condition_motorbike_height)):
        if (condition_motorbike_height[i] <100):
            motorbike_height_100_count+=1
        elif ((condition_motorbike_height[i]>=100) & (condition_motorbike_height[i]<200)):
            motorbike_height_100_200_count+=1
        elif ((condition_motorbike_height[i]>=200) & (condition_motorbike_height[i]<300)):
            motorbike_height_200_300_count+=1
        elif ((condition_motorbike_height[i]>=300) & (condition_motorbike_height[i]<400)):
            motorbike_height_300_400_count+=1
        elif ((condition_motorbike_height[i]>=400) & (condition_motorbike_height[i]<=600)):
            motorbike_height_400_600_count+=1
        elif (condition_motorbike_height[i]>600):
            motorbike_height_600_count+=1


        if (condition_motorbike_width[i]<100):
            motorbike_width_100_count+=1
        elif ((condition_motorbike_width[i]>=100) & (condition_motorbike_width[i]<150)):
            motorbike_width_100_150_count+=1
        elif ((condition_motorbike_width[i]>=150) & (condition_motorbike_width[i]<200)):
            motorbike_width_150_200_count+=1
        elif ((condition_motorbike_width[i]>=200) & (condition_motorbike_width[i]<300)):
            motorbike_width_200_300_count+=1
        elif ((condition_motorbike_width[i]>=300) & (condition_motorbike_width[i]<=600)):
            motorbike_width_300_600_count+=1
        elif (condition_motorbike_width[i]>600):
            motorbike_width_600_count+=1

    person_height_high_count=person_height_200_300_count+person_height_300_400_count+person_height_400_600_count+person_height_600_count
    person_width_high_count=person_width_150_200_count+person_width_200_300_count+person_width_300_600_count+person_width_600_count
    car_height_high_count=car_height_200_300_count+car_height_300_400_count+car_height_400_600_count+car_height_600_count
    car_width_high_count=car_width_150_200_count+car_width_200_300_count+car_width_300_600_count+car_width_600_count
    bus_height_high_count=bus_height_200_300_count+bus_height_300_400_count+bus_height_400_600_count+bus_height_600_count
    bus_width_high_count=bus_width_150_200_count+bus_width_200_300_count+bus_width_300_600_count+bus_width_600_count
    truck_height_high_count=truck_height_200_300_count+truck_height_300_400_count+truck_height_400_600_count+truck_height_600_count
    truck_width_high_count=truck_width_150_200_count+truck_width_200_300_count+truck_width_300_600_count+truck_width_600_count
    unknowncar_height_high_count=unknowncar_height_200_300_count+unknowncar_height_300_400_count+unknowncar_height_400_600_count+unknowncar_height_600_count
    unknowncar_width_high_count=unknowncar_width_150_200_count+unknowncar_width_200_300_count+unknowncar_width_300_600_count+unknowncar_width_600_count
    bicycle_height_high_count=bicycle_height_200_300_count+bicycle_height_300_400_count+bicycle_height_400_600_count+bicycle_height_600_count
    bicycle_width_high_count=bicycle_width_150_200_count+bicycle_width_200_300_count+bicycle_width_300_600_count+bicycle_width_600_count
    motorbike_height_high_count=motorbike_height_200_300_count+motorbike_height_300_400_count+motorbike_height_400_600_count+motorbike_height_600_count
    motorbike_width_high_count=motorbike_width_150_200_count+motorbike_width_200_300_count+motorbike_width_300_600_count+motorbike_width_600_count

    print('--------------------------------------------------------------------------------')
    print('person_height_low: %s' %person_height_100_count)
    print('person_height_mid: %s' %person_height_100_200_count)
    print('person_height_high: %s' %person_height_high_count)
    print('person_height_200_300_count: %s' %person_height_200_300_count)
    print('person_height_300_400_count: %s' %person_height_300_400_count)
    print('person_height_400_600_count: %s' %person_height_400_600_count)
    print('person_height_600_count: %s' %person_height_600_count)
    print('--------------------------------------------------------------------------------')

    print('person_width_low: %s' %person_width_100_count)
    print('person_width_mid: %s' %person_width_100_150_count)
    print('person_width_high: %s' %person_width_high_count)
    print('person_width_150_200_count: %s' %person_width_150_200_count)
    print('person_width_200_300_count: %s' %person_width_200_300_count)
    print('person_width_300_600_count: %s' %person_width_300_600_count)
    print('person_width_600_count: %s' %person_width_600_count)
    print('--------------------------------------------------------------------------------')

    print('car_height_low: %s' %car_height_100_count)
    print('car_height_mid: %s' %car_height_100_200_count)
    print('car_height_high: %s' %car_height_high_count)
    print('car_height_200_300_count: %s' %car_height_200_300_count)
    print('car_height_300_400_count: %s' %car_height_300_400_count)
    print('car_height_400_600_count: %s' %car_height_400_600_count)
    print('car_height_600_count: %s' %car_height_600_count)

    print('--------------------------------------------------------------------------------')
    print('car_width_low: %s' %car_width_100_count)
    print('car_width_mid: %s' %car_width_100_150_count)
    print('car_width_high: %s' %car_width_high_count)
    print('car_width_150_200_count: %s' %car_width_150_200_count)
    print('car_width_200_300_count: %s' %car_width_200_300_count)
    print('car_width_300_600_count: %s' %car_width_300_600_count)
    print('car_width_600_count: %s' %car_width_600_count)
    print('--------------------------------------------------------------------------------')

    print('bus_height_low: %s' %bus_height_100_count)
    print('bus_height_mid: %s' %bus_height_100_200_count)
    print('bus_height_high: %s' %bus_height_high_count)
    print('bus_height_200_300_count: %s' %bus_height_200_300_count)
    print('bus_height_300_400_count: %s' %bus_height_300_400_count)
    print('bus_height_400_600_count: %s' %bus_height_400_600_count)
    print('bus_height_600_count: %s' %bus_height_600_count)

    print('--------------------------------------------------------------------------------')
    print('bus_width_low: %s' %bus_width_100_count)
    print('bus_width_mid: %s' %bus_width_100_150_count)
    print('bus_width_high: %s'%bus_width_high_count)
    print('bus_width_150_200_count: %s' %bus_width_150_200_count)
    print('bus_width_200_300_count: %s' %bus_width_200_300_count)
    print('bus_width_300_600_count: %s' %bus_width_300_600_count)
    print('bus_width_600_count: %s' %bus_width_600_count)
    print('--------------------------------------------------------------------------------')

    print('truck_height_low: %s' %truck_height_100_count)
    print('truck_height_mid: %s' %truck_height_100_200_count)
    print('truck_height_high: %s' %truck_height_high_count)
    print('truck_height_200_300_count: %s' %truck_height_200_300_count)
    print('truck_height_300_400_count: %s' %truck_height_300_400_count)
    print('truck_height_400_600_count: %s' %truck_height_400_600_count)
    print('truck_height_600_count: %s' %truck_height_600_count)

    print('--------------------------------------------------------------------------------')
    print('truck_width_low: %s' %truck_width_100_count)
    print('truck_width_mid: %s' %truck_width_100_150_count)
    print('truck_width_high: %s' %truck_width_high_count)
    print('truck_width_150_200_count: %s' %truck_width_150_200_count)
    print('truck_width_200_300_count: %s' %truck_width_200_300_count)
    print('truck_width_300_600_count: %s' %truck_width_300_600_count)
    print('truck_width_600_count: %s' %truck_width_600_count)
    print('--------------------------------------------------------------------------------')


    print('unknowncar_height_low: %s' %unknowncar_height_100_count)
    print('unknowncar_height_mid: %s' %unknowncar_height_100_200_count)
    print('unknowncar_height_high: %s' %unknowncar_height_high_count)
    print('unknowncar_height_200_300_count: %s' %unknowncar_height_200_300_count)
    print('unknowncar_height_300_400_count: %s' %unknowncar_height_300_400_count)
    print('unknowncar_height_400_600_count: %s' %unknowncar_height_400_600_count)
    print('unknowncar_height_600_count: %s' %unknowncar_height_600_count)

    print('--------------------------------------------------------------------------------')
    print('unknowncar_width_low: %s' %unknowncar_width_100_count)
    print('unknowncar_width_mid: %s' %unknowncar_width_100_150_count)
    print('unknowncar_width_high: %s' %unknowncar_width_high_count)
    print('unknowncar_width_150_200_count: %s' %unknowncar_width_150_200_count)
    print('unknowncar_width_200_300_count: %s' %unknowncar_width_200_300_count)
    print('unknowncar_width_300_600_count: %s' %unknowncar_width_300_600_count)
    print('unknowncar_width_600_count: %s' %unknowncar_width_600_count)
    print('--------------------------------------------------------------------------------')


    print('bicycle_height_low: %s' %bicycle_height_100_count)
    print('bicycle_height_mid: %s' %bicycle_height_100_200_count)
    print('bicycle_height_high: %s'%bicycle_height_high_count)
    print('bicycle_height_200_300_count: %s' %bicycle_height_200_300_count)
    print('bicycle_height_300_400_count: %s' %bicycle_height_300_400_count)
    print('bicycle_height_400_600_count: %s' %bicycle_height_400_600_count)
    print('bicycle_height_600_count: %s' %bicycle_height_600_count)

    print('--------------------------------------------------------------------------------')
    print('bicycle_width_low: %s' %bicycle_width_100_count)
    print('bicycle_width_mid: %s' %bicycle_width_100_150_count)
    print('bicycle_width_high: %s' %bicycle_width_high_count)
    print('bicycle_width_150_200_count: %s' %bicycle_width_150_200_count)
    print('bicycle_width_200_300_count: %s' %bicycle_width_200_300_count)
    print('bicycle_width_300_600_count: %s' %bicycle_width_300_600_count)
    print('bicycle_width_600_count: %s' %bicycle_width_600_count)
    print('--------------------------------------------------------------------------------')

    print('motorbike_height_low: %s' %motorbike_height_100_count)
    print('motorbike_height_mid: %s' %motorbike_height_100_200_count)
    print('motorbike_height_high: %s' %motorbike_height_high_count)
    print('motorbike_height_200_300_count: %s' %motorbike_height_200_300_count)
    print('motorbike_height_300_400_count: %s' %motorbike_height_300_400_count)
    print('motorbike_height_400_600_count: %s' %motorbike_height_400_600_count)
    print('motorbike_height_600_count: %s' %motorbike_height_600_count)

    print('--------------------------------------------------------------------------------')
    print('motorbike_width_low: %s' %motorbike_width_100_count)
    print('motorbike_width_mid: %s' %motorbike_width_100_150_count)
    print('motorbike_width_high: %s'%motorbike_width_high_count)
    print('motorbike_width_150_200_count: %s' %motorbike_width_150_200_count)
    print('motorbike_width_200_300_count: %s' %motorbike_width_200_300_count)
    print('motorbike_width_300_600_count: %s' %motorbike_width_300_600_count)
    print('motorbike_width_600_count: %s' %motorbike_width_600_count)
    print('--------------------------------------------------------------------------------')

    print('person','car','bus','truck','unkonwncar','bicycle','motobike',sep='\t\t')
    print('height','width','height','width','height','width','height','width','height','width','height','width','height','width',sep='\t\t')
    print(person_height_100_count,person_width_100_count,car_height_100_count,car_width_100_count,bus_height_100_count,bus_width_100_count,truck_height_100_count,truck_width_100_count,unknowncar_height_100_count,unknowncar_width_100_count,bicycle_height_100_count,bicycle_width_100_count,motorbike_height_100_count,motorbike_width_100_count,sep='\t')
    print(person_height_100_200_count,person_width_100_150_count,car_height_100_200_count,car_width_100_150_count,bus_height_100_200_count,bus_width_100_150_count,truck_height_100_200_count,truck_width_100_150_count,unknowncar_height_100_200_count,unknowncar_width_100_150_count,bicycle_height_100_200_count,bicycle_width_100_150_count,motorbike_height_100_200_count,motorbike_width_100_150_count,sep='\t')
    print(person_height_high_count,person_width_high_count,car_height_high_count,car_width_high_count,bus_height_high_count,bus_width_high_count,truck_height_high_count,truck_width_high_count,unknowncar_height_high_count,unknowncar_width_high_count,bicycle_height_high_count,bicycle_width_high_count,motorbike_height_high_count,motorbike_width_high_count,sep='\t')



#low value check
def low_function(number,condition):
    if condition =="width":
        if (int(number) <100):
            return number

        else:
            return False
    if condition =='height':
        if (int(number) <100):
            return number

        else:
            return False
#mid value check
def mid_function(number,condition):
    if condition =="width":
        if ((int(number) >= 100) & (int(number) <150)):
            return number
        else:
            return False
    if condition =="height":
        if ((int(number) >= 100) & (int(number) <200)):
            return number
        else:
            return False
#high value check
def high_function(number,condition):
    if condition =="width":
        if ((int(number) >=150)):
            return number
        else:
            return False
    if condition =="height":
        if ((int(number) >=200)):
            return number
        else:
            return False
#xml class count
def parse_xml_count(path,file, name,result,condition,shape):
    count = 0
    tree = ET.parse(os.path.join(path,file))
    note = tree.getroot()
    for child in note.findall('object'):
        class_name = child.find('name').text
        bndbox = child.find('bndbox')
        xmin = int(float(bndbox.find('xmin').text))
        ymin = int(float(bndbox.find('ymin').text))
        xmax = int(float(bndbox.find('xmax').text))
        ymax = int(float(bndbox.find('ymax').text))
        width = abs(xmin-xmax)
        height = abs(ymin-ymax)
        if (str(class_name)==name) and (condition =='mid') and (shape== 'width'):
            if(int(width) >= 100) & (int(width) < 150):
                #print(width,shape)
                count += 1
        elif (str(class_name)==name) and (condition =='low') and (shape== 'width'):
            if(int(width) < 100) :
                #print(width,shape)
                count += 1
        elif (str(class_name)==name) and (condition =='high') and (shape== 'width'):
            if(int(width) >= 150) :
                #print(width,shape)
                count += 1
        if (str(class_name)==name) and (condition =='mid') and (shape== 'height'):
            if(int(height) >= 100) & (int(height) < 200):
                #print(height,shape)
                count += 1
        elif (str(class_name)==name) and (condition =='low') and (shape== 'height'):
            if(int(height) < 100) :
                #print(height,shape)
                count += 1
        elif (str(class_name)==name) and (condition =='high') and (shape== 'height'):
            if(int(height) >= 200) :
                #print(height,shape)
                count += 1
    #print(os.path.join(path,file))
    return count
#condition check make xml list
def xxx(classs, condition, shape , setcount):
    global result,seed_count,class_no,result_count
    result_count=0
    result=0
    seed_count=0
    class_no=0
    #목표 url 안의 모든 내부 폴더 및 파일 읽기
    for (path, dir, files) in os.walk(cvatxmlRootpath):
        for file in files:
            if file.endswith(".xml"):
                path1 = os.path.join(path,file)
                #random.shuffle(path1)
                tree = ET.parse(os.path.join(path,file))
                note = tree.getroot()
                for child in note.findall('object'):
                    name = child.find('name').text
                    if  name == "excavator" or name == "forklift" or name == "ladder truck" or name == "unknown car" :
                        name ="unknown car"
                    if name == str(classs):
                        name = child.find('name').text
                        bndbox = child.find('bndbox')
                        xmin = int(float(bndbox.find('xmin').text))
                        ymin = int(float(bndbox.find('ymin').text))
                        xmax = int(float(bndbox.find('xmax').text))
                        ymax = int(float(bndbox.find('ymax').text))
                        width = abs(xmin-xmax)
                        height = abs(ymin-ymax)
                        if (setcount==0):
                            if (condition =='low') and (shape== 'width') :
                                result=low_function(width,"width")
                            elif(condition =='mid') and (shape == 'width') :
                                result=mid_function(width,"width")
                            elif(condition =='high') and (shape == 'width') :
                                result=high_function(width,"width")
                            elif(condition =='low') and (shape == 'height'):
                                result=low_function(height,"height")
                            elif(condition == 'mid') and (shape == 'height'):
                                result=mid_function(height,"height")
                            elif(condition =='high') and (shape =='height'):
                                result=high_function(height,"height")

                            if((result) != False) :
                                result_path.append(os.path.join(path,file))
                                result_name.append(file)
                                result_only_path.append(path)

                        elif (setcount >0):
                            if (condition =='low') and (shape== 'width')and (seed_count < setcount) :
                                result=low_function(width,"width")

                            elif(condition =='mid') and (shape == 'width')  and (seed_count < setcount):
                                result=mid_function(width,"width")

                            elif(condition =='high') and (shape == 'width') and (seed_count < setcount):
                                result=high_function(width,"width")

                            elif(condition =='low') and (shape == 'height')and (seed_count < setcount) :
                                result=low_function(height,"height")

                            elif(condition == 'mid') and (shape == 'height') and (seed_count < setcount):
                                result=mid_function(height,"height")

                            elif(condition =='high') and (shape =='height')and (seed_count < setcount):
                                result=high_function(height,"height")

                            #print(seed_count)

                            if((result) != False) and (seed_count < setcount):


                                print(os.path.join(path,file))
                                result_name.append(file)
                                result_only_path.append(path)
                                #name classs 의 개수 세기
                                class_no = parse_xml_count(path, file, name,result,condition,shape)
                                if (class_no >= 1):
                                    class_no=1
                                    if (class_no ==1):
                                        #print(class_no)
                                        result_path.append(os.path.join(path,file))
                                        seed_count += class_no
                                        #print(seed_count, setcount,class_no)

    return result_path

def copyxml(resultpath,copypath):
    total_xml_name=[]
    #------복사시작---------------#
    list_1=list(set(result_path))
    print('복사되야할 xml 개수 :%s'%len(list_1))
    print('-----복사시작-------')
    for (path, dir, files) in os.walk(cvatxmlRootpath):
        for file in files:
            if file.endswith(".xml"):
                total_xml_name.append(file)

    for i in range(len(total_xml_name)):
        for j in range(len(result_name)):
            if(total_xml_name[i] == result_name[j]):
                a=os.path.join(result_only_path[j],result_name[j])
                b=os.path.join(move_xml_path,result_name[j])

                shutil.copy(a,b)
# Main Loop

# classes=['person','car','bus','truck','unknowncar','bicycle','motorbike']
# condition=['low','mid','high']
# shape=['width','height']
result_final_list=[]
for i in range(len(result_list)):
    result1=xxx(result_list[i][0],result_list[i][1],result_list[i][2],result_list[i][3])
statistics(result_path)
print('작업 수행된 시간 : %f 초' % (time.time() - start_time))

####xml copy하려면 함수실행
#copyxml(result_path,move_xml_path)
#------복사끝---------------#
print('-----복사끝-------')
