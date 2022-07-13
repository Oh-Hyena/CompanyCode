# IMPORT
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
import os
import cv2
import sys
import copy


# INSTALLED PACKAGE IMPORT
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
import numpy                    as np


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
from Core.CvatXmlClass          import CvatXml
from Core.SingletonClass        import Singleton


# UI
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
from UI.SelectUI.SelectUIClass  import *


# SOURCE & DEST PATH
# 해당 OriginXmlDirPath 과 ResultDirPath 값을 변경하고 싶으면, CoreDefine.py 에서 변경하면 됨! ( 경로 변경 통합 )
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
OriginVideoDirPath    = copy.copy(OriginSource_Video_Path)  # 동영상 가져오기
ResultDirPath         = copy.copy(Result_Dir_Path)          # 이미지 저장하기

encodingFormat        = copy.copy(CORE_ENCODING_FORMAT)
validVideoFormat      = copy.copy(VALID_VIDEO_FORMAT)


# SAVE FILE & DIR NAME
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
RES_FOLDER_NAME  =  "seongnamfalse0125"
saveFolderName   =  "seongnamfalse0125.txt"


# VARIABLE DEFINE
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
FILE_NUM              =  10


# Local Function
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
def imread(fileName, flags=cv2.IMREAD_COLOR, dtype=np.uint8):
    try :
        n   = np.fromfile(fileName, dtype)
        img = cv2.imdecode(n, flags)
        return img
    except Exception as e:
        error_handling(f"imread() failed in {fileName} - {e}", filename(), lineNum())
        return None


def imwrite(fileName, img, params=None):
    try:
        ext         = os.path.splitext(fileName)[1]
        result, n   = cv2.imencode(ext, img, params)

        if result:
            with open(fileName, mode='w+b') as f:
                 n.tofile(f)
            return True
        else:
            ErrorLog(f"imwrite() failed in {fileName} - cv2.imencode return None",  lineNum=lineNum(), errorFileName=filename())
            return False
    except Exception as e:
        error_handling(f"imwrite() failed in {fileName} - {e}", filename(), lineNum())
        return False


