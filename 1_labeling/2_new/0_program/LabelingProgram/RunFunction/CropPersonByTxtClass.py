# IMPORT
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
import os
import sys
import cv2
import numpy as np


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
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
OriginImgDirPath      = copy.copy(OriginSource_Img_Path)  # IMG  파일 불러오기
OriginTxtDirPath      = copy.copy(OriginSource_Txt_Path)  # TXT  파일 불러오기
ResultDirPath         = copy.copy(Result_Dir_Path)        # CROP 파일 저장하기

encodingFormat        = copy.copy(CORE_ENCODING_FORMAT)
validImgFormat        = copy.copy(VALID_IMG_FORMAT)


# SAVE FILE & DIR NAME
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
RES_FOLDER_NAME       = "att_seongnamfalse0311"


# VARIABLE DEFINE
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
FILE_NUM             = 100
X_LEN                = 10
Y_LEN                = 10
# class 선택 (default == person)


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
class CropPersonByTxt(Singleton):
    def __init__(self, QApp):
        self.app             = QApp
        self.ProgramName     = "CropPersonByTxt"

        self.dirList         = []

        self.imgDirList      = []
        self.imgSizeList     = []
        
        self.txtDirList      = []
        self.txtInfoList     = []

        self.imgInfoList     = []
        self.xyInfoList      = []

        self.sendArgsList    = []

        self.initializeCPT()


    def initializeCPT(self):
        self.selectUi = SelectUI(self.setInitSettingSelectUI, self.getEditSettingSelectUI)    
        
        self.selectUi.show()
        self.app.exec()
        
        if self.selectUi.isQuitProgram():
            return
    
        self.initAfterSetUI()


    def initAfterSetUI(self):
        self.savePath = self.makeResDir(ResultDirPath)

        
    def makeResDir(self, Dir):
        NoticeLog("Crop Person Result Dir Start")
        
        if not os.path.isdir(Dir):
            os.makedirs(Dir, exist_ok=True)
            SuccessLog(f'Create Done {Dir}')
        
        return Dir


    def setInitSettingSelectUI(self):
        self.SyncAllValue()
        self.sendArgsList = [   ['FD', 'OriginImgDirPath',              True,   f'{OriginImgDirPath}'],
                                ['FD', 'OriginTxtDirPath',              True,   f'{OriginTxtDirPath}'],
                                ['FD', 'ResultDirPath',                 True,   f'{ResultDirPath}'],
                                ['FD', 'HLINE_0',                       False,  'None'],

                                ['LE', 'RES_FOLDER_NAME',               False,  f'{RES_FOLDER_NAME}'],
                                ['LE', 'FILE_NUM',                      False,  f'{FILE_NUM}'],
                                ['LE', 'X_LEN',                         False,  f'{X_LEN}'],
                                ['LE', 'Y_LEN',                         False,  f'{Y_LEN}'],
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
        self.xLen    = int(X_LEN)
        self.yLen    = int(Y_LEN)


    def SyncAllValue(self):
        self.SyncEachValue('OriginSource_Img_Path',   'OriginImgDirPath')
        self.SyncEachValue('OriginSource_Txt_Path',   'OriginTxtDirPath')
        self.SyncEachValue('Result_Dir_Path',         'ResultDirPath')


    def SyncEachValue(self, CoreName, LinkName, SENDER_DEPTH=3):
        # set 하기 전에 CoreDefine.py의 값을 get
        if callername(SENDER_DEPTH) == 'setInitSettingSelectUI':
            globals()[LinkName] = getCoreValue(CoreName)

        elif callername(SENDER_DEPTH) == 'getEditSettingSelectUI':
            setCoreValue(CoreName, globals()[LinkName])


    # getImgPath() 검색하기 위한 Dict 만드는 함수
    def getOriginImgDataDict(self):
        workPath = OriginImgDirPath

        # 돌리면서 유효한 이미지 확장자만 Dict, List 에 추가하기
        self.OriginImgDict = getImageSearchDict(workPath, validImgFormat)

        # 유효한 이미지가 있었을 때
        if self.OriginImgDict is None:
            ErrorLog(f'`{workPath}` is Nothing Vaild Img', lineNum=lineNum(), errorFileName=filename())
            return False

        return True


    # 주어진 ImgName 이 OriginImgDirPath 내 파일에 있는 이미지인지, 있다면 어떤 경로인지 리턴하는 함수
    def getImgPath(self):
        for each in self.OriginImgDict.keys():
            if self.OriginImgDict.get(each) == None:
                return None
        
        return os.path.join(self.OriginImgDict[each], each)


    def listDir(self, Dir):
        for root, _, files in os.walk(Dir):
            for file in files:
                dirPath = os.path.join(root, file)
                self.dirList.append(dirPath)

        return self.dirList
        
    
    def makeImgSizeList(self):
        NoticeLog(f'Start << Get Each Image Size (width, height)')

        self.imgDirList   = self.listDir(OriginImgDirPath)

        for each in self.imgDirList:
            imgFolderName = os.path.basename(each.split('\\')[-2])
            imgFileName   = os.path.basename(each.split('.')[0])
            img           = cv2.imread(each, cv2.IMREAD_COLOR)
            h, w, c       = img.shape
            self.imgSizeList.append(f'{imgFolderName} {imgFileName} {w} {h}')


    def makeTxtList(self):
        NoticeLog(f'Start << Get Only Person(0) of All TxtFiles')

        self.txtDirList   = self.listDir(OriginTxtDirPath)
        
        for each in self.txtDirList:
            txtFileName   = os.path.basename(each.split('.')[0])
            with open(each, 'r', encoding=encodingFormat) as f:
                for eachLine in f:
                    if eachLine[0] == '0':  # 0 == person / 1 == car
                        eachLine = eachLine.strip('\n')
                        self.txtInfoList.append(f'{txtFileName} {eachLine}')


    def makeImgInfoList(self):
        NoticeLog(f'Start << Group the Same File Names')

        for eachTxt in self.txtInfoList:
            eachTxtSplit = eachTxt.split(" ")
            txtFilename  = eachTxtSplit[0]

            for eachImg in self.imgSizeList:
                eachImgSplit  = eachImg.split(" ")
                imgFoldername = eachImgSplit[0]

                if txtFilename in eachImg:
                    #                            {폴더이름}     {파일이름}     {x 중앙 좌표}      {y 중앙 좌표}      {box width}       {box height}      {img width}       {img height}
                    self.imgInfoList.append(f'{imgFoldername} {txtFilename} {eachTxtSplit[2]} {eachTxtSplit[3]} {eachTxtSplit[4]} {eachTxtSplit[5]} {eachImgSplit[2]} {eachImgSplit[3]}')


    def makeXyInfoList(self):
        NoticeLog(f'Start << Get Only "Xlen>{self.xLen}", "Ylen>{self.yLen}" of All Person TxtFiles')

        for each in self.imgInfoList:
            eachSplit      = each.split(" ")
            
            cropfolderName = eachSplit[0]
            cropfileName   = eachSplit[1]

            box_x_mid      = float(eachSplit[2])
            box_y_mid      = float(eachSplit[3])
            box_width      = float(eachSplit[4])
            box_height     = float(eachSplit[5])

            img_width      = int(eachSplit[6])
            img_height     = int(eachSplit[7])

            xtl  = ((2 * box_x_mid * img_width)  - (box_width  * img_width))  / 2
            ytl  = ((2 * box_y_mid * img_height) - (box_height * img_height)) / 2
            xbr  = ((2 * box_x_mid * img_width)  + (box_width  * img_width))  / 2
            ybr  = ((2 * box_y_mid * img_height) + (box_height * img_height)) / 2

            xlen = abs(int(float(xtl)) - int(float(xbr)))
            ylen = abs(int(float(ytl)) - int(float(ybr)))

            if (xlen > self.xLen) and (ylen > self.yLen):
                self.xyInfoList.append(f'{cropfolderName} {cropfileName} {xtl} {ytl} {xbr} {ybr}')
        

    def makeEachDestDir(self, Count):  
        self.folderName = RES_FOLDER_NAME + "_" + str(Count).zfill(6)
        self.DestDir    = os.path.join(ResultDirPath, self.folderName)
        os.makedirs(self.DestDir, exist_ok=True)


    def cropPerson(self):
        OneImgPath = self.getImgPath()

        # 유효한 이미지 경로 없으면 return False
        if OneImgPath is None:
            error_handling(f"imread() failed '{OneImgPath}'", filename(), lineNum())
            return False

        folderCount   = 1
        fileCount     = 1

        NoticeLog(f'Crop "Person" and "Xlen>{self.xLen}" and "Ylen>{self.yLen}" Images')
        for eachXy in self.xyInfoList:
            DestDir = self.makeEachDestDir(folderCount)

            eachXySplit    = eachXy.split(" ")
            cropFolderName = eachXySplit[0]
            cropFileName   = eachXySplit[1]
            imgPath        = os.path.join(OriginImgDirPath, cropFolderName)
            img            = imread(os.path.join(imgPath, cropFileName + '.jpg'), cv2.IMREAD_COLOR)

            if img is None: break

            src     = img.copy()
            cropXtl = eachXySplit[2]
            cropYtl = eachXySplit[3]
            cropXbr = eachXySplit[4]
            cropYbr = eachXySplit[5]

            cropImg = src[int(float(cropYtl)):int(float(cropYbr)), int(float(cropXtl)):int(float(cropXbr))]

            DestFileName = cropFolderName + "_" + str(fileCount).zfill(6) + '.jpg'
            imwrite(os.path.join(DestDir, DestFileName), cropImg)

            fileCount += 1

            if fileCount == self.fileNum + 1:
                folderCount += 1
                fileCount    = 1


    def run(self):
        if self.selectUi.isQuitProgram():
            NoticeLog(f'{self.__class__.__name__} Program EXIT\n')
        else:
            self.makeImgSizeList()
            self.makeTxtList()
            self.makeImgInfoList()
            self.makeXyInfoList()
            self.cropPerson()
            os.startfile(ResultDirPath)
            


if __name__ == "__main__":
    App         = QApplication(sys.argv)
    RunProgram  = CropPersonByTxt(App)
    RunProgram.run()