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
from . json_settings    import Settings
from . general_function import *


# Defines
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
ShowLog = copy.copy(CoreShowLog)
TestMode = copy.copy(CoreTestMode)


# RunFunction Send Argv Check & Package Class
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
class SendArgvClass():

    # settings.json 인자값 매칭시킬 변수 앞에 붙일 식별자 문자
    Detect_SArg = "SArg"


    def __init__(self, setRunFunction=""):
        super().__init__()

        # Load Settings
        # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
        settings = Settings()
        self.settings = settings

        # 함수에 보낼 SendArgv값 다 적으면 내부 함수에서 함수별로 걸러줌
        # 만약 해당 함수에 보낼 인자값이 json 파일에 ABC 라고 정했을 때
        # 여기에 self.SArg_ABC = "" 해두면 됨
        # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
        self.SArg_StartIndex = ""
        self.SArg_LogPath = ""
        self.SArg_AddWork = ""
        self.SArg_ResDir = ""
        self.SArg_NoMean = ""

        self.fileName = ""
        self._sep = ""

        # 클래스 생성할 때 파일 이름 넣으면 할당도 생성과 동시에
        # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
        if setRunFunction:
            self.set_SendArgv_Function(setRunFunction)


    # 파일 이름을 입력했을 때 해당 이름값에 매칭되는 json 인자를 불러와서 세팅하는 함수
    # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
    def set_SendArgv_Function(self, FuncFileName):
        # 인자값 처리
        # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
        FileName = FuncFileName.split('.')[0]
        self.fileName = FileName

        # 갱신 불러오기
        # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
        self.settings.deserialize()

        # 해당 파일명 키값이 있는지 유효값 체크
        # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
        ArgValueByFunc = self.settings.items['run_function_argv'].get(FileName)

        # 해당 키에 맞는 밸류값이 없다면 디폴트값으로 생성해주기
        if ArgValueByFunc == None:
            self.new_setting_option_by_fileName(FileName)

        # 기본값 할당
        # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
        # Json File 내 인자값 함수명 파일의 키값 리스트
        curFunc_settingValueList = list(self.settings.items['run_function_argv'][FileName].keys())
        # 현재 클래스 self. 변수 리스트
        classValueList = self.SArgList()

        # 구분자
        sep = self.settings.items['run_function_argv'][FileName]['sep']
        self._sep = sep

        # 값 필터링해서 파일에 맞게 알아서 할당해주는 부분
        # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
        # 클래스 변수들 중에 지금 고른 RunFunction 파일의 json 값 내 SendArgv가 있을 때만 Set
        for Cvalue in classValueList:                   # ex) SArg_StartIndex, SArg_LogPath ... : self 변수값
            for Jvalue in curFunc_settingValueList:     # ex) StartIndex, LogPath ... : json key값
                if Jvalue in Cvalue:
                    curDict  = self.settings.items['run_function_argv'][FileName][Jvalue]
                    head = curDict['head']
                    cval = curDict['CurValue']
                    
                    setVal = f"{head}{sep}{cval}"
                    self.__dict__[Cvalue] = setVal

        showLog(f": set_SendArgv_Function --> File : {FileName}", True)


    # 클래스의 변수 이름들 중 'SArg_' 접두사가 있는 변수들 이름만 리스트로 리턴하는 함수
    # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
    def SArgList(self):
        SArg_List = self.__dict__
        SArg_List = [x for x in SArg_List if self.Detect_SArg in x]

        return SArg_List


    # 현재 클래스 변수들에 저장된 값을 settings.json에 갱신해 저장하는 함수
    # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
    def ChangedSettingSaveToJson(self):
        # 유효값 체크
        self.checkValidValue()

        """ Xml_To_Text.py 파일일 때 기준 각 변수값 예시

            curSetDict = {'sep': '$$$', 'StartIndex': {'head': 'StartIndex', 'type': 'int', 'default': '0', 'CurValue': '0'}, ... }
            res_val_dict = {'SArg_StartIndex': '0', 'SArg_LogPath': 'NoneChanged', 'SArg_AddWork': 'ON', ... }
            res_key_list = ['SArg_StartIndex', 'SArg_LogPath', 'SArg_AddWork', 'SArg_ResDir', 'SArg_NoMean']
            split_res_key_list = ['StartIndex', 'LogPath', 'AddWork', 'ResDir', 'NoMean']

        """
        curSetDict          = self.settings.items['run_function_argv'][self.fileName]
        res_val_dict        = self.getValueByRealValue()
        res_key_list        = list(res_val_dict)
        split_res_key_list  = [x.split('_')[1] for x in res_key_list]

        # 현재 SendArgv 클래스에 저장된 변수들을 Settings 클래스에 복사하기
        for idx, each in enumerate(split_res_key_list):
            try:
                curSetDict[each]['CurValue'] = res_val_dict[res_key_list[idx]]
            except Exception as e:
                continue

        # 복사된 값 settings.json 파일에 json 형식으로 저장하기
        self.settings.serialize()
        showLog(f": Changed Setting Saved \'settings.json\' in {self.fileName}", True)


    # SendArgv 보낼 값이 유효한 값인지 체크하는 함수
    # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
    def checkValidValue(self):

        callerName = callername()
        RunFunctionLog(f"for {callerName}()")

        # 변수값 할당
        # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
        selfDict = self.__dict__
        get_attr = [x for x in selfDict if self.Detect_SArg in x]   # self 변수들 중 SArg 값이 들어간 변수들만 리스트화
        check_val = [x.split('_')[1] for x in get_attr]             # 거기서 SArg_ 접두사 뺀 리스트

        curSetDict = self.settings.items['run_function_argv'][self.fileName] # json 세팅값

        # 유효값 체크하는 파트
        # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
        for idx, each_val in enumerate(check_val):

            # 일단 해당값이 인자값으로 넣은 파일에 속한 json 인자값들인지 체크 : 없으면 예외처리로 컨티뉴
            try:
                head = curSetDict[each_val]['head']
                sep  = curSetDict['sep']
                dflt = curSetDict[each_val]['default']
                valid_val = f"{head}{sep}"

            except Exception as e:
                continue

            # 여기 for 문에서 유효값 체크하고, 만약 이상한 값이 SendArgv에 들어있으면 디폴트 값으로 리셋해줌
            if valid_val in selfDict[get_attr[idx]]:
                realValue = selfDict[get_attr[idx]].split(sep)[-1]

                if len(realValue) == 0:
                    selfDict[get_attr[idx]] = f"{head}{sep}{dflt}"

                # showLog(f"\x1b[32m{get_attr[idx]:25}\t--> {selfDict[get_attr[idx]]:80}\t--> {realValue}\x1b[0m")

            else:
                showLog(f"\x1b[31m{get_attr[idx]:25}\t--> {selfDict[get_attr[idx]]:80}\t--> Reset Default!\x1b[0m")
                selfDict[get_attr[idx]] = f"{head}{sep}{dflt}"


    # Default 를 기준으로 새로운 함수명에 해당하는 Dict 만들어주기
    # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
    def new_setting_option_by_fileName(self, FileName):
        RunFunctionLog()
        self.settings.items['run_function_argv'][FileName] = self.settings.items['run_function_argv']['Default']
        # 저장 후 다시 불러오기
        self.settings.serialize()
        self.settings.deserialize()


    # os.system 으로 실제 RunFunction 실행할 때 인자로 넘기기 위한 SendArgv 통째로 묶은 문자열 반환
    # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
    def get_Engraft_SendArgv(self):
        
        RunFunctionLog()
        
        # 유효값 체크를 먼저 거치기
        self.checkValidValue()

        returnVal = ""
        selfDict  = self.__dict__
        get_attr  = self.SArgList()

        for each in get_attr:
            if selfDict[each]:
                addParam = f"{selfDict[each]} "
                returnVal = returnVal + addParam

        return returnVal


    # 현재 클래스에서 가지고 있는 값들 아래 예시 형식으로 추출
    # ex ) {'SArg_StartIndex': '0', 'SArg_LogPath': 'C:\\PythonHN\\AutomationProgram\\save.txt', ... }
    # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
    def getValueByRealValue(self):

        selfDict = self.__dict__
        get_attr = self.SArgList()
        returnValue = {}
        
        for each in get_attr:
            returnValue[each] = selfDict[each].split(self._sep)[-1]

        return returnValue


    # 현재 클래스에서 가지고 있는 값들 아래 예시 형식으로 추출
    # ex ) {'SArg_StartIndex': 'StartIndex$$$0', 'SArg_LogPath': 'LogPath$$$C:\\PythonHN\\AutomationProgram\\save.txt', ... }
    # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
    def getValueBySargFormat(self):

        selfDict = self.__dict__
        get_attr = self.SArgList()

        returnValue = {}
        
        for each in get_attr:
            returnValue[each] = selfDict[each]

        return returnValue


    # 현재 클래스에서 가지고 있는 값들 settings.json 에서 default 값들 불러옴
    # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
    def getValueDefaultSetting(self):

        get_attr = self.SArgList()
        check_val = [x.split('_')[1] for x in get_attr]
        curSetDict = self.settings.items['run_function_argv'][self.fileName]
        returnValue = {}
        
        for idx, each in enumerate(check_val):

            try:
                dflt = curSetDict[each]['default']

            except Exception as e:
                continue

            returnValue[get_attr[idx]] = dflt

        return returnValue


    # 현재 클래스의 값들을 디폴트값으로 리셋해주는 함수
    # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
    def setValueDefaultSetting(self):
        RunFunctionLog()

        curFunc_settingValueList = list(self.settings.items['run_function_argv'][self.fileName].keys())
        classValueList = self.SArgList()

        for Cvalue in classValueList:
            for Jvalue in curFunc_settingValueList:
                if Jvalue in Cvalue:
                    curDict = self.settings.items['run_function_argv'][self.fileName][Jvalue]
                    head = curDict['head']
                    defv = curDict['default']

                    setVal = f"{head}{self._sep}{defv}"
                    self.__dict__[Cvalue] = setVal

