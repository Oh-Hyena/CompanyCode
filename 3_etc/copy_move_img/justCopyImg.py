import os
import shutil

srcDir = r'H:\seongnamfalse\2021\1112\seongnam_oldperson1112\labeling\seongnam_oldperson1112_img'
dstDir = r'C:\Users\Unicomnet\Desktop\new\seongnam_oldperson1112'

for root, dirs, files in os.walk(srcDir):
    for file in files:
        shutil.copy(os.path.join(root, file), os.path.join(dstDir, file))