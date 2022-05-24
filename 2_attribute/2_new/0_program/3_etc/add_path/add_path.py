import os
import shutil

# targetDir = r'/home/unicomnet/docker/Unicardataset_2class_add_dataset/train_dataset'
# targetDir = r'/home/unicomnet/docker/Unicardataset_6class_to_2class_dataset/train_dataset'
targetDir = r'/home/unicomnet/docker/falldown'
imgListFilePath = r'/home/unicomnet/docker/0112_unicar2class_v17_0001/train_list.txt'
# resultMoveDir = r'C:\Users\user\Desktop\add_path\resultImgMove'
resultAddPath_FilePath = targetDir + r'/add_path_img_list.txt'


OriginalDict = {}
for root, dirs, files in os.walk(targetDir):
    for file in files:
        OriginalDict[file] = root


imgNameList = []
with open(imgListFilePath, 'r', encoding='utf8') as f:
    for eachLine in f:
        eachLine = eachLine.strip('\n')
        imgNameList.append(eachLine)


txtNameList = []
with open(imgListFilePath, 'r', encoding='utf8') as f:
    for eachLine in f:
        eachLine = eachLine.split('.')[0]
        eachLine = eachLine + '.txt'
        eachLine = eachLine.strip('\n')
        txtNameList.append(eachLine)


addPathList = []
moveImgList = []
for eachImg in imgNameList:
    validRoot = OriginalDict.get(eachImg)
    if validRoot is not None:
        # addPathList -> 이미지가 있는 경로만 append / moveImgList -> 이미지와 이미지가 있는 경로 append
        addPathList.append(os.path.join(validRoot, eachImg))
        moveImgList.append([os.path.join(OriginalDict[eachImg], eachImg), eachImg])


moveTxtList = []
for eachTxt in txtNameList:
    validRoot = OriginalDict.get(eachTxt)
    if validRoot is not None:
        # moveTxtList -> txt 파일과 txt 파일이 있는 경로 append
        moveTxtList.append([os.path.join(OriginalDict[eachTxt], eachTxt), eachTxt])


# for eachMoveImg in moveImgList:
#     # eachMoveImg[0] -> move 할 img path / eachMoveImg[1] -> move 할 img name
#     savePath = os.path.join(resultMoveDir, eachMoveImg[1])
#     try :
#         shutil.move(eachMoveImg[0], savePath)
#     except Exception as e:
#         print(e)


# for eachMoveTxt in moveTxtList:
#     # eachMoveTxt[0] -> move 할 txt path / eachMoveTxt[1] -> move 할 txt name
#     savePath = os.path.join(resultMoveDir, eachMoveTxt[1])
#     try :
#         shutil.move(eachMoveTxt[0], savePath)
#     except Exception as e:
#         print(e)


with open(resultAddPath_FilePath, 'w', encoding='utf8') as f:
    for each in addPathList:
        f.write(f"{each}\n")





