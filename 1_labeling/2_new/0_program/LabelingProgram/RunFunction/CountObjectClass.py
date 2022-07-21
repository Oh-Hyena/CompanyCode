# IMPORT
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
from asyncore import read
import os
import sys


# Add Import Path
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../UI/SelectUI'))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../Core'))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../'))


# Refer to CoreDefine.py
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
from CoreDefine                 import *


# Custom Modules
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
from Core.CommonUse             import *
from Core.SingletonClass        import Singleton


# UI
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
from UI.SelectUI.SelectUIClass  import *


# SOURCE & DEST PATH
# 해당 OriginXmlDirPath 과 ResultDirPath 값을 변경하고 싶으면, CoreDefine.py 에서 변경하면 됨! ( 경로 변경 통합 )
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
OriginTxtDirPath      = copy.copy(OriginSource_Txt_Path)  
ResultDirPath         = copy.copy(Result_Dir_Path)        

encodingFormat        = copy.copy(CORE_ENCODING_FORMAT)


# Class
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
class CountObject(Singleton):
    def __init__(self, QApp):
        self.app                 = QApp
        self.ProgramName         = "CountObject"

        self.txtList             = []
        self.readList            = []
        self.TotalImg            = 0
        self.TotalLen            = 0
        self.Totalperson         = 0
        self.Totalcar            = 0

        self.sendArgsList        = []

        self.initializeCO()


    def initializeCO(self):
        self.selectUi = SelectUI(self.setInitSettingSelectUI, self.getEditSettingSelectUI)    
        
        self.selectUi.show()
        self.app.exec()
        
        if self.selectUi.isQuitProgram():
            return
    
        self.initAfterSetUI()


    def initAfterSetUI(self):
        self.savePath = self.makeResDir(ResultDirPath)


    def makeResDir(self, Dir):
        NoticeLog("Count Object Result Dir Start")
        
        if not os.path.isdir(Dir):
            os.makedirs(Dir, exist_ok=True)
            SuccessLog(f'Create Done {Dir}')
        
        return Dir


    def setInitSettingSelectUI(self):
        self.SyncAllValue()
        self.sendArgsList = [   ['FD', 'OriginTxtDirPath',              True,   f'{OriginTxtDirPath}'],
                                ['FD', 'ResultDirPath',                 True,   f'{ResultDirPath}'],
                                ['FD', 'HLINE_0',                       False,  'None'],
                            ]
        return self.ProgramName, self.sendArgsList


    def getEditSettingSelectUI(self):
        NAME = 1
        returnDict = self.selectUi.getReturnDict()

        print("\n* Change Path/Define Value By SelectUI")
        print("--------------------------------------------------------------------------------------")
        for Arg in self.sendArgsList:
            eachTarget = Arg[NAME]
            if returnDict.get(eachTarget) != None:
                globals()[eachTarget] = returnDict[eachTarget]
                showLog(f'- {eachTarget:40} -> {globals()[eachTarget]}')            
        showLog("--------------------------------------------------------------------------------------\n")

        self.SyncAllValue()
        setResultDir(ResultDirPath)


    def SyncAllValue(self):
        self.SyncEachValue('OriginSource_Txt_Path',   'OriginTxtDirPath')
        self.SyncEachValue('Result_Dir_Path',         'ResultDirPath')


    def SyncEachValue(self, CoreName, LinkName, SENDER_DEPTH=3):
        # set 하기 전에 CoreDefine.py의 값을 get
        if callername(SENDER_DEPTH) == 'setInitSettingSelectUI':
            globals()[LinkName] = getCoreValue(CoreName)

        elif callername(SENDER_DEPTH) == 'getEditSettingSelectUI':
            setCoreValue(CoreName, globals()[LinkName])

        
    def countObject(self):
        self.txtList    = os.listdir(OriginTxtDirPath)
        self.TotalImg   = len(self.txtList)                 # 이미지 장수
        
        print()
        NoticeLog(f'Start >> Read .txt files and Count number of each object')

        for txtfile in self.txtList:
            if txtfile.endswith(".txt"):
                totalSrcFilePath    = os.path.join(OriginTxtDirPath, txtfile)
                readFileToList(totalSrcFilePath, self.readList)
                
                self.TotalLen       += len(self.readList)   # 전체 객체 개수
                
                for each in self.readList:
                    eachSplit  = each.split(" ")
                    classes    = eachSplit[0]
                                
                    if classes == '0':
                        self.Totalperson += 1               # person 객체 개수
                    else:
                        self.Totalcar    += 1               # car 객체 개수
                    
                with open(os.path.join(ResultDirPath, "countObject_" + os.path.basename(OriginTxtDirPath) + ".txt"), 'w', encoding=encodingFormat) as f:
                    f.write(f"[ img count ]\n")
                    f.write(f"* 전체 : {str(self.TotalImg).rjust(5)}\n")
                    f.write(f"\n[ obj count ]\n")
                    f.write(f"* 사람 : {str(self.Totalperson).rjust(5)}\n")
                    f.write(f"* 차량 : {str(self.Totalcar).rjust(5)}\n")  
                    f.write(f"* 전체 : {str(self.TotalLen).rjust(5)}\n")  
        
        SuccessLog(f'Done >> Save Result.txt file\n')
                
    
    def run(self):
        if self.selectUi.isQuitProgram():
            NoticeLog(f'{self.__class__.__name__} Program EXIT')
            print()
        else:
            self.countObject()
            os.startfile(ResultDirPath)


if __name__ == "__main__":
    App         = QApplication(sys.argv)
    RunProgram  = CountObject(App)
    RunProgram.run()
