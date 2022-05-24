"""
ConditionCheck Error 를 엑셀로 저장하는 클래스

LAST_UPDATE : 2021/11/08
AUTHOR      : OH HYENA
"""


import  sys
import  os
import pandas as pd

from CoreDefine     import *
from Core.CommonUse import *


XML_FILE_NAME = 0
IMG_FILE_NAME = 1
FAIL_CON_NAME = 2

SAVE_LOG_EXCEL_PATH = r"ConditionCheckError.xlsx"


class SaveErrorLog():
    def __init__(self):
        self.ResDirPath     = ""
        self.ErrorLogList   = []


    def set_ResDir(self, resPath):
        self.ResDirPath = resPath

    def set_ErrorLogList(self, logList):
        self.ErrorLogList = logList


    # 해당 list들을 pandas의 dataframe 형태로 만드는 함수
    def ListToDataFrame(self):
        xmlFileNameList = []
        imgFileNameList = []
        failConNameList = []

        for eachArg in self.ErrorLogList:
            xmlFileNameList.append(eachArg[XML_FILE_NAME])
            imgFileNameList.append(eachArg[IMG_FILE_NAME])
            failConNameList.append(eachArg[FAIL_CON_NAME])

        raw_data =  {   'XML File Name':xmlFileNameList,
                        'IMG File Name':imgFileNameList,
                        'Error Information':failConNameList }
        raw_data = pd.DataFrame(raw_data)

        return raw_data

    # dataframe 형태로 만든 raw_data를 excel 파일에 저장하는 함수
    def saveLogToFile(self):
        if self.ErrorLogList:
            save_path   = os.path.join(self.ResDirPath, SAVE_LOG_EXCEL_PATH)
            raw_data    = self.ListToDataFrame()
            raw_data.to_excel(excel_writer=save_path)

            SuccessLog(f'Condition Error List Save to Excel File -> {save_path}')

