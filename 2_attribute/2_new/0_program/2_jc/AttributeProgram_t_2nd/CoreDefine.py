TITLE   = 'Attribute Program'
DATE    = '2022-03-11'
VERSION = '1.1.0'
IDE     = 'Visual Studio Code 1.62.0'
OS      = 'Windows 10'
AUTHOR  = 'OH HYENA'


ERROR_STRICT_HARD = 0
ERROR_STRICT_SOFT = 1


CORE_SHOW_LOG       = True              # 터미널 창에 로그가 나오게 하는지 총괄하는 시스템 변수
CORE_TEST_MODE      = False
CORE_ERROR_STRICT   = ERROR_STRICT_SOFT # 에러 발생 시, 처리 정도를 결정하는 시스템 변수


import sys


CrushedImgFileName          = 'CrushImg.txt'

OriginSource_cvatXml_Path   = r"H:\39class_attribute\4_dataset\seongnamfalse\2022\0125\seongnam0125\att_seongnam0125_500_xml\30"
OriginSource_Img_Path       = r"H:\39class_attribute\4_dataset\seongnamfalse\2022\0125\seongnam0125\att_seongnam0125_500_img\30"

OriginSource_AnntationPath  = r"C:\Users\Unicomnet\Desktop\3rd_val_test_dataset\1216_make_val_test_dataset\4_oldperson\ConditionFilter_Annotation.txt"
OriginSource_ImageListPath  = r"C:\Users\Unicomnet\Desktop\3rd_val_test_dataset\1216_make_val_test_dataset\4_oldperson\ConditionFilter_ImgList.txt"

OriginSource_AnalysisPath   = r"C:\PythonHN\Data\Res1107\ImageSize_Analysis_Source.txt"

Result_Dir_Path             = r"H:\39class_attribute\4_dataset\seongnamfalse\2022\0125\seongnam0125\make_class\30"

Abbreviated_Img_Path        = r"C:\PythonHN\Data\ABB TEST\condition_common_img"   # 축약시킨 이미지 들어있는 폴더
RealExistCheck_Path         = r""

Pre_Search_Remember_Path    = r"H:/39class_attribute/4_dataset/seongnamfalse/2022/0125/seongnam0125/make_class"


CORE_ENCODING_FORMAT    = 'utf-8' 
VALID_IMG_FORMAT        = ['.jpg', '.png', '.jpeg'] 
CORE_FILTER_CONDITION   = '(Attribute[1] == "1")'


# SIZE_FILTER_DICT
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
