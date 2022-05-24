
import time
import os
import shutil

# img를 복사할 xml rootpath (bus xml을 전체 원본 img와 비교해서 bus img만 뽑을 것이므로 xml은 bus xml로 적어야 함)
xml_Rootpath=r"D:\HN_dataset\change_class\7class_to_6class\7class_밤영상(xml,img)\Unitraindataset\성남에서수집한_야간데이터셋\data_process\valid_dataset_xml"
#원본 imgRootpath (pure > JPEGImages > train 에 있는 image 사용)
img_Rootpath=r"D:\HN_dataset\change_class\7class_to_6class\7class_밤영상(xml,img)\Unitraindataset\성남에서수집한_야간데이터셋\data_process\6class\copy_img_Rootpath"
yolotxt_Rootpath=r"D:\HN_dataset\change_class\7class_to_6class\7class_밤영상(xml,img)\Unitraindataset\성남에서수집한_야간데이터셋\data_process\6class\save_yolo"

makeDatset=r"D:\HN_dataset\change_class\7class_to_6class\7class_밤영상(xml,img)\Unitraindataset\성남에서수집한_야간데이터셋\data_process\6class\valid_dataset"
os.mkdir(makeDatset)

xmlname=os.listdir(xml_Rootpath)

total_jpg_file_name=[]
total_jpg_file_path=[]
full_total_jpg_file_name=[]

copy_xmlname_list=[]


total_txt_file_name=[]
total_txt_file_path=[]
full_total_txt_file_name=[]


def some_process(x):
    return True

for i in xmlname:
    copy_xmlname_list.append(i[:-4])

for (path, dir, files) in os.walk(img_Rootpath):
    for j,file in enumerate(files):
        if file.endswith(".jpg"):
            total_jpg_file_name.append(file[:-4])
            total_jpg_file_path.append(path)
            full_total_jpg_file_name.append(file)

total = len(full_total_jpg_file_name)

for (path, dir, files) in os.walk(yolotxt_Rootpath):
    for j,file in enumerate(files):
        if file.endswith(".txt"):
            total_txt_file_name.append(file[:-4])
            total_txt_file_path.append(path)
            full_total_txt_file_name.append(file)

total = len(full_total_jpg_file_name)
start = time.time()

for i in range(len(total_jpg_file_name)):
    some_process(i)
    now=time.time()
    print(f'\r{i+1}/{total} runtime: {now - start:.2f}', end='')
    for j in range(len(copy_xmlname_list)):
        if(total_jpg_file_name[i]==copy_xmlname_list[j]):
            path=os.path.join(total_jpg_file_path[i],full_total_jpg_file_name[i])
            path1=os.path.join(makeDatset,full_total_jpg_file_name[i])
            shutil.copy(path,path1)
            txtpath=os.path.join(total_txt_file_path[i],full_total_txt_file_name[i])
            txtpath1=os.path.join(makeDatset,full_total_txt_file_name[i])
            shutil.copy(txtpath,txtpath1)
            
time.sleep(0.5)
