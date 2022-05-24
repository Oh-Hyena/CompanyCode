# 검색 and 선별(att(X)) 용

import os

folderDir = r"E:\hyena\3_dataset\seongnamfalse\2021\1112\seongnamfalse1112\att_seongnamfalse1112_500_img"
resultDir = r"E:\test\count_file\img_count"


# resultDir 만들기
if not os.path.exists(resultDir):
    os.makedirs(resultDir, exist_ok=True)


# 폴더마다 이미지 장수 count해서 list에 append하기
folderCountList = []
filesCount = 0
for root, dirs, files in os.walk(folderDir):
    folderName = root.split('\\')[-1]
    if 'att' in folderName:
        attName     = folderName.split("_")[0]
        attsaveName = folderName.split("_")[1]
    else:
        resultName  = folderName.split("_")[0]
    
    folderCountList.append(f'{folderName} : {len(files)}')
    filesCount += len(files)


# list가져와서 txt 파일에 입력하기
if 'att' in folderName:
    attSavePath = os.path.join(resultDir, f'{attName}_{attsaveName}_img.txt')
    with open(attSavePath, 'w', encoding='utf8') as f:
        del folderCountList[0]
        for each in folderCountList:
            f.write(f'{each}\n')
        f.write(f'\n총 이미지 장수 : {filesCount}')
else:
    savePath = os.path.join(resultDir, f'{resultName}_img.txt')
    with open(savePath, 'w', encoding='utf8') as f:
        del folderCountList[0]
        for each in folderCountList:
            f.write(f'{each}\n')
        f.write(f'\n총 이미지 장수 : {filesCount}')

