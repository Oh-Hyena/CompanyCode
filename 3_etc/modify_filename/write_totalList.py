# 중복 이미지 없는지 확인하는 코드

import os


folderDir = r"G:\ai_hub\CCTV_추적_영상\잡상인\cctv_merchant3\cctv_merchant3_origin"


# 전체 파일 root+file list 만들기
def make_rootList(folderDir):
    rootList = []
    for root, dirs, files in os.walk(folderDir):
        for file in files:
            rootList.append(os.path.join(root, file))
    
    return rootList

# root_file list 출력하기
def write_totalList(rootList):
    savePath = os.path.join(folderDir, "totalList.txt")
    with open(savePath, 'w', encoding='utf8') as f:
        for each in rootList:
            f.write(f'{each}\n')


if __name__ == "__main__": 
    rootList = make_rootList(folderDir)
    write_totalList(rootList)