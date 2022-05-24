"""
ImgList Line 마다 경로를 추가해주는 클래스

LAST_UPDATE : 21/11/09
AUTHOR      : OH HYENA
"""

import os
import sys


sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../UI/SelectUI'))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../Core'))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../'))


from CoreDefine                 import *
from Core.CommonUse             import *
from Core.SingletonClass        import Singleton
from UI.SelectUI.SelectUIClass  import *


ImgListFile         = copy.copy(OriginSource_ImageListPath)
ResultDirPath       = copy.copy(Result_Dir_Path)

encodingFormat      = copy.copy(CORE_ENCODING_FORMAT)
validImgFormat      = copy.copy(VALID_IMG_FORMAT)

AddPrefixFileName   = "JoinPath"
JoinDirPath         = r"Please Write Path This EditBox"


class JoinPath(Singleton):
    def __init__(self, QApp):
        self.app            = QApp
        self.ProgramName    = "JoinPath"
        self.OriginImgList  = []
        self.initJP()


    def initJP(self):
        self.selectUi = SelectUI(self.setInitSettingForSelectUI, self.getEditSettingForSelectUI)

        self.selectUi.show()
        self.app.exec()

        if self.selectUi.isQuitProgram():
            return

        NoticeLog(f'JoinPath : {JoinDirPath}')


    # 이미지 파일 이름에 경로 붙이는 함수
    def writeImgListFileWithJoinPath(self):
        fileName            = os.path.basename(ImgListFile)
        fileName            = f'{AddPrefixFileName}_{fileName}'
        savePath            = os.path.join(ResultDirPath, fileName)
        self.OriginImgList  = [ os.path.join(JoinDirPath, eachLine) for eachLine in self.OriginImgList ]

        writeListToFile(savePath, self.OriginImgList, encodingFormat)


    def setInitSettingForSelectUI(self):
        self.SyncAllValue()
        self.sendArgsList = [   ['FD', 'ImgListFile',   False,  f'{ImgListFile}'],
                                ['FD', 'ResultDirPath', True,   f'{ResultDirPath}'],

                                ['LE', 'JoinDirPath',   False,  f'{JoinDirPath}'],
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


    def SyncAllValue(self):
        self.SyncEachValue('OriginSource_ImageListPath',    'ImgListFile')
        self.SyncEachValue('Result_Dir_Path',               'ResultDirPath')

    def SyncEachValue(self, CoreName, LinkName, SENDER_DEPTH=3):
        if callername(SENDER_DEPTH) == 'setInitSettingForSelectUI':
            globals()[LinkName] = getCoreValue(CoreName)

        elif callername(SENDER_DEPTH) == 'getEditSettingForSelectUI':
            setCoreValue(CoreName, globals()[LinkName])


    # class 실행 함수
    def run(self):
        if self.selectUi.isQuitProgram():
            NoticeLog(f'{self.__class__.__name__} Program EXIT\n')
        else:
            readFileToList(ImgListFile, self.OriginImgList, encodingFormat)
            self.writeImgListFileWithJoinPath()

            os.startfile(ResultDirPath)


if __name__ == "__main__":
    App         = QApplication(sys.argv)
    RunProgram  = JoinPath(App)
    RunProgram.run()