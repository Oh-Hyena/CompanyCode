"""
Parent class code of classes using CVAT XML file

LAST_UPDATE : 2021/11/08
AUTHOR      : OH HYENA
"""


import  sys
import  os
import  xml.etree.ElementTree as ET
from    abc    import *                            # 추상 클래스를 만들기 위한 모듈

from CoreDefine import *
from Core.CommonUse         import *
from Core.CheckCondClass    import CheckCondition
from Core.SaveLogClass      import SaveErrorLog


START = 0
END   = 1


class CvatXml(metaclass=ABCMeta):
    """
        cvatXml 파일을 이용하는 클래스들의 부모 클래스.
        생성자와 공용 변수, run 관련 가상함수를 제공한다.
    """
    def __init__(self, OriginXmlDirPath):
        self.cvatXmlList        = []
        self.OriginXmlDirPath   = OriginXmlDirPath
        
        self.CC_LogList         = []
        self.LogToExcel         = SaveErrorLog()

        self.condClass          = None
        self.RunFunctionName    = "NoneFunction"

        self.CurBoxListByImage  = []
        self.CurImageName       = ""
        self.CurImageSizeList   = []

        self.checkPercentageNum = 0
        self.prePercentageCount = 0

        self.TotalRunImgCount   = 0
        self.SuccessImageCount  = 0


    # 실제 CvatXml init 함수
    def initCvatXmlClass(self):
        """
            setInitCheckCondList() 을 통해 Default CheckCond List 를 CvatXml 생성시 바로 할당
            SelectUI 에서 새로 경로를 받는 Case 때문에, __init__ 시 자동 실행이 아닌 수동 실행
        """
        # CheckCondition 생성과 동시에 Default CheckCond List ADD
        self.condClass = CheckCondition(self.setInitCheckCondList())


    # OriginXmlDirPath 에서 cvatXml 파일들 리스트 추출하는 함수
    def extract_cvatXmlList(self):
        self.cvatXmlList.clear()

        CheckExistDir(self.OriginXmlDirPath)

        for path, _, files in os.walk(self.OriginXmlDirPath):
            for eachFile in files:
                _, ext = os.path.splitext(eachFile)
                if ext != ".xml":
                    error_handling(f"{eachFile} is Not XML", filename(), lineNum())
                    break
                else:
                    self.cvatXmlList.append(os.path.join(path, eachFile))

        if not self.cvatXmlList:
            error_handling("cvatXmlList is Empty. There are no files to run the program. Quit the program.", filename(), lineNum())
            showErrorList()
            sys.exit(-1)

        SuccessLog(f"Extract cvatXmlList Done : {len(self.cvatXmlList)} Files")


    # RunFunctionName 을 set 하는 함수
    def setRunFunctionName(self, funcName):
        self.RunFunctionName = funcName


    # RunFunctionName 을 get 하는 함수
    def getRunFunctionName(self):
        return self.RunFunctionName


    # cvatXmlList 를 리셋하고 다시 채워넣는 함수
    def setChanged_Xml_n_Res_Path(self, xmlPath, resPath):
        self.OriginXmlDirPath = xmlPath
        self.LogToExcel.set_ResDir(resPath)

        self.extract_cvatXmlList()


    # Default CheckCond 들을 규칙에 맞게 리스트로 만들어서 반환하는 함수
    def setInitCheckCondList(self):
        initCheckCondList = [   ['CheckMissingImg',     self.CheckMissingImg,   self.getArgs_CheckMissingImg],
                                ['CheckLabelCount',     self.CheckLabelCount,   self.getArgs_CheckLabelCount],
                                ['CheckLabelNested',    self.CheckLabelNested,  self.getArgs_CheckLabelNested],
                                ['CheckBagError',       self.CheckBagError,     self.getArgs_CheckBagError]
                            ]
        return initCheckCondList


    # imageName 이 입력되었는지 체크하는 조건 함수
    def CheckMissingImg(self, imageName):
        if not imageName:
            return COND_FAIL
        return COND_PASS


    # 해당 이미지의 label 이 네 개 다 있는지 1차 체크하는 함수
    def CheckLabelCount(self, labelCount):
        if labelCount != 4:
            return COND_FAIL
        return COND_PASS


    # 해당 이미지의 label 이 각각 별개의 값인지 2차 체크하는 함수
    def CheckLabelNested(self, labelSetLen):
        if labelSetLen != 4:
            return COND_FAIL
        return COND_PASS


    # 가방에 해당하는 값이 두 개 이상인지 체크하는 함수
    def CheckBagError(self, boxValue):
        bagList  = ["unknown_bag", "plasticbag", "shoulderbag", "handbag", "backpack", "bagless"]
        ValidBox = [ box for box in boxValue if box.get('label') == 'all' ]
        bagCount = 0

        for box in ValidBox:
            for att in box.findall('attribute'):
                if att.get('name') in bagList:
                    bagCount += isTrue(att.text)

        if bagCount != 1:
            return COND_FAIL
        return COND_PASS


    # 각 이미지별로 CheckMissingImg() 조건 함수를 실행하기 위해 이미지마다 변동되는 인자를 리턴하는 함수
    def getArgs_CheckMissingImg(self):
        return self.getCurImgName()


    # 각 이미지별로 CheckLabelCount() 조건 함수를 실행하기 위해 이미지마다 변동되는 인자를 리턴하는 함수 
    def getArgs_CheckLabelCount(self):
        return len(self.getCurBoxList())


    # 각 이미지별로 CheckLabelNested() 조건 함수를 실행하기 위해 이미지마다 변동되는 인자를 리턴하는 함수 
    def getArgs_CheckLabelNested(self):
        boxValue    = self.getCurBoxList()
        labelList   = []

        for box in boxValue:
            labelList.append(box.get('label'))
        
        return len(set(labelList))


    # 각 이미지별로 CheckBagError() 조건 함수를 실행하기 위해 이미지마다 변동되는 인자를 리턴하는 함수
    def getArgs_CheckBagError(self):
        return self.getCurBoxList()


    # CvatXml 클래스를 상속받은 클래스가 실제로 실행하는 RunFunction 부분
    @abstractmethod
    def RunFunction(self):
        pass

    # 재정의된 RunFunction 이 사용할 인자들을 set 하는 함수
    @abstractmethod
    def setRunFunctionParam(self):
        pass

    # RunFunction 의 결과값(True/False) 에 따라 실행 되는 함수
    @abstractmethod
    def AfterRunFunction(self): 
        pass

    # 재정의 된 AfterRunFunction 이 사용할 인자들을 set 하는 함수
    @abstractmethod
    def setAfterRunFunctionParam(self):
        pass

    # 모든 RunFunction 이 끝나고 run() 함수 마지막에 실행하는 함수
    @abstractmethod
    def FinishFunction(self):
        pass

    # 재정의 된 FinishFunction 이 사용할 인자들을 set 하는 함수
    @abstractmethod
    def setFinishFunctionParam(self):
        pass


    def setCurBoxList(self, boxList):
        self.CurBoxListByImage = boxList

    def getCurBoxList(self):
        return self.CurBoxListByImage


    def setCurImgName(self, imgName):
        self.CurImageName = imgName

    def getCurImgName(self):
        return self.CurImageName


    def setCurImgSize(self, sizeList):
        self.CurImageSizeList = sizeList

    def getCurImgSize(self):
        return self.CurImageSizeList

    # 현재 진행상황 Percentage Bar 로 시각화 해서 터미널에 보여주는 함수
    def showCurCount(self, curCount, totalCount):
        if curCount == totalCount:
            print(' '*100, '\r', end='')
            return
            
        percentCount = int(curCount * self.checkPercentageNum)

        if percentCount != self.prePercentageCount:
            curBar  = '#' if CRESET == '' else '|'
            showBar = f'{CGREEN}' + f'{curBar}' * percentCount + f'{CRESET}' + '|' * (50 - percentCount)
            print(f' [ {curCount:^5} / {totalCount:5} ] {showBar:60} {percentCount*2:3}%\r', end='')

        self.prePercentageCount = percentCount

    # xml 파일 읽고 실행하는 함수
    def runEachXmlFile(self, eachXmlFile):
        FullXmlPath     = eachXmlFile
        tree            = ET.parse(FullXmlPath)
        note            = tree.getroot()

        noteImage       = note.findall("image")
        totalImgCount   = len(noteImage)
        SuccessCount    = 0

        self.checkPercentageNum = 50 / totalImgCount

        print(f"* [{FullXmlPath}] - Image Count {totalImgCount}")
        print("--------------------------------------------------------------------------------------")

        self.condClass.resetCurFailCheckAll()

        for idx, eachImage in enumerate(noteImage):
            self.showCurCount(idx + 1, totalImgCount)

            imgName  = eachImage.get("name")
            boxValue = eachImage.findall("box")
            sizeList = [int(eachImage.get("width")), int(eachImage.get("height"))]

            self.setCurBoxList(boxValue)
            self.setCurImgName(imgName)
            self.setCurImgSize(sizeList)

            checkRes, failCondName = self.condClass.checkCondAllParam()

            if checkRes == COND_FAIL:
                self.CC_LogList.append([ eachXmlFile, imgName, failCondName ])
                continue

            self.setRunFunctionParam()

            runFuncRes = True
            runFuncRes = self.RunFunction()

            if runFuncRes is False:
                self.setAfterRunFunctionParam()
                self.AfterRunFunction()
                continue

            SuccessCount += 1

        self.condClass.showCurFailLog()

        return totalImgCount, SuccessCount


    # 클래스를 실행하는 함수
    def run(self):
        if self.RunFunctionName == "NoneFunction":
            error_handling('Is Set RunFunction? check setRunFunctionName()', filename(), lineNum())

        print()
        NoticeLog(f'{self.RunFunctionName} START\n')

        TotalRunImageCount  = 0
        TotalSuccessCount   = 0
        XmlFileCount        = len(self.cvatXmlList)
        TimeList            = []

        TimeList.append(getCurTime())

        for idx, eachXmlPath in enumerate(self.cvatXmlList):
            print(f"[ {CGREEN}{idx+1:3}{CRESET} / {XmlFileCount:3} ]")
            print("--------------------------------------------------------------------------------------")
            perRunImage, perSuccessCount    = self.runEachXmlFile(eachXmlPath)
            TotalRunImageCount              += perRunImage
            TotalSuccessCount               += perSuccessCount

        TimeList.append(getCurTime())

        self.setOperateImageCount(TotalRunImageCount, TotalSuccessCount)

        self.setFinishFunctionParam()
        self.FinishFunction()

        self.LogToExcel.set_ErrorLogList(self.CC_LogList)
        self.LogToExcel.saveLogToFile()

        self.FinishLog(TotalRunImageCount, TotalSuccessCount, TimeList, XmlFileCount)
        

    # 넘겨받은 인자값들을 참고하여 Result Summary Print
    def FinishLog(self, TotalRun, TotalSuccess, TimeList, FileCount):
        print()
        print(f"# [ {self.RunFunctionName} DONE ] -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
        self.condClass.showTotalFailLog()
        print("# [ INFO ]")
        print(f"- {'Program Start':36} : {timeToString(TimeList[START])}")
        print(f"- {'Program End':36} : {timeToString(TimeList[END])}")
        print(f"- {'RunTime':36} : {diffTime(TimeList[START], TimeList[END])}")
        print(f"- {'Total Run Image Count':36} : {TotalRun} ( {FileCount} Files )")
        print(f"- {'Total Success Count':36} : {TotalSuccess}")
        print("--------------------------------------------------------------------------------------")
        print(f"# [ {self.RunFunctionName} DONE ] -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*\n")
        showErrorList()


    def setOperateImageCount(self, TotalRunCount, TotalSuccessCount):
        self.TotalRunImgCount   = TotalRunCount
        self.SuccessImageCount  = TotalSuccessCount
    
    def getOperateImageCount(self):
        return self.TotalRunImgCount, self.SuccessImageCount