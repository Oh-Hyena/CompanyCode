# 검색 and 선별(att(X)) 용 함수화한 코드

import os

folderDir = r"F:\39class_attribute\4_dataset\seongnamfalse\2022\0429\seongnam0429_img"
resultDir = r"F:\39class_attribute\4_dataset\seongnamfalse\2022\0429\img_count\1_img"

# resultDir 만들기
def makeResultDir():
    if not os.path.exists(resultDir):
        os.makedirs(resultDir, exist_ok=True)


# 폴더마다 이미지 장수 count해서 list에 append하기
def countFiles(folderDir):
    global attName, attsaveName, resultName
    folderCountList = []
    filesCount = 0
    for root, dirs, files in os.walk(folderDir):
        folderName = root.split('\\')[-1]
        if 'att' in folderName:
            attName     = folderName.split("_")[0]
            attsaveName = folderName.split("_")[1]
        else:            
            resultName = folderName.split("_")[0]
        
        folderCountList.append(f'{folderName} : {len(files)}')
        filesCount += len(files)
        
    return folderName, folderCountList, filesCount


# list가져와서 txt 파일에 입력하기
def writeCountFiles(resultDir, folderName, folderCountList, filesCount):
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


if __name__ == "__main__":
    makeResultDir()
    folderName, folderCountList, filesCount = countFiles(folderDir)
    writeCountFiles(resultDir, folderName, folderCountList, filesCount)