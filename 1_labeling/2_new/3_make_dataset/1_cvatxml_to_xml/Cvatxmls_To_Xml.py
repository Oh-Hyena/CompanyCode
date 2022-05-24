# Import Packages and Modules
# Standard Library
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
import json
import xml.etree.ElementTree as ET
from xml.dom import minidom
from lxml import etree
from PIL import Image
import os
import pickle
import sys
import time
import datetime
import shutil
import random
import io
import label
import csv


# Installed Library - CV
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
import cv2

# Add Import Path
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../Core'))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../'))

# Custom Modules
# python -m PyQt6.uic.pyuic -x main.ui -o ui_main.py
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
from Core.general_function import ErrorLog, NoticeLog, RunFunctionLog, ShowLog, callername, filename, funcname, \
    showLog  # General Function Anyware use it
from Core.send_argv import SendArgvClass
from Core.json_settings import Settings

# 변수 목록 : setting.json 혹은 main.py UI에서 값을 읽어오는 목록들
# 만약 UseJson 변수값이 False 이고, main.py UI에서 DefualtRun 으로 돌린다면 아래값 그대로 쓸...걸요?
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
UseJson  = True
LogPath  = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../save.txt')      # CAN EDIT
AddWork  = True                                                                         # CAN EDIT
StartIdx = 0                                                                            # CAN EDIT

# Current RunFunction Result Directory
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
UseSeperateResultDir = False
ResultDir      = r'D:/Ai_Save'                                                          # CAN EDIT
ResultDir10Xml = '10class_xml'
ResultDirTxt   = '2class_txt'   # "2class_txt", "6class_txt", "7class_txt"              # NEED EDIT!!!!!!
ResultDirImg   = '2class_img'   # "2class_img", "6class_img", "7class_img"              # NEED EDIT!!!!!!
ResultDirXml   = '2class_xml'   # "2class_xml", "6class_xml", "7class_xml"              # NEED EDIT!!!!!!

# Var For Run Function
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
FromFormat    = "xml"                                                                   # NEED EDIT
ToFormat10Xml = 'xml'                                                                   # NEED EDIT
ToFormatTxt   = "txt"                                                                   # NEED EDIT
ToFormatImg   = "jpg"                                                                   # NEED EDIT
ToFormatXml   = "xml"                                                                   # NEED EDIT
CheckWord     = "cvatxmls"                                                              # NEED EDIT
ExceptionWord = "xml"                                                                   # NEED EDIT

ClassChoice = "6Class"  # "2Class", 6Class", 7Class" - Default 2Class                   # NEED EDIT!!!!!!

changeList  = ['bus', 'truck', 'excavator', 'forklift', 'ladder truck', 'unknown car']  # NEED EDIT
nameList    = ['person', 'car']                                                         # NEED EDIT

TotalRunCount = 0
CurRunCount   = StartIdx

# 중간값과 결과값 저장하는 리스트들
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
run_dir_list           = []  # 이 함수를 실행해서 xml, txt, img파일로 바꿀 cvatxmls이 들어있는 경로들 리스트
xml10_result_dir_list  = []  # 이 함수 실행 결과(10class_xml)를 저장할 결과 폴더 리스트
txt_result_dir_list    = []  # 이 함수 실행 결과(txt)를 저장할 결과 폴더 리스트
img_result_dir_list    = []  # 이 함수 실행 결과(img)를 저장할 결과 폴더 리스트
xml_result_dir_list    = []  # 이 함수 실행 결과(xml)를 저장할 결과 폴더 리스트
uncertain_dir_list     = []  # CheckWord는 아닌데 ExceptionWord에도 걸리지 않은 애매한 리스트들

# TColor
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
TRed    = "\x1b[31m"
TGreen  = "\x1b[32m"
TYellow = "\x1b[33m"
TSky    = "\x1b[36m"
TReset  = "\x1b[0m"


