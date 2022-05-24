"""
LAST_UPDATE : 2021/10/15
AUTHOR      : OH HYENA
"""


from Core.CommonUse                             import *

from RunFunction.MakeClass                      import MakeClassSource
from RunFunction.SliceImgClass                  import SliceImage
from RunFunction.ExtractAnnotationClass         import ExtractAnnotation
from RunFunction.JoinPathClass                  import JoinPath
from RunFunction.ConditionFilterClass           import FilterCondition

from UI.SelectUI.SelectUIClass                  import *
from UI.ChoiceProgramUI.ChoiceProgramUIClass    import *


# run program
def Activate(Program, App): return eval(f'{Program}(App)')  # type:class


def main():
    showProgramInfo()
    App             = QApplication(sys.argv)
    ChoiceProgram   = ChoiceProgramUI(App)

    while True:
        ProgramName = ChoiceProgram.run()
        if CheckExit(ProgramName) : break
        Activate(ProgramName, App).run()


if __name__ == "__main__":
    main()
