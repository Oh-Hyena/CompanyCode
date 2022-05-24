import os
import shutil
import glob


mergeDir = r"E:\test\merge_test"
annotaionSaveDir = r"E:\test\merge_test\save\annotation"
imglistSaveDir = r'E:\test\merge_test\save\imglist'

findTxt = ["annotation", "ImgList"]


# 상위폴더에서 findTxt 문자열이 들어가는 파일을 찾아 경로와 파일명 list 에 append 하기
annotationList = []
imglistList = []
for root, dirs, files in os.walk(mergeDir):
    for file in files :
        # 파일명에 있는 문자로 바꿔주기!
        if findTxt[0] in file:
            annotationList.append([os.path.join(root, file), file])
        else:
            imglistList.append([os.path.join(root, file), file])


# anno list를 읽어와서 anno save Dir에 중복되지 않게 숫자 붙여 복사하기
for idx, each in enumerate(annotationList):
    saveAnnotationPath = os.path.join(annotaionSaveDir, f"{idx+1}_{each[1]}")
    try:
        shutil.copy(each[0], os.path.join(annotaionSaveDir, f"{idx+1}_{each[1]}"))
    except Exception as e:
        print("move error : ", e)


# img list를 읽어와서 img save Dir에 중복되지 않게 숫자 붙여 복사하기
for idx, each in enumerate(imglistList):
    saveImglistPath = os.path.join(imglistSaveDir, f"{idx+1}_{each[1]}")
    try:
        shutil.copy(each[0], os.path.join(imglistSaveDir, f"{idx+1}_{each[1]}"))
    except Exception as e:
        print("move error : ", e)


# anno save Dir 에 있는 모든 txt 파일 가져와서 merge anno txt 파일에 붙여넣기
resultAnnotationPath = os.path.join(annotaionSaveDir, 'merge_annotation.txt')
readAnnotationFiles = glob.glob(os.path.join(annotaionSaveDir, '*.txt'))
with open(resultAnnotationPath, 'w', encoding='utf8') as f:
    # each : anno.txt 파일 경로
    for each in readAnnotationFiles:
        with open(each) as f2:
            # each2 : anno.txt 파일 내용
            for each2 in f2:
                each2 = each2.strip('\n')
                f.write(f"{each2}\n")


resultImglistPath = os.path.join(imglistSaveDir, 'merge_img_list.txt')
readImglistFiles = glob.glob(os.path.join(imglistSaveDir, '*.txt'))
with open(resultImglistPath, 'w', encoding='utf8') as f:
    for each in readImglistFiles:
        with open(each) as f2:
            for each2 in f2:
                each2 = each2.strip('\n')
                f.write(f"{each2}\n")