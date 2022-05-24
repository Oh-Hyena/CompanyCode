# 상위폴더만 만들어줌

import os
import shutil

targetDir = r"E:\hyena\3_dataset\seongnamfalse\2021\1112\seongnamfalse1112\seongnamfalse1112_video"
resultDir = r"E:\test"

# find_name = ["분당", "수정", "중원"]

file_list = []
find_name_list = []
for (path, dir, files) in os.walk(targetDir):
    for each in files:
        if each.endswith(".mp4"):   
            file_list.append(each)
            findname = each.split("_")[0]
            # findname = each.split(")")[1]
            findname = findname[:2]
            find_name_list.append(findname)


copy_list = []
for each in file_list:
    for each2 in find_name_list:
        if each2 in each:
            resultPath = os.path.join(resultDir, each2)
            resultPath = os.path.normpath(resultPath)
            os.makedirs(resultPath, exist_ok=True)
            shutil.copy(os.path.join(targetDir, each), os.path.join(resultPath, each))
print("done")

