TITLE   = 'Attribute Program'
DATE    = '2022-03-14'
VERSION = '1.1.1'
IDE     = 'Visual Studio Code 1.64.0'
OS      = 'Windows 10'
AUTHOR  = 'SHY'


ERROR_STRICT_HARD = 0
ERROR_STRICT_SOFT = 1


CORE_SHOW_LOG       = True              # 터미널 창에 로그가 나오게 하는지 총괄하는 시스템 변수
CORE_TEST_MODE      = False
CORE_ERROR_STRICT   = ERROR_STRICT_SOFT # 에러 발생 시, 처리 정도를 결정하는 시스템 변수


import sys
import re


CrushedImgFileName          = 'CrushImg.txt'

OriginSource_cvatXml_Path   = r"H:\39class_attribute\4_dataset\스마트어린이집\2021_스마트어린이집\att_2021_nursery_child_pure_500_xml"
OriginSource_Img_Path       = r"H:\39class_attribute\4_dataset\스마트어린이집\2021_스마트어린이집\att_2021_nursery_child_pure_500_img"

OriginSource_AnntationPath  = r"D:\PyCharm\Res_0207\Annotation_39_Class.txt"
OriginSource_ImageListPath  = r"D:\PyCharm\Res_0207\39_Class_ImgList.txt"

OriginSource_AnalysisPath   = r"C:\PythonHN\Data\Res1107\ImageSize_Analysis_Source.txt"

Result_Dir_Path             = r"H:\39class_attribute\4_dataset\스마트어린이집\2021_스마트어린이집\3rd_test"

Abbreviated_Img_Path        = r"C:\PythonHN\Data\ABB TEST\condition_common_img"   # 축약시킨 이미지 들어있는 폴더
RealExistCheck_Path         = r""

Pre_Search_Remember_Path    = r"H:/39class_attribute/4_dataset/스마트어린이집/2021_스마트어린이집"


CORE_ENCODING_FORMAT    = 'utf-8'                       # 파일 Read 할 때, 인코딩 포맷
VALID_IMG_FORMAT        = ['.jpg', '.png', '.jpeg']     # Img 유효한 확장자
CORE_FILTER_CONDITION   = '(Attribute[0] == "1") and (Attribute[5] == "1") and ((Attribute[7] == "1") or (Attribute[10] == "1"))'
CUR_ZIP_CLASS_XLSX      = r"ClassData\24Class.xlsx"


CORE_SIZE_FILTER_DICT   =   {   'common':
                                    {
                                        'isCheck'   : False,
                                        'CheckSize' : False,    # Size(True) / Width&Height(False)
                                        'Width'     : 0,
                                        'Height'    : 0,
                                        'Size'      : 0
                                    },
                                'head':
                                    {
                                        'isCheck'   : False,
                                        'CheckSize' : False,
                                        'Width'     : 0,
                                        'Height'    : 0,
                                        'Size'      : 0
                                    },
                                'upper':
                                    {
                                        'isCheck'   : False,
                                        'CheckSize' : False,
                                        'Width'     : 0,
                                        'Height'    : 0,
                                        'Size'      : 0
                                    },
                                'lower':
                                    {
                                        'isCheck'   : False,
                                        'CheckSize' : False,
                                        'Width'     : 0,
                                        'Height'    : 0,
                                        'Size'      : 0
                                    },                                                        
                            }


COND_PASS = True
COND_FAIL = False

WIDTH     = 0
HEIGHT    = 1

CORE_LINK_DICT  = {}
LINK_NAME_LIST  = 0
CORE_SAVE_VALUE = 1


def setCoreValue(CoreName, Value):
    globals()[CoreName] = Value

def getCoreValue(CoreName):
    return globals()[CoreName]

def getZipClassNum() -> int:
    classNumCP  = re.compile('[0-9]+')
    classNum    = classNumCP.search(CUR_ZIP_CLASS_XLSX)
    return int(classNum.group())
