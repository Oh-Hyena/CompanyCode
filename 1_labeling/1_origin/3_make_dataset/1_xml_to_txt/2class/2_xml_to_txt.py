
###최신. 2020-02-04버전임.


import json
import xml.etree.ElementTree as ET
import os
import cv2

                              

dir_name = r"H:\seongnamfalse\2021\1008\labeling\condition_1st_seongnamfalse1008\data_process\xmls" #.xml파일의 위치를 전부 로드한다.(이미지 섞여있어도 됨.) (절대경로)
save_dir = r"H:\seongnamfalse\2021\1008\labeling\condition_1st_seongnamfalse1008\condition_1st_seongnamfalse1008_txt"              #yolo style txt 저장 위치. (절대경로)

category_dir = r"H:\seongnamfalse\2021\1008\labeling\condition_1st_seongnamfalse1008\basemodel.names" #카테고리 로드 (절대경로)


#적어놓은 카테고리를 리스트화
with open(category_dir, 'r') as categorys:
    namelist = [cate.strip() for cate in categorys]
    
#작업을 진행할 디렉토리 지정
file_list = os.listdir(dir_name)
print(len(file_list), end="")
print("개 작업 예정.")



if not os.path.isdir(save_dir):
    os.mkdir(save_dir)
#결과를 저장할 디렉토리 오픈 혹은 생성
    

def convert_xywh(width,height,xmin,xmax,ymin,ymax):
    dw = 1/width
    dy = 1/height
    #[x,y,w,h]
    xywh = [str(((xmin+xmax)/2.0)*dw),str(((ymin+ymax)/2.0)*dy),str((xmax-xmin)*dw),str((ymax-ymin)*dy)] #YOLO의 영역 표시방법을 계산식으로 써놓은 모습. 
    
    return xywh


for file in file_list:
    if file.endswith(".xml"): #확장자가 xml이라면 작업 시행
        tree = ET.parse(os.path.join(dir_name,str(file)))
        note = tree.getroot()
        
        fname = note.find('filename').text
        
        size = note.find('size')
        height = int(size.find('height').text) #이미지의 height
        width = int(size.find('width').text) #이미지의 width

        result = open(os.path.join(save_dir, file[:-4]+".txt"),"w")
        
        print(fname[:-4])
        
        for child in note.findall('object'): #모든 객체에 대한 작업 실행
            name = child.find('name').text #객체의 카테고리 이름
            
            #-------------------------------------------------
            
            if name == "bus" or name == "truck" or name == "excavator" or name == "forklift" or name == "ladder truck" or name == "unknown car" :
                name = "car"
                
            #-------------------------------------------------
            
            
            
            if name in namelist: #category list에 해당하는 카테고리의 이름이 있다면 작업 실행
#                name = child.find('name').text 
                bndbox = child.find('bndbox')
                xmin = int(float(bndbox.find('xmin').text))
                ymin = int(float(bndbox.find('ymin').text))
                xmax = int(float(bndbox.find('xmax').text))
                ymax = int(float(bndbox.find('ymax').text))
                
                yolo_data = convert_xywh(width,height,xmin,xmax,ymin,ymax)
                #VOC 영역표시법을 YOLO로 변환하는 함수 실행
                if name == namelist[0].strip():
                    result.write("0"+" "+yolo_data[0]+" "+yolo_data[1]+" "+yolo_data[2]+" "+yolo_data[3]+"\n") # 결과를 .txt에 삽입
                elif name == namelist[1].strip():
                    result.write("1"+" "+yolo_data[0]+" "+yolo_data[1]+" "+yolo_data[2]+" "+yolo_data[3]+"\n") # 결과를 .txt에 삽입
            
        result.close()



