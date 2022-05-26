# Import Packages and Modules
# Standard Library
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
import json
import xml.etree.ElementTree as ET
import os
import pickle
import sys
import datetime

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
from Core.general_function  import ErrorLog, NoticeLog, RunFunctionLog, ShowLog, callername, filename, funcname, showLog  # General Function Anyware use it
from Core.send_argv         import SendArgvClass
from Core.json_settings     import Settings

# 변수 목록 : setting.json 혹은 main.py UI에서 값을 읽어오는 목록들
# 만약 UseJson 변수값이 False 이고, main.py UI에서 DefualtRun 으로 돌린다면 아래값 그대로 쓸...걸요?
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
UseJson     = True
LogPath     = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../save.txt')   # CAN EDIT
AddWork     = True                                                                      # CAN EDIT
StartIdx    = 0                                                                         # CAN EDIT

# Current RunFunction Result Directory
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
ResultDir   = r'D:/Ai_Save'                                                             # CAN EDIT

# Var For Run Function
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
FromFormat      = "xml"                                                                 # NEED EDIT
ToFormat        = "txt"                                                                 # NEED EDIT
ExceptionFormat = "cvatxml"                                                             # NEED EDIT

changeList = ['bus', 'truck', 'excavator', 'forklift', 'ladder truck', 'unknown car']   # NEED EDIT
nameList   = ['person', 'car']                                                          # NEED EDIT

TotalRunCount   = 0
CurRunCount     = StartIdx

# 중간값과 결과값 저장하는 리스트들 
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
run_dir_list        = []    # 이 함수를 실행해서 txt파일로 바꿀 xml이 들어있는 경로들 리스트
result_dir_list     = []    # 이 함수 실행 결과를 저장할 결과 폴더 리스트
uncertain_dir_list  = []    # FromFormat은 아닌데 ExceptionFormat에도 걸리지 않은 애매한 리스트들

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
            EditPath_Json   = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../')
            jsonSetting     = Settings(EditPath_Json)
            fileName        = filename()

            LogPath     = jsonSetting.items['run_function_argv'][fileName]['LogPath']['CurValue']
            AddWork     = jsonSetting.items['run_function_argv'][fileName]['AddWork']['CurValue']
            StartIdx    = jsonSetting.items['run_function_argv'][fileName]['StartIndex']['CurValue']
            ResultDir   = jsonSetting.items['run_function_argv'][fileName]['ResDir']['CurValue']
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
    showLog(f"# LogPath : {LogPath}")
    showLog(f"# StrtIdx : {StartIdx}")
    showLog(f"# ResPath : {ResultDir}")
    showLog(f"# AddWork : {str(AddWork)}")
    showLog("==============================================================================\n")
    pass


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


# FromFormat 과 ExceptionFormat 기준으로 작업할 디렉토리를 선별하는 함수
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
def filter_path_is_in_it_format(pathList):
    RunFunctionLog(f"[ Check Path Name : {TGreen}{FromFormat}{TReset} / Exception Path Name : {TRed}{ExceptionFormat}{TReset} ]\n")

    CorrectCount = 0
    UncertainCount = 0
    ExceptionCount = 0

    filter_path_list = []
    for path in pathList:
        if ExceptionFormat:
            if ExceptionFormat in path:
                print(f"{TRed}{path}{TReset}")
                ExceptionCount += 1
                continue
            elif FromFormat in path:
                print(f"{TGreen}{path}{TReset}")
                filter_path_list.append(path)
                CorrectCount += 1
            else:
                uncertain_dir_list.append(path)
                print(f"{TYellow}{path}{TReset}")
                UncertainCount += 1
        else:
            if FromFormat in path:
                print(f"{TGreen}{path}{TReset}")
                filter_path_list.append(path)
                CorrectCount += 1
            else:
                uncertain_dir_list.append(path)
                print(f"{TYellow}{path}{TReset}")
                UncertainCount += 1

    TotalCount = CorrectCount + UncertainCount + ExceptionCount
    showLog(f"\n[ {funcname()}() Result ]")
    showLog(f"- TotalCount     : {TotalCount}")
    showLog(f"- CorrectCount   : {CorrectCount}")
    showLog(f"- UncertainCount : {UncertainCount}")
    showLog(f"- ExceptionCount : {ExceptionCount}\n")

    return filter_path_list


