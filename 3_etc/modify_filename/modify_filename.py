import os


folderDir = r"G:\ai_hub\CCTV_추적_영상\잡상인\cctv_merchant3\cctv_merchant3_origin"

# originImgList 만들기
def make_originList(folderDir):
    originImgList = []
    for root, dirs, files in os.walk(folderDir):
        for file in files:
            originImgList.append([root, file]) 
            
    return originImgList
        
# imgName 변경하기
def modify_filename(originImgList):
    count = 0
    for each in originImgList:
        src = os.path.join(each[0], each[1])
        dst = os.path.join(each[0], f'{count}_{each[1]}')
        os.renames(src, dst)
        count += 1


if __name__ == "__main__": 
    originImgList = make_originList(folderDir)
    modify_filename(originImgList)