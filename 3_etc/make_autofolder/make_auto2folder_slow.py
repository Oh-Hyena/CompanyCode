# 상위폴더 + 하위폴더 한꺼번에 만들어줌 (대신 속도가 느림)

import os
import shutil

targetDir = r"E:\test\video"
resultDir = r"E:\test\result"


file_list = []
one_findname_list = []
two_findname_list = []
for (path, dir, files) in os.walk(targetDir):
    for each in files:
        if each.endswith(".mp4"):   
            file_list.append(each)
            
            one_findname = each.split("_")[0]
            one_findname = one_findname[:2]
            one_findname_list.append(one_findname)
            
            two_findname = each.split(")")[1]
            two_findname = two_findname[:2]
            two_findname_list.append(two_findname)
            

for file_each in file_list:
    for one_each in one_findname_list:
        if one_each in file_each:
            resultPath = os.path.join(resultDir, one_each)
            resultPath = os.path.normpath(resultPath)
            os.makedirs(resultPath, exist_ok=True)
            
            for two_each in two_findname_list:
                if two_each in file_each:
                    two_resultPath = os.path.join(resultPath, two_each)
                    two_resultPath = os.path.normpath(two_resultPath)
                    os.makedirs(two_resultPath, exist_ok=True)
                    shutil.copy(os.path.join(targetDir, file_each), os.path.join(two_resultPath, file_each))
print("done")