import os
import numpy as np
import xml.etree.ElementTree as ET
import shutil
import time


#total_xml_path=r"D:\전체채널동영상_성남시[아침_점심_점심_저녁_밤]\night_dataset\night_dataset_7class\data_process\xmls"
img_rootpath=r"D:\HN_code\test\1_labeling\9_specific_class_dataset\1_seongnamfalse1112_img"
total_xml_path=r"D:\HN_code\test\1_labeling\9_specific_class_dataset\3_6class_data_process\class6_xml"
copy_xml_path=r"D:\HN_code\test\1_labeling\9_specific_class_dataset\4_bus_img_xml\bus_xml"
copt_img_path=r"D:\HN_code\test\1_labeling\9_specific_class_dataset\4_bus_img_xml\bus_img"


cvatxml_list=[]
total_jpg_file_name=[]
total_jpg_file_path=[]
full_total_jpg_file_name=[]
copy_xmlname_list=[]


for (path, dir, files) in os.walk(total_xml_path):
    for file in files:
        if file.endswith(".xml"):
            c=os.path.join(path,file)
            tree = ET.parse(os.path.join(path,file))
            note = tree.getroot()
            for child in note.findall('object'):
                name = child.find('name').text
                if name  == "bus":
                    a=os.path.join(path,file)
                    print(a)
                    b=os.path.join(copy_xml_path,file)
                    shutil.copy(a,b)


def some_process(x):
    return True


xmlname=os.listdir(copy_xml_path)
for i in xmlname:
    copy_xmlname_list.append(i[:-4])


for (path, dir, files) in os.walk(img_rootpath):
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
            path1=os.path.join(copt_img_path,full_total_jpg_file_name[i])
            shutil.copy(path,path1)
time.sleep(0.5)
