"""
Class code that reads, stores, and processes data for MakeClass in an Excel file

LAST_UPDATE : 2021/11/08
AUTHOR      : OH HYENA
"""


from CoreDefine import *
from Core.CommonUse         import *
from Core.SingletonClass    import Singleton

import pandas as pd


EXCEL_PATH = r"classData.xlsx"

DEFAULT_CLASS_NUM       = 83
MAKECLASS_MAX_CNT       = 2

DELETE_VALUE_24CLASS    = 1

DELETE_LIST_24CLASS_IDX = 0

FIX_HAT_ANNOTATE_ERROR  = True
HATLESS_IDX             = 29
EQUIPED_HAT_START_IDX   = 31
EQUIPED_HAT_END_IDX     = 41


class ExcelData(Singleton):
    # classData.xlsx 의 시트들을 읽고, 기초 전처리 및 에러 처리하는 init 부분
    def __init__(self):
        CheckExistFile(EXCEL_PATH)

        self.df_ClassData = pd.read_excel(EXCEL_PATH, sheet_name='ClassData')
        self.df_MergeData = pd.read_excel(EXCEL_PATH, sheet_name='MergeData')
        self.df_NameData  = pd.read_excel(EXCEL_PATH, sheet_name='NameData')
        self.df_CtgrData  = pd.read_excel(EXCEL_PATH, sheet_name='CategoryData')

        self.IdxDict    = {}
        self.DataDict   = {}
        self.mergeDict  = {}
        self.mergeList  = []

        self.class83NameDict = {}
        self.class24NameDict = {}

        self.unknownList    = []
        self.deleteList     = [ [] for _ in range(1, MAKECLASS_MAX_CNT) ]

        self.MakeClassDefaultData  = [ 0 for _ in range(DEFAULT_CLASS_NUM) ]
        self.defaultClassNameDict  = {}
        self.categoryDict          = {} 
        self.categoryNameDict      = {} 

        self.checkDefaultClassNum()

        self.pretreatmentMergeData()
        self.pretreatmentClassData()
        self.pretreatmentNameData()
        self.pretreatmentCategoryNameData()

        SuccessLog('ExcelData Set Done')


    # 읽어들인 데이터의 갯수가 83개가 맞는지 체크하는 함수
    def checkDefaultClassNum(self):
        ReadClassNum = len(self.df_ClassData)
        if DEFAULT_CLASS_NUM != ReadClassNum:
            error_handling(f'Read Class Count Not {DEFAULT_CLASS_NUM} : {ReadClassNum}', filename(), lineNum())
            sys.exit(-1)


    # MergeData 시트에 해당하는 부분 전처리하는 함수
    def pretreatmentMergeData(self):
        MergeIdxNum = len(self.df_MergeData)

        TotalOriginList     = self.df_MergeData['originIdx'].tolist()
        Total24MergList     = self.df_MergeData['mergeIdx_24'].tolist()

        for idx in range(0, MergeIdxNum):
            curOriginIdx    = TotalOriginList[idx]
            curMerge24Idx   = Total24MergList[idx]
            self.mergeDict[curOriginIdx] = [curMerge24Idx]

        self.mergeList = [ [] for _ in range(0, MergeIdxNum) ]


    # NameData 시트에 해당하는 부분 전처리하는 함수
    def pretreatmentNameData(self):
        Total83NameList     = self.df_NameData['class83'].tolist()
        Total24NameList     = self.df_NameData['class24'].tolist()

        for idx in range(DEFAULT_CLASS_NUM):
            self.class83NameDict[idx] = Total83NameList[idx]
            self.class24NameDict[idx] = Total24NameList[idx]


    # CategoryData 시트에 해당하는 부분 전처리하는 함수
    def pretreatmentCategoryNameData(self):
        CategoryIdxNum      = len(self.df_CtgrData)
        TotalCtIdxList      = self.df_CtgrData['categoryIdx'].tolist()
        TotalCtNameList     = self.df_CtgrData['categoryName'].tolist()

        for idx in range(CategoryIdxNum):
            curCategoryIdx  = TotalCtIdxList[idx]
            curCategoryName = TotalCtNameList[idx]
            self.categoryNameDict[curCategoryIdx] = curCategoryName


    # ClassData 시트에 해당하는 부분 전처리하는 함수
    def pretreatmentClassData(self):
        TotalClassNameList  = self.df_ClassData['className'].tolist()
        TotalAttNameList    = self.df_ClassData['attName'].tolist()
        TotalAttTextList    = self.df_ClassData['attText'].tolist()
        TotalMergeIdxList   = self.df_ClassData['mergedIdx'].tolist()
        TotalIsDeleteList   = self.df_ClassData['isDeleted'].tolist()
        TotalUnKnownList    = self.df_ClassData['unknownDeleted'].tolist()
        TotalCategoryList   = self.df_ClassData['category'].tolist()

        for idx in range(0, DEFAULT_CLASS_NUM):
            className       = TotalClassNameList[idx]
            curAttName      = TotalAttNameList[idx]
            curAttText      = TotalAttTextList[idx]
            curMergeIdx     = TotalMergeIdxList[idx]
            curIsDelete     = TotalIsDeleteList[idx]
            curUnKnown      = TotalUnKnownList[idx]
            curCategory     = TotalCategoryList[idx]

            if curMergeIdx > 0:
                self.mergeList[curMergeIdx-1].append(idx)

            if curIsDelete == DELETE_VALUE_24CLASS:
                self.deleteList[DELETE_LIST_24CLASS_IDX].append(idx)

            if curUnKnown > 0:
                self.unknownList.append(idx)

            self.categoryDict[idx] = curCategory

            self.IdxDict[f'{curAttName}/{curAttText}'] = idx

            self.DataDict[className] = [curAttName, curAttText]

            self.defaultClassNameDict[idx] = className


    # Attribute "name" 과 "text" 를 받아서 해당 열 객체값 0/1 실제로 기입하는 함수
    def setValidValueByAttListElement(self, AttElem_AttName, AttElem_AttText):
        try:
            if AttElem_AttText == "true":
                param = f'{AttElem_AttName}/None'

            elif AttElem_AttText == "false":
                return True
            else:
                param = f'{AttElem_AttName}/{AttElem_AttText}'

            getIdx = self.IdxDict[param]

        except Exception as e:
            ErrorLog(f'{AttElem_AttName}/{AttElem_AttText} is Not Matched - {e}', lineNum=lineNum(), errorFileName=filename())
            return False

        self.MakeClassDefaultData[getIdx] = 1
        return True


    # MakeClass 할 클래스 넘버값 받아서, MakeClassDefaultData 를 83/66/39 MakeClass 로 변환하는 함수
    def refineMakeClass(self, ClassNum, makeClassDefaultList:list):
        ClassOther_ResList  = [ 0 for _ in range(ClassNum) ]
        curEditIdx          = 0
        DeleteValue         = 0
        isUnknownDelete     = False

        if ClassNum == 83:
            return makeClassDefaultList, isUnknownDelete
        elif ClassNum == 24:
            DeleteValue = DELETE_LIST_24CLASS_IDX
        else:
            error_handling(f'{ClassNum} Class is Not Define', filename(), lineNum())
            return None, False

        MergeValue      = DeleteValue
        mergeValueList  = [ each[MergeValue] for each in list(self.mergeDict.values()) ]

        UNKNOWN_SHOES_IDX = 82

        for idx, eachValue in enumerate(makeClassDefaultList):
            if idx in self.unknownList:
                if eachValue == 1 and idx != UNKNOWN_SHOES_IDX:
                    isUnknownDelete = True
                    return None, isUnknownDelete

            # Delete
            if idx in self.deleteList[DeleteValue]:
                continue    

            # Merge
            if curEditIdx in mergeValueList:
                curEditIdx += 1

            isMerged = False
            for mergeDictIdx, eachMergeList in enumerate(self.mergeList):
                if idx in eachMergeList:
                    mergedResIdx    = self.mergeDict[mergeDictIdx+1][MergeValue]
                    preValue        = ClassOther_ResList[mergedResIdx]
                    ClassOther_ResList[mergedResIdx] = ( preValue | eachValue )
                    isMerged        = True  

            if isMerged is True:
                continue

            # Merge / Delete 아닐 경우에만 신규 MakeClass Idx 인 curEditIdx 자리값에 값 기입하고, 다음 Idx 로 ++
            ClassOther_ResList[curEditIdx] = eachValue
            curEditIdx += 1

        return ClassOther_ResList, isUnknownDelete


    # DefualtClass 에 해당하는 [0, 1, 0, 0, ...] List 생성
    def setMakeClassDefaultData(self, attList:list):
        ATT_NAME_INDEX  = 1
        ATT_TEXT_INDEX  = 2

        self.MakeClassDefaultData = [ 0 for _ in range(DEFAULT_CLASS_NUM) ]       

        for AttElem in attList:
            if not self.setValidValueByAttListElement(AttElem[ATT_NAME_INDEX], AttElem[ATT_TEXT_INDEX]):
                pass

        # Headless 값이 1 인데도, Hat Color 중 하나에 체크가 되어있을 때 전부 다 0 값으로 수정
        if (FIX_HAT_ANNOTATE_ERROR is True) and (self.MakeClassDefaultData[HATLESS_IDX] == 1):
            if sum(self.MakeClassDefaultData[EQUIPED_HAT_START_IDX:EQUIPED_HAT_END_IDX]) > 0:
                for i in range(EQUIPED_HAT_START_IDX, EQUIPED_HAT_END_IDX):
                    self.MakeClassDefaultData[i] = 0


    def getMakeClassDefaultData(self):
        return self.MakeClassDefaultData

    
    def getClassNameDict(self):
        return self.defaultClassNameDict


    def getClassCategoryDict(self):
        return self.categoryDict


    def getCategoryNameDict(self):
        return self.categoryNameDict


    def getClassNameDictByClassNum(self, classNum):
        if classNum == 83:
            return self.class83NameDict
        elif classNum == 24:
            return self.class24NameDict
        else:
            return None


    def getClassNameListByClassNum(self, classNum):
        classNameList = []
        if classNum == 83:
            for idx in range(83):
                classNameList.append(self.class83NameDict[idx])
        elif classNum == 24:
            for idx in range(24):
                classNameList.append(self.class24NameDict[idx])
        else:
            return None
        return classNameList


    def getClassDataTotal(self):
        return [self.class24NameDict, self.class83NameDict, self.DataDict]