# 현재 파일이 실행되기 전, main.py 에서 가져온 값이나 settings.json 파일 값을 현재 파일 변수에 대입하는 함수
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
def PretreatmentSettings():
    global LogPath, AddWork, StartIdx, ResultDir, CurRunCount

    # 실행 인자가 자기 자신밖에 없다 == main.py에서 실행시킨 게 아니라 해당 프로그램 자체로 실행시켰을 때
    # 어지간하면 main.py 이용해서 실행시켜주세용...
    # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
    if len(sys.argv) == 1:
        if UseJson:
            EditPath_Json = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../')
            jsonSetting   = Settings(EditPath_Json)
            fileName      = filename()

            LogPath   = jsonSetting.items['run_function_argv'][fileName]['LogPath']['CurValue']
            AddWork   = jsonSetting.items['run_function_argv'][fileName]['AddWork']['CurValue']
            StartIdx  = jsonSetting.items['run_function_argv'][fileName]['StartIndex']['CurValue']
            ResultDir = jsonSetting.items['run_function_argv'][fileName]['ResDir']['CurValue']
        else:
            # settings.json 파일도 안 쓰고 그냥 내부 Local 변수로만 작동시킬 때
            return

    # 실행 인자값이 main.py에서 추가로 넘어왔을 때 처리하는 부분                            # NEED EDIT
    # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
    else:
        _sep = '$$$'

        for arg in sys.argv:
            try:
                ExtractValue = arg.split(_sep)[-1]
            except Exception as e:
                NoticeLog(f"{arg} is Not Valid SendArgv Value!!")

            if "LogPath" in arg and ExtractValue != "NoneChanged":
                LogPath = ExtractValue

            elif "StartIndex" in arg:
                StartIdx = int(ExtractValue)
                CurRunCount = StartIdx

            elif "UncertainOn" in arg:
                if ExtractValue == "ON":
                    AddWork = True
                else:
                    AddWork = False

            elif "resDir" in arg and ExtractValue != "NoneChanged":
                ResultDir = ExtractValue


# 시작 로그 함수
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
def StartLog():
    showLog("\n==============================================================================")
    showLog(f"# RunFile : {TSky}{filename()}{TReset}")
    showLog(f"# CurTime : {datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')}")
    showLog("------------------------------------------------------------------------------")
    showLog(f"# CurClass: {ClassChoice}")
    showLog("------------------------------------------------------------------------------")
    showLog(f"# LogPath : {LogPath}")
    showLog(f"# StrtIdx : {StartIdx}")
    showLog(f"# ResPath : {ResultDir} _ ( Use Full Seperate Directory : {UseSeperateResultDir} )")
    showLog(f"# AddWork : {str(AddWork)}")
    showLog("==============================================================================\n")


# 끝 로그 함수
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
def EndLog(PathCount, FileCount, ResultTime):
    showLog("==============================================================================")
    showLog(f"# CurTime   : {datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')}")
    showLog(f"# PathCount : {PathCount} Directories")
    showLog(f"# FileCount : {FileCount} Files Run")
    showLog(f"# SpendTime : {ResultTime}")
    showLog("==============================================================================\n")


# LogPath 에 기입된 경로에서 main.py UI를 통해 추출한 최하단 디렉토리 리스트를 불러오는 함수
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
def load_Logfile(savePath):
    RunFunctionLog(f"when \'{savePath}\'")
    path_list = []
    try:
        with open(savePath, 'rb') as f:
            path_list = pickle.load(f)
        return path_list
    except Exception as e:
        print("Load Data Error!!")
        return False


