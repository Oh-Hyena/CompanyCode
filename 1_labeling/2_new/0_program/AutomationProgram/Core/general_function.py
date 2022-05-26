# Import Packages and Modules
# Standard Library
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
import os
import sys
import datetime
import inspect
import copy


# Installed Library - QT CORE
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
from qt_core import *


# Custom Modules
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
from . json_settings import Settings


# Defines
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
ShowLog = copy.copy(CoreShowLog)
TestMode = copy.copy(CoreTestMode)


# print when ShowLog == True
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
def showLog(Msg, bTime=False):
    if ShowLog:
        if bTime:
            print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] {Msg}")
        else:
            print(Msg)


# Notice Log
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
def NoticeLog(Msg, bTime=False):
    NoticeMsg = "[ \x1b[33mNotice\x1b[0m ] : "
    if ShowLog:
        if bTime:
            print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] {NoticeMsg}{Msg}")
        else:
            print(f"{NoticeMsg}{Msg}")


# Error Log
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
def ErrorLog(Msg, bTime=False):
    NoticeMsg = "[ \x1b[33mError\x1b[0m ] : "
    if ShowLog:
        if bTime:
            print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] {NoticeMsg}{Msg}")
        else:
            print(f"{NoticeMsg}{Msg}")


# Show Log - Start Function Name & Start Runtime
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
def RunFunctionLog(AddMsg=""):
    if ShowLog:
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] : {inspect.getmodule((inspect.stack()[1])[0]).__file__}-> {callername()}() {AddMsg}")


# Return Run Function Name
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
def funcname():
    return sys._getframe(1).f_code.co_name


# Return Run Caller Name
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
def callername():
    return sys._getframe(2).f_code.co_name


# Return Current FileName expect Format
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
def filename(bFullPath=False):
    if bFullPath:
        return inspect.stack()[1].filename
    else:
        return os.path.basename(inspect.stack()[1].filename).split('.')[0]


# Signal Send Class
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
class SignalClass(QObject):
    s = pyqtSignal(list)

    # str 문자열을 넣었을 때 Signal 전송용 리스트 [ Caller 함수, 메세지 ]로 만들어주는 함수
    def send_signal_format(self, send_msg):
        sendFormat = []
        sendFormat.append(callername())
        sendFormat.append(send_msg)
        return sendFormat

