# 검색(att) 용

import os

folderDir = r"E:\test\count_file\att_seongnamfalse1112_500_img"
resultDir = r"E:\test\count_file\img_count"


# resultDir 만들기
if not os.path.exists(resultDir):
    os.makedirs(resultDir, exist_ok=True)


# 폴더마다 이미지 장수 count해서 list에 append하기
folderCountList = []
for root, dirs, files in os.walk(folderDir):
    folderName  = root.split('\\')[-1]
    attName     = folderName.split("_")[0]
    attsaveName = folderName.split("_")[1]
    folderCountList.append(f'{folderName} : {len(files)}')


# list가져와서 txt 파일에 입력하기
attSavePath = os.path.join(resultDir, f'{attName}_{attsaveName}_img.txt')
with open(attSavePath, 'w', encoding='utf8') as f:
    del folderCountList[0]
    for each in folderCountList:
        f.write(f'{each}\n')
