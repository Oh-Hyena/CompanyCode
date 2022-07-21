# IMPORT
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
import os
import sys
import zipfile
import shutil


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
# from Core.CvatXmlClass          import CvatXml
from Core.SingletonClass        import Singleton


# UI
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
from UI.SelectUI.SelectUIClass  import *


# SOURCE & DEST PATH
# 해당 OriginXmlDirPath 과 ResultDirPath 값을 변경하고 싶으면, CoreDefine.py 에서 변경하면 됨! ( 경로 변경 통합 )
# extract 'yolo txt' zipfile at cvatxml server ('not image')
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
OriginZipDirPath      = copy.copy(OriginSource_Zip_Path)  #  ZIP  파일 불러오기
ResultDirPath         = copy.copy(Result_Dir_Path)        # UNZIP 파일 저장하기

encodingFormat        = copy.copy(CORE_ENCODING_FORMAT)
validImgFormat        = copy.copy(VALID_IMG_FORMAT)


# DELETE LIST
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
deleteFileList  = ["obj.data", "obj.names"]  # 고정값


# Class
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
class UnzipYoloTxt(Singleton):
    def __init__(self, QApp):
        self.app            = QApp
        self.ProgramName    = "UnzipYoloTxt"

        self.zipList        = []
        self.sendArgsList   = []
        
        self.initializeUZ()
        
    
    def initializeUZ(self):
        self.selectUi = SelectUI(self.setInitSettingSelectUI, self.getEditSettingSelectUI)    
        
        self.selectUi.show()
        self.app.exec()
        
        if self.selectUi.isQuitProgram():
            return
    
        self.initAfterSetUI()


    def initAfterSetUI(self):
        self.savePath = self.makeResDir(ResultDirPath)


    def makeResDir(self, Dir):
        print()
        NoticeLog("Change Zip To Unzip Result Dir Start")
        
        if not os.path.isdir(Dir):
            os.makedirs(Dir, exist_ok=True)
            SuccessLog(f'Create Done {Dir}')
        
        return Dir
    

    def setInitSettingSelectUI(self):
        self.SyncAllValue()
        self.sendArgsList = [   ['FD', 'OriginZipDirPath',              True,   f'{OriginZipDirPath}'],
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
        self.SyncEachValue('OriginSource_Zip_Path',   'OriginZipDirPath')
        self.SyncEachValue('Result_Dir_Path',         'ResultDirPath')


    def SyncEachValue(self, CoreName, LinkName, SENDER_DEPTH=3):
        # set 하기 전에 CoreDefine.py의 값을 get
        if callername(SENDER_DEPTH) == 'setInitSettingSelectUI':
            globals()[LinkName] = getCoreValue(CoreName)

        elif callername(SENDER_DEPTH) == 'getEditSettingSelectUI':
            setCoreValue(CoreName, globals()[LinkName])


    def writeZipList(self):
        for path, dirs, files in os.walk(OriginZipDirPath):
            for file in files:
                self.zipList.append(os.path.join(path, file))

    
    def unzip(self):
        self.writeZipList()
        
        for zipFile in self.zipList:
            with zipfile.ZipFile(zipFile, 'r') as f:
                f.extractall(ResultDirPath)   
        
    
    def moveYoloTxtFile(self):
        for path, dirs, files in os.walk(ResultDirPath):
            for file in files:
                if file.endswith(".txt") and file != "train.txt":
                    shutil.move(os.path.join(path, file), os.path.join(ResultDirPath, file))
        
    
    # 폴더 안에 파일이 없어야 폴더 삭제 가능!
    def deleteNothing(self):
        # zip 파일 삭제
        for each in os.listdir(OriginZipDirPath):
            os.remove(os.path.join(OriginZipDirPath, each))
        
        # 빈 폴더 삭제
        os.rmdir(OriginZipDirPath)
        os.rmdir(os.path.join(ResultDirPath, "obj_train_data"))
        
        # 파일 삭제
        for each in deleteFileList:
            os.remove(os.path.join(ResultDirPath, each))
    

    def run(self):
        if self.selectUi.isQuitProgram():
            NoticeLog(f'{self.__class__.__name__} Program EXIT\n')
        else:
            self.unzip()
            self.moveYoloTxtFile()
            self.deleteNothing()
            os.startfile(ResultDirPath)
        
    
if __name__ == "__main__":
    App         = QApplication(sys.argv)
    RunProgram  = UnzipYoloTxt(App)
    RunProgram.run()
