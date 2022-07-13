# Refer to CoreDefine.py
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
from CoreDefine     import *


# IMPORT CORE
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
from Core.CommonUse import *


# CONST DEFINE
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
CONDITION_NAME      = 0
CONDITION_FUNC      = 1
CONDITION_ARGS_FUNC = 2

CUR_FAIL            = 0
TOT_FAIL            = 1


# CheckCondition Class
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
class CheckCondition:
    def __init__(self, defaultAddConditionList:list):
        self.condDict = {}
        self.condArgsDict = {}
        self.condFailCountDict = {}

        # 생성자에서 인자로 넘겨준 DefaultCondition 들이 여기서 등록
        self.addConditionList(defaultAddConditionList)

        SuccessLog('CheckCondition Class Create Done')


    def addConditionList(self, AddConditionList:list):
        for eachElem in AddConditionList:
            self.addCondition(eachElem)


    def addCondition(self, AddConditionElem:list):
        # 등록하려는 ConditionName 이 이미 있다면 등록 실패 처리 : Condition Check 가 꼬일 수도 있기 때문에
        if AddConditionElem[CONDITION_NAME] in self.getCondNameList():
            error_handling(f'checkCondition Name [{AddConditionElem[CONDITION_NAME]}] is Already Exist!', filename(), lineNum())
            return

        # ConditionName 을 key 값으로 각 Dict 에 추가 등록
        self.condDict[AddConditionElem[CONDITION_NAME]]             = AddConditionElem[CONDITION_FUNC]
        self.condArgsDict[AddConditionElem[CONDITION_NAME]]         = AddConditionElem[CONDITION_ARGS_FUNC]
        self.condFailCountDict[AddConditionElem[CONDITION_NAME]]    = [0, 0]    # [CurConditionFailCount(리셋 가능), TotalConditionFailCount]

        NoticeLog(f'Add CheckCondition - {AddConditionElem[CONDITION_NAME]}')


    def getCondNameList(self):
        return list(self.condDict.keys())


    def getCondFuncList(self):
        return list(self.condDict.values())


    def resetCurFailCheckByCondName(self, condName:str):
        try:
            self.condFailCountDict[condName][CUR_FAIL] = 0
        except Exception as e:
            # 예상 시나리오 - 잘못된 condName 을 입력했을 경우
            ErrorLog(f'{condName} curFailCount Reset Failed - {e}', lineNum=lineNum())


    def resetCurFailCheckAll(self):
        resetList = self.getCondNameList()
        for eachElem in resetList:
            self.condFailCountDict[eachElem][CUR_FAIL] = 0


    def getCondFailCountDict(self):
        return self.condFailCountDict


    def checkCondAllParam(self):
        checkNameList   = self.getCondNameList()
        checkRes        = COND_PASS

        for eachName in checkNameList:
            func        = self.condDict[eachName]
            args        = self.condArgsDict[eachName]()
            checkRes    = self.checkCondEachElem(eachName, func, args)

            if checkRes == COND_FAIL:
                return COND_FAIL, eachName

        return COND_PASS, None


    def checkCondEachElem(self, name:str, func, args):
        checkRes = func(args)
        if checkRes == COND_FAIL:
            self.condFailCountDict[name][CUR_FAIL] += 1
            self.condFailCountDict[name][TOT_FAIL] += 1
        return checkRes

    
    def showCurFailLog(self):
        checkNameList = self.getCondNameList()
        
        for eachName in checkNameList:
            print(f"- {eachName:30} : {self.condFailCountDict[eachName][CUR_FAIL]}")
        print("--------------------------------------------------------------------------------------\n")
            

    def showTotalFailLog(self):
        checkNameList = self.getCondNameList()
        print("--------------------------------------------------------------------------------------")
        print("# [ FAILS ]")
        for eachName in checkNameList:
            print(f"- Total {eachName:30} : {self.condFailCountDict[eachName][TOT_FAIL]}")
        print("--------------------------------------------------------------------------------------")
    

    def getTotalFailLog(self):
        checkNameList   = self.getCondNameList()
        sendDict        = {}

        for eachName in checkNameList:
            sendDict[eachName] = self.condFailCountDict[eachName][TOT_FAIL]

        return sendDict