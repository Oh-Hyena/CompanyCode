# IMPORT CORE
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
from Core.CommonUse                             import *


# IMPORT RUNFUNCTION
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
from RunFunction.ChangeVideoToImgClass          import ChangeVideoToImg
from RunFunction.UnzipClass                     import UnzipYoloTxt
from RunFunction.CountObjectClass               import CountObject
from RunFunction.CropPersonByTxtClass           import CropPersonByTxt


# IMPORT UI
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
from UI.SelectUI.SelectUIClass                  import *
from UI.ChoiceProgramUI.ChoiceProgramUIClass    import *


# Activate Function
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
def Activate(Program, App): 
    return eval(f'{Program}(App)')  # type:class

# Main Function
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
def main():
    showProgramInfo()
    App             = QApplication(sys.argv)
    ChoiceProgram   = ChoiceProgramUI(App)

    while True:
        ProgramName = ChoiceProgram.run()
        if CheckExit(ProgramName) : break
        Activate(ProgramName, App).run()

# RUN
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
if __name__ == "__main__":
    main()

