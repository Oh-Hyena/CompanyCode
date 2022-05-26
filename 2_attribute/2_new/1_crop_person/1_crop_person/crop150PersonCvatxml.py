import os
import cv2
import numpy as np
import xml.etree.ElementTree as ET


xmlDir     = r"E:\hyena\3_dataset\seongnamfalse\seongnamfalse0211\seongnamfalse0211_xml"
imgDir     = r"E:\hyena\3_dataset\seongnamfalse\seongnamfalse0211\seongnamfalse0211_img"
cropResDir = r"E:\hyena\3_dataset\seongnamfalse\seongnamfalse0211\crop"

cropImgNum = 500



def make_cropResDir(cropResDir):
    if not os.path.isdir(cropResDir):
        os.makedirs(cropResDir, exist_ok=True)
        print("ResDir 생성")


def make_noteList(xmlDir):
    noteList = []
    fileNameList = []
    for root, dirs, files in os.walk(xmlDir):
        for file in files:
            # tree = <xml.etree.ElementTree.ElementTree object at 0x0000023A184808B0>
            tree = ET.parse(os.path.join(root, file))
            # note = <Element 'annotations' at 0x00000263327672C0>
            note = tree.getroot()
            noteList.append(note)
            
            fileName  = file.split(".")[0]
            fileNameList.append(fileName)
            
    firstName = file.split("_")[0]
    return noteList, fileNameList, firstName
        

def pick_annoInfo(noteList, fileNameList, firstName): 
    xmlInfoList = []       
    
    for note, filename in zip(noteList, fileNameList):
        # image = <Element 'image' at 0x0000015F12DA5680>
        for image in note.findall("image"):
            # name = seongnamfalse1112_000009_00147.jpg
            name = image.get("name")
            for box in image.findall("box"):
                # label = car
                label = box.get("label")
                # attribute = cloudy
                attribute = box.find("attribute").text
                
                # xtl, ytl, xbr, ybr = 352 126 371 143
                xtl = int(float(box.get("xtl")))
                ytl = int(float(box.get("ytl")))
                xbr = int(float(box.get("xbr")))
                ybr = int(float(box.get("ybr")))
                
                xlen = abs(int(xtl)-int(xbr))
                ylen = abs(int(ytl)-int(ybr))
                #                        {0},     {1},   {2},      {3},     {4},   {5},   {6},  {7},  {8},  {9},    {10}
                xmlInfoList.append(f'{filename},{name},{label},{attribute},{xlen},{ylen},{ytl},{ybr},{xtl},{xbr},{firstName}')
                # list에 append할 때 조건에 해당하는 것만 append 하게 하기
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


def num_count(length, num):
    rotate = length - len(num)
    if rotate > 0:
        for i in range(rotate):
            num = "0" + num
    return num


def crop_person(xmlInfoList, imgDir):
    folderCount = 1
    fileCount   = 0

    for each in xmlInfoList:
        each = each.split(",")
        if ('person' in each[2]) and ('pure' in each[3]) and (int(each[4]) > 25) and (int(each[5]) > 25 ):
            imgPath = os.path.join(imgDir, each[0])
            img     = imread(os.path.join(imgPath, each[1]), cv2.IMREAD_COLOR)
            
            if img is None:
                break
            src = img.copy()
            
            cropImg = src[int(each[6]):int(each[7]), int(each[8]):int(each[9])]
        
            resPath    = os.path.join(cropResDir, "att_" + each[10] + "_" + num_count(6, str(folderCount)))
            filename   = each[1].split(".")[0] + "_" + num_count(6, str(fileCount)) + ".jpg"
            fileCount += 1
            
            if not os.path.isdir(resPath):
                os.makedirs(resPath, exist_ok=True)
            imwrite(os.path.join(resPath, filename), cropImg)
                
            if fileCount == cropImgNum:
                folderCount += 1
                fileCount = 0                
                
                

if __name__ == "__main__":
    make_cropResDir(cropResDir)
    noteList, fileNameList, firstName = make_noteList(xmlDir)
    xmlInfoList = pick_annoInfo(noteList, fileNameList, firstName)
    crop_person(xmlInfoList, imgDir)
    
    
    