# Class
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
class ChangeVideoToImg(Singleton):
    def __init__(self, QApp):
        self.app                 = QApp
        self.ProgramName         = "ChangeVideoToImg"
        self.videoList           = []
        self.fileNum             = FILE_NUM
        self.OriginVideoDict     = {}
        self.imgCountList        = []
        self.totalFiles          = 0
        self.sendArgsList        = []

        self.initializeCV()
        
     
    def initializeCV(self):
        self.selectUi = SelectUI(self.setInitSettingSelectUI, self.getEditSettingSelectUI)    
        
        self.selectUi.show()
        self.app.exec()
        
        if self.selectUi.isQuitProgram():
            return
    
        self.initAfterSetUI()
        
        
    def initAfterSetUI(self):
        self.savePath = self.makeResDir(ResultDirPath)

        if self.getOriginVideoDataDict() is False:
            sys.exit(-1)

        
    def makeResDir(self, Dir):
        print()
        NoticeLog("Change Video To Image Result Dir Start")
        
        if not os.path.isdir(Dir):
            os.makedirs(Dir, exist_ok=True)
            SuccessLog(f'Create Done {Dir}')
        
        return Dir
    

    def setInitSettingSelectUI(self):
        self.SyncAllValue()
        self.sendArgsList = [   ['FD', 'OriginVideoDirPath',            True,   f'{OriginVideoDirPath}'],
                                ['FD', 'ResultDirPath',                 True,   f'{ResultDirPath}'],
                                ['FD', 'HLINE_0',                       False,  'None'],

                                ['LE', 'RES_FOLDER_NAME',               False,  f'{RES_FOLDER_NAME}'],
                                ['LE', 'FILE_NUM',                      False,  f'{FILE_NUM}'],
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
        self.fileNum = int(FILE_NUM)


    def SyncAllValue(self):
        self.SyncEachValue('OriginSource_Video_Path', 'OriginVideoDirPath')
        self.SyncEachValue('Result_Dir_Path',         'ResultDirPath')


    def SyncEachValue(self, CoreName, LinkName, SENDER_DEPTH=3):
        # set 하기 전에 CoreDefine.py의 값을 get
        if callername(SENDER_DEPTH) == 'setInitSettingSelectUI':
            globals()[LinkName] = getCoreValue(CoreName)

        elif callername(SENDER_DEPTH) == 'getEditSettingSelectUI':
            setCoreValue(CoreName, globals()[LinkName])

    
    # getVideoPath() 검색하기 위한 Dict 만드는 함수
    def getOriginVideoDataDict(self):
        workPath = OriginVideoDirPath

        # 돌리면서 유효한 비디오 확장자만 Dict, List 에 추가하기
        self.OriginVideoDict = getVideoSearchDict(workPath, validVideoFormat)

        # 유효한 이미지가 있었을 때
        if self.OriginVideoDict is None:
            ErrorLog(f'`{workPath}` is Nothing Vaild Video', lineNum=lineNum(), errorFileName=filename())
            return False

        return True


    # 주어진 VideoName 이 OriginVideoDirPath 내 파일에 있는 비디오인지, 있다면 어떤 경로인지 리턴하는 함수
    def getVideoPath(self):
        for each in self.OriginVideoDict.keys():
            if self.OriginVideoDict.get(each) == None:
                return None
        
        return os.path.join(self.OriginVideoDict[each], each)


    def makeEachDestDir(self, Count):  
        self.folderName = RES_FOLDER_NAME + "_" + str(Count).zfill(6)
        self.DestDir    = os.path.join(ResultDirPath, self.folderName)
        os.makedirs(self.DestDir, exist_ok=True)


    def VideoToImg(self):
        OneVideoPath = self.getVideoPath()

        # 유효한 비디오 경로 없으면 return False
        if OneVideoPath is None:
            error_handling(f"imread() failed '{OneVideoPath}'", filename(), lineNum())
            return False

        folderCount  = 1
        fileCount    = 1
        
        self.videoList = os.listdir(OriginVideoDirPath)
        
        NoticeLog(f'Start << Change Video To Img')
        for video in self.videoList:
            if video.endswith(".mp4"):
                self.makeEachDestDir(folderCount)
                    
                print(f"[ {str(folderCount).zfill(4)} ] {video}")
                    
                capture = cv2.VideoCapture(os.path.join(OriginVideoDirPath, video))
                length  = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))  # 동영상 길이
                frame   = -1
                
                countNum = length / self.fileNum 
                
                while(capture.isOpened()):
                    ret, img = capture.read()
                    frame += 1
                    
                    if not ret: break
                    if not frame % countNum < 1: continue
                    
                    fileName = "_" + str(fileCount).zfill(6) + ".jpg"
                    cv2.imwrite(os.path.join(self.DestDir, self.folderName + fileName), img)
                    
                    fileCount  += 1
                    
                    if fileCount == self.fileNum + 1:
                        folderCount += 1
                        fileCount    = 1
                        
                capture.release()

        SuccessLog(f'Done << Changed Video To Img')
        print()

        return True
    

    def saveImgCount(self):
        for root, dirs, files in os.walk(ResultDirPath):
            self.totalFiles += len(files)
            if RES_FOLDER_NAME in root:
                self.imgCountList.append(f'{os.path.basename(root)} : {len(files)}')

        savePath      = os.path.join(ResultDirPath,'../')
        saveNormPath  = os.path.normpath(savePath)
        saveWritePath = os.path.join(saveNormPath, saveFolderName)

        with open(saveWritePath, 'w', encoding='utf-8') as f:
            for eachLine in self.imgCountList:
                f.write(f'{eachLine}\n')
            f.write(f'\n총 이미지 장수 : {self.totalFiles}')

        SuccessLog(f'Done << Count Number of Imgs')


    def run(self):
        if self.selectUi.isQuitProgram():
            NoticeLog(f'{self.__class__.__name__} Program EXIT\n')
        else:
            self.VideoToImg()
            self.saveImgCount()
            os.startfile(ResultDirPath)
            


if __name__ == "__main__":
    App         = QApplication(sys.argv)
    RunProgram  = ChangeVideoToImg(App)
    RunProgram.run()



            
               
