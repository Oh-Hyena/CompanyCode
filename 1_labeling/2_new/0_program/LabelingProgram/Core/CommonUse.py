# Import Packages and Modules
# Standard Library
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
import os
import sys
import datetime
import inspect
import copy


# Refer to CoreDefine.py
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
from CoreDefine import *


# Defines
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
SHOW_LOG        = copy.copy(CORE_SHOW_LOG)
TEST_MODE       = copy.copy(CORE_TEST_MODE)
ERROR_STRICT    = copy.copy(CORE_ERROR_STRICT)


# Color Defines
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
CRED            = '\x1b[31m'
CGREEN          = '\x1b[32m'
CYELLOW         = '\x1b[33m'
CSKY            = '\x1b[36m'
CRESET          = '\x1b[0m'

if len(sys.argv) >1 and sys.argv[1] == 'RUN_BAT':
    CRED    = ''
    CGREEN  = ''
    CYELLOW = ''
    CSKY    = ''
    CRESET  = ''


# VAR
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
errorLogList    = []


# get LineNumber when called
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
def lineNum():
    return inspect.getlineno((inspect.stack()[1])[0])


# print when SHOW_LOG == True
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
def showLog(Msg, bTime=False):
    if SHOW_LOG:
        if bTime:
            print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] {Msg}")
        else:
            print(Msg)


# Notice Log
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
def NoticeLog(Msg, bTime=False):
    NoticeMsg = f"[ {CYELLOW}Notice{CRESET} ] "
    if SHOW_LOG:
        if bTime:
            print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] {NoticeMsg}{Msg}")
        else:
            print(f"{NoticeMsg}{Msg}")


# Error Log
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
def ErrorLog(Msg, bTime=False, lineNum=0, errorFuncName=None, errorFileName=None):
    ErrorMsg = f"[ {CRED}Error{CRESET} ] "

    if SHOW_LOG:
        if bTime:
            print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] {ErrorMsg}{Msg}")
        else:
            print(f"{ErrorMsg}{Msg}")
    
    # 들어온 lineNum/errorFileName 이 기본값이면 입력을 안했다는 뜻이니 Not Checked
    lineNum         = "Not Checked Line"    if lineNum == 0         else f"{lineNum} Line"
    errorFileName   = "Not Checked"         if not errorFileName    else f"{errorFileName}.py"
    
    # errorLogList 추가
    if not errorFuncName:
        errorLogList.append(f"| {errorFileName:<25}| {callername():<25} | {lineNum:<18} | {Msg:<77} | {timeToString(getCurTime())}")
    else:
        errorLogList.append(f"| {errorFileName:<25}| {errorFuncName:<25} | {lineNum:<18} | {Msg:<77} | {timeToString(getCurTime())}")


# SuccessLog
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
def SuccessLog(Msg, bTime=False):
    SuccessMsg = f"[ {CGREEN}Done{CRESET} ] "

    if SHOW_LOG:
        if bTime:
            print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] {SuccessMsg}{Msg}")
        else:
            print(f"{SuccessMsg}{Msg}")


# ModeLog
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
def ModeLog(Msg, bTime=False):
    ModeMsg = f"[ {CSKY}MODE{CRESET} ] "

    if SHOW_LOG:
        if bTime:
            print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] {ModeMsg}{Msg}")
        else:
            print(f"{ModeMsg}{Msg}")


# Show Log - Start Function Name & Start Runtime
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
def RunFunctionLog(AddMsg=""):
    if SHOW_LOG:
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] : {inspect.getmodule((inspect.stack()[1])[0]).__file__}-> {callername()}() {AddMsg}")


# get Current Time
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
def getCurTime():
    return datetime.datetime.now()


# convert datetime data to specific string format
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
def timeToString(timeData):
    return timeData.strftime('%Y/%m/%d %H:%M:%S')


# return subs time
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
def diffTime(startTime, endTime):
    return endTime - startTime


# Return Run Function Name
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
def funcname():
    return sys._getframe(1).f_code.co_name


# Return Run Caller Name
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
def callername(Depth=2):
    return sys._getframe(Depth).f_code.co_name


# Return Current FileName expect Format
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
def filename(bFullPath=False):
    if bFullPath:
        return inspect.stack()[1].filename
    else:
        return os.path.basename(inspect.stack()[1].filename).split('.')[0]


# Code that handles errors according to the degree of ERROR_STRICT
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
def error_handling(errorMsg, filename=None, lineNum=0):
    if ERROR_STRICT == ERROR_STRICT_HARD:
        ErrorLog(errorMsg, True, lineNum, callername(), filename)
        showErrorList()
        sys.exit(-1)
    elif ERROR_STRICT == ERROR_STRICT_SOFT:
        ErrorLog(errorMsg, True, lineNum, callername(), filename)


# Returns a bool value in string form as 0/1
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
def isTrue(Bool):
    if Bool == "true" or Bool == "True":
        return 1
    else:
        return 0


