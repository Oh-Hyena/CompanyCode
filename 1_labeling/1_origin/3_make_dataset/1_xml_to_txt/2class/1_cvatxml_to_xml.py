# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 15:57:50 2020
@author: kth

v1.4 (2020년 5월 19일에 업데이트)
변경점 : 
1. imageRootPath 경로를 잘 못읽는 버그 수정.
2. xmls 폴더 안에 일괄적으로 모든 xml 다 넣음.

+ 근데 이제 빈파일 못찾음 나중에 수정해서 빈파일 관련 코드 지울것.


1. 이미지만 모아놓은 images 디렉토리 필요.(계층 여러개 있어도됨)
    imageRootpath
       ㄴ 0001_d
           ㄴ JPEGImages
                ㄴ 0001_d_0001.jpg
                        ...
                   0001_d_0150.jpg
       ㄴ 0002_r
           ㄴ JPEGImages
                ㄴ 0002_r_0001.jpg
                        ...
                   0002_r_0150.jpg
       ㄴ 0003_d
           ...

2. cvat Xml for images xml만 모아놓은 cvatxmls 디렉토리 필요. (1층으로 만들것)
    cvatxmlRootpath
        ㄴ0001_d.xml
        ㄴ0002_r.xml
        ...
"""



import os
import xml.etree.ElementTree as ET
import shutil
import random
from xml.dom import minidom

# data_process > cvatxmls, documents, notpure, pure, xmls 하위 폴더 만들기
rootpath = r"G:\labelingDataset\origin\test_dataset\coco17\data_process"

imageRootpath = r"G:\labelingDataset\origin\test_dataset\coco17\img"

logpath = os.path.join(rootpath, "documents")

##로그 저장되는 디렉터리.
cvatxmlRootpath = os.path.join(rootpath, "cvatxmls")
##cvatxml 목록이 있는 디렉터리. 이 안에 있는 xml에서 지칭하는 이미지만큼만 작업함.
# 즉 이 안에 있는 xml개수 * 150장 만큼 작업이 됨.

#cvatxml 을 이용하여 생성되는 xmls들의 패스. cvatxml을 이용하여 여기
xmlRootpath = os.path.join(rootpath, "xmls")


##새로 복사될 디렉터리.
pureImageRootpath = os.path.join(rootpath, "pure", "JPEGImages")
pureXmlRootpath = os.path.join(rootpath, "pure", "Annotations")
notPureImageRootpath = os.path.join(rootpath, "notpure", "JPEGImages")
notPureXmlRootpath = os.path.join(rootpath, "notpure", "Annotations")





purePercentThreshold = -1
pureLabel = "box"   ## "person" or "car" or "box" or "both")




##  is_Ratio
#   True : 비율대로 랜덤으로 valid set 만듬. (완벽하게 안떨어짐), validcount는 사용안함.
#   False : validCount만큼 valid set만듬. (ratio는 사용 안함.)
is_Ratio = False
validRatio = 0.1
pureValidCount = 0
notPureValidCount = 0


# person : 퓨어 기준을 사람으로만 잡음.
# car : 퓨어 기준을 차로만 잡음.
# box : 퓨어 기준을 박스로 잡음.(모든 박스가 기준이됨) All elements
# both : 퓨어 기준을 사람, 차량 둘다 충족해야함. human and car







###-----------------------------------------------------------------------------------------------


cars = ["car", "bus", "truck", "excavator", "forklift", "ladder truck", "unknown car" ]
###범차량 통합용.
others = ["bicycle", "motorbike"]
### 학습에 


imageDict = {}
xmlDict = {}

def readCvatxml():
#    f = open(os.path.join(logpath, "pureExtractor("+pureLabel+","+str(purePercentThreshold)+").log"), "w")
    f = open(os.path.join(logpath, "pureExtractor.log") ,"w")
    ff = open(os.path.join(logpath, "pureExtractedList.txt"), "w")
    fff = open(os.path.join(logpath, "notPureExtractedList.txt"), "w")
    totalImageCount = 0
    totalBoxCount = 0
    totalPersonBoxCount = 0
    totalCarBoxCount = 0
    totalPureBoxCount = 0
    
    totalPurePersonBoxCount = 0
    totalPureCarBoxCount = 0
    
    totalPureImageCount = 0
    
    totalOthersBoxCount = 0
    totalPureOthersBoxCount = 0
    
    totalInPerson = 0
    totalInCar = 0
    totalInOthers = 0
    
    totalPureInPerson = 0
    totalPureInCar = 0
    totalPureInOthers = 0
    
    cvatxmllist = os.listdir(cvatxmlRootpath)
    
 
    ###---------------------------------------------
    imageList = []
    xmlList = []
    

    
    for (path, dir, files) in os.walk(imageRootpath):
        for file in files:
            if file.endswith(".jpg"):         
                if os.path.basename(file)[:-4]+".xml" in os.listdir(xmlRootpath):
                    imageList.append(file[:-4])
                    imageDict[file] = os.path.join(path,file)
                    
    for (path, dir, files) in os.walk(xmlRootpath):
        for file in files:
            if file.endswith(".xml"):
                xmlList.append(file[:-4])
                xmlDict[file] = os.path.join(path,file)
                
    imageList.sort()
    xmlList.sort()
    
    
    emptyimageList = list(set(imageList)-set(xmlList))
    emptyimageList.sort()
    
    emptyimageListLog = open(os.path.join(logpath, "emptyImageList.log") ,"w")
    for line in emptyimageList:
        emptyimageListLog.write(line+".jpg")
        emptyimageListLog.write("\n")
    emptyimageListLog.close()
    
    ###-----------------------------------------------

    #cvatxmllist = os.listdir(cvatxmlRootpath) 위로 올림. 
    
    
    for cvatxml in cvatxmllist:
        if cvatxml.endswith(".xml"):
            tree = ET.parse(os.path.join(cvatxmlRootpath, cvatxml))
            note = tree.getroot()
            
            for image in note.findall("image"):
                totalImageCount += 1
                
                pureCount = 0
                boxCount = 0
                
                
                inPerson = 0
                inCar = 0
                inOthers = 0
                
                pureInPerson = 0
                pureInCar = 0
                pureInOthers = 0
                
                
                personBoxCountForBoth = 0
                carBoxCountForBoth = 0
                purePersonCountForBoth = 0
                pureCarCountForBoth = 0
                
                
                for box in image.findall("box"):
                    totalBoxCount += 1
                    label = box.get("label")
                    
                    if pureLabel == "box":
                        boxCount += 1
                    
                    if label == "person":
                        totalPersonBoxCount += 1
                        inPerson += 1
                        if pureLabel == "person":
                            boxCount += 1
                        if pureLabel == "both":
                            personBoxCountForBoth += 1
                    elif label in cars:
                        totalCarBoxCount += 1
                        inCar += 1
                        if pureLabel == "car":
                            boxCount += 1
                        if pureLabel == "both":
                            carBoxCountForBoth += 1
                    elif label in others:
                        totalOthersBoxCount += 1
                        inOthers += 1
                        
                            
                    attribute = box.find("attribute").text
                    
                    
                    if attribute == "pure":
                        totalPureBoxCount += 1
                        
                        if pureLabel == "box":
                            pureCount += 1
                            
        
                        if label == "person":
                            totalPurePersonBoxCount += 1
                            pureInPerson += 1
                            if pureLabel == "person":
                                pureCount += 1
                            if pureLabel == "both":
                                purePersonCountForBoth += 1
                            
                        elif label in cars:
                            totalPureCarBoxCount += 1
                            pureInCar += 1
                            if pureLabel == "car":
                                pureCount += 1
                            if pureLabel == "both":
                                pureCarCountForBoth += 1
                                
                        elif label in others:
                            totalPureOthersBoxCount += 1
                            pureInOthers += 1
                                
                
                if inPerson > 0:
                    totalInPerson += 1
                if inCar > 0:
                    totalInCar += 1
                if inOthers > 0:
                    totalInOthers += 1
                    
                if pureInPerson > 0:
                    totalPureInPerson += 1
                if pureInCar > 0:
                    totalPureInCar += 1
                if pureInOthers > 0:
                    totalPureInOthers += 1
              
                    
                
                f.write("이미지 이름 :"+image.get("name")+"  \t")
#                print("이미지 이름 :"+image.get("name"))
                
                
                
                """
                if boxCount == 0:
                    f.write("box 하나도 없음.\n")
                    purePercent = 0
                else:
