"""
Class code to register condition and batch process

LAST_UPDATE : 2021/10/15
AUTHOR      : OH HYENA
"""


from CoreDefine     import *
from Core.CommonUse import *

CONDITION_NAME      = 0
CONDITION_FUNC      = 1
CONDITION_ARGS_FUNC = 2

CUR_FAIL            = 0
TOT_FAIL            = 1


class CheckCondition:
    def __init__(self, defaultAddConditionList:list):
        self.condDict = {}
        self.condArgsDict = {}
        self.condFailCountDict = {}

        # 생성자에서 인자로 넘겨준 DefaultCondition 들이 여기서 등록
        self.addConditionList(defaultAddConditionList)

        SuccessLog('CheckCondition Class Create Done')


    # AddConditionList 들을 리스트 돌리면서 addCondition 로 넘겨주는 함수 
    def addConditionList(self, AddConditionList:list):
        for eachElem in AddConditionList:
            self.addCondition(eachElem)


    # AddConditionElem 값을 바탕으로 ConditionCheck 를 실제 등록하는 함수
    def addCondition(self, AddConditionElem:list):
        if AddConditionElem[CONDITION_NAME] in self.getCondNameList():
            error_handling(f'checkCondition Name [{AddConditionElem[CONDITION_NAME]}] is Already Exist!', filename(), lineNum())
            return

        self.condDict[AddConditionElem[CONDITION_NAME]]             = AddConditionElem[CONDITION_FUNC]
        self.condArgsDict[AddConditionElem[CONDITION_NAME]]         = AddConditionElem[CONDITION_ARGS_FUNC]
        self.condFailCountDict[AddConditionElem[CONDITION_NAME]]    = [0, 0]    # [CurConditionFailCount(리셋 가능), TotalConditionFailCount]

        NoticeLog(f'Add CheckCondition - {AddConditionElem[CONDITION_NAME]}')


    def getCondNameList(self):
        return list(self.condDict.keys())


    def getCondFuncList(self):
        return list(self.condDict.values())


    # 주어진 ContiditionName 에 해당하는 Condition의 CurrentFailCount 를 0으로 초기화하는 함수
    def resetCurFailCheckByCondName(self, condName:str):
        try:
            self.condFailCountDict[condName][CUR_FAIL] = 0
        except Exception as e:
            ErrorLog(f'{condName} curFailCount Reset Failed - {e}', lineNum=lineNum())


    # 등록된 모든 Condition의 CurrentFailCount 를 0으로 초기화하는 함수
    def resetCurFailCheckAll(self):
        resetList = self.getCondNameList()
        for eachElem in resetList:
            self.condFailCountDict[eachElem][CUR_FAIL] = 0


    # 등록된 모든 Condition의 CurrentFailCount 를 리턴하는 함수
    def getCondFailCountDict(self):
        return self.condFailCountDict


    # 일괄적으로 Condition Check 하는 함수
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


    # 실제로 ConditionCheck 를 시행하는 함수
    def checkCondEachElem(self, name:str, func, args):
        checkRes = func(args)
        if checkRes == COND_FAIL:
            self.condFailCountDict[name][CUR_FAIL] += 1
            self.condFailCountDict[name][TOT_FAIL] += 1
        return checkRes

    
    # 등록된 모든 Condition의 CurrentFailCount 를 출력하는 함수
    def showCurFailLog(self):
        checkNameList = self.getCondNameList()

        for eachName in checkNameList:
            print(f"- {eachName:30} : {self.condFailCountDict[eachName][CUR_FAIL]}")
        print("--------------------------------------------------------------------------------------\n")
        

    # 등록된 모든 Condition의 TotalFailCount 를 출력하는 함수
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