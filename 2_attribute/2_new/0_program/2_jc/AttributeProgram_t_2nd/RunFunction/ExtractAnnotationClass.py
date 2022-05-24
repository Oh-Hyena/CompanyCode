"""
This python file is a code that extracts a random percentage 
from a given xml file and image path file.

Set the source file path to extract,
After setting the file name to save the result value,
Adjust the extraction manipulation parameters.

LAST_UPDATE : 21/11/09
AUTHOR      : OH HYENA
"""


from    random  import randint, sample
import  os
import  sys
import  copy
import  pandas                   as pd


sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../UI/SelectUI'))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../Core'))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../'))


from CoreDefine                 import *
from Core.CommonUse             import *
from Core.ExcelDataClass        import ExcelData
from Core.SingletonClass        import Singleton
from UI.SelectUI.SelectUIClass  import *


AnnotationFile          = copy.copy(OriginSource_AnntationPath)
ImgListFile             = copy.copy(OriginSource_ImageListPath)
ResultDirPath           = copy.copy(Result_Dir_Path)

encodingFormat          = copy.copy(CORE_ENCODING_FORMAT)
validImgFormat          = copy.copy(VALID_IMG_FORMAT)

SaveAnnotationFileName  = "Annotation.txt"
SaveImgFileName         = "ImgList.txt"

RandomExtractPrefix     = "RandomExtract"
SplitTrainPrefix        = "Split_Train"
SplitTestPrefix         = "Split_Test"

ConditionExtractPrefix  = "ConditionExtract"
ExtractResExcelPath     = "ExtractAnnotation.xlsx"


RUN_RANDOM_EXTRACT      = True
RUN_SPLIT_TRAIN_TEST    = False


overCount               = 0     # 각 객체 유효값 합이 최소 overCount
ExtractPercent          = 50    # 몇 %나 원본에서 추출할지
SplitPercent            = 75    # 몇 대 몇으로 슬라이스 할지(백분위)