#                    print("pure 백분율 : ",end="")
#                    print(pureCount/boxCount*100)
                    
                    purePercent = float(pureCount/boxCount*100)
                    f.write("pure("+ pureLabel +") 백분율 :")
                    
                    f.write(str(pureCount/boxCount*100)+"\n")
                    
                    if purePercent > float(purePercentThreshold):
#                        print("퓨어한 이미지 :"+image.get("name"))
                        totalPureImageCount += 1
                        ff.write(image.get("name")+"\n")
                """

                if not pureLabel == "both":
                    if boxCount == 0:
                        f.write("box 하나도 없음.\n")
                        purePercent = 0
                    else:
                        purePercent = float(pureCount/boxCount*100)
                        f.write("pure("+ pureLabel +") 백분율 :")
                        f.write(str(purePercent)+"\n")
                    
                    if purePercent > float(purePercentThreshold):
#                        print("퓨어한 이미지 :"+image.get("name"))
                        totalPureImageCount += 1
                        ff.write(image.get("name")+"\n")
                    else:
                        fff.write(image.get("name")+"\n")
                        
                        
                else:
                    if personBoxCountForBoth == 0:
                        purePersonPercent = 0
                    else:
                        purePersonPercent = float(purePersonCountForBoth/personBoxCountForBoth*100)
                        
                    if carBoxCountForBoth == 0:
                        pureCarPercent = 0
                    else:
                        pureCarPercent = float(pureCarCountForBoth/carBoxCountForBoth*100)
                        
                        
                    f.write("pure("+ pureLabel +":person) 백분율 :")
                    
                    if personBoxCountForBoth == 0:
                         f.write("box 하나도 없음.\t")
                    else:
                        f.write(str(purePersonPercent)+"\t")
                    
                    
                    f.write(" / pure("+ pureLabel +":car) 백분율 :")
                    
                    
                    if carBoxCountForBoth == 0 :
                        f.write("box 하나도 없음.\t")
                    else:
                        f.write(str(pureCarPercent)+"\n")
            
        
                    
                    if purePersonPercent > float(purePercentThreshold) and pureCarPercent > float(purePercentThreshold):
                        totalPureImageCount += 1
                        ff.write(image.get("name")+"\n")
                    else:
                        fff.write(image.get("name")+"\n")
                        
                        
                              
    print("퓨어 기준 클래스 : ",end="")
    print(pureLabel)
    
    print("이미지 추출용 퓨어 임계값 : ",end="")
    print(str(purePercentThreshold)+"%")
    
    if is_Ratio:
        print("valid 비율 : ",end="")
        print(str(validRatio*100)+"%")
    else:
        print("퓨어데이터 valid 개수 : ",end="")
        print(str(pureValidCount))
        print("낫퓨어 데이터 valid 개수 : ",end="")
        print(str(notPureValidCount))
    
    print("전체 데이터셋 총 이미지 장수 : ",end="")
    print(str(totalImageCount+len(emptyimageList)))
    print("객체가 존재하는 이미지 장수 : ",end="")
    print(str(totalImageCount))
    print("객체가 하나도 없는 이미지 장수 : ",end="")
    print(str(len(emptyimageList)))
    
    print("전체 데이터셋 사람이 하나라도 포함된 이미지 개수 : ",end="")
    print(str(totalInPerson))
    print("전체 데이터셋 차량이 하나라도 포함된 이미지 개수 : ",end="")
    print(str(totalInCar))   
    
    print("전체 데이터셋 퓨어한 사람이 하나라도 포함된 이미지 개수 : ",end="")
    print(str(totalPureInPerson))
    print("전체 데이터셋 퓨어한 차량이 하나라도 포함된 이미지 개수 : ",end="")
    print(str(totalPureInCar))   
    
    
        
    print("전체 데이터셋 총 박스 개수 : ",end="")
    print(str(totalBoxCount))
    print("전체 데이터셋 총 사람 박스 개수 : ",end="")
    print(str(totalPersonBoxCount))
    print("전체 데이터셋 총 차량 박스 개수 : ",end="")
    print(str(totalCarBoxCount))
    print("전체 데이터셋 총 그외 박스 개수 : ",end="")
    print(str(totalOthersBoxCount))
    
    
    print("전체 데이터셋 총 퓨어 박스 개수 : ",end="")
    print(str(totalPureBoxCount))
    print("전체 데이터셋 총 퓨어 사람 박스 수 : ",end="")
    print(str(totalPurePersonBoxCount))
    print("전체 데이터셋 총 퓨어 차량 박스 수 : ",end="")
    print(str(totalPureCarBoxCount))
    print("전체 데이터셋 총 퓨어 그외 박스 개수 : ",end="")
    print(str(totalPureOthersBoxCount))
    
    print("최종 퓨어 판정 이미지 장수 : ",end="")
    print(str(totalPureImageCount))
    print("최종 낫 퓨어 판정 이미지 장수 : ",end="")
    print(str(totalImageCount-totalPureImageCount))
    
    
    f.write("퓨어 기준 클래스 : ")
    f.write(pureLabel+"\n")

    f.write("이미지 추출용 퓨어 임계값 : ")
    f.write(str(purePercentThreshold)+"%"+"\n")
    
    
    if is_Ratio:
        f.write("valid 비율 : ")
        f.write(str(validRatio*100)+"%\n")
    else:
        f.write("퓨어데이터 valid 개수 : ")
        f.write(str(pureValidCount)+"\n")
        f.write("낫퓨어 데이터 valid 개수 : ")
        f.write(str(notPureValidCount)+"\n")
        
        
    
    f.write("전체 데이터셋 총 이미지 장수 : ")
    f.write(str(totalImageCount+len(emptyimageList))+"\n")
    f.write("객체가 존재하는 이미지 장수 : ")
    f.write(str(totalImageCount)+"\n")
    f.write("객체가 하나도 없는 이미지 장수 : ")
    f.write(str(len(emptyimageList))+"\n")

    
    f.write("전체 데이터셋 사람이 하나라도 포함된 이미지 개수 : ")
    f.write(str(totalInPerson)+"\n")
    f.write("전체 데이터셋 차량이 하나라도 포함된 이미지 개수 : ")
    f.write(str(totalInCar)+"\n")   
    
    
    f.write("전체 데이터셋 퓨어한 사람이 하나라도 포함된 이미지 개수 : ")
    f.write(str(totalPureInPerson)+"\n")
    f.write("전체 데이터셋 퓨어한 차량이 하나라도 포함된 이미지 개수 : ")
    f.write(str(totalPureInCar)+"\n")   
    
    
    
    
    f.write("전체 데이터셋 총 박스 개수 : ")
    f.write(str(totalBoxCount)+"\n")
    f.write("전체 데이터셋 총 사람 박스 개수 : ")
    f.write(str(totalPersonBoxCount)+"\n")
    f.write("전체 데이터셋 총 차량 박스 개수 : ")
    f.write(str(totalCarBoxCount)+"\n")
    f.write("전체 데이터셋 총 그외 박스 개수 : ")
    f.write(str(totalOthersBoxCount)+"\n")    
    f.write("전체 데이터셋 총 퓨어 박스 개수 : ")
    f.write(str(totalPureBoxCount)+"\n")
    f.write("전체 데이터셋 총 퓨어 사람 박스 수 : ")
    f.write(str(totalPurePersonBoxCount)+"\n")
    f.write("전체 데이터셋 총 퓨어 차량 박스 수 : ")
    f.write(str(totalPureCarBoxCount)+"\n")
    f.write("전체 데이터셋 총 퓨어 그외 박스 개수 : ")
    f.write(str(totalPureOthersBoxCount)+"\n")
    
    
    f.write("최종 퓨어 판정 이미지 장수 : ")
    f.write(str(totalPureImageCount)+"\n")
    f.write("최종 낫 퓨어 판정 이미지 장수 : ")
    f.write(str(totalImageCount-totalPureImageCount)+"\n")

    
    f.close()
    ff.close()
    fff.close()
    
    
    
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
                    
            
                #ugly xml
#                newtree = ET.ElementTree(annotation)
#                newtree.write(os.path.join(xmlRootpath, name[:-9], name[:-4]+".xml"))
                    


                pretty = minidom.parseString(ET.tostring(annotation)).toprettyxml(indent="   ")
                with open(os.path.join(xmlRootpath, name[:-4]+".xml"), "w") as f:
                    f.write(pretty)
    
    
    
    
    
    

          
def getImagePath(file):
    file= file.strip()
    return imageDict[file]

def getXmlPath(file):  
    fname, ext = os.path.splitext(file)
    return xmlDict[fname+".xml"]



        
        
def pureExtract():
    f = open(os.path.join(logpath,"pureExtractedList.txt" ), "r")
    ff = open(os.path.join(logpath,"copy.log" ), "w")
    pureTrain =  open(os.path.join(logpath,"pureTrainList.log" ), "w")
    pureValid =  open(os.path.join(logpath,"pureValidList.log" ), "w")
    notPureTrain =  open(os.path.join(logpath,"notPureTrainList.log" ), "w")
    notPureValid =  open(os.path.join(logpath,"notPureValidList.log" ), "w")
    
    
    
    lines = f.readlines()
    f.close()
    if not os.path.isdir(pureImageRootpath):
        os.mkdir(pureImageRootpath)
    if not os.path.isdir(pureXmlRootpath):
        os.mkdir(pureXmlRootpath)

    if not os.path.isdir(notPureImageRootpath):
        os.mkdir(notPureImageRootpath)
    if not os.path.isdir(notPureXmlRootpath):
        os.mkdir(notPureXmlRootpath)        
        
        

    if not os.path.isdir(os.path.join(pureImageRootpath, "train")):
        os.mkdir(os.path.join(pureImageRootpath, "train"))
    if not os.path.isdir(os.path.join(pureXmlRootpath, "train")):
        os.mkdir(os.path.join(pureXmlRootpath, "train"))
    if not os.path.isdir(os.path.join(pureImageRootpath, "valid")):
        os.mkdir(os.path.join(pureImageRootpath, "valid"))
    if not os.path.isdir(os.path.join(pureXmlRootpath, "valid")):
        os.mkdir(os.path.join(pureXmlRootpath, "valid"))
        
    if not os.path.isdir(os.path.join(notPureImageRootpath, "train")):
        os.mkdir(os.path.join(notPureImageRootpath, "train"))
    if not os.path.isdir(os.path.join(notPureXmlRootpath, "train")):
        os.mkdir(os.path.join(notPureXmlRootpath, "train"))
    if not os.path.isdir(os.path.join(notPureImageRootpath, "valid")):
        os.mkdir(os.path.join(notPureImageRootpath, "valid"))
    if not os.path.isdir(os.path.
    join(notPureXmlRootpath, "valid")):
        os.mkdir(os.path.join(notPureXmlRootpath, "valid"))
    
    
    
    if is_Ratio == False:
        sampled = random.sample(range(0,len(lines)), pureValidCount)
        validList = []
        for index in sampled:
            validList.append(lines[index].strip())
    
    
    for line in lines:
        line = line.strip()
        print(line, end="   ")
        print("pure 이미지, xml 복사하는 중...")
        
        
        if is_Ratio == True:
            try:
                thres = random.random()
                fname, fext = os.path.splitext(line)
                if thres > validRatio:
                    dataType = "train"
                else:
                    dataType = "valid"
                if dataType == "train":
                    shutil.copy(getImagePath(line), os.path.join(pureImageRootpath, "train"))
                    shutil.copy(getXmlPath(line), os.path.join(pureXmlRootpath, "train"))
                    
                    
                    pureTrain.write("pure:" + dataType + " ")
                    pureTrain.write(line)
                    pureTrain.write("\n")
                else:
                    shutil.copy(getImagePath(line), os.path.join(pureImageRootpath, "valid"))
                    shutil.copy(getXmlPath(line), os.path.join(pureXmlRootpath,  "valid"))
                    pureValid.write("pure:" + dataType + " ")
                    pureValid.write(line)
                    pureValid.write("\n")
                    
                ff.write("pure:" + dataType + " ")
                ff.write(line)
                ff.write("\n")
            except:
                ff.write("except: ")
                ff.write(line)
                ff.write("\n")
        else: ##is_Ratio == False:
            try:
                fname, fext = os.path.splitext(line)
                if line in validList:
                    
                    dataType = "valid"
                    shutil.copy(getImagePath(line), os.path.join(pureImageRootpath, "valid"))
                    shutil.copy(getXmlPath(line), os.path.join(pureXmlRootpath,  "valid"))
                    
                    pureValid.write("pure:" + dataType + " ")
                    pureValid.write(line)
                    pureValid.write("\n")
                else:
                    dataType = "train"
                    shutil.copy(getImagePath(line), os.path.join(pureImageRootpath, "train"))
                    shutil.copy(getXmlPath(line), os.path.join(pureXmlRootpath, "train"))
              
                    pureTrain.write("pure:" + dataType + " ")
                    pureTrain.write(line)
                    pureTrain.write("\n")
                ff.write("pure:" + dataType + " ")
                ff.write(line)
                ff.write("\n")
            except:
                ff.write("except: ")
                ff.write(line)
                ff.write("\n")
            
    
    f = open(os.path.join(logpath,"notPureExtractedList.txt" ), "r")
    lines = f.readlines()
    f.close()
    
    
    if not os.path.isdir(notPureImageRootpath):
        os.mkdir(notPureImageRootpath)
    if not os.path.isdir(notPureXmlRootpath):
        os.mkdir(notPureXmlRootpath)
        
        
    if is_Ratio == False:
        sampled = random.sample(range(0,len(lines)), notPureValidCount)
        validList = []
        for index in sampled:
            validList.append(lines[index].strip())
        
    for line in lines:
        line = line.strip()
        print(line, end="   ")
        print("Not pure 이미지, xml 복사하는 중...")
        if is_Ratio == True:
            try:
                thres = random.random()
                fname, fext = os.path.splitext(line)
                if thres > validRatio:
                    dataType = "train"
                else:
                    dataType = "valid"
                if dataType == "train":
                    shutil.copy(getImagePath(line), os.path.join(notPureImageRootpath, "train"))
                    shutil.copy(getXmlPath(line), os.path.join(notPureXmlRootpath,  "train"))
                    notPureTrain.write("Not pure:" + dataType + " ")
                    notPureTrain.write(line)
                    notPureTrain.write("\n")
                else:
                    shutil.copy(getImagePath(line), os.path.join(notPureImageRootpath,  "valid"))
                    shutil.copy(getXmlPath(line), os.path.join(notPureXmlRootpath, "valid"))
                    notPureValid.write("Not pure:" + dataType + " ")
                    notPureValid.write(line)
                    notPureValid.write("\n")
                ff.write("Not pure:" + dataType + " ")
                ff.write(line)
                ff.write("\n")
            except:
                ff.write("except: ")
                ff.write(line)
                ff.write("\n")
        else:
            try:
                fname, fext = os.path.splitext(line)
                if line in validList:
                    dataType = "valid"
                    shutil.copy(getImagePath(line), os.path.join(notPureImageRootpath, "valid"))
                    shutil.copy(getXmlPath(line), os.path.join(notPureXmlRootpath,  "valid"))
                    notPureValid.write("not Pure:" + dataType + " ")
                    notPureValid.write(line)
                    notPureValid.write("\n")
                else:
                    dataType = "train"
                    shutil.copy(getImagePath(line), os.path.join(notPureImageRootpath, "train"))
                    shutil.copy(getXmlPath(line), os.path.join(notPureXmlRootpath, "train"))
                    notPureTrain.write("Not pure:" + dataType + " ")
                    notPureTrain.write(line)
                    notPureTrain.write("\n")
                ff.write("Not pure:" + dataType + " ")
                ff.write(line)
                ff.write("\n")
            except:
                ff.write("except: ")
                ff.write(line)
                ff.write("\n")
                
                
        
    print("복사완료")
    
    ff.close()
    pureTrain.close()
    pureValid.close()
    notPureTrain.close()
    notPureValid.close()
    
    
makeXmlByCvatxml()
readCvatxml()
pureExtract()

# while True:
#     pass

    
    
    
    

