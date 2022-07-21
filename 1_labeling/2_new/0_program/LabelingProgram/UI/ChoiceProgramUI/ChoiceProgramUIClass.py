# Import Packages and Modules
# Standard Library
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
import sys
import os
import copy


# Add Import Path
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../Core'))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../'))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../'))


# Refer to CoreDefine.py
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
from CoreDefine         import *


# IMPORT CORE
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
from Core.CommonUse     import *


# Installed Library - QT CORE
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
from qt_core            import *


# UI
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
from .ui_main            import Ui_MainWindow


# ProgramList
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
ProgramList =   [   'ChangeVideoToImg',
                    'UnzipYoloTxt',
                    'MakeLabelingDataset',
                    'CombineDataset',
                    'CountObject',
                    'LabelingAugmentation',
                    'CropPersonByTxt'
                ]


# ProgramInformationList
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
DetailList  =   [   'Video(.mp4) 파일을 Image(.jpg) 파일로 변환해주는 프로그램',
                    'YOLO.txt Zip 파일을 풀어주는 프로그램',
                    'Dataset 을 shuffle 하고, ration 에 맞게 train, valid, test dataset 을 만들어주는 프로그램',
                    'New Dataset 을 Origin Dataset 에 복사해주는 프로그램',
                    'YOLO.txt 파일을 읽어서 이미지와 객체 개수를 출력하는 프로그램',
                    'Labeling Dataset 을 원하는 횟수만큼 증강하는 프로그램',
                    'Txt 파일을 읽어서 입력한 크기 이상의 Person 이미지만 추출하는 프로그램'
                ]


# ChoiceProgramUI Class
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
class ChoiceProgramUI(QMainWindow):
    def __init__(self, QApp=None):
        super().__init__()

        self.app                = QApp
        self.res                = 'EXIT'

        self.programNameList    = []
        self.infoDict           = {}

        self.ui                 = Ui_MainWindow()
        self.ui.setupUi(self)

        self.initialize()


    def initialize(self):
        self.setProgramNameList()
        self.syncComboBoxToProgramList()
        self.setInfoDict()
        self.ui.detailLabel.setText(self.getProgramInformation())

        self.ui.selectProgramComboBox.currentTextChanged.connect(self.syncDetailLabelToComboBox)
        self.ui.selectProgramBtn.clicked.connect(self.selectDone)


    def setInfoDict(self):
        for idx, eachValue in enumerate(ProgramList):
            self.infoDict[eachValue] = DetailList[idx]


    def getProgramInformation(self):
        return self.infoDict[self.ui.selectProgramComboBox.currentText()]

    def setProgramNameList(self):
        for eachValue in ProgramList:
            self.programNameList.append(eachValue)


    def syncComboBoxToProgramList(self):
        self.ui.selectProgramComboBox.addItems(self.programNameList)

    def syncDetailLabelToComboBox(self):
        self.ui.detailLabel.setText(self.getProgramInformation())


    def selectDone(self):
        self.res = self.ui.selectProgramComboBox.currentText()
        NoticeLog(f'{self.res} Program INIT')
        QCoreApplication.instance().quit()


    def run(self):
        NoticeLog('Select the program you want to run from the UI')
        self.res = 'EXIT'
        self.show()
        self.app.exec()
        return self.res


    def __del__(self):
        ChangeVideoPath         = getCoreValue('OriginSource_Video_Path')
        ChangeImagePath         = getCoreValue('OriginSource_Img_Path')
        ChangeZipPath           = getCoreValue('OriginSource_Zip_Path')
        ChangeTxtPath           = getCoreValue('OriginSource_Txt_Path')
        ChangeResDirPath        = getCoreValue('Result_Dir_Path')
        ChangeCvatPath          = getCoreValue('OriginSource_CvatXml_Path')

        Rmb_VideoLine           = 0
        Rmb_ImgLine             = 0
        Rmb_ZipLine             = 0
        Rmb_TxtLine             = 0
        Rmb_ResDirLine          = 0
        Rmb_CvatLine            = 0

        LineSaveList            = []
        readFileToList('CoreDefine.py', LineSaveList)

        for idx, eachLine in enumerate(LineSaveList):
            Tmp_Rmb_VideoLine   = eachLine.find('OriginSource_Video_Path      =')
            Tmp_Rmb_ImgLine     = eachLine.find('OriginSource_Img_Path        =')
            Tmp_Rmb_ZipLine     = eachLine.find('OriginSource_Zip_Path        =')
            Tmp_Rmb_TxtLine     = eachLine.find('OriginSource_Txt_Path        =')
            Tmp_Rmb_ResDirLine  = eachLine.find('Result_Dir_Path              =')
            Tmp_Rmb_CvatLine    = eachLine.find('OriginSource_CvatXml_Path    =')

            if Tmp_Rmb_VideoLine >= 0:
                Rmb_VideoLine    = idx
            elif Tmp_Rmb_ImgLine >= 0:
                Rmb_ImgLine      = idx
            elif Tmp_Rmb_ZipLine >= 0:
                Rmb_ZipLine      = idx
            elif Tmp_Rmb_TxtLine >= 0:
                Rmb_TxtLine      = idx
            elif Tmp_Rmb_ResDirLine >= 0:
                Rmb_ResDirLine   = idx
            elif Tmp_Rmb_CvatLine >= 0:
                Rmb_CvatLine     = idx

        with open('CoreDefine.py', 'w', encoding=CORE_ENCODING_FORMAT) as wf:
            for idx, line in enumerate(LineSaveList):
                if idx == Rmb_VideoLine:
                    wf.write(f'OriginSource_Video_Path   = r"{ChangeVideoPath}"\n')
                elif idx == Rmb_ImgLine:
                    wf.write(f'OriginSource_Img_Path     = r"{ChangeImagePath}"\n')
                elif idx == Rmb_ZipLine:
                    wf.write(f'OriginSource_Zip_Path     = r"{ChangeZipPath}"\n')
                elif idx == Rmb_TxtLine:
                    wf.write(f'OriginSource_Txt_Path     = r"{ChangeTxtPath}"\n')
                elif idx == Rmb_ResDirLine:
                    wf.write(f'Result_Dir_Path           = r"{ChangeResDirPath}"\n')
                elif idx == Rmb_CvatLine:
                    wf.write(f'OriginSource_CvatXml_Path = r"{ChangeCvatPath}"\n')
                else:
                    wf.write(f'{line}\n')

        SuccessLog('Changed values are overwritten in CoreDefine\n')
        
