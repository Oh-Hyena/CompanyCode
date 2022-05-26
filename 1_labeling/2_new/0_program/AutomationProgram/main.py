# Import Packages and Modules
# Standard Library
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
import sys
import copy
import os
import pickle
import datetime

# Installed Library - QT CORE
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
from qt_core import *

# Custom Modules
# python -m PyQt6.uic.pyuic -x main.ui -o ui_main.py
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
from Core.json_settings         import Settings
from Widgets.py_toggle          import PyToggle             # Toggle Widtet
from Core.general_function      import *                    # General Function Anyware use it
from Core.pretreatment_function import set_RunFunction_list # Pretreatment Part Functions
from Core.send_argv             import SendArgvClass

# MainWindow Setup & Function Modules
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
from MainWindow.ui_main                 import Ui_MainWindow    
from MainWindow.setup_main_window       import SetupMainWindow
from MainWindow.functions_main_window   import MainFunctions

# For Extern Values by RunFunction
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
from RunFunction.Xml_To_Text    import ResultDir as ResultDir_Xml_To_Text
from RunFunction.Make_2_Class   import ResultDir as ResultDir_Make_2_Class 

# Defines
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
ShowLog = copy.copy(CoreShowLog)
TestMode = copy.copy(CoreTestMode)


# MainWindow Class
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Load UI by Designer
        # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Load Settings
        # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
        settings = Settings()
        self.settings = settings

        # Set Signal
        # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
        self.Signal = SignalClass()
        self.Signal.s.connect(self.ReactSignal)

        # Setup MainWindow
        # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
        SetupMainWindow.setup_GUI(self)

        # Make PyToggle Widgets
        # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
        self.isRunDefaultToggle = PyToggle()
        self.settingUncertainListOnToggle = PyToggle()

        # For Global var. ( 차후 정리 )
        # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-

        # For SearchSubDir Save var.
        # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
        self.SaveDir = os.path.dirname(os.path.abspath(__file__))
        self.SaveFileName = "save.txt"
        self.scanLimitCount = 500
        self.searchTargetDir = ""

        # For Drag
        # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
        self.m_flag = False
        self.m_Position = 0

        # For RunFunctionList var
        # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
        self.CurResultDirValName = ""
        self.CurResultDir = ""
        self.RunFunctionList = []
        self.RunFuncSaveDirDict = {}
        self.RunFunc_Path = ""

        self.sendArgv = SendArgvClass()

        # For Pretreatment var.
        # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
        self.SubDirSearchList = []
        self.CheckFormat = ".txt"
        self.isCountTotalFile = False   # CountTotalFile OR SearchSubDir

        # Init Ui
        # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
        self.InitUI()

    # InitUI Function
    # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
    def InitUI(self):
        # RunFunction 폴더 안에 프로그램 실행 함수 파일(.py)들 목록값 추출하기
        # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
        self.RunFunctionList, self.RunFuncSaveDirDict, self.RunFunc_Path = set_RunFunction_list()
        self.ui.comboBoxSelectFunction.addItems(self.RunFunctionList)

        # RunFunction 결과값 저장 디렉토리 판단 변수 설정
        # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
        self.CurResultDirValName = self.RunFuncSaveDirDict[self.ui.comboBoxSelectFunction.currentText()]
        self.CurResultDir = globals()[self.CurResultDirValName]

        # SendArgv 값 초기값 할당
        # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
        self.OverwriteByJson()

        # PyToggle Set
        # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
        self.isRunDefaultToggle.setName("isRunDefaultToggle")
        self.settingUncertainListOnToggle.setName("settingUncertainListOnToggle")

        self.ui.toggleLayout.addWidget(self.isRunDefaultToggle)
        self.ui.addWorkUncertainLayout.addWidget(self.settingUncertainListOnToggle)

        self.isRunDefaultToggle.stateChanged.connect(self.toggle_changed)
        self.settingUncertainListOnToggle.stateChanged.connect(self.toggle_changed)


    # A function that handles when a signal is received
    # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
    def ReactSignal(self, arg):
        self.ui.TE_Log.append(arg[1])
        self.ui.TE_Log.repaint()
        self.update()

    # Run Function When BTN is clicked
    # Check function by object name / btn_id
    # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
    def btn_clicked(self):  # TODO : Make BTN Click Function
        # Get BTN Clicked
        btn = SetupMainWindow.setup_BTNs(self)
        ButtonName = btn.objectName()

        # Setting Frame Function
        # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
        if ButtonName == "InSettingButton":
            MainFunctions.InSetting(self, self.SaveDir, 
                                    self.SaveFileName,      
                                    self.scanLimitCount)

        elif ButtonName == "SettingQuitBotton":
            MainFunctions.OutSetting(self)
            self.sendArgv.ChangedSettingSaveToJson()
            self.OverwriteByJson()

        # Select & Modify Path Function Here
        # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
        elif ButtonName == "selectPathButton":
            self.searchTargetDir = MainFunctions.selectPath(self, ButtonName)
        
        elif ButtonName == "selectPathButton_ExtractSubDirPath":
            self.SaveDir, self.sendArgv.SArg_LogPath = MainFunctions.selectPath(self, ButtonName)

        elif ButtonName == "selectPathButton_runFunctionResDir":
            self.sendArgv.SArg_ResDir = MainFunctions.selectPath(self, ButtonName)
            self.CurResultDir = self.ui.LE_Setting_RunFunctionDir.text()

        # Pretreatment Run Button
        # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
        elif ButtonName == "ExtractPathButton":
            sendParam = self.Package_sendParam(ButtonName)
            MainFunctions.PretreatmentRun(self, self.Signal, sendParam)

        # RunFunction Button
        # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
        elif ButtonName == "RunFuncButton" or \
             ButtonName == "CustomRunButton" :    

            Sargv = ""
            isCustomRun = self.isRunDefaultToggle.isChecked()

            if ButtonName == "RunFuncButton" and isCustomRun == False:
                self.sendArgv.setValueDefaultSetting()
                Sargv = self.sendArgv.get_Engraft_SendArgv()

            elif ButtonName == "CustomRunButton":
                Sargv = self.sendArgv.get_Engraft_SendArgv()
                self.sendArgv.ChangedSettingSaveToJson()
                
            MainFunctions.runFunctionFile(self, ButtonName, Sargv, self.RunFunc_Path, isCustomRun)

        # Quit Button
        # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
        elif ButtonName == "QuitBotton":
            self.close()


    # Packaging Send Parameter
    # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
    def Package_sendParam(self, objName):
        sendParam = {}
        if objName == "ExtractPathButton":
            sendParam['LimitCount'] = self.scanLimitCount
            sendParam['SaveDir'] = self.SaveDir
            sendParam['SaveFileName'] = self.SaveFileName
            sendParam['TargetPath'] = self.searchTargetDir
            sendParam['checkFormat'] = self.CheckFormat
            sendParam['isRunCount'] = self.isCountTotalFile

        return sendParam


    # Run Function When ComboBox is changed
    # Check function by getName
    # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
    def comboBox_changed(self):
        # Get comboBox Changed
        # box = SetupMainWindow.setup_comboBox(self)
        box = self.sender()

        if box.objectName() == "comboBoxSelectMenu":
            self.isCountTotalFile = MainFunctions.runOptionChange(self)
        if box.objectName() == "comboBoxSelectFunction":
            NoticeLog(f"Set/Changed RunFunction ")
            self.CurResultDirValName = self.RunFuncSaveDirDict[MainFunctions.setCurResultDirValue(self)]
            self.sendArgv.set_SendArgv_Function(self.ui.comboBoxSelectFunction.currentText())
            self.OverwriteByJson()


    # Run Function When LineEdit is changed
    # Check function by getName
    # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-   
    def lineEdit_changed(self):
        # Get lineEdit Changed
        #le = SetupMainWindow.setup_lineEdit(self)
        le = self.sender()

        # Set Change : Pretreatment - Search Skip CountSendLogPathArgv
        if le.objectName() == "LE_SkipCount":
            self.scanLimitCount = MainFunctions.skipCountChanged(self)

        # Set Change : RunFunction - Start Idx Change Run Dir List
        elif le.objectName() == "LE_StartCount":
            self.sendArgv.SArg_StartIndex = MainFunctions.StartCountChanged(self)

        elif le.objectName() == "LEFormat":
            self.CheckFormat = MainFunctions.formatChanged(self)

        elif le.objectName() == "LE_Setting_ExtractSubDirFileName":
            self.SaveFileName, self.sendArgv.SArg_LogPath = MainFunctions.saveFilenameChanged(self)

        elif le.objectName() == "LE_Setting_ExtractSubDirPath":
            self.SaveDir, self.sendArgv.SArg_LogPath = MainFunctions.saveFilePathChanged(self)
            

    # Run Function When Toggle is changed
    # Check function by getName
    # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
    def toggle_changed(self):
        # Get Toggle
        tg = self.sender()
        isToggleChecked = tg.isChecked()

        # Run Defualt OR Run Custom
        if tg.getName() == "isRunDefaultToggle":
            MainFunctions.RunModeChangedCustom(self, isToggleChecked)

        # Run AddWork for Uncertain List
        elif tg.getName() == "settingUncertainListOnToggle":
            self.sendArgv.SArg_AddWork = MainFunctions.AddWorkUncertainListChanged(self, isToggleChecked)


    # MOUSE Click drag EVENT function
    # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.m_flag = True
            # Get the position of the mouse relative to the window
            self.m_Position = event.globalPosition().toPoint() - self.pos()
            event.accept()

    def mouseMoveEvent(self, QMouseEvent):
        if Qt.MouseButton.LeftButton and self.m_flag:
            # Change window position
            self.move(QMouseEvent.globalPosition().toPoint() - self.m_Position)  
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag = False

    def OverwriteByJson(self):                                  
        self.settings.deserialize()

        sarg_name_list  = self.sendArgv.SArgList()
        sarg_dict       = self.sendArgv.getValueByRealValue()
        sarg_deft       = self.sendArgv.getValueDefaultSetting()

        # sarg_name_list = ['SArg_LogPath', 'SArg_ResDir' ... ]
        for each in sarg_name_list:  
            try:
                # Default 세팅값과 다른 값이 Json의 현재 값일 때 -> 변경해주기
                if sarg_dict[each] != sarg_deft[each]:                              
                    if each == "SArg_LogPath":
                        self.SaveDir = os.path.dirname(sarg_dict[each])
                        self.SaveFileName = os.path.basename(sarg_dict[each])

                        self.ui.LE_Setting_ExtractSubDirPath.setText(self.SaveDir)
                        self.ui.LE_Setting_ExtractSubDirFileName.setText(self.SaveFileName)

                    elif each == "SArg_ResDir":
                        self.CurResultDir = sarg_dict[each]
                        self.ui.LE_Setting_RunFunctionDir.setText(self.CurResultDir)

                    elif each == "SArg_StartIndex":
                        self.ui.LE_StartCount.setText(sarg_dict[each])

                # Default 값일 때 세팅해주는 파트
                else:
                    if each == "SArg_LogPath":
                        self.SaveDir = os.path.dirname(os.path.abspath(__file__))
                        self.SaveFileName = "save.txt"

                        self.ui.LE_Setting_ExtractSubDirPath.setText(self.SaveDir)
                        self.ui.LE_Setting_ExtractSubDirFileName.setText(self.SaveFileName)

                    elif each == "SArg_ResDir":
                        self.CurResultDir = globals()[self.CurResultDirValName]
                        self.ui.LE_Setting_RunFunctionDir.setText(self.CurResultDir)

            except Exception as e:
                NoticeLog(f"\'{each}\' is Not in \'settings.json\' at \'{self.ui.comboBoxSelectFunction.currentText()[:-3]}\'")
                continue
                    



def main():
    RunFunctionLog()
    app = QApplication(sys.argv)
    ProgramUI = MainWindow()

    if TestMode:
    # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
        print("FILE : ", __file__)
        Sargv = ProgramUI.sendArgv.get_Engraft_SendArgv()
        RunPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'RunFunction/Xml_To_Text.py')
        os.system(f"python {RunPath} {Sargv}")
    # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-

    ProgramUI.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