# CheckWord 와 ExceptionWord 기준으로 작업할 디렉토리를 선별하는 함수
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
def filter_path_is_in_it_format(pathList):
    RunFunctionLog(f"[ Check Path Name : {TGreen}{CheckWord}{TReset} / Exception Path Name : {TRed}{ExceptionWord}{TReset} ]\n")

    CorrectCount   = 0
    UncertainCount = 0
    ExceptionCount = 0

    filter_path_list = []
    for path in pathList:
        if ExceptionWord:
            if ExceptionWord in path:
                print(f"{TRed}{path}{TReset}")
                ExceptionCount += 1
                continue
            elif CheckWord in path:
                print(f"{TGreen}{path}{TReset}")
                filter_path_list.append(path)
                CorrectCount += 1
            else:
                print(f"{TYellow}{path}{TReset}")
                uncertain_dir_list.append(path)
                UncertainCount += 1
        else:
            if CheckWord in path:
                print(f"{TGreen}{path}{TReset}")
                filter_path_list.append(path)
                CorrectCount += 1
            else:
                print(f"{TYellow}{path}{TReset}")
                uncertain_dir_list.append(path)
                UncertainCount += 1

    TotalCount = CorrectCount + UncertainCount + ExceptionCount
    showLog(f"\n[ {funcname()}() Result ]")
    showLog(f"- TotalCount     : {TotalCount}")
    showLog(f"- CorrectCount   : {CorrectCount}")
    showLog(f"- UncertainCount : {UncertainCount}")
    showLog(f"- ExceptionCount : {ExceptionCount}\n")

    return filter_path_list


# run_dir_list 에 매칭되는 각각의 xml_result_dir_list, txt_result_dir_list 를 만드는 함수
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
# run_dir_list 중 하나씩 패스를 뽑아 작업하는 함수
def make_result_dir(path):
    global xml10_result_dir_list, xml_result_dir_list, img_result_dir_list, txt_result_dir_list

    xml10_result_dir = ""
    xml_result_dir = ""
    img_result_dir = ""
    txt_result_dir = ""

    # 새로 폴더 생성해서 저장
    if UseSeperateResultDir:
        path = os.path.splitdrive(path)[-1]
        result_dir = ResultDir + path
        result_dir = os.path.normpath(result_dir)
        result_dir_list.append(result_dir)

    # Default : 개별 폴더 동일 위치에 이름만 바꿔서 폴더 생성
    else:
        xml10_result_dir = os.path.join(path, f'../{ResultDir10Xml}')
        xml10_result_dir_list.append(xml10_result_dir)

        txt_result_dir = os.path.join(path, f'../{ResultDirTxt}')
        txt_result_dir_list.append(txt_result_dir)

        img_result_dir = os.path.join(path, f'../{ResultDirImg}')
        img_result_dir_list.append(img_result_dir)

        xml_result_dir = os.path.join(path, f'../{ResultDirXml}')
        xml_result_dir_list.append(xml_result_dir)

    if not os.path.isdir(xml10_result_dir):
        os.makedirs(xml10_result_dir)

    if not os.path.isdir(txt_result_dir):
        os.makedirs(txt_result_dir)

    if not os.path.isdir(img_result_dir):
        os.makedirs(img_result_dir)

    if not os.path.isdir(xml_result_dir):
        os.makedirs(xml_result_dir)


# 전체 run_dir_list 에 대해서 make_result_dir 함수를 돌리는 총괄 함수
def make_result_dirs(path_list):
    for path in path_list:
        make_result_dir(path)
    showLog(f"[ {funcname()}() Done : {len(path_list)*3} dirs ]\n")


