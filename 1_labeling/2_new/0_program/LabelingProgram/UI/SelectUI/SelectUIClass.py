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
from CoreDefine import *


# IMPORT CORE
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
from Core.CommonUse         import *


# Installed Library - QT CORE
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
from qt_core                import *


# UI
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
from .ui_main                       import Ui_MainWindow


# CONST DEFINE
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
TYPE        = 0
NAME        = 1
ISDIR       = 2
DEFAULT_VAL = 3

LAST_APPEND = -1
LABEL_INDEX = 0
CB_INDEX    = 0
LE_INDEX    = 1
BT_INDEX    = 2


# Remember Pre_Path
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
encodingFormat  = copy.copy(CORE_ENCODING_FORMAT)


# SelectUI Class
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
class SelectUI(QMainWindow):
    def __init__(   self, 
                    callBackInFunction=None,
                    callBackOutFunction=None):
        super().__init__()

        # Load UI
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # set CallBack
        self.initSetting = callBackInFunction
        self.doneSetting = callBackOutFunction

        self.runProgramName     = ""
        self.initSettingList    = []
        self.settingNameList    = []
        self.selectFDList       = []
        self.selectCBList       = []
        self.selectLEList       = []
        self.selectUIList       = []
        self.returnDict         = {}

        self.initSettingFDList  = []
        self.initSettingCBList  = []
        self.initSettingLEList  = []
        self.initSettingUIList  = []

        self.isSelectDone       = False

        self.PreRememberPath    = ""
        self.transFilterMsg     = ""
        self.loadRememberDir()


        # 'Done' ?????? ????????? ???, ????????? ???????????? ?????? ??????
        self.ui.quitButton.clicked.connect(self.selectDone)

        # ????????? ?????? ?????? CallbackIn ?????? ??????
        self.runProgramName, self.initSettingList = self.initSetting()
        self.setSettingNameList()
        self.settingBytInitSettingList()

        self.settingFinish()


    def selectDone(self):
        # ????????? ?????? - ????????? ?????? ?????? CallbackOut ?????? ??????
        self.setReturnDict()
        self.doneSetting()

        # ?????? ????????? ??????
        self.saveRememberDir()

        self.isSelectDone = True

        # ??? ?????? ????????? UI ??????
        QCoreApplication.instance().quit()


    def loadRememberDir(self):
        LineSaveList = []
        RememberLine = 0

        with open('CoreDefine.py', 'r', encoding=encodingFormat) as rf:
            for eachLine in rf:
                eachLine = eachLine.strip('\n')
                LineSaveList.append(eachLine)

        for idx, eachLine in enumerate(LineSaveList):
            SearchRememberLine = eachLine.find('Pre_Search_Remember_Path')
            if SearchRememberLine >= 0:
                RememberLine = idx

        self.PreRememberPath = LineSaveList[RememberLine].split('= r"')[1][:-1]

        if os.path.isdir(self.PreRememberPath) is False:
            self.PreRememberPath = r"C:/"


    def saveRememberDir(self):
        LineSaveList = []
        RememberLine = 0

        with open('CoreDefine.py', 'r', encoding=encodingFormat) as rf:
            for eachLine in rf:
                eachLine = eachLine.strip('\n')
                LineSaveList.append(eachLine)

        for idx, eachLine in enumerate(LineSaveList):
            SearchRememberLine = eachLine.find('Pre_Search_Remember_Path')
            if SearchRememberLine >= 0:
                RememberLine = idx

        with open('CoreDefine.py', 'w', encoding=encodingFormat) as wf:
            for idx, line in enumerate(LineSaveList):
                if idx == RememberLine:
                    wf.write(f'Pre_Search_Remember_Path    = r"{self.PreRememberPath}"\n')
                else:
                    wf.write(f'{line}\n')


    # CallbackOut ?????? ??? ?????? ????????? setting
    def setReturnDict(self):
        # init ??? ??? ????????? ??????????????? ??????????????? returnDict ???????????? ????????????
        for eachArg in self.initSettingList:
            if 'HLINE' in eachArg[NAME]:
                continue
            # FileDialog ?????? : ?????? ??????
            elif eachArg[TYPE] == 'FD':
                self.returnDict[eachArg[NAME]] = os.path.normpath(self.get_LE_text_by_Name_FD(eachArg[NAME]))
            # CheckBox ?????? : Boolean ??????
            elif eachArg[TYPE] == 'CB':
                self.returnDict[eachArg[NAME]] = self.get_CheckValid_by_Name(eachArg[NAME])
            # LE ?????? : str ??????
            elif eachArg[TYPE] == 'LE':
                self.returnDict[eachArg[NAME]] = str(self.get_LE_text_by_Name_LE(eachArg[NAME]))
            # UI ?????? : dict ??????
            elif eachArg[TYPE] == 'UI':
                self.returnDict[eachArg[NAME]] = self.get_Dict_by_UI_Name(eachArg[NAME])

    def getReturnDict(self):
        return self.returnDict


    # ????????? ?????? ???????????? ???????????? ?????? ??????
    def setSettingNameList(self):
        for each in self.initSettingList:
            self.settingNameList.append(each[NAME])


    # ????????? ??? ?????? initSettingList ?????????, type ??? ?????? ????????? ?????? ??? UI ?????? ???????????? ????????????
    def settingBytInitSettingList(self):
        for eachSetArg in self.initSettingList:
            if eachSetArg[TYPE] == 'FD':
                self.appendNewFD(eachSetArg)
                self.initSettingFDList.append(eachSetArg)

            elif eachSetArg[TYPE] == 'CB':
                self.appendNewCB(eachSetArg)
                self.initSettingCBList.append(eachSetArg)

            elif eachSetArg[TYPE] == 'LE':
                self.appendNewLE(eachSetArg)
                self.initSettingLEList.append(eachSetArg)

            elif eachSetArg[TYPE] == 'UI':
                self.appendNewUI(eachSetArg)
                self.initSettingUIList.append(eachSetArg)


    def getTransMsgFilter(self):
        return self.transFilterMsg


    def appendNewLE(self, SetArg):
        if 'HLINE' in SetArg[NAME]:
            self.selectLEList.append([QFrame()])
            self.selectLEList[LAST_APPEND][0].setFrameShape(QFrame.Shape.HLine)
            self.selectLEList[LAST_APPEND][0].setFrameShadow(QFrame.Shadow.Sunken)
            return

        self.selectLEList.append([QLabel(self) ,QLineEdit(self)])

        # LABEL SETTING
        self.selectLEList[LAST_APPEND][LABEL_INDEX].setText(f'{SetArg[NAME]}')

        # LineEdit Setting
        self.selectLEList[LAST_APPEND][LE_INDEX].setText(f'{SetArg[DEFAULT_VAL]}')
        self.selectLEList[LAST_APPEND][LE_INDEX].setObjectName(f'LE_{SetArg[NAME]}')


    # True/False Define ????????? CheckBox ????????? ????????????
    def appendNewCB(self, SetArg):
        if 'HLINE' in SetArg[NAME]:
            self.selectCBList.append([QFrame()])
            self.selectCBList[LAST_APPEND][0].setFrameShape(QFrame.Shape.HLine)
            self.selectCBList[LAST_APPEND][0].setFrameShadow(QFrame.Shadow.Sunken)
            return

        self.selectCBList.append([QCheckBox(self)])

        # CheckBox Setting
        self.selectCBList[LAST_APPEND][LABEL_INDEX].setText(f'{SetArg[NAME]}')

        # ?????? ???????????? ???????????? True ????????? UI ?????? ??? ?????? ??????????????? (?????????????????? ?????? ?????? ????????????)
        if SetArg[DEFAULT_VAL] == 'True':
            self.selectCBList[LAST_APPEND][LABEL_INDEX].toggle()


    # ????????? Define ????????? Label/LineEdit/PushButton ???????????? ????????????
    def appendNewFD(self, SetArg):
        if 'HLINE' in SetArg[NAME]:
            self.selectFDList.append([QFrame()])
            self.selectFDList[LAST_APPEND][0].setFrameShape(QFrame.Shape.HLine)
            self.selectFDList[LAST_APPEND][0].setFrameShadow(QFrame.Shadow.Sunken)
            return

        self.selectFDList.append([QLabel(self) ,QLineEdit(self), QPushButton(self)])

        # LABEL SETTING
        self.selectFDList[LAST_APPEND][LABEL_INDEX].setText(f'{SetArg[NAME]}')

        # LineEdit Setting
        self.selectFDList[LAST_APPEND][LE_INDEX].setText(f'{SetArg[DEFAULT_VAL]}')
        self.selectFDList[LAST_APPEND][LE_INDEX].setObjectName(f'LE_{SetArg[NAME]}')
        # ?????? ?????? ????????? LineEdit ?????? ?????? ?????? / ?????? ????????? ?????? ?????? ??????
        if SetArg[ISDIR] == 'True':
            self.selectFDList[LAST_APPEND][LE_INDEX].setReadOnly(True)

        # PushButton Setting
        getValue    = self.getTextByFDStatus(SetArg)
        msg         = getValue.split('_')[0]
        color       = getValue.split('_')[1]

        self.selectFDList[LAST_APPEND][BT_INDEX].setText(f'{msg}')
        self.selectFDList[LAST_APPEND][BT_INDEX].setStyleSheet(f'color:{color}')
        self.selectFDList[LAST_APPEND][BT_INDEX].setObjectName(f'BT_{SetArg[NAME]}')
        self.selectFDList[LAST_APPEND][BT_INDEX].clicked.connect(self.btn_clicked)


    def getTextByFDStatus(self, SetArg):
        if SetArg[ISDIR]:
            if JustCheckDir(SetArg[DEFAULT_VAL]):
                return 'EDIT_#000000'
            else:
                return 'Not Exist_#FF6666'
        else:
            if JustCheckFile(SetArg[DEFAULT_VAL]):
                return 'EDIT_#000000'
            else:
                return 'Not Exist_#FF6666'


    # Setup Custom BTNs of Custom Widgets
    # Get sender() function when btn is clicked
    def setup_BTNs(self):
        for eachArg in self.selectFDList:
            if eachArg[BT_INDEX].sender() != None:
                return eachArg[BT_INDEX].sender()


    # ?????? ????????? ??? ???????????? ?????? ??????
    def btn_clicked(self):
        sender      = self.sender()
        btn         = self.setup_BTNs()
        ButtonName  = btn.objectName()           # Ex) Res = BT_AbbreviatedImgPath
        ButtonName  = ButtonName.split('_')[1]   # Ex) Res = AbbreviatedImgPath
        isChanged   = True

        prePath     = self.get_LE_text_by_Name_FD(ButtonName)
        isDir       = self.get_isDir_by_Name(ButtonName)

        # ????????? Define ??? ?????? ??????
        if isDir is True:
            targetDir = QFileDialog.getExistingDirectory(self, 'Select Path', self.PreRememberPath)
        # ????????? Define ??? ?????? ?????? 
        else:
            targetDir = QFileDialog.getOpenFileName(self, 'Select File', self.PreRememberPath)[0]

        # ?????? ????????? ????????? ?????? ????????? ?????? ?????????
        if len(targetDir) == 0:
            targetDir = prePath
            isChanged = False

        self.PreRememberPath = os.path.dirname(targetDir)

        # ????????? ??? LineEdit ???????????? update
        self.set_LE_text_by_Name(ButtonName, targetDir)

        if isChanged:
            sender.setText('APPLIED')
            sender.setStyleSheet(f'color:#000000')


    def get_isDir_by_Name(self, Name):
        for eachArg in self.initSettingFDList:
            if eachArg[NAME] == Name:
                return eachArg[ISDIR]


    # Ex) AbbreviatedImgPath ????????? ????????????, ?????? ????????? ?????? LineEdit ???????????? ??????
    def get_LE_text_by_Name_FD(self, Name):
        for idx, eachArg in enumerate(self.initSettingFDList):
                if eachArg[NAME] == Name:
                    return self.selectFDList[idx][LE_INDEX].text()
        return None


    def get_LE_text_by_Name_LE(self, Name):
        for idx, eachArg in enumerate(self.initSettingLEList):
                if eachArg[NAME] == Name:
                    return self.selectLEList[idx][LE_INDEX].text()
        return None


    def set_LE_text_by_Name(self, Name, Text):
        for idx, eachArg in enumerate(self.initSettingFDList):
                if eachArg[NAME] == Name:
                    return self.selectFDList[idx][LE_INDEX].setText(Text)

    
    def get_Dict_by_UI_Name(self, Name):
        for idx, eachArg in enumerate(self.initSettingUIList):
            if eachArg[NAME] == Name:
                return self.selectUIList[idx][1]


    def set_Dict_by_UI_Name(self, Name, Dict):     
        for idx, eachArg in enumerate(self.initSettingUIList):
            if eachArg[NAME] == Name:
                self.selectUIList[idx][1] = Dict


    def get_String_by_UI_Name(self, Name):
        for idx, eachArg in enumerate(self.initSettingUIList):
            if eachArg[NAME] == Name:
                return self.selectUIList[idx][1]


    def set_String_by_UI_Name(self, Name, String):
        for idx, eachArg in enumerate(self.initSettingUIList):
            if eachArg[NAME] == Name:
                self.selectUIList[idx][1] = String        

    # Ex) MAKE_39_CLASS ????????? ????????????, ?????? ????????? ?????? True/False ???????????? ??????
    def get_CheckValid_by_Name(self, Name):
        for idx, eachArg in enumerate(self.initSettingCBList):
                if eachArg[NAME] == Name:
                    return self.selectCBList[idx][CB_INDEX].isChecked()

    def set_CheckValid_by_Name(self, Name, Value:bool):
        for idx, eachArg in enumerate(self.initSettingCBList):
                if eachArg[NAME] == Name:
                    self.selectCBList[idx][CB_INDEX].setChecked(Value)        


    # appendNewCB / appendNewFD ?????? ?????? ????????? UI ??? ?????? ????????? ??????
    def settingFinish(self):
        self.setWindowTitle(f'{TITLE}')

        # ??????
        TitleLabel = QLabel()
        TitleLabel.setText(f'[ {self.runProgramName} ]')
        
        font = QFont()
        font.setPointSize(15)
        font.setBold(True)
        TitleLabel.setFont(font)

        self.ui.mainLayout.addWidget(TitleLabel, 1)

        FD_GroupBox = QGroupBox('Select File/Directory Path')
        FD_Vbox     = QVBoxLayout()

        # ??? ?????? ???????????? ????????? ??? ?????? UI ????????????
        for eachFD in self.selectFDList:
            add_H_Layout = QHBoxLayout()

            if str(type(eachFD[0])) == "<class 'PyQt6.QtWidgets.QFrame'>":
                add_H_Layout.addStretch(1)
                add_H_Layout.addWidget(eachFD[0], 16)
                add_H_Layout.addStretch(1)
                FD_Vbox.addLayout(add_H_Layout)
                continue

            add_H_Layout.addStretch(1)
            add_H_Layout.addWidget(eachFD[LABEL_INDEX], 4)
            add_H_Layout.addWidget(eachFD[LE_INDEX], 10)
            add_H_Layout.addWidget(eachFD[BT_INDEX], 2)
            add_H_Layout.addStretch(1)

            # self.ui.mainLayout.addLayout(add_H_Layout, 2)
            FD_Vbox.addLayout(add_H_Layout)

        FD_GroupBox.setLayout(FD_Vbox)
        self.ui.mainLayout.addWidget(FD_GroupBox, 3)

        CB_GroupBox = QGroupBox('Select Option')
        CB_Vbox     = [QVBoxLayout()]

        if len(self.selectCBList) > 6:
            CB_Vbox.append(QVBoxLayout())

        EACH_LINE_MAX_OPT_NUM   = 6
        EmptyIdx                = 0
        LAST_BOX                = -1
        
        # ??? True/False ???????????? ????????? ??? ?????? UI ????????????
        for idx, eachCB in enumerate(self.selectCBList):
            VBoxIdx      = idx // EACH_LINE_MAX_OPT_NUM
            EmptyIdx     = EACH_LINE_MAX_OPT_NUM - ( idx % EACH_LINE_MAX_OPT_NUM )
            add_H_Layout = QHBoxLayout()

            if str(type(eachCB[0])) == "<class 'PyQt6.QtWidgets.QFrame'>":
                add_H_Layout.addStretch(1)
                add_H_Layout.addWidget(eachCB[0], 20)
                add_H_Layout.addStretch(1)
                CB_Vbox[VBoxIdx].addLayout(add_H_Layout)
                continue

            add_H_Layout.addStretch(1)
            add_H_Layout.addWidget(eachCB[CB_INDEX], 20)
            add_H_Layout.addStretch(1)

            # self.ui.mainLayout.addLayout(add_H_Layout, 2)
            CB_Vbox[VBoxIdx].addLayout(add_H_Layout)

        for _ in range(EmptyIdx):
            EmptyLabel  = QLabel()
            EmptyBox    = QHBoxLayout()
            EmptyBox.addWidget(EmptyLabel)
            CB_Vbox[LAST_BOX].addLayout(EmptyBox)

        CB_HBox = QHBoxLayout()
        for eachBox in CB_Vbox:
            CB_HBox.addLayout(eachBox, 1)

        # LineEdit ?????? ???????????? ?????? ????????? ????????????
        LE_GroupBox = QGroupBox('ETC')
        LE_Vbox     = QVBoxLayout()

        for idx, eachLE in enumerate(self.selectLEList):
            add_H_Layout = QHBoxLayout()

            if str(type(eachLE[0])) == "<class 'PyQt6.QtWidgets.QFrame'>":
                add_H_Layout.addStretch(1)
                add_H_Layout.addWidget(eachLE[0], 6)
                add_H_Layout.addStretch(1)
                LE_Vbox.addLayout(add_H_Layout)
                continue

            add_H_Layout.addStretch(1)
            add_H_Layout.addWidget(eachLE[LABEL_INDEX], 2)
            add_H_Layout.addWidget(eachLE[LE_INDEX], 4)
            add_H_Layout.addStretch(1)   

            LE_Vbox.addLayout(add_H_Layout)

        for eachUI in self.selectUIList:
            add_H_Layout = QHBoxLayout()

            add_H_Layout.addStretch(1)
            add_H_Layout.addWidget(eachUI[0], 6)
            add_H_Layout.addStretch(1)

            LE_Vbox.addLayout(add_H_Layout)

        LE_GroupBox.setLayout(LE_Vbox)
        CB_HBox.addWidget(LE_GroupBox, 2)

        CB_GroupBox.setLayout(CB_HBox)
        self.ui.mainLayout.addWidget(CB_GroupBox, 3)

        # Done ?????? ????????????
        self.ui.mainLayout.addWidget(self.ui.quitButton, 1)

    
    def isQuitProgram(self):
        if self.isSelectDone is False:
            return True
        return False
        
