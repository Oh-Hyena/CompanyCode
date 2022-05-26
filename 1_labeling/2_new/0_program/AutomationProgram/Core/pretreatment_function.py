"""
    Pretreatment Part Function.     """

# Import Packages and Modules
# Standard Library
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
import os
import datetime
import copy
import inspect


# Installed Library - QT CORE
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
from qt_core import *


# Custom Modules
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
from Core.general_function import RunFunctionLog, SignalClass, showLog


# Defines
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
ShowLog = copy.copy(CoreShowLog)
TestMode = copy.copy(CoreTestMode)


# 특정 확장자를 가진 파일의 갯수를 해당 경로( 하위 디렉토리 포함 )에서 세는 함수
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
def check_count_with_format_by_files(pathName, signal:SignalClass, checkFormat=".txt"):
    TotalCount = 0

    RunFunctionLog()

    # 하위 디렉토리 파고들면서 확장자명과 일치하는 파일 갯수 카운트
    for _, _, files in os.walk(pathName):
        for eachFile in files:
            if checkFormat in eachFile:
                TotalCount += 1

                # Show Log : 1000번째마다 중간 로그 출력
                if ShowLog and TotalCount % 1000 == 0:
                    sendMsg = f"[ Run ] File Count... [ {TotalCount:6} ] : {eachFile}"
                    signal.s.emit(signal.send_signal_format(sendMsg))
                    showLog(sendMsg)
    
    sendMsg = f"[ Done ] ToTal File Count : {TotalCount}"
    signal.s.emit(signal.send_signal_format(sendMsg))
    showLog(sendMsg)


# RunFunction 폴더 안에 프로그램 실행 함수 파일(.py)들 목록값 추출하기
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
def set_RunFunction_list(runFuncDirName="RunFunction"):
    RunFunctionList = []
    RunFuncSaveDirDict = {}

    runFunc_path = os.path.abspath(os.getcwd())
    runFunc_path = os.path.normpath(os.path.join(runFunc_path, runFuncDirName))

    # 프로그램 실행 디렉토리 내 RunFunction 디렉토리에 있는 .py 함수들 목록 추출
    runFuncList = os.listdir(runFunc_path)

    for file in runFuncList:
        if file.endswith('.py'):
            
            if file == '__init__.py':
                continue

            RunFunctionList.append(file)        # RunFunction .py 함수 목록

            # RunFunction .py 별 결과 저장 디렉토리 이름 딕셔너리에 저장
            split_name = os.path.splitext(file)
            RunFuncSaveDirDict[file] = f"ResultDir_{split_name[0]}"

    return RunFunctionList, RunFuncSaveDirDict, runFunc_path


# 재귀함수 : 검색 지정 디렉토리부터 시작해서, 내부에 파일이 존재하는 최하위 디렉토리 탐색
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
def get_subDir_by_path( path, 
                        TotalList:list, 
                        signal:SignalClass, 
                        scanLimitCount=500,
                        Depth = 0  ):

    isBottomDir = True  # 해당 값이 False로 변경되지 않아야, 검색한 경로값이 최하위 디렉토리임
    cur_depth = copy.copy(Depth)

    if cur_depth == 0:
        RunFunctionLog()

    with os.scandir(path) as entries:       # 검색한 경로 본인이 가진 entries만 스캔하는 함수
        for i, entry in enumerate(entries):
            try:
                if entry.is_dir():          # 해당 엔트리가 디렉토리다 == 여기 최하위 디렉토리 아니다
                    isBottomDir = False

                    path_name = os.path.normpath(os.path.join(path, entry.name))

                    # 만약 해당 디렉토리가 최하위 디렉토리지만 내부 파일이 없을 때 continue
                    if len(os.listdir(path_name)) == 0:
                        continue

                    # 최하위 디렉토리 아니니깐 재귀함수 호출
                    get_subDir_by_path(path_name, TotalList, signal, scanLimitCount, cur_depth+1)

                # 해당 디렉토리 내 파일 갯수가 스캔 제한 갯수 넘을 때 :
                # 파일이 많다 == 최하위 디렉토리 간주해서 탐색 중지 후 리스트에 추가                
                if i > scanLimitCount:
                        break

            except Exception as e:
                ErrorMessage = f"Error : Searching {path} Denied - {e}"
                signal.s.emit(signal.send_signal_format(ErrorMessage))
                showLog(ErrorMessage)

    if isBottomDir:     # 해당 조건이 변동 없을 때 : 최하위 디렉토리가 맞다
        path = os.path.normpath(path)
        TotalList.append(path)

        # 여기부터는 로그 출력하는 코드
        # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
        if ShowLog:
            ListCount   = len(TotalList)
            logPrint    = ""
            Ratio       = 1

            logPrint = f"[{ListCount:4}] : {TotalList[-1]}"

            # 로그 메세지 출력 빈도 : 1, 2, 3, 4, ..., 10, 20, 30, ... 100, 200...
            for i in range(1, 5):
                if ListCount <= (Ratio * 10) and ListCount % Ratio == 0:
                    signal.s.emit(signal.send_signal_format(logPrint))
                    showLog(logPrint)
                    break
                Ratio *= 10

