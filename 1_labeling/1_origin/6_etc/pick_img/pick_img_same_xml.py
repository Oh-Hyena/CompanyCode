
import time
import os
import shutil

# img를 복사할 xml rootpath (bus xml을 전체 원본 img와 비교해서 bus img만 뽑을 것이므로 xml은 bus xml로 적어야 함)
xml_Rootpath=r"D:\HN_code\change_night7class_6class\Unitrain16\Night\train_xml"
#원본 imgRootpath (pure > JPEGImages > train 에 있는 image 사용)
img_Rootpath=r"D:\HN_code\change_night7class_6class\Unitrain16\Night\6class\copy_img_Rootpath"
copy_img_Rootpath=r"D:\HN_code\change_night7class_6class\Unitrain16\Night\6class\train_dataset"
#os.mkdir(copy_img_Rootpath)

xmlname=os.listdir(xml_Rootpath)

total_jpg_file_name=[]
total_jpg_file_path=[]
full_total_jpg_file_name=[]
copy_xmlname_list=[]

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