# cvatxmls 로 original 10class_xml 을 만드는 함수
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
def cvatxmls_to_10class_xml(note, run_file_name):
    # run_file_name 은 cvatxml 파일에 대응되는 xml 파일 이름이어야함
    # ex) 1_cvatxml.xml 파일이 대상 ( note ) 입력값이라면 run_file_name은 1_xml.xml

    """
    cvatxmllist = os.listdir(cvatxmlRootpath)
    if not os.path.isdir(xmlRootpath):
        os.mkdir(xmlRootpath)
    for cvatxml in cvatxmllist:
        if cvatxml.endswith(".xml"):
            tree = ET.parse(os.path.join(cvatxmlRootpath, cvatxml))
            note = tree.getroot()
    """

    with open(run_file_name, "w") as f:
        for image in note.findall("image"):
            name   = image.get("name")
            width  = image.get("width")
            height = image.get("height")

            annotation = ET.Element("annotation")
            ET.SubElement(annotation, "folder").text    = ""
            ET.SubElement(annotation, "filename").text  = name
            ET.SubElement(annotation, "segmented").text = "0"

            sourceTag = ET.SubElement(annotation, "source")
            ET.SubElement(sourceTag, "database").text = "Unknown"

            sizeTag = ET.SubElement(annotation, "size")
            ET.SubElement(sizeTag, "height").text = str(int(height))
            ET.SubElement(sizeTag, "width").text  = str(int(width))
            ET.SubElement(sizeTag, "depth").text  = "3"

            for box in image.findall("box"):
                label = box.get("label")
                xtl   = box.get("xtl")
                ytl   = box.get("ytl")
                xbr   = box.get("xbr")
                ybr   = box.get("ybr")

                xtl   = str(int(float(xtl)))
                ytl   = str(int(float(ytl)))
                xbr   = str(int(float(xbr)))
                ybr   = str(int(float(ybr)))

                objectTag = ET.SubElement(annotation, "object")
                ET.SubElement(objectTag, "name").text      = label
                ET.SubElement(objectTag, "pose").text      = "Unspecified"
                ET.SubElement(objectTag, "difficult").text = "0"
                ET.SubElement(objectTag, "truncated").text = "0"

                bndboxTag = ET.SubElement(objectTag, "bndbox")
                ET.SubElement(bndboxTag, "xmin").text = xtl
                ET.SubElement(bndboxTag, "ymin").text = ytl
                ET.SubElement(bndboxTag, "xmax").text = xbr
                ET.SubElement(bndboxTag, "ymax").text = ybr

            pretty = minidom.parseString(ET.tostring(annotation)).toprettyxml(encoding="utf-8")
            f.write(pretty)


# Calculate Function
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
def convert_xywh(dw, dy, xmin, xmax, ymin, ymax):
    xywh = [((xmin + xmax) / 2.0) * dw, ((ymin + ymax) / 2.0) * dy,
            (xmax - xmin) * dw, (ymax - ymin) * dy
            ]  # YOLO의 영역 표시방법을 계산식으로 써놓은 모습.

    return " ".join(map(str, xywh))  # [x,y,w,h] -> "x y w h"


# 2, 6, 7 클래스로 바꾸는 함수
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
def ClassChange():
    global changeList, nameList

    if ClassChoice == "2Class":
        changeList = ['bus', 'truck', 'excavator', 'forklift', 'ladder truck', 'unknown car']
        nameList = ['person', 'car']
    elif ClassChoice == "6Class":
        changeList = ['excavator', 'forklift', 'ladder truck', 'unknown car']
        nameList = ['person', 'car', 'bus', 'truck', 'bicycle', 'motorbike']
    elif ClassChoice == "7Class":
        changeList = ['excavator', 'forklift', 'ladder truck']
        nameList = ['person', 'car', 'bus', 'truck', 'bicycle', 'unknown car', 'motorbike']


# 10class_xml 을 2/6/7 class yolo_txt 로 변환하는 함수
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
def xml_to_txt(note, result_file_name):
    size = note.find('size')
    height = int(size.find('height').text)  # 이미지의 height
    width = int(size.find('width').text)  # 이미지의 width

    # 나눗셈 연산이 가장 연산량 많이 잡아먹으니 for 문 밖에서 처리하기
    dw = 1 / width
    dy = 1 / height

    with open(result_file_name, "w") as f:
        # print(f"- Save : {os.path.splitext(fname)[0]}")

        for child in note.findall('object'):
            yolo_data = ""
            name = child.find('name').text

            if ClassChoice == "2Class":
                if name in changeList:
                    name = "car"
            elif ClassChoice == "6Class":
                if name in changeList:
                    name = "car"
            elif ClassChoice == "7Class":
                if name in changeList:
                    name = "unknown car"

            if name in nameList:
                idx = nameList.index(name)
                bndbox = child.find('bndbox')
                xmin = int(float(bndbox.find('xmin').text))
                ymin = int(float(bndbox.find('ymin').text))
                xmax = int(float(bndbox.find('xmax').text))
                ymax = int(float(bndbox.find('ymax').text))

                yolo_data = convert_xywh(dw, dy, xmin, xmax, ymin, ymax)

                f.write(f"{idx} {yolo_data}\n")


