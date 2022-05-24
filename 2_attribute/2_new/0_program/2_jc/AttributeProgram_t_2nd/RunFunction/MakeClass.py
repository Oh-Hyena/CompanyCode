"""
This python file creates annotation txt output of class 83/66/39 
using classData.xlsx file and xml / img file of the given path.

LAST_UPDATE : 21/11/09
AUTHOR      : OH HYENA
"""


import os
import sys
import numpy                    as np


sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../UI/SelectUI'))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../Core'))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../'))


from CoreDefine                 import *
from Core.CommonUse             import *
from Core.ExcelDataClass        import ExcelData
from Core.CvatXmlClass          import CvatXml
from Core.SingletonClass        import Singleton
from UI.SelectUI.SelectUIClass  import *


OriginXmlDirPath    = copy.copy(OriginSource_cvatXml_Path)
OriginImgDirPath    = copy.copy(OriginSource_Img_Path)
ResultDirPath       = copy.copy(Result_Dir_Path)
AbbreviatedImgPath  = copy.copy(Abbreviated_Img_Path)
CheckRealExistPath  = copy.copy(RealExistCheck_Path)
CrushedImgFilePath  = os.path.join(ResultDirPath, CrushedImgFileName)

encodingFormat      = copy.copy(CORE_ENCODING_FORMAT)
validImgFormat      = copy.copy(VALID_IMG_FORMAT)


ANNOTATION_83_TXT   = "Annotation_83_Class.txt"
ANNOTATION_24_TXT   = "Annotation_24_Class.txt"

IMAGE_LIST_83_TXT   = "83Class_ImgList.txt"
IMAGE_LIST_24_TXT   = "24Class_ImgList.txt"

CHECK_EXTRACT_TXT   = "SizeFilterList.txt"
SIZE_ANALYSIS_TXT   = "ImageSize_Analysis_Source.txt"

MAKE_83_CLASS       = True
MAKE_24_CLASS       = True
SIZE_FILTERING      = False

CHECK_CRUSH_IMAGE   = False
CHECK_REAL_EXIST    = False
ANALYSIS_IMAGE_SIZE = True

# 원본 이미지를 축약시킨 폴더 기준으로 작업할 때 :
# 해당 cvat 이미지가 원본 이미지에 실제로 있는지 따져야함
ORIGIN_IMG_FILES_ABBREVIATED = False

SIZE_FILTERING_DICT = copy.copy(CORE_SIZE_FILTER_DICT)


