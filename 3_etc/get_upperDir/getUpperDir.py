import os

imgDir = r'E:\attTest\0704\img'
fileName = 'seongnamfalse0125'

imgCountList = []
for root, dirs, files in os.walk(imgDir):
    if fileName in root:
        imgCountList.append(f'{os.path.basename(root)} : {len(files)}')

savePath      = os.path.join(imgDir,'../')
saveNormPath  = os.path.normpath(savePath)
saveFileName  = fileName + '.txt'

saveTotalPath = os.path.join(saveNormPath, saveFileName)

with open(saveTotalPath, 'w', encoding='utf-8') as f:
    for each in imgCountList:
        f.write(f'{each}\n')