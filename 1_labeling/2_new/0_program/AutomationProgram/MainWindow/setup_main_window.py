# Import Packages and Modules
# Standard Library
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
import sys
import os

# Installed Library - QT CORE
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
from qt_core import *

# Import Settings
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
from Core.json_settings import Settings

# Import Widget
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
from Widgets.py_toggle import PyToggle

# Load UI Main
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
from MainWindow.ui_main import *


# Setup MainWindow Class
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
class SetupMainWindow():
    def __init__(self):
        super().__init__()

        # Setup MainWindow
        # Load Widgets from "MainWindow\ui_main.py"
        # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Load Settings
        # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
        settings = Settings()
        self.settings = settings

    # Setup Custom BTNs of Custom Widgets
    # Get sender() function when btn is clicked
    # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
    def setup_BTNs(self):
        # For Setting
        if self.ui.selectPathButton_ExtractSubDirPath.sender() != None:
            return self.ui.selectPathButton_ExtractSubDirPath.sender()
        elif self.ui.selectPathButton_runFunctionResDir.sender() != None:
            return self.ui.selectPathButton_runFunctionResDir.sender()
        elif self.ui.InSettingButton.sender() != None:
            return self.ui.InSettingButton.sender()
        elif self.ui.SettingQuitBotton.sender() != None:
            return self.ui.SettingQuitBotton.sender()


        # For Pretreatment
        elif self.ui.selectPathButton.sender() != None:
            return self.ui.selectPathButton.sender()
        elif self.ui.ExtractPathButton.sender() != None:
            return self.ui.ExtractPathButton.sender()

        # For RunFunction
        elif self.ui.RunFuncButton.sender() != None:
            return self.ui.RunFuncButton.sender()
        elif self.ui.CustomRunButton.sender() != None:
            return self.ui.CustomRunButton.sender()

        # ETC
        elif self.ui.QuitBotton.sender() != None:
            return self.ui.QuitBotton.sender()

    # Setup Custom ComboBox of Custom Widgets
    # Get sender() function when ComboBox is changed
    # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
    def setup_comboBox(self):
        if self.ui.comboBoxSelectMenu.sender() != None:
            return self.ui.comboBoxSelectMenu.sender()
        elif self.ui.comboBoxSelectFunction.sender() != None:
            return self.ui.comboBoxSelectFunction.sender()

    # Setup Custom LineEdit of Custom Widgets
    # Get sender() function when LineEdit is changed
    # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
    def setup_lineEdit(self):
        if self.ui.LE_SkipCount.sender() != None:
            return self.ui.LE_SkipCount.sender()
        elif self.ui.LE_StartCount.sender() != None:
            return self.ui.LE_StartCount.sender()
        elif self.ui.LEFormat.sender() != None:
            return self.ui.LEFormat.sender()
        elif self.ui.LE_Setting_ExtractSubDirFileName.sender() != None:
            return self.ui.LE_Setting_ExtractSubDirFileName.sender()
        elif self.ui.LE_Setting_ExtractSubDirPath.sender() != None:
            return self.ui.LE_Setting_ExtractSubDirPath.sender()


    # Setup MainWindow with Custom Param
    # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
    def setup_GUI(self):
        # Remove TitleBar
        if self.settings.items["custom_title_bar"]:
            self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
            self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # Adjust Layout Attribute
        # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
        self.ui.toggleLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ui.addWorkUncertainLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Set Page Index
        # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
        self.ui.SettingStackedWidget.setCurrentIndex(0)

        # Set Enable & Disable
        # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
        self.ui.LEFormat.setEnabled(False)
        self.ui.TE_Log.setReadOnly(True)

        # Set Hide
        # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
        self.ui.SettingMainFrame.hide()
        self.ui.CustomRunButton.hide()

        # Set Text
        # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
        self.ui.LE_Setting_ExtractSubDirPath.setText(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../'))
        self.ui.LEFormat.setText(".txt")

        # Set Signals - BTN
        # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
        self.ui.InSettingButton.clicked.connect(self.btn_clicked)
        self.ui.SettingQuitBotton.clicked.connect(self.btn_clicked)
        self.ui.selectPathButton_ExtractSubDirPath.clicked.connect(self.btn_clicked)
        self.ui.selectPathButton_runFunctionResDir.clicked.connect(self.btn_clicked)
        self.ui.selectPathButton.clicked.connect(self.btn_clicked)
        self.ui.ExtractPathButton.clicked.connect(self.btn_clicked)
        self.ui.RunFuncButton.clicked.connect(self.btn_clicked)
        self.ui.CustomRunButton.clicked.connect(self.btn_clicked)
        self.ui.QuitBotton.clicked.connect(self.btn_clicked)

        # Set Signals - ComboBox
        # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
        self.ui.comboBoxSelectMenu.currentIndexChanged.connect(self.comboBox_changed)
        self.ui.comboBoxSelectFunction.currentIndexChanged.connect(self.comboBox_changed)

        # Set Signals - LineEdit
        # -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
        self.ui.LEFormat.textChanged.connect(self.lineEdit_changed)
        self.ui.LE_StartCount.textChanged.connect(self.lineEdit_changed)
        self.ui.LE_SkipCount.textChanged.connect(self.lineEdit_changed)
        self.ui.LE_Setting_ExtractSubDirFileName.textChanged.connect(self.lineEdit_changed)




    