class MakeClassSource(Singleton, CvatXml):
    def __init__(self, QApp):
        super().__init__(OriginXmlDirPath)
        self.app                            = QApp

        self.MakeClassFailList              = []
        self.CrushImgFileNameList           = []

        self.Result_83_ClassList            = []
        self.Result_24_ClassList            = []

        self.Result_83_ImageNameList        = []
        self.ResultDeleteUnknown_24_List    = []

        self.Deleted_24_Count               = 0

        self.imgSizeValueList               = []
        self.imgSizeSaveList                = []

        self.ClassData                      = None

        self.CurBoxList                     = []
        self.CurImgName                     = ""
        self.CurImgSizeList                 = []

        self.AbbreviatedImgDict             = {}
        self.CheckRealExistDict             = {}

        self.sendArgsList                   = []

        self.initializeMC()

    # SliceImage 실행 결과 저장된 CrushImageList.txt 를 불러오는 함수
    def initializeMC(self):
        self.setRunFunctionName('MAKE_CLASS')

        self.selectUi    = SelectUI(self.setInitSettingSelectUI, self.getEditSettingSelectUI)

        self.selectUi.show()
        self.app.exec()

        if self.selectUi.isQuitProgram():
            return

        self.ClassData = ExcelData()

        self.initCvatXmlClass()

        self.setMode()


    # 모드 설정하는 함수
    def setMode(self):
        if CHECK_CRUSH_IMAGE is True:
            ModeLog('CRUSH_IMG_FILTER ON\n')
            readFileToList(CrushedImgFilePath, self.CrushImgFileNameList, encodingFormat)

            if self.CrushImgFileNameList:
                self.condClass.addCondition(['CheckCrushImg', self.CheckCrushImg, self.getArgs_CheckCrushImg])
            else:
                ModeLog('CHECK_CRUSH_IMAGE FORCED CANCLELLATION')

        if ORIGIN_IMG_FILES_ABBREVIATED is True:
            ModeLog('ORIGIN_IMG_FILES_ABBREVIATED ON')
            if self.getAbbreviatedImgDataDict() is True:
                self.condClass.addCondition(['CheckIsExistAbbImg', self.CheckIsExistAbbImg, self.getArgs_CheckIsExistAbbImg])
            else:
                ModeLog('ORIGIN_IMG_FILES_ABBREVIATED FORCED CANCLELLATION')

        if CHECK_REAL_EXIST is True:
            ModeLog('CHECK_REAL_EXIST ON')
            if self.getCheckRealExistDataDict() is True:
                self.condClass.addCondition(['CheckRealExist', self.CheckRealExist, self.getArgs_CheckRealExist])
            else:
                ModeLog('CHECK_REAL_EXIST FORCED CANCLELLATION')

        if SIZE_FILTERING is True:
            ModeLog('SIZE_FILTERING ON')
            self.condClass.addCondition(['SizeFilter', self.SizeFilter, self.getArgs_SizeFilter])


    # SelectUI 에 넘길 초기값 세팅
    def setInitSettingSelectUI(self):
        self.SyncAllValue()
        self.sendArgsList = [   ['FD', 'OriginXmlDirPath',              True,   f'{OriginXmlDirPath}'],
                                ['FD', 'OriginImgDirPath',              True,   f'{OriginImgDirPath}'],
                                ['FD', 'ResultDirPath',                 True,   f'{ResultDirPath}'],
                                ['FD', 'HLINE_0',                       False,  'None'],
                                ['FD', 'AbbreviatedImgPath',            True,   f'{AbbreviatedImgPath}'],
                                ['FD', 'CrushedImgFilePath',            False,  f'{CrushedImgFilePath}'],
                                ['FD', 'CheckRealExistPath',            True,   f'{CheckRealExistPath}'],

                                ['CB', 'MAKE_83_CLASS',                 False,  f'{MAKE_83_CLASS}'],
                                ['CB', 'MAKE_24_CLASS',                 False,  f'{MAKE_24_CLASS}'],
                                ['CB', 'HLINE_1',                       False,  'None'],
                                ['CB', 'SIZE_FILTERING',                False,  f'{SIZE_FILTERING}'],
                                ['CB', 'ANALYSIS_IMAGE_SIZE',           False,  f'{ANALYSIS_IMAGE_SIZE}'],
                                ['CB', 'HLINE_2',                       False,  'None'],
                                ['CB', 'ORIGIN_IMG_FILES_ABBREVIATED',  False,  f'{ORIGIN_IMG_FILES_ABBREVIATED}'],
                                ['CB', 'CHECK_REAL_EXIST',              False,  f'{CHECK_REAL_EXIST}'],
                                ['CB', 'CHECK_CRUSH_IMAGE',             False,  f'{CHECK_CRUSH_IMAGE}'],

                                ['UI',  'SIZE_FILTERING_DICT',          False,  SIZE_FILTERING_DICT]
                            ]
        return self.getRunFunctionName(), self.sendArgsList


    # SelectUI 에서 넘겨받은 값 적용
    def getEditSettingSelectUI(self):
        NAME        = 1        
        returnDict  = self.selectUi.getReturnDict()

        print("\n* Change Path/Define Value By SelectUI")
        print("--------------------------------------------------------------------------------------")
        for Arg in self.sendArgsList:
            eachTarget = Arg[NAME]
            if returnDict.get(eachTarget) != None:
                globals()[eachTarget] = returnDict[eachTarget]

                if eachTarget == "SIZE_FILTERING_DICT":
                    showLog(f'- {eachTarget:40} -> {summaryFilterDict(globals()[eachTarget])}')
                else:
                    showLog(f'- {eachTarget:40} -> {globals()[eachTarget]}')
        print("--------------------------------------------------------------------------------------\n")

        self.SyncAllValue()
        setResultDir(ResultDirPath)
        self.setChanged_Xml_n_Res_Path(OriginXmlDirPath, ResultDirPath)


    def SyncAllValue(self):
        self.SyncEachValue('OriginSource_cvatXml_Path', 'OriginXmlDirPath')
        self.SyncEachValue('OriginSource_Img_Path',     'OriginImgDirPath')
        self.SyncEachValue('Result_Dir_Path',           'ResultDirPath')
        self.SyncEachValue('CORE_SIZE_FILTER_DICT',     'SIZE_FILTERING_DICT')

    def SyncEachValue(self, CoreName, LinkName, SENDER_DEPTH=3):
        if callername(SENDER_DEPTH) == 'setInitSettingSelectUI':
            globals()[LinkName] = getCoreValue(CoreName)

        elif callername(SENDER_DEPTH) == 'getEditSettingSelectUI':
            setCoreValue(CoreName, globals()[LinkName])


    # ORIGIN_IMG_FILES_ABBREVIATED 가 True 일 때, 이미지 비교하기 위해 Dict Data 만드는 함수
    def getAbbreviatedImgDataDict(self):
        self.AbbreviatedImgDict = getImageSearchDict(AbbreviatedImgPath, validImgFormat)

        if self.AbbreviatedImgDict is None:
            ErrorLog(f'`{AbbreviatedImgPath}` is Nothing Vaild Image', lineNum=lineNum(), errorFileName=filename())
            return False

        return True


    # CHECK_REAL_EXIST 가 True 일 때, 이미지 비교하기 위해 Dict Data 만드는 함수
    def getCheckRealExistDataDict(self):
        self.CheckRealExistDict = getImageSearchDict(CheckRealExistPath, validImgFormat)

        if self.CheckRealExistDict is None:
            ErrorLog(f'`{CheckRealExistPath}` is Nothing Vaild Image', lineNum=lineNum(), errorFileName=filename())
            return False

        return True


    # imageName 이 CrushImgFileNameList 에 있는지 체크하는 함수
    def CheckCrushImg(self, imgName):
        if imgName in self.CrushImgFileNameList:
            return COND_FAIL
        return COND_PASS


    # imageName 이 AbbreviatedImgDict 에 있는지 체크하는 함수
    def CheckIsExistAbbImg(self, imgName):
        if self.AbbreviatedImgDict.get(imgName) == None:
            return COND_FAIL
        else:
            return COND_PASS


    # imageName 이 CheckRealExistDict 에 있는지 체크하는 함수
    def CheckRealExist(self, imgName):
        if self.CheckRealExistDict.get(imgName) == None:
            return COND_FAIL
        else:
            return COND_PASS


    # imgsize filter 함수
    def SizeFilter(self, getArgsList):
        BoxValue    = getArgsList[0]    # 현재 이미지의 BoxValue 들의 리스트
        ImgSizeList = getArgsList[1]    # 현재 이미지의 [너비, 높이] 리스트
        condDict    = getArgsList[2]
        BoxDict     = {}
        BoxNameList = ['head', 'upper', 'lower']
        
        def getBoxSizebyLabel(box):
            xTopLeft     = int(float(box.get("xtl")))
            yTopLeft     = int(float(box.get("ytl")))
            xBottomRight = int(float(box.get("xbr")))
            yBottomRight = int(float(box.get("ybr")))

            return [xBottomRight - xTopLeft, yBottomRight - yTopLeft]

        def checkSizeByLabel(labelName:str):
            if BoxDict.get(f'{labelName}') == None:
                return COND_FAIL
            
            boxSizeList = getBoxSizebyLabel(BoxDict[f'{labelName}'])
            if condDict[f'{labelName}']['CheckSize'] is True:
                boxSize = boxSizeList[WIDTH] * boxSizeList[HEIGHT]
                if boxSize >= condDict[f'{labelName}']['Size']:
                    return COND_PASS
                else:
                    return COND_FAIL
            else:
                if  ( boxSizeList[WIDTH]  >= condDict[f'{labelName}']['Width'] ) and \
                    ( boxSizeList[HEIGHT] >= condDict[f'{labelName}']['Height'] ):
                    return COND_PASS
                else:
                    return COND_FAIL            

        if condDict['common']['isCheck'] is True:
            if condDict['common']['CheckSize'] is True:
                imgSize = ImgSizeList[WIDTH] * ImgSizeList[HEIGHT]
                if imgSize >= condDict['common']['Size']:
                    return COND_PASS
                else:
                    return COND_FAIL
            else:
                if  ( ImgSizeList[WIDTH]  >= condDict['common']['Width'] ) and \
                    ( ImgSizeList[HEIGHT] >= condDict['common']['Height'] ):
                    return COND_PASS
                else:
                    return COND_FAIL

        for box in BoxValue:
            BoxDict[box.get('label')] = box

        for eachName in BoxNameList:
            if condDict[f'{eachName}']['isCheck'] is True:
                return checkSizeByLabel(eachName)

        return COND_FAIL


    def getArgs_CheckCrushImg(self):
        return self.getCurImgName()

    def getArgs_CheckIsExistAbbImg(self):
        return self.getCurImgName()

    def getArgs_SizeFilter(self):
        return [ self.getCurBoxList(), self.getCurImgSize(), SIZE_FILTERING_DICT ]

    def getArgs_CheckRealExist(self):
        return self.getCurImgName()

    def getBoxSize(self, box):
        xTopLeft     = int(float(box.get("xtl")))
        yTopLeft     = int(float(box.get("ytl")))
        xBottomRight = int(float(box.get("xbr")))
        yBottomRight = int(float(box.get("ybr")))

        return [xBottomRight - xTopLeft, yBottomRight - yTopLeft]   


    # setRunFunctionParam() 을 통해 갱신된 CurBoxList 변수를 이용하여,
    # RunFunction 내부 setMakeClassDefaultData() 함수에 인자로 줄 sendAttList 값을 만드는 함수 
    def createAttListByBoxList(self):
        sendAttList = []
        for box in self.CurBoxList:
            for att in box.findall('attribute'):
                sendAttList.append([box.get('label'), att.get('name'), att.text])

        return sendAttList


    # CvatXml 의 가상함수를 상속받아 재정의한 실제 실행 부분 함수
    def RunFunction(self):
        attList = self.createAttListByBoxList()
        self.ClassData.setMakeClassDefaultData(attList)

        MCD                 = self.ClassData.getMakeClassDefaultData()

        make83Class_Res     = ""
        make24Class_Res     = ""

        isUnknownDelete_24  = False

        imgName             = self.CurImgName

        if MAKE_83_CLASS is True:
            make83Class_PreRes, _   = self.ClassData.refineMakeClass(83, MCD)
            make83Class_Res         = self.listToString(make83Class_PreRes)
            self.Result_83_ClassList.append(make83Class_Res)

        if MAKE_24_CLASS is True:
            make24Class_PreRes, isUnknownDelete_24 = self.ClassData.refineMakeClass(24, MCD)
            if isUnknownDelete_24 is False:
                make24Class_Res = self.listToString(make24Class_PreRes)
                self.Result_24_ClassList.append(make24Class_Res)
                self.ResultDeleteUnknown_24_List.append(imgName)
            else:
                self.Deleted_24_Count += 1

        self.Result_83_ImageNameList.append(imgName)

        if ANALYSIS_IMAGE_SIZE is True:
            if MAKE_24_CLASS is True:
                if isUnknownDelete_24 is False:
                    self.imgSizeValueList.append(self.CurImgSizeList)
            else:
                self.imgSizeValueList.append(self.CurImgSizeList)

        
    def analysisImageSize(self):
        widthList   = [ each[WIDTH] for each in self.imgSizeValueList ]
        heightList  = [ each[HEIGHT] for each in self.imgSizeValueList ]

        widthArray  = np.array(widthList)
        heightArray = np.array(heightList)
        widthAvg    = np.mean(widthArray)
        heightAvg   = np.mean(heightArray)
        AreaAvg     = np.mean(np.multiply(widthAvg, heightArray))

        print()
        showLog('# [ SIZE ANALYSIS ]')
        if SIZE_FILTERING:
            showLog('--------------------------------------------------------------------------------------')
            showLog(f'- Condition      : {summaryFilterDict(SIZE_FILTERING_DICT)}')
        showLog('--------------------------------------------------------------------------------------')
        showLog(f'- Avgarge Width  : {round(widthAvg,2)}')
        showLog(f'- Avgarge Height : {round(heightAvg,2)}')
        showLog(f'- Avgarge Szie   : {round(AreaAvg,2)}')
        showLog('--------------------------------------------------------------------------------------')
        print()

    
    def setImageAnalysisSaveList(self):
        widthList   = [ each[WIDTH] for each in self.imgSizeValueList ]
        heightList  = [ each[HEIGHT] for each in self.imgSizeValueList ]

        for eachIdx in range(len(self.imgSizeValueList)):
            self.imgSizeSaveList.append(f'{widthList[eachIdx]} {heightList[eachIdx]}')
        

    # [0, 1, 0, 0, ...] 꼴의 리스트를 '0100...' 꼴의 문자열로 변환시켜 반환하는 함수
    def listToString(self, fromList):
        toString = ""
        for eachValue in fromList:
            toString += str(eachValue)
        return toString


    # 결과값들을 저장한 리스트를 파일로 Save 하는 함수
    def saveMakeClassFile(self, SubPath, SaveList):
        savePath = os.path.join(ResultDirPath, SubPath)
        writeListToFile(savePath, SaveList, encodingFormat)


    # RunFunction 전부 다 돌린 후 나온 결과값들을 각각의 저장경로로 배분해 saveMakeClassFile() 로 저장하는 함수
    def saveMakeClassFiles(self):
        if MAKE_83_CLASS is True:
            self.saveMakeClassFile(ANNOTATION_83_TXT, self.Result_83_ClassList)
            self.saveMakeClassFile(IMAGE_LIST_83_TXT, self.Result_83_ImageNameList)

        if MAKE_24_CLASS is True:
            self.saveMakeClassFile(ANNOTATION_24_TXT, self.Result_24_ClassList)
            self.saveMakeClassFile(IMAGE_LIST_24_TXT, self.ResultDeleteUnknown_24_List)

        if ANALYSIS_IMAGE_SIZE is True:
            self.setImageAnalysisSaveList()
            self.saveMakeClassFile(SIZE_ANALYSIS_TXT, self.imgSizeSaveList)


    # Result Sammary 출력하는 함수
    def FinishFunction(self):
        TotalLen_83_Img = len(self.Result_83_ClassList)
        TotalLen_24_Img = len(self.Result_24_ClassList)

        showLog(f'- {"Pass the ConditionCheck":<35} [{CGREEN}{TotalLen_83_Img:^8}{CRESET}]  ->  MakeClass 83 Image [{CGREEN}{TotalLen_83_Img:^8}{CRESET}]')
        showLog(f'- {"Deleted by UnknownCheck in 24Class":<35} [{CRED}{self.Deleted_24_Count:^8}{CRESET}]  ->  MakeClass 24 Image [{CYELLOW}{TotalLen_24_Img:^8}{CRESET}]')

        self.saveMakeClassFiles()

        if ANALYSIS_IMAGE_SIZE is True:
            self.analysisImageSize()


    # RunFunction 에 들어가기 전 사용할 Param 을 setting 하는 함수
    def setRunFunctionParam(self):
        self.CurBoxList     = self.getCurBoxList()
        self.CurImgName     = self.getCurImgName()
        self.CurImgSizeList = self.getCurImgSize()


    # ABS FUNC(가상 함수) 재정의 함수
    def setFinishFunctionParam(self):
        return super().setFinishFunctionParam()


    # ABS FUNC(가상 함수) 재정의 함수
    def AfterRunFunction(self):
        return super().AfterRunFunction()


    # ABS FUNC(가상 함수) 재정의 함수
    def setAfterRunFunctionParam(self):
        return super().setAfterRunFunctionParam()

    # 클래스를 실행하는 함수
    def run(self):
        if self.selectUi.isQuitProgram():
            NoticeLog(f'{self.__class__.__name__} Program EXIT\n')
        else:
            super().run()
            os.startfile(ResultDirPath)


if __name__ == "__main__":
    App         = QApplication(sys.argv)
    RunProgram  = MakeClassSource(App)
    RunProgram.run()