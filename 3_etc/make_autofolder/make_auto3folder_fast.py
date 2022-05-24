import os
import shutil

targetDir = r"E:\hyena\3_dataset\seongnamfalse\2021\1112\seongnamfalse1112\seongnamfalse1112_video"
resultDir = r"E:\test\auto\save"


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


for one_each, two_each in zip(one_findname_list, two_findname_list):
    for file_each in file_list:
        if one_each and two_each in file_each:
            one_resultPath = os.path.join(resultDir, one_each)
            one_resultPath = os.path.normpath(one_resultPath)
            os.makedirs(one_resultPath, exist_ok=True)
            two_resultPath = os.path.join(one_resultPath, two_each)
            two_resultPath = os.path.normpath(two_resultPath)
            os.makedirs(two_resultPath, exist_ok=True)
            shutil.copy(os.path.join(targetDir, file_each), os.path.join(two_resultPath, file_each))
print("done")