class ExtractAnnotation(Singleton):
    def __init__(self, QApp):
        self.app = QApp
        self.ProgramName            = "ExtractAnnotation"

        self.TotalObjectSumList     = []    
        self.ExtractObjectSumlist   = []    
        self.Sp_TrainObjectSumList  = [] 
        self.Sp_TestObjectSumList   = [] 

        self.AnnotationTxtList      = []    
        self.AnnotationImgList      = []   

        self.ExtractRandomTxtList   = []   
        self.ExtractRandomIdxList   = []   
        self.ExtractRandomImgList   = []

        self.SplitTrainResTxtList   = []
        self.SplitTrainResImgList   = []
        self.SplitTestResTxtList    = []
        self.SplitTestResImgList    = []
        self.ConditionResTxtList    = []
        self.ConditionResImgList    = []

        self.overCount              = overCount
        self.ExtractPercent         = ExtractPercent
        self.SplitPercent           = SplitPercent

        self.ClassNum               = 0   
        self.TryCount               = 1  

        self.classData              = None
        self.classNameList          = []

        self.sendArgsList           = []

        self.initializeEA()


    def initializeEA(self):
        self.selectUi = SelectUI(self.setInitSettingForSelectUI, self.getEditSettingForSelectUI)

        self.selectUi.show()
        self.app.exec()

        if self.selectUi.isQuitProgram():
            return

        self.initAfterSetUI()
        self.setMode()

    
    def initAfterSetUI(self):
        self.classData = ExcelData()

        CheckExistFile(AnnotationFile)
        readFileToList(AnnotationFile, self.AnnotationTxtList, encodingFormat)

        if self.checkTotalObjectSum() is False:
            error_handling(f'checkTotalObjectSum() Faild', filename(), lineNum())

        CheckExistFile(ImgListFile)
        readFileToList(ImgListFile, self.AnnotationImgList, encodingFormat)

        self.countClassNum()
        self.classNameList = self.classData.getClassNameListByClassNum(self.ClassNum)

        if self.classNameList is None:
            error_handling('Load ClassName Failed', filename(), lineNum())


    def setMode(self):
        if RUN_RANDOM_EXTRACT is True:
            ModeLog('RANDOM_EXTRACT ON')

        if RUN_SPLIT_TRAIN_TEST is True:
            ModeLog('SPLIT_TRAIN_TEST ON')


    def setInitSettingForSelectUI(self):
        self.SyncAllValue()
        self.sendArgsList = [   ['FD', 'AnnotationFile',            False,  f'{AnnotationFile}'],
                                ['FD', 'ImgListFile',               False,  f'{ImgListFile}'],
                                ['FD', 'ResultDirPath',             True,   f'{ResultDirPath}'],

                                ['CB', 'RUN_RANDOM_EXTRACT',        False,  f'{RUN_RANDOM_EXTRACT}'],
                                ['CB', 'RUN_SPLIT_TRAIN_TEST',      False,  f'{RUN_SPLIT_TRAIN_TEST}'],

                                ['LE', 'overCount',                 False,  f'{overCount}'],
                                ['LE', 'ExtractPercent',            False,  f'{ExtractPercent}'],

                                ['LE', 'HLINE_1',                   False,  'None'],
                                ['LE', 'SplitPercent',              False,  f'{SplitPercent}'],
                                ['LE', 'HLINE_2',                   False,  'None'],
                                ['LE', 'SaveAnnotationFileName',    False,  f'{SaveAnnotationFileName}'],
                                ['LE', 'SaveImgFileName',           False,  f'{SaveImgFileName}'],
                                ['LE', 'RandomExtractPrefix',       False,  f'{RandomExtractPrefix}'],
                                ['LE', 'SplitTrainPrefix',          False,  f'{SplitTrainPrefix}'],
                                ['LE', 'SplitTestPrefix',           False,  f'{SplitTestPrefix}'],
                            ]
        return self.ProgramName, self.sendArgsList


    # SelectUI 에서 넘겨받은 값 적용
    def getEditSettingForSelectUI(self):
        NAME        = 1        
        returnDict  = self.selectUi.getReturnDict()

        print("\n* Change Path/Define Value By SelectUI")
        print("--------------------------------------------------------------------------------------")
        for Arg in self.sendArgsList:
            eachTarget = Arg[NAME]
            if returnDict.get(eachTarget) != None:
                # 해당 변수명에 SelectUI 에서 갱신된 값 집어넣기
                globals()[eachTarget] = returnDict[eachTarget]
                showLog(f'- {eachTarget:40} -> {globals()[eachTarget]}')
        print("--------------------------------------------------------------------------------------\n")

        self.SyncAllValue()
        setResultDir(ResultDirPath)
        self.overCount          = int(overCount)    
        self.ExtractPercent     = int(ExtractPercent)
        self.SplitPercent       = int(SplitPercent)


    def SyncAllValue(self):
        self.SyncEachValue('OriginSource_AnntationPath',    'AnnotationFile')
        self.SyncEachValue('OriginSource_ImageListPath',    'ImgListFile')
        self.SyncEachValue('Result_Dir_Path',               'ResultDirPath')

    def SyncEachValue(self, CoreName, LinkName, SENDER_DEPTH=3):
        if callername(SENDER_DEPTH) == 'setInitSettingForSelectUI':
            globals()[LinkName] = getCoreValue(CoreName)

        elif callername(SENDER_DEPTH) == 'getEditSettingForSelectUI':
            setCoreValue(CoreName, globals()[LinkName])


    def countClassNum(self):
        if not self.AnnotationTxtList:
            error_handling(f"{AnnotationFile} has nothing annotation list", filename(), lineNum())
            return False

        if self.ClassNum != 0:
            return True
        
        self.ClassNum = len(self.AnnotationTxtList[0])
        NoticeLog(f"ClassNum : {self.ClassNum}")

        return True


    # 각 객체마다 overCount가 넘는지 체크
    def isOverCount(self, checkObjectSum):
        if checkObjectSum >= self.overCount:
            return True
        else:
            return False


    def checkTotalObjectSum(self):
        if not self.AnnotationTxtList:
            error_handling(f"{AnnotationFile} has nothing annotation list", filename(), lineNum())
            return False

        if self.countClassNum() is False:
            return False

        self.TotalObjectSumList = [ 0 for _ in range(self.ClassNum) ]
        NoticeLog(f'Total Annotation Count - {len(self.AnnotationTxtList)}')

        for idx, each in enumerate(self.AnnotationTxtList):
            try:
                for i in range(self.ClassNum):
                    self.TotalObjectSumList[i] += int(each[i])
            except Exception as e:
                error_handling(f"{idx} Line Error - Contents : {each}", filename(), lineNum())
                sys.exit(-1)

        return True


    def checkExtractObjectSum(self):
        if not self.ExtractRandomTxtList:
            error_handling("'checkExtractObjectSum()' Failed - has nothing extract random list", filename(), lineNum())
            return False

        if self.countClassNum() is False:
            return False

        extractObjectSumList = [ 0 for _ in range(self.ClassNum) ]

        for each in self.ExtractRandomTxtList:
            for i in range(self.ClassNum):
                extractObjectSumList[i] += int(each[i])

        for i in range(self.ClassNum):
            checkNum = extractObjectSumList[i]
            if self.isOverCount(checkNum) is False:
                print(f'\t> Fail - {i}th Element [{self.classNameList[i]:^15}] is Not Over {self.overCount} : {checkNum}')
                return False

        self.ExtractObjectSumlist = extractObjectSumList
        return True


    def checkSplitTrainObjectSum(self):
        self.Sp_TrainObjectSumList = [0 for _ in range(self.ClassNum)]

        for each in self.SplitTrainResTxtList:
            for i in range(self.ClassNum):
                self.Sp_TrainObjectSumList[i] += int(each[i])

    
    def checkSplitTestObjectSum(self):
        self.Sp_TestObjectSumList = [0 for _ in range(self.ClassNum)]

        for each in self.SplitTestResTxtList:
            for i in range(self.ClassNum):
                self.Sp_TestObjectSumList[i] += int(each[i])


    def showResult(self):
        DF_HeadString       = "  ClassIdx  |  ClassName      |  TotalSum        "
        RE_HeadString       = ""
        SP_HeadString       = ""

        DF_Line             = ""
        RE_Line             = ""
        SP_Line             = ""

        RE_EachPercent      = 0

        printLine           = '------------------------------------------------'

        if RUN_RANDOM_EXTRACT is True:
            RE_HeadString   = "|  ExtractSum      |  %        "
            printLine       += "------------------------------"

        if RUN_SPLIT_TRAIN_TEST is True:
            SP_HeadString   = "|  TrainSum        |  TestSum        "
            printLine       += "-------------------------------------"

            self.checkSplitTrainObjectSum()
            self.checkSplitTestObjectSum()

        HeadString          = f'{DF_HeadString}{RE_HeadString}{SP_HeadString}'

        print()
        print(printLine)
        print(HeadString)
        print(printLine)

        for i in range(self.ClassNum):
            if RUN_RANDOM_EXTRACT is True:
                if self.TotalObjectSumList[i] != 0:
                    RE_EachPercent = (self.ExtractObjectSumlist[i] / self.TotalObjectSumList[i]) * 100
                else:
                    RE_EachPercent = 0
                RE_Line = f'|  {self.ExtractObjectSumlist[i]:<16}|  {round(RE_EachPercent, 2):>6}%  '
            if RUN_SPLIT_TRAIN_TEST is True:
                SP_Line = f'|  {self.Sp_TrainObjectSumList[i]:<16}|  {self.Sp_TestObjectSumList[i]:<16}'

            DF_Line = f'  {i:<10}|  {self.classNameList[i]:<15}|  {self.TotalObjectSumList[i]:<16}'
            print(f'{DF_Line}{RE_Line}{SP_Line}')

        print(printLine)
        print()

        showLog(f"* Total Try\t\t: {self.TryCount}")
        showLog(f"* Origin File Count\t: {len(self.AnnotationTxtList)}")

        if RUN_RANDOM_EXTRACT:
            extractRealPercent = (len(self.ExtractRandomTxtList) / len(self.AnnotationTxtList)) * 100
            showLog(f"* RE_Condition\t\t: Extract {self.ExtractPercent}% ( eachSum >= {self.overCount} )")
            showLog(f"* Extract File Count\t: {len(self.ExtractRandomTxtList)} ( {round(extractRealPercent,2):>6}% )")
        
        if RUN_SPLIT_TRAIN_TEST:
            showLog(f"* SP_Condition\t\t: Train {self.SplitPercent}% - Test {100-int(self.SplitPercent)}%")
        print()

    
    def saveResultByExcel(self):
        classNameList = self.classNameList

        raw_data =  {   'ClassName':classNameList,
                        'TotalSum':self.TotalObjectSumList
                    }

        if RUN_RANDOM_EXTRACT:
            raw_data['ExtractSum'] = self.ExtractObjectSumlist

        if RUN_SPLIT_TRAIN_TEST:
            raw_data['TrainSetSum'] = self.Sp_TrainObjectSumList
            raw_data['TestSetSum']  = self.Sp_TestObjectSumList

        raw_data = pd.DataFrame(raw_data)
        savePath = ExtractResExcelPath

        if RUN_SPLIT_TRAIN_TEST:
            savePath = f'SP[{self.SplitPercent}Pcnt]_' + savePath
        
        if RUN_RANDOM_EXTRACT:
            savePath = f'RE[{self.ExtractPercent}Pcnt_{self.overCount}OvCnt]_' + savePath

        savePath = os.path.join(ResultDirPath, savePath)
        raw_data.to_excel(excel_writer=savePath)

        SuccessLog(f'RandomExtract Summary Log Save to Excel File -> {savePath}')


    def RunRandomExtract(self):
        # 유효한 추출값(각 Element 합이 OverCount 이상일 때) 뽑을 때까지 반복하는 While 문
        while True:
            print()
            showLog(f"[{self.TryCount} Try] Select Correct List : Each ObjectSum over {overCount} [ Total File Count : {len(self.AnnotationTxtList)} ]")

            self.ExtractRandomTxtList.clear()
            self.ExtractRandomIdxList.clear()
            randomNum = 0

            for Idx, eachTxt in enumerate(self.AnnotationTxtList):
                randomNum = randint(1, 100)
                if randomNum <= self.ExtractPercent: # 여기서 정한 %만큼 추출
                    self.ExtractRandomTxtList.append(eachTxt)
                    self.ExtractRandomIdxList.append(Idx)

            showLog("\t> Extract Done. Check...")
            if self.checkExtractObjectSum() is True:
                showLog("\t> Extract Success!\n")
                break

            self.TryCount += 1

        for eachIdx in self.ExtractRandomIdxList:
            self.ExtractRandomImgList.append(self.AnnotationImgList[eachIdx])


    def SaveRandomExtract(self):
        SaveAnnoResFileName = f'{RandomExtractPrefix}_[{self.ExtractPercent}]Pcnt_[{self.overCount}]OverCnt_{SaveAnnotationFileName}'
        TextSavePath        = os.path.join(ResultDirPath, SaveAnnoResFileName)

        SaveImgResFileName  = f'{RandomExtractPrefix}_[{self.ExtractPercent}]Pcnt_[{self.overCount}]OverCnt_{SaveImgFileName}'
        ImageSavePath       = os.path.join(ResultDirPath, SaveImgResFileName)

        writeListToFile(TextSavePath,   self.ExtractRandomTxtList,  encodingFormat)
        writeListToFile(ImageSavePath,  self.ExtractRandomImgList,  encodingFormat)


    def SaveSplitExtract(self):
        SaveTrainAnnoFileName   = f'{SplitTrainPrefix}_[{self.SplitPercent}]Pcnt_{SaveAnnotationFileName}'
        SaveTestAnnoFileName    = f'{SplitTestPrefix}_[{100 - int(self.SplitPercent)}]Pcnt_{SaveAnnotationFileName}'
        TrainAnnoSavePath       = os.path.join(ResultDirPath, SaveTrainAnnoFileName)
        TestAnnoSavePath        = os.path.join(ResultDirPath, SaveTestAnnoFileName)

        writeListToFile(TrainAnnoSavePath,  self.SplitTrainResTxtList,  encodingFormat)
        writeListToFile(TestAnnoSavePath,   self.SplitTestResTxtList,   encodingFormat)

        SaveTrainImgFileName    = f'{SplitTrainPrefix}_[{self.SplitPercent}]Pcnt_{SaveImgFileName}'
        SaveTestImgFileName     = f'{SplitTestPrefix}_[{100 - int(self.SplitPercent)}]Pcnt_{SaveImgFileName}'
        TrainImgSavePath        = os.path.join(ResultDirPath, SaveTrainImgFileName)
        TestImgSavePath         = os.path.join(ResultDirPath, SaveTestImgFileName)

        writeListToFile(TrainImgSavePath,  self.SplitTrainResImgList,  encodingFormat)
        writeListToFile(TestImgSavePath,   self.SplitTestResImgList,   encodingFormat)


    def RunSplitAnnotation(self):
        TotalAnnotationCount        = 0
        BaseAnnotationList          = []
        BaseImgList                 = []
        TextPairImgDict             = {}

        ANNOTATION_IDX              = 0
        IMAGELIST_IDX               = 1

        if RUN_RANDOM_EXTRACT is True:
            TotalAnnotationCount    = len(self.ExtractRandomTxtList)
            BaseAnnotationList      = self.ExtractRandomTxtList[:]
            BaseImgList             = self.ExtractRandomImgList[:]
        else:
            TotalAnnotationCount    = len(self.AnnotationTxtList)
            BaseAnnotationList      = self.AnnotationTxtList[:]
            BaseImgList             = self.AnnotationImgList[:]

        for idx in range(TotalAnnotationCount):
            TextPairImgDict[idx]    = [BaseAnnotationList[idx], BaseImgList[idx]]

        TotalIdxList                = [ i for i in range(TotalAnnotationCount) ]
        SplitTrainAmount            = int( (TotalAnnotationCount * self.SplitPercent) / 100 )
        SplitTrainIdxList           = sample(TotalIdxList, SplitTrainAmount)
        SplitTestIdxList            = list(filter(lambda v: v not in SplitTrainIdxList, TotalIdxList))

        showLog('\nSplit Train - Test Set Done')
        showLog('------------------------------------------------------')
        showLog(f'- TotalCount : {TotalAnnotationCount}')
        showLog(f'- TrainCount : {len(SplitTrainIdxList)}')
        showLog(f'- TestCount  : {len(SplitTestIdxList)}\n')

        for eachIdx in SplitTrainIdxList:
            self.SplitTrainResTxtList.append(TextPairImgDict[eachIdx][ANNOTATION_IDX])
            self.SplitTrainResImgList.append(TextPairImgDict[eachIdx][IMAGELIST_IDX])

        for eachIdx in SplitTestIdxList:
            self.SplitTestResTxtList.append(TextPairImgDict[eachIdx][ANNOTATION_IDX])
            self.SplitTestResImgList.append(TextPairImgDict[eachIdx][IMAGELIST_IDX])


    def saveResult(self):
        if RUN_RANDOM_EXTRACT is True:
            self.SaveRandomExtract()

        if RUN_SPLIT_TRAIN_TEST is True:
            self.SaveSplitExtract()


    def run(self):
        if self.selectUi.isQuitProgram():
            NoticeLog(f'{self.__class__.__name__} Program EXIT\n')
        else:
            if RUN_RANDOM_EXTRACT is True:
                self.RunRandomExtract()

            if RUN_SPLIT_TRAIN_TEST is True:
                self.RunSplitAnnotation()

            self.saveResult()
            self.showResult()
            self.saveResultByExcel()

            os.startfile(ResultDirPath)


if __name__ == "__main__":
    App         = QApplication(sys.argv)
    RunProgram  = ExtractAnnotation(App)
    RunProgram.run()