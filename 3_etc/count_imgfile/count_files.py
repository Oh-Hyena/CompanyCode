# 선별(att(X)) 용

import os

folderDir = r"E:\hyena\3_dataset\seongnamfalse\2021\1112\seongnamfalse1112\seongnamfalse1112_img"
resultDir = r"E:\test\count_file\img_count"


# resultDir 만들기
if not os.path.exists(resultDir):
    os.makedirs(resultDir, exist_ok=True)


# 폴더마다 이미지 장수 count해서 list에 append하기
folderCountList = []
for root, dirs, files in os.walk(folderDir):
    folderName = root.split('\\')[-1]
    resultName = folderName.split("_")[0]
    folderCountList.append(f'{folderName} : {len(files)}')


# list가져와서 txt 파일에 입력하기
savePath = os.path.join(resultDir, f'{resultName}_img.txt')
with open(savePath, 'w', encoding='utf8') as f:
    del folderCountList[0]
    for each in folderCountList:
        f.write(f'{each}\n')

