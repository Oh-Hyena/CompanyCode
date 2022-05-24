import os
import cv2
import numpy as np
import xml.etree.ElementTree as ET


xmlDir     = r"E:\hyena\3_dataset\seongnamfalse\2021\1112\seongnamfalse1112\test\xml"
imgDir     = r"E:\hyena\3_dataset\seongnamfalse\2021\1112\seongnamfalse1112\test\img"
resDir = r"E:\hyena\3_dataset\seongnamfalse\2021\1112\seongnamfalse1112\test\crop"



def make_resDir(resDir):
    if not os.path.isdir(resDir):
        os.makedirs(resDir, exist_ok=True)
        print("resDir 생성")


def make_noteList(xmlDir):
    noteList = []
    for root, dirs, files in os.walk(xmlDir):
        for file in files:
            # tree = <xml.etree.ElementTree.ElementTree object at 0x0000023A184808B0>
            tree = ET.parse(os.path.join(root, file))
            # note = <Element 'annotations' at 0x00000263327672C0>
            note = tree.getroot()
            noteList.append(note)
            
    return noteList
        

def pick_annoInfo(noteList): 
    xmlInfoList = []       
    
    for note in noteList:
        # image = <Element 'image' at 0x0000015F12DA5680>
        for image in note.findall("image"):
            # name = seongnamfalse1112_000009_00147.jpg
            name = image.get("name")
            nameSplit  = name.split("_")
            firstName  = nameSplit[0] 
            secondName = nameSplit[1]
            DirName   = f'{firstName}_{secondName}'     
               
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
                #                       {0},    {1},    {2},      {3},     {4},   {5},   {6},  {7},  {8},  {9}
                xmlInfoList.append(f'{DirName},{name},{label},{attribute},{xlen},{ylen},{ytl},{ybr},{xtl},{xbr}')
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
        print(e)
        return False


def num_count(length, num):
    rotate = length - len(num)
    if rotate > 0:
        for i in range(rotate):
            num = "0" + num
    return num


def crop_person(xmlInfoList, imgDir):
    count = 1
    
    for each in xmlInfoList:
        each = each.split(",")
        if ('person' in each[2]) and ('pure' in each[3]) and (int(each[4]) > 25) and (int(each[5]) > 25 ):
            imgPath = os.path.join(imgDir, each[0])
            img     = imread(os.path.join(imgPath, each[1]), cv2.IMREAD_COLOR)
            
            if img is None:
                break
            src = img.copy()
            cropImg = src[int(each[6]):int(each[7]), int(each[8]):int(each[9])]
            
            resPath  = os.path.join(resDir, each[0])
            filename = each[1].split(".")[0] + "_" + num_count(6, str(count)) + ".jpg"
            count += 1
            
            # each[1]이 중복되지 않으면 _000001, each[1]이 중복되면 _000001, _000002, _000003으로 증가되게 하기
            if not os.path.isdir(resPath):
                os.makedirs(resPath, exist_ok=True)
            imwrite(os.path.join(resPath, filename), cropImg)
            
        

if __name__ == "__main__":
    make_resDir(resDir)
    noteList = make_noteList(xmlDir)
    xmlInfoList = pick_annoInfo(noteList)
    crop_person(xmlInfoList, imgDir)
    
    