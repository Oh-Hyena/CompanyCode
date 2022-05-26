# Import Packages and Modules
# Standard Library
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
import pickle
import sys
import os
import copy
import time
import datetime

# Custom Modules
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
from Core.general_function          import RunFunctionLog, SignalClass, callername, filename, showLog
from Core.pretreatment_function     import check_count_with_format_by_files, get_subDir_by_path

# Installed Library - QT CORE
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
from qt_core import *

# Load UI Main
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
from MainWindow.ui_main import Ui_MainWindow

# For Extern Values by RunFunction
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
from RunFunction.Xml_To_Text    import ResultDir as ResultDir_Xml_To_Text
from RunFunction.Make_2_Class   import ResultDir as ResultDir_Make_2_Class

# Defines
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
ShowLog = copy.copy(CoreShowLog)
TestMode = copy.copy(CoreTestMode)

# Functions
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
class MainFunctions():
    def __init__(self):
        super().__init__()

        # Setup MainWindow
        # Load Widgets from "MainWindow\ui_main.py"
        # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

    # Function Define
    # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-

    # BTN Functions
    # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
    # Open Setting Frame
    def InSetting(self, SaveDir, SaveFileName, LimitCount):
        # Write Setting Value
        self.ui.LE_Setting_ExtractSubDirFileName.setText(SaveFileName)
        self.ui.LE_Setting_ExtractSubDirPath.setText(SaveDir)
        self.ui.LE_SkipCount.setText(str(LimitCount))

        self.ui.SettingStackedWidget.setCurrentIndex(0)
        self.ui.SettingMainFrame.show() 

    def OutSetting(self):
        self.ui.SettingMainFrame.hide()
        self.ui.CustomRunButton.hide()

    # Select & Modify Path Button Function Total Here  
    # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
    def selectPath(self, ButtonName):   # TODO : 경로 선택 취소했을 때 공백값 대체해야함
        # 최하위 디렉토리 검색 시작할 타겟 경로 선택 및 변경
        if ButtonName == "selectPathButton":
            preTargetDir = self.ui.PathLE.text()
            targetDir = QFileDialog.getExistingDirectory(self, 'SelectPath', 'C:/')
            
            if len(targetDir) == 0:
                targetDir = preTargetDir

            self.ui.PathLE.setText(targetDir)
            return targetDir

        # 최하위 디렉토리 검색 함수 결과 로그값 저장할 경로 선택 및 변경
        elif ButtonName == "selectPathButton_ExtractSubDirPath":
            preTargetDir = self.ui.LE_Setting_ExtractSubDirPath.text()
            targetDir       = QFileDialog.getExistingDirectory(self, 'SelectPath', os.path.realpath(os.getcwd()))
            
            if len(targetDir) == 0:
                targetDir = preTargetDir
            
            LogPath         = os.path.join(targetDir, self.ui.LE_Setting_ExtractSubDirFileName.text())
            SendLogPathArgv = f"LogPath$$${os.path.normpath(LogPath)}"
            self.ui.LE_Setting_ExtractSubDirPath.setText(targetDir)
            return targetDir, SendLogPathArgv

        elif ButtonName == "selectPathButton_runFunctionResDir":
            preTargetDir = self.ui.LE_Setting_RunFunctionDir.text()
            targetDir = QFileDialog.getExistingDirectory(self, 'SelectPath', 'C:/')

            if len(targetDir) == 0:
                targetDir = preTargetDir

            self.ui.LE_Setting_RunFunctionDir.setText(targetDir)
            SendResDirArgv = f"resDir$$${targetDir}"
            return SendResDirArgv

    # Pretreatment Run Button
    # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
    def PretreatmentRun(self, signal:SignalClass, recvParam):
        self.ui.TE_Log.clear()
        
        # set Param
        targetPath = recvParam['TargetPath']
        isRunCount = recvParam['isRunCount']
        checkFormat = recvParam['checkFormat']
        limitCount = recvParam['LimitCount']
        saveDir = recvParam['SaveDir']
        savePath = recvParam['SaveFileName']

        if not targetPath:
            ErrorMessgae = "Path is not Selected!"
            self.ui.TE_Log.append()
            showLog(ErrorMessgae)
            return

        # Run Count File Num by fileFormat
        if isRunCount:
            logMsg = f"[ Run ] check_count_with_format_by_files : {targetPath} ({checkFormat})"
            self.ui.TE_Log.append(logMsg)
            showLog(logMsg)
    
            check_count_with_format_by_files(targetPath, signal, checkFormat)    

        # Search SubDir
        else:     
            logMsg = f"[ Run ] get_subDir_by_path : {targetPath}"
            self.ui.TE_Log.append(logMsg)
            showLog(logMsg)

            TotalList = []
            get_subDir_by_path(targetPath, TotalList, signal, limitCount, 0)

            signalMsg = f"[ Done ] List Total Num : {len(TotalList)}"
            signal.s.emit(signal.send_signal_format(signalMsg))
            showLog(signalMsg)

            savePath = os.path.join(saveDir, savePath)
            saveMsg = f"[ Save ] List Log Save -> {savePath}"
            signal.s.emit(signal.send_signal_format(saveMsg))
            showLog(saveMsg)

            with open(savePath, 'wb') as f:
                pickle.dump(TotalList, f)


    # RunFunction File Run Func
    # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
    def runFunctionFile(self, ButtonName, sendArgv, runFuncPath, isCustomRun=False):
        # For RunFunction
        funcName = self.ui.comboBoxSelectFunction.currentText()
        filePath = os.path.join(runFuncPath, funcName)

        # For Log
        startTime = time.time()
        startTimeLog = datetime.datetime.now().strftime('%H:%M:%S')
        RunFileLog = f" [ RunFile : \x1b[36m{funcName}\x1b[0m ]"

        # PrefixLog & SuffixLog inline Function
        # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
        def prefixLog(func_name):
                TE_Log = f"<b>[ RunFile Operate ] {func_name} </b>"
                TE_WARING_Log = '<b><p style="color:red">[ WARNING ] Do not do anything else while RunFile is running!</p></b>'
                
                self.ui.TE_Log.append("")
                self.ui.TE_Log.append("="*45)
                self.ui.TE_Log.append(TE_Log)
                self.ui.TE_Log.append(TE_WARING_Log)
                self.ui.TE_Log.append("="*45)
                self.ui.TE_Log.repaint()

        def suffixLog(startTime, startTimeLog):
            RunTime = time.time() - startTime
            endTimeLog = datetime.datetime.now().strftime('%H:%M:%S')
            ResultTime = str(datetime.timedelta(seconds=RunTime)).split(".")
            ResultTime = ResultTime[0]

            self.ui.TE_Log.append("")
            self.ui.TE_Log.append("<b>[ RunFile Done ]</b>")
            self.ui.TE_Log.append(f"- Start : {startTimeLog}")
            self.ui.TE_Log.append(f"- End : {endTimeLog}")
            self.ui.TE_Log.append(f"--------------------------> {ResultTime}")
            self.ui.TE_Log.repaint()

        # Run Function
        # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
        if ButtonName == "RunFuncButton":
            if isCustomRun:
                self.ui.SettingStackedWidget.setCurrentIndex(1)
                self.ui.SettingMainFrame.show()
                self.ui.CustomRunButton.show()
            else:
                RunFunctionLog(RunFileLog)
                prefixLog(funcName)

                os.system(f"python {filePath} {sendArgv}")

                suffixLog(startTime, startTimeLog)

        elif ButtonName == "CustomRunButton":
            self.ui.SettingMainFrame.hide()
            self.ui.CustomRunButton.hide()

            RunFunctionLog(RunFileLog)
            prefixLog(funcName)

            os.system(f"python {filePath} {sendArgv}")

            suffixLog(startTime, startTimeLog)


    # Toggle Functions
    # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
    def RunModeChangedCustom(self, bOn:bool):
        if bOn:
            self.ui.RunFuncButton.setText("Run Custom")
        else:
            self.ui.RunFuncButton.setText("Run Default")

    def AddWorkUncertainListChanged(self, bOn:bool):
        if bOn:
            return "UncertainOn$$$ON"
        else:
            return "UncertainOn$$$OFF"

    # LineEdit Functions
    # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
    # scanLimitCount Change
    def skipCountChanged(self):
        change_count = int(self.ui.LE_SkipCount.text())
        return change_count

    # RunFunction Start Index Change
    def StartCountChanged(self):
        change_count = int(self.ui.LE_StartCount.text())
        return_value = f"StartIndex$$${change_count}"
        return return_value

    # FileCount CheckFormat Change
    def formatChanged(self):
        check_text = self.ui.LEFormat.text()
        if len(check_text) == 0:
            return ""

        if check_text[0] != ".":
            check_text = '.' + check_text
        
        return check_text

    # Search SubDir Log (save.txt) : 최하위 디렉토리 검색 로그 저장 파일 변경
    def saveFilenameChanged(self):
        file_path = self.ui.LE_Setting_ExtractSubDirPath.text()
        file_name = self.ui.LE_Setting_ExtractSubDirFileName.text()

        if len(file_name) == 0:
            path = os.path.normpath(os.path.join(file_path, "save.txt"))
            return file_name, f"LogPath$$${path}"
        
        path = os.path.normpath(os.path.join(file_path, file_name))
        return file_name, f"LogPath$$${path}"

    def saveFilePathChanged(self):
        file_path = self.ui.LE_Setting_ExtractSubDirPath.text()
        file_name = self.ui.LE_Setting_ExtractSubDirFileName.text()

        if len(file_path) == 0:
            temp_save_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../')
            path = os.path.normpath(os.path.join(temp_save_dir, file_name))
            return file_path, f"LogPath$$${path}"
        
        path = os.path.normpath(os.path.join(file_path, file_name))
        return file_path, f"LogPath$$${path}"

    
    # ComboBox Functions
    # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
    def runOptionChange(self):
        option = self.ui.comboBoxSelectMenu.currentText()
        if option == "Extract Lower Dir":
            self.ui.LEFormat.setEnabled(False)
            return False
            
        elif option == "Count File Num":
            self.ui.LEFormat.setEnabled(True)
            return True

    def setCurResultDirValue(self):
        return self.ui.comboBoxSelectFunction.currentText()