# Show Program Information By CoreDefine.py
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
def showProgramInfo():
    """
        CoreDefine.py 의 정의를 참조하여, Program 정보를 출력
    """
    print()
    print('*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*')
    print(f'*  {"TITLE":13}|  {TITLE:<41}*')
    print(f'*  {"DATE":13}|  {DATE:<41}*')
    print(f'*  {"VERSION":13}|  {VERSION:<41}*')
    print(f'*  {"IDE":13}|  {IDE:<41}*')
    print(f'*  {"OS":13}|  {OS:<41}*')
    print(f'*  {"AUTHOR":13}|  {AUTHOR:<41}*')
    print('*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*')
    print()


# if ErrorLog Exist, Show Error
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
def showErrorList():
    print('\n[ Error While Run Program ]')
    if errorLogList:
        print('-'*180)
        # 출력 내용 : 파일 이름 / 함수 이름 / 라인 / 메세지 / 발생 시간
        print(f"  | {'FileName':25}| {'FunctionName':<25} | {'Line':<18} | {'ErrorInfo':<77} | Time")
        print('-'*180)
        for eachError in errorLogList:
            print(f"- {eachError}")
        print('-'*180)
    else:
        print("- Error Not Detected! :D")
    print()


# Summarize a dict of the form CORE_SIZE_FILTER_DICT
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
def summaryFilterDict(filterDict:dict):
    resMsg      = ""
    validSort   = ""
    validCond   = ""

    for k, v in filterDict.items():
        if v['isCheck'] == True:
            validSort = k

    if not validSort:
        return "Not Checked"

    if filterDict[validSort]['CheckSize'] is True:
        validCond = f"[ AreaSize >= {filterDict[validSort]['Size']} ]"
    else:
        validCond = f"[ (WIDTH >= {filterDict[validSort]['Width']}) AND (HEIGHT >= {filterDict[validSort]['Height']}) ]"

    resMsg = f"[ {validSort.upper()} ] {validCond}"

    return resMsg


# Main.py Check Exit
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
def CheckExit(CheckName):
    if CheckName == 'EXIT':
        NoticeLog('Attribute Program Finished... Close still running programs\n')
        return True
    return False


# Check File or Dir Exist
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
def CheckExistFile(FileName):
    if os.path.isfile(FileName) is False:
        ErrorLog(f'{FileName} is Not Exist File! Program Quit.')
        sys.exit(-1)

def CheckExistDir(DirName):
    if os.path.isdir(DirName) is False:
        ErrorLog(f'{DirName} is Not Exist Directory! Program Quit.')
        sys.exit(-1)


def JustCheckFile(FileName):
    return os.path.isfile(FileName)

def JustCheckDir(DirName):
    return os.path.isdir(DirName)


def setResultDir(resDirPath):
    if os.path.isdir(resDirPath) is False:
        os.makedirs(resDirPath, exist_ok=True)
        NoticeLog(f'{resDirPath} is Not Exists, Create Done')


# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
def writeListToFile(filePath, wList, encodingFormat=CORE_ENCODING_FORMAT):
    with open(filePath, 'w', encoding=encodingFormat) as f:
        for line in wList:
            f.write(f'{line}\n')
    SuccessLog(f'Save Done >> {filePath}')


def readFileToList(filePath, rList:list, encodingFormat=CORE_ENCODING_FORMAT):
    CheckExistFile(filePath)
    rList.clear()
    with open(filePath, 'r', encoding=encodingFormat) as f:
        for eachLine in f:
            eachLine = eachLine.strip('\n')
            rList.append(eachLine)
    SuccessLog(f'Read Done << {filePath}')


# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
def showListLog(showList):
    if not showList:
        return
    for eachElem in showList:
        showLog(f'- {eachElem}')


# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
def getImageSearchDict(SearchDir, filterFormat):
    CheckExistDir(SearchDir)
    resDict = {}

    for root, _, files in os.walk(SearchDir):
        if len(files) > 0:
            for file in files:
                _, ext = os.path.splitext(file)
                if ext in filterFormat:
                    resDict[file] = root
    
    if resDict:
        SuccessLog(f'Get ImageData Done << {SearchDir}')
        return resDict

    return None


# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
def getVideoSearchDict(SearchDir, filterFormat):
    CheckExistDir(SearchDir)
    resDict = {}

    for root, _, files in os.walk(SearchDir):
        if len(files) > 0:
            for file in files:
                _, ext = os.path.splitext(file)
                if ext in filterFormat:
                    resDict[file] = root
    
    if resDict:
        SuccessLog(f'Get VideoData Dict Done << {SearchDir}')
        print()
        return resDict

    return None


# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
def getVideoSearchList(SearchDir, filterFormat):
    CheckExistDir(SearchDir)
    resList = []

    for root, _, files in os.walk(SearchDir):
        if len(files) > 0:
            for file in files:
                _, ext = os.path.splitext(file)
                if ext in filterFormat:
                    resList.append(file)
    
    if resList:
        SuccessLog(f'Get VideoData List Done << {SearchDir}')
        print()
        return resList

    return None

