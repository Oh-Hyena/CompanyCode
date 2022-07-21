OriginSource_Video_Path   = r"E:\attTest\0704\video"
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
TITLE   = 'Labeling Program'
DATE    = '2022-06-28'
VERSION = '1.1.0'
IDE     = 'Visual Studio Code 1.62.0'
OS      = 'Windows 10'
AUTHOR  = 'OH HYE NA'


# CONST Defines
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
ERROR_STRICT_HARD = 0
ERROR_STRICT_SOFT = 1


# VAR Defines
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
CORE_SHOW_LOG       = True              # 터미널 창에 로그가 나오게 하는지 총괄하는 시스템 변수
CORE_TEST_MODE      = False
CORE_ERROR_STRICT   = ERROR_STRICT_SOFT # 에러 발생 시, 처리 정도를 결정하는 시스템 변수


# PATH Defines
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
CrushedImgFileName        = 'CrushImg.txt'

OriginSource_Video_Path   = r"E:\attTest\0704\video"
OriginSource_Img_Path     = r""
OriginSource_Zip_Path     = r""
OriginSource_Txt_Path     = r""

OriginSource_NewDataset_Path = r''
OriginSource_OriDataset_Path = r''

OriginSource_CvatXml_Path = r""
OriginSource_AnalysisPath = r''

Result_Dir_Path           = r"E:\attTest\0704\img"
RealExistCheck_Path       = r''
Pre_Search_Remember_Path    = r"E:/attTest/0713"


# OTHER DEFINES
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
CORE_ENCODING_FORMAT    = 'utf-8'                       # 파일 Read 할 때, 인코딩 포맷
VALID_IMG_FORMAT        = ['.jpg', '.png', '.jpeg']     # Img 유효한 확장자
VALID_VIDEO_FORMAT      = ['.mp4']                      # Video 유효한 확장자


# CONST DEFINE
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
COND_PASS = True
COND_FAIL = False

WIDTH     = 0
HEIGHT    = 1


# Link VAR
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
CORE_LINK_DICT  = {}
LINK_NAME_LIST  = 0
CORE_SAVE_VALUE = 1


# FunctionDefine
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
def setCoreValue(CoreName, Value):
    globals()[CoreName] = Value

def getCoreValue(CoreName):
    return globals()[CoreName]