# run_dir_list 에 매칭되는 각각의 result_dir_list 를 만드는 함수
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
# run_dir_list 중 하나씩 패스를 뽑아 작업하는 함수
def make_result_dir(path):
    global result_dir_list

    path = os.path.splitdrive(path)[-1]
    result_dir = ResultDir + path
    result_dir = os.path.normpath(result_dir)

    result_dir_list.append(result_dir)

    if not os.path.isdir(result_dir):
        os.makedirs(result_dir)

# 전체 run_dir_list 에 대해서 make_result_dir 함수를 돌리는 총괄 함수
def make_result_dirs(path_list):
    for path in path_list:
        make_result_dir(path)
    showLog(f"[ {funcname()}() Done : {len(path_list)} dirs ]\n")


# Calculate Function
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
def convert_xywh(dw,dy,xmin,xmax,ymin,ymax):
    xywh =  [   ((xmin+xmax)/2.0)*dw,  ((ymin+ymax)/2.0)*dy,
                (xmax-xmin)*dw,        (ymax-ymin)*dy
            ]       # YOLO의 영역 표시방법을 계산식으로 써놓은 모습.
    return " ".join(map(str, xywh))     # [x,y,w,h] -> "x y w h"


# XML 파일을 계산 후 TXT 파일로 만드는 실제 함수
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
def xml_to_txt(note, result_file_name):
    size    = note.find('size')
    height  = int(size.find('height').text)     # 이미지의 height
    width   = int(size.find('width').text)      # 이미지의 width

    # 나눗셈 연산이 가장 연산량 많이 잡아먹으니 for 문 밖에서 처리하기
    dw = 1/width
    dy = 1/height

    with open(result_file_name, "w") as f:
        # print(f"- Save : {os.path.splitext(fname)[0]}")

        for child in note.findall('object'):
            yolo_data   = ""
            name        = child.find('name').text

            if name in changeList:
                name = "car"

            if name in nameList:
                idx = nameList.index(name)
                bndbox = child.find('bndbox')
                xmin = int(float(bndbox.find('xmin').text))
                ymin = int(float(bndbox.find('ymin').text))
                xmax = int(float(bndbox.find('xmax').text))
                ymax = int(float(bndbox.find('ymax').text))

                yolo_data = convert_xywh(dw, dy, xmin, xmax, ymin, ymax)

                f.write(f"{idx} {yolo_data}\n")