# txt 와 같은 img 가져오는 함수
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
def txt_same_img(cvatxmls_path):
    txt_list = []
    img_files_name = []
    img_file_path  = []
    img_file_name  = []

    img_path = os.path.join(cvatxmls_path, '../img')

    for i in txt_result_dir_list:
        txt_list.append(i[:-4])

    for path, dir, files in os.walk(img_path):
        for file in enumerate(files):
            if file.endswith(ToFormatImg):
                img_files_name.append(file[:-4])
                img_file_path.append(path)
                img_file_name.append(file)

    for i in range(len(img_files_name)):
        for j in range(len(txt_list)):
            if(img_files_name[i] == txt_list[j]):
                img_path      = os.path.join(img_file_path[i], img_file_name[i])
                copy_img_path = os.path.join(ResultDirImg, img_file_name[i])
                shutil.copy(img_path, copy_img_path)


# csv_file 은 각 라인의 컬럼들이 콤마로 분리된 txt 파일 포맷이다.
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
def csv_read(csv_file):
    with open(csv_file, 'r') as cf:
        csv_list = []
        reader = csv.reader(cf, delimiter=' ')     # 콤마 형태 -> ' '로 바꿔서 출력

        for row in reader:
            csv_list.append(row)
            
    return csv_list


def convert_label(eachRowFirstValue):
    # txt 파일 행 별로 맨 앞 숫자 즉 클래스 인덱스를 가져와서 클래스 이름으로 바꾸는 함수

    for idx, name in enumerate(nameList):
        if idx == int(eachRowFirstValue):
            return name


def extract_coord(txt_file, img_width, img_height):
    x_rect_mid  = float(txt_file[1])
    y_rect_mid  = float(txt_file[2])
    width_rect  = float(txt_file[3])
    height_rect = float(txt_file[4])

    calcWidth = img_width * width_rect
    calcHeight = img_height * height_rect

    x_min_rect = (x_rect_mid * img_width) - (calcWidth / 2)
    x_max_rect = x_min_rect + calcWidth

    y_min_rect = (y_rect_mid * img_height) - (calcHeight / 2)
    y_max_rect = y_min_rect + calcHeight

    return x_min_rect, x_max_rect, y_min_rect, y_max_rect


# 2/6/7 class yolo_txt 로 2/6/7 xml 을 구하는 함수
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
def txt_to_xml(pathName):

    fileList = os.listdir(pathName)

    for eachFile in fileList:
        txt_file =  csv_read(eachFile)

        root = etree.Element("annotation")

        img_size   = Image.open(image_info).size

        img_width        = img_size[0]
        image_width      = etree.SubElement(size, "width")
        image_width.text = "%d" % (img_width)

        img_height        = img_size[1]
        image_height      = etree.SubElement(size, "height")
        image_height.text = "%d" % (img_height)

        img_depth        = 3
        image_depth      = etree.SubElement(size, "depth")
        image_depth.text = "%d" % (img_depth)

        folder      = etree.Element("folder")
        folder.text = "%s" % (img_style)
        root.append(folder)

        filename      = etree.Element("filename")
        filename.text = "%s" % (img_name)
        root.append(filename)

        path      = etree.Element("path")
        path.text = "%s" % (save_yolo)
        root.append(path)

        source               = etree.Element("source")
        source_database      = etree.SubElement(source, "database")
        source_database.text = "Unknown"
        root.append(source)

        size = etree.Element("size")
        root.append(size)

        segmented      = etree.Element("segmented")
        segmented.text = "0"
        root.append(segmented)

        for i in range(len(txt_file)):
            label = convert_label(txt_file[i][0])
            x_min_rect, x_max_rect, y_min_rect, y_max_rect = extract_coor(txt_file[i], img_width, img_height)

            object = etree.Element("object")
            root.append(object)

            name      = etree.SubElement(object, "name")
            name.text = "%s" % (label)

            pose      = etree.SubElement(object, "pose")
            pose.text = "Unspecified"

            truncated      = etree.SubElement(object, "truncated")
            truncated.text = "0"

            difficult      = etree.SubElement(object, "difficult")
            difficult.text = "0"

            bndbox = etree.SubElement(object, "bndbox")

            xmin      = etree.SubElement(bndbox, "xmin")
            xmin.text = "%d" % (x_min_rect)
            ymin      = etree.SubElement(bndbox, "ymin")
            ymin.text = "%d" % (y_min_rect)
            xmax      = etree.SubElement(bndbox, "xmax")
            xmax.text = "%d" % (x_max_rect)
            ymax      = etree.SubElement(bndbox, "ymax")
            ymax.text = "%d" % (y_max_rect)

        file_output = etree.tostring(root, pretty_print=True, encoding='UTF-8')
        xml_file = io.open(ResultDirXml + "." + ToFormatXml, 'w', encoding="utf-8")
        xml_file.write(file_output.decode('utf-8'))


# MAIN
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
if __name__ == "__main__":
    # Prefix
    # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
    RunFunctionLog()
    PretreatmentSettings()
    ClassChange()
    StartLog()

    StartTime = time.time()

    # LogPath 에서 최하위 디렉토리 리스트 뽑아와서 유효한 / 확실하지 않은 / 거르는 디렉토리 구별
    # 그 중 유효한 리스트들만 일단 작업 시작
    # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
    run_dir_list  = load_Logfile(LogPath)
    run_dir_list  = filter_path_is_in_it_format(run_dir_list)
    TotalRunCount = len(run_dir_list)

    # 결과값 저장할 디렉토리들 ResultDir 및 run_dir_list 참고해 생성
    # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
    make_result_dirs(run_dir_list)

    format_style              = "." + FromFormat
    xml10_result_format_sytle = "." + ToFormat10Xml
    xml_result_format_sytle   = "." + ToFormatXml
    txt_result_format_sytle   = "." + ToFormatTxt
    slice_fmt_len             = (-1) * len(format_style)
    totalConversionCount      = 0

    # Run Correct Format Directories
    # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
    for run_dir in run_dir_list[StartIdx:]:
        # Extract FileList
        # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
        file_list = os.listdir(run_dir)

        # 나중에 지워도 되는 터미널상 정보 출력 파트
        # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
        len_file_list         = len(file_list)
        percent_count         = len_file_list / 10
        cur_percent_count     = percent_count
        cur_percent           = 10
        totalConversionCount += len_file_list

        showLog(f"[ {TGreen}{CurRunCount + 1:2} / {TotalRunCount}{TReset} ] {run_dir:100} : {len_file_list} 개 작업 예정")

        try:
            # RUN
            # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
            for count, file in enumerate(file_list):
                # 나중에 지워도 되는 터미널상 정보 출력 파트
                # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
                if len_file_list > 1000:
                    if count + 1 > cur_percent_count:
                        showLog(f"\t[ {cur_percent:3}% ] {count + 1:6} / {len_file_list:6} ... {file}")
                        cur_percent_count += percent_count
                        cur_percent += 10

                if count + 1 == len_file_list:
                    showLog(f"\t[ 100% ] Done => {result_dir_list[CurRunCount]}")

                # 실제 작동 함수 부분
                # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
                run_dir = os.path.normpath(run_dir)

                if file.endswith(format_style):  # .xml
                    tree = ET.parse(os.path.join(run_dir, str(file)))
                    note = tree.getroot()

                    result_file_name = os.path.join(result_dir_list[CurRunCount], file[:slice_fmt_len] + result_format_sytle)

                    xml_to_txt(note, result_file_name)

        except Exception as e:
            ErrorLog(f"is that \'{file}\' Format {FromFormat}?")

        CurRunCount += 1

    NoticeLog("Run with Correct Format Directories Done")

    # Run Uncertain Format Directories if 'AddWork == True'
    # 필터링에 걸려지지 않았지만 애매했던 리스트 다시 출력해서 원모어찬스
    # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
    if AddWork:
        NoticeLog("AddWork for Uncertain Derectories Start")
        SelectNum = -1

        # Var for Paging : 1page = 20 idx
        # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
        CurrentPage = 1
        PerPage = 20
        Already_Select_Num_List = []
        Total_Uncertain_Num = len(uncertain_dir_list)

        Total_Page_Num = (Total_Uncertain_Num // PerPage) + 1
        if Total_Uncertain_Num % PerPage == 0:
            Total_Page_Num -= 1

        # Run while Select 0
        # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
        while True:
            # 선택 문구 출력 문장
            # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
            printPrefix = f"==== [ PAGE {CurrentPage:2} / {Total_Page_Num:2} ] "
            print(printPrefix, "=" * 100)

            PageCount = (CurrentPage - 1) * PerPage
            for count, dirName in enumerate(uncertain_dir_list[PageCount:PageCount + PerPage]):
                Idx = PageCount + count + 1
                if str(Idx) in Already_Select_Num_List:
                    print(f"{TSky}", end='')
                print(f"[ {PageCount + count + 1} ] {dirName}{TReset}")

            suffixLen = len(printPrefix) + 100 - 14
            print("[ <- ] ", "=" * suffixLen, " [ -> ]")
            print("Select Add Work Dir Num ( Exit[0] Prev[p] Next[n] ) : ")

            SelectNum = input()

            # Change Page
            # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
            if SelectNum == "p" or SelectNum == "P":
                if CurrentPage == 1:
                    continue
                else:
                    CurrentPage -= 1
                    continue
            elif SelectNum == "n" or SelectNum == "N":
                if CurrentPage == Total_Page_Num:
                    continue
                else:
                    CurrentPage += 1
                    continue

            try:
                SelectNum = int(SelectNum)
            except Exception as e:
                continue

            if SelectNum == 0:
                break

            Already_Select_Num_List.append(str(SelectNum))  # 선택한 번호 저장
            SelectNum -= 1  # 선택한 번호 -> Index
            SelectPath = uncertain_dir_list[SelectNum]

            # 선택한 항목 실제 실행 파트
            # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
            make_result_dir(SelectPath)
            file_list = os.listdir(SelectPath)

            # 나중에 지워도 되는 터미널상 정보 출력 파트
            # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
            len_file_list = len(file_list)
            percent_count = len_file_list / 10
            cur_percent_count = percent_count
            cur_percent = 10
            totalConversionCount += len_file_list

            showLog(f"[ AddWork ] {SelectPath:100} : {len_file_list} 개 예정")

            try:
                # RUN
                # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
                for count, file in enumerate(file_list):
                    # 나중에 지워도 되는 터미널상 정보 출력 파트
                    # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
                    if len_file_list > 1000:
                        if count + 1 > cur_percent_count:
                            showLog(f"\t[ {cur_percent:3}% ] {count + 1:6} / {len_file_list:6} ... {file}")
                            cur_percent_count += percent_count
                            cur_percent += 10

                    if count + 1 == len_file_list:
                        showLog(f"\t[ 100% ] Done => {result_dir_list[CurRunCount]}")

                    # 실제 작동 함수 부분
                    # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
                    SelectPath = os.path.normpath(SelectPath)

                    if file.endswith(format_style):  # .xml
                        tree = ET.parse(os.path.join(SelectPath, str(file)))
                        note = tree.getroot()

                        result_file_name = os.path.join(result_dir_list[CurRunCount],
                                                        file[:slice_fmt_len] + result_format_sytle)

                        xml_to_txt(note, result_file_name)

            except Exception as e:
                ErrorLog(f"is that \'{file}\' Format {FromFormat}?")

            CurRunCount += 1

    RunTime = time.time() - StartTime
    ResultTime = str(datetime.timedelta(seconds=RunTime)).split(".")
    ResultTime = ResultTime[0]

    NoticeLog("RunFunction - Xml_To_Text Done")
    EndLog(len(result_dir_list), totalConversionCount, ResultTime)
