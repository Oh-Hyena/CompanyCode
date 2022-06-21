# cvatxml 파일을 읽어서 xx개씩 img crop 하기

import os
import cv2
import numpy as np
import xml.etree.ElementTree as ET
import sys


cvatxmlDir = r"E:\0610\seongnamfalse0125_cvatxml"
imgDir     = r"E:\0610\seongnamfalse0125_img"
resDir     = r"E:\0610\att_seongnamfalse0125_img"


ENCODING_FORMAT = "UTF-8"
resFolderName   = "att_seongnamfalse0125"
fileNum         = 150


def checkInitDirValid():
    if os.path.isdir(cvatxmlDir) is False:
        print(f'[Error] {cvatxmlDir} is invalid')
        return False
    if os.path.isdir(imgDir) is False:
        print(f'[Error] {imgDir} is invalid')
        return False
    if os.path.isdir(resDir) is False:
        print(f'[Error] {resDir} is invalid')
        return False
    
    return True


def makeCropResDir(resDir):
    if not os.path.isdir(resDir):
        os.makedirs(resDir, exist_ok=True)


def makeNoteList(cvatxmlDir):
    noteList     = []
    fileNameList = []
    
    for root, dirs, files in os.walk(cvatxmlDir):
        for file in files:
            tree = ET.parse(os.path.join(root, file))   # tree = <xml.etree.ElementTree.ElementTree object at 0x0000023A184808B0>
            note = tree.getroot()                       # note = <Element 'annotations' at 0x00000263327672C0>
            noteList.append(note)
            
            fileName  = file.split(".")[0]
            fileNameList.append(fileName)
            
    return noteList, fileNameList
        

def pickAnnoInfo(noteList, fileNameList): 
    xmlInfoList = []       
    
    for note, filename in zip(noteList, fileNameList): 
        
        for image in note.findall("image"):             # image = <Element 'image' at 0x0000015F12DA5680>
            name = image.get("name")                    # name = seongnamfalse1112_000009_00147.jpg
            
            for box in image.findall("box"):
                label     = box.get("label")            # label = car
                attribute = box.find("attribute").text  # attribute = pure
                
                xtl  = int(float(box.get("xtl")))       # xtl, ytl, xbr, ybr = 352 126 371 143
                ytl  = int(float(box.get("ytl")))
                xbr  = int(float(box.get("xbr")))
                ybr  = int(float(box.get("ybr")))
                
                xlen = abs(int(xtl)-int(xbr))
                ylen = abs(int(ytl)-int(ybr))
                
                if (label == "person") and (attribute == "pure") and (xlen > 25) and (ylen > 25):
                    #                        {0},     {1},  {2},  {3},  {4},  {5}
                    xmlInfoList.append(f'{filename},{name},{ytl},{ybr},{xtl},{xbr}')
                    
    return xmlInfoList


def imread(filename, flags=cv2.IMREAD_COLOR, dtype=np.uint8):
    try:
        n   = np.fromfile(filename, dtype)
        img = cv2.imdecode(n, flags)
        return img
    
    except Exception as e:
        print(f"imread error : {e}")
        return None
    
    
def imwrite(filename, img, params=None):
    try:
        ext       = os.path.splitext(filename)[1]
        result, n = cv2.imencode(ext, img, params)

        if result:
             with open(filename, mode='w+b') as f:
                 n.tofile(f)
             return True
        else:
             return False
         
    except Exception as e:
        print(f"imwrite error : {e}")
        return False


def numCount(length, num):
    rotate = length - len(num)
    if rotate > 0:
        for i in range(rotate):
            num = "0" + num
    return num


def makeEachDestDir(Count):  
    folderName = resFolderName + "_" + numCount(6, str(Count))
    DestDir = os.path.join(resDir, folderName)
    os.makedirs(DestDir, exist_ok=True)
    
    return DestDir


def cropPerson(xmlInfoList, imgDir):
    folderCount     = 1
    fileCount       = 1

    for each in xmlInfoList:
        DestDir = makeEachDestDir(folderCount)
        
        each    = each.split(",")
        imgPath = os.path.join(imgDir, each[0])
        img     = imread(os.path.join(imgPath, each[1]), cv2.IMREAD_COLOR)
        
        if img is None:
            break
        src = img.copy()
        
        cropImg  = src[int(each[2]):int(each[3]), int(each[4]):int(each[5])]
    
        filename = each[1].split(".")[0] + "_" + numCount(6, str(fileCount)) + ".jpg"
        imwrite(os.path.join(DestDir, filename), cropImg)
            
        fileCount += 1
        
        if fileCount == fileNum + 1:
            folderCount += 1
            fileCount    = 1         
        


if __name__ == "__main__":
    makeCropResDir(resDir)
    
    if checkInitDirValid() is False:
        sys.exit(-1)
    
    noteList, fileNameList = makeNoteList(cvatxmlDir)
    xmlInfoList            = pickAnnoInfo(noteList, fileNameList)
    cropPerson(xmlInfoList, imgDir)
    
    