# MAIN
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
if __name__ == "__main__":
    # Prefix
    # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
    RunFunctionLog()
    PretreatmentSettings()
    StartLog()

    # LogPath 에서 최하위 디렉토리 리스트 뽑아와서 유효한 / 확실하지 않은 / 거르는 디렉토리 구별
    # 그 중 유효한 리스트들만 일단 작업 시작
    # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
    run_dir_list    = load_Logfile(LogPath)
    run_dir_list    = filter_path_is_in_it_format(run_dir_list)
    TotalRunCount   = len(run_dir_list)

    # 결과값 저장할 디렉토리들 ResultDir 및 run_dir_list 참고해 생성
    # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
    make_result_dirs(run_dir_list)

    format_style            = "." + FromFormat
    result_format_sytle     = "." + ToFormat
    slice_fmt_len           = (-1) * len(format_style)
    totalConversionCount    = 0
    
    # Run Correct Format Directories
    # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
    for run_dir in run_dir_list[StartIdx:]:
        # Extract FileList
        # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
        file_list = os.listdir(run_dir)

        # 나중에 지워도 되는 터미널상 정보 출력 파트
        # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
        len_file_list           = len(file_list)
        percent_count           = len_file_list / 10
        cur_percent_count       = percent_count
        cur_percent             = 10
        totalConversionCount    += len_file_list

        showLog(f"[ {TGreen}{CurRunCount+1:2} / {TotalRunCount}{TReset} ] {run_dir:100} : {len_file_list} 개 작업 예정")

        try:
            # RUN
            # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
            for count, file in enumerate(file_list):
                # 나중에 지워도 되는 터미널상 정보 출력 파트
                # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
                if len_file_list > 1000:
                    if count + 1 > cur_percent_count:
                        showLog(f"\t[ {cur_percent:3}% ] {count+1:6} / {len_file_list:6} ...")
                        cur_percent_count   += percent_count
                        cur_percent         += 10

                if count + 1 == len_file_list:
                    showLog(f"\t[ 100% ] Done => {result_dir_list[CurRunCount]}")

                # 실제 작동 함수 부분
                # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
                run_dir = os.path.normpath(run_dir)

                if file.endswith(format_style): # .xml
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
        
        Total_Page_Num = Total_Uncertain_Num // PerPage
        if Total_Uncertain_Num % PerPage == 0:
            Total_Page_Num -= 1

        # Run while Select 0
        # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
        while True:
            # 선택 문구 출력 문장
            # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
            printPrefix = f"==== [ PAGE {CurrentPage:2} / {Total_Page_Num:2} ] "
            print(printPrefix, "="*100)

            PageCount = (CurrentPage - 1) * PerPage
            for count, dirName in enumerate(uncertain_dir_list[PageCount:PageCount+PerPage]):
                Idx = PageCount + count + 1
                if str(Idx) in Already_Select_Num_List:
                    print(f"{TSky}", end='')
                print(f"[ {PageCount + count + 1} ] {dirName}{TReset}")

            suffixLen = len(printPrefix) + 100
            print("="*suffixLen)
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
            SelectNum -= 1                                  # 선택한 번호 -> Index
            SelectPath = uncertain_dir_list[SelectNum]            
            
            # 선택한 항목 실제 실행 파트
            # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
            make_result_dir(SelectPath)
            file_list = os.listdir(SelectPath)

            # 나중에 지워도 되는 터미널상 정보 출력 파트    <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< 여기부터!!
            # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
            len_file_list           = len(file_list)
            percent_count           = len_file_list / 10
            cur_percent_count       = percent_count
            cur_percent             = 10
            totalConversionCount    += len_file_list

            showLog(f"[ {TGreen}{CurRunCount+1:2} / {TotalRunCount}{TReset} ] {run_dir:100} : {len_file_list} 개 작업 예정")

            try:
                # RUN
                # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
                for count, file in enumerate(file_list):
                    # 나중에 지워도 되는 터미널상 정보 출력 파트
                    # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
                    if len_file_list > 1000:
                        if count + 1 > cur_percent_count:
                            showLog(f"\t[ {cur_percent:3}% ] {count+1:6} / {len_file_list:6} ...")
                            cur_percent_count   += percent_count
                            cur_percent         += 10

                    if count + 1 == len_file_list:
                        showLog(f"\t[ 100% ] Done => {result_dir_list[CurRunCount]}")

                    # 실제 작동 함수 부분
                    # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
                    run_dir = os.path.normpath(run_dir)

                    if file.endswith(format_style): # .xml
                        tree = ET.parse(os.path.join(run_dir, str(file)))
                        note = tree.getroot()

                        result_file_name = os.path.join(result_dir_list[CurRunCount], file[:slice_fmt_len] + result_format_sytle)
                        
                        xml_to_txt(note, result_file_name)

            except Exception as e:
                ErrorLog(f"is that \'{file}\' Format {FromFormat}?")