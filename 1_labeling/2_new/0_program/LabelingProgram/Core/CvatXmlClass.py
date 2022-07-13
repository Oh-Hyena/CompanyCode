# IMPORT
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
import  sys
import  os
import  xml.etree.ElementTree   as ET
from    abc                     import *    # 추상 클래스를 만들기 위한 모듈


# Refer to CoreDefine.py
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
from CoreDefine                 import *


# IMPORT CORE
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
from Core.CommonUse             import *
from Core.CheckCondClass        import CheckCondition
from Core.SaveLogClass          import SaveErrorLog


# CONST DEFINE
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
START = 0
END   = 1


# CvatXml Class
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
class CvatXml(metaclass=ABCMeta):
    def __init__(self, OriginVideoDirPath):
        self.videoList          = []
        self.OriginVideoDirPath = OriginVideoDirPath

        self.RunFunctionName    = "NoneFunction"

        self.CurBoxListByImage  = []
        self.CurImageName       = ""
        self.CurImageSizeList   = []

        self.checkPercentageNum = 0
        self.prePercentageCount = 0

        self.TotalRunImgCount   = 0
        self.SuccessImageCount  = 0


    def extract_videoList(self):
        self.videoList.clear()

        # 경로가 실제로 있는지 체크하고, 없다면 프로그램 종료
        CheckExistDir(self.OriginVideoDirPath)

        # 실제 있는 경로면, xml 파일들만 목록에 추가
        for path, _, files in os.walk(self.OriginVideoDirPath):
            for eachFile in files:
                _, ext = os.path.splitext(eachFile)
                if ext != ".mp4":
                    error_handling(f"{eachFile} is Not VIDEO", filename(), lineNum())
                    break
                else:
                    self.videoList.append(os.path.join(path, eachFile))

        if not self.videoList:
            error_handling("videoList is Empty. There are no files to run the program. Quit the program.", filename(), lineNum())
            showErrorList()
            sys.exit(-1)

        SuccessLog(f"Extract videoList Done : {len(self.videoList)} Files")


    def setRunFunctionName(self, funcName):
        self.RunFunctionName = funcName

    def getRunFunctionName(self):
        return self.RunFunctionName


    # 가상 함수 : 상속받은 클래스에서 해당 함수를 정의해야만 함
    # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
    @abstractmethod
    def RunFunction(self):
        pass

    @abstractmethod
    def setRunFunctionParam(self):
        pass

    @abstractmethod
    def AfterRunFunction(self):
        pass

    @abstractmethod
    def setAfterRunFunctionParam(self):
        pass

    @abstractmethod
    def FinishFunction(self):
        pass

    @abstractmethod
    def setFinishFunctionParam(self):
        pass


    # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
    def setCurBoxList(self, boxList):
        self.CurBoxListByImage = boxList

    def getCurBoxList(self):
        return self.CurBoxListByImage


    # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
    def setCurImgName(self, imgName):
        self.CurImageName = imgName

    def getCurImgName(self):
        return self.CurImageName


    # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
    def setCurVideoName(self, VideoName):
        self.CurVideoName = VideoName

    def getCurVideoName(self):
        return self.CurVideoName


    # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
    def setCurImgSize(self, sizeList):
        self.CurImageSizeList = sizeList

    def getCurImgSize(self):
        return self.CurImageSizeList


    # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
    def showCurCount(self, curCount, totalCount):
        # 100% 완료되면 잔상 지우려고 해당 줄 싹 밀어버리기
        if curCount == totalCount:
            print(' '*100, '\r', end='')
            return
            
        percentCount = int(curCount * self.checkPercentageNum)

        # 이미지가 넘어갈 때마다 터미널에 보여주면 너무 속도 느려지니까, 퍼센트값이 달라질때만 출력
        # 만약 이미지가 80000개면 80000번 출력할 걸 50번(2%마다 출력하니까) 출력으로 압축 
        if percentCount != self.prePercentageCount:
            curBar  = '#' if CRESET == '' else '|'
            showBar = f'{CGREEN}' + f'{curBar}' * percentCount + f'{CRESET}' + '|' * (50 - percentCount)
            print(f' [ {curCount:^5} / {totalCount:5} ] {showBar:60} {percentCount*2:3}%\r', end='')

        self.prePercentageCount = percentCount


    def runEachVideoFile(self, eachVideoFile):
        FullVideoPath = eachVideoFile

        self.setCurVideoName(FullVideoPath)

        self.setRunFunctionParam()

        runFuncRes = True
        runFuncRes = self.RunFunction()
    
        if runFuncRes is False:
            self.setAfterRunFunctionParam()
            self.AfterRunFunction()

        return True


    def run(self):
        # setRunFunctionName() 을 안 했다면 여기서 일단 체크 : 안전장치
        if self.RunFunctionName == "NoneFunction":
            error_handling('Is Set RunFunction? check setRunFunctionName()', filename(), lineNum())

        print()
        NoticeLog(f'{self.RunFunctionName} START\n')

        # Result Summary 출력을 위한 Count 변수들
        VideoFileCount      = len(self.videoList)
        TimeList            = []

        # 시작 시간 체크
        TimeList.append(getCurTime())

        # cvatXmlList 하나씩 돌면서 각 xml 파일을 runEachXmlFile() 실행
        for idx, eachVideoPath in enumerate(self.videoList):
            print(f"[ {CGREEN}{idx+1:3}{CRESET} / {VideoFileCount:3} ]")
            print("--------------------------------------------------------------------------------------")
            self.runEachVideoFile(eachVideoPath)

        # 종료 시간 체크
        TimeList.append(getCurTime())

        # 상속 받은 클래스에서 재정의 된 최종 실행 함수 - 후처리 함수들
        self.setFinishFunctionParam()
        self.FinishFunction()

        # 다 돌고나서 Result Print
        self.FinishLog(TimeList, VideoFileCount)
        

    def FinishLog(self, TimeList, FileCount):
        print()
        print(f"# [ {self.RunFunctionName} DONE ] -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
        print("# [ INFO ]")
        print(f"- {'Program Start':36} : {timeToString(TimeList[START])}")
        print(f"- {'Program End':36} : {timeToString(TimeList[END])}")
        print(f"- {'RunTime':36} : {diffTime(TimeList[START], TimeList[END])}")
        print("--------------------------------------------------------------------------------------")
        print(f"# [ {self.RunFunctionName} DONE ] -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*\n")
        showErrorList()


    def setOperateImageCount(self, TotalRunCount, TotalSuccessCount):
        self.TotalRunImgCount   = TotalRunCount
        self.SuccessImageCount  = TotalSuccessCount
    
    def getOperateImageCount(self):
        return self.TotalRunImgCount, self.SuccessImageCount