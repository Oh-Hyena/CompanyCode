import os
import sys
import cv2


videoDir        = r"E:\sampling_test\seongnamfalse0211_video"
resDir          = r"E:\sampling_test\seongnamfalse0211_img3"

ENCODING_FORMAT = "UTF-8"
resFolderName   = "seongnamfalse0211"
fileNum         = 10


def checkInitDirValid():
    if os.path.isdir(videoDir) is False:
        print(f'[Error] {videoDir} is invalid')
        return False
    if os.path.isdir(resDir) is False:
        print(f'[Error] {resDir} is invalid')
        return False
    return True


def numCount(length, num):
    rotate = length - len(num)
    if rotate > 0:
        for i in range(rotate):
            num = "0" + num
    return num 


def makeEachDestDir(Count):  
    folderName = resFolderName + "_" + numCount(6, str(Count))
    DestDir = os.path.join(resDir, folderName)
    os.makedirs(DestDir, exist_ok=True)
    
    return folderName, DestDir


def VideoToImg():
    folderCount  = 1
    fileCount    = 1
    totalCount   = 0
    imgCountList = []
    
    videoList = os.listdir(videoDir)
        
    for video in videoList:
        if video.endswith(".mp4"):
            folderName, DestDir = makeEachDestDir(folderCount)
                
            print(f"[ 실행 ] {video}")
                
            capture = cv2.VideoCapture(os.path.join(videoDir, video))
            length  = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))  # 동영상 길이
            frame   = -1
            
            countNum = length / fileNum 
            
            while(capture.isOpened()):
                ret, img = capture.read()
                frame += 1
                
                if not ret: break
                if not frame%countNum < 1: continue
                
                fileName = "_" + numCount(6, str(fileCount)) + ".jpg"
                cv2.imwrite(os.path.join(DestDir, folderName + fileName), img)
                
                totalCount  = fileCount
                fileCount  += 1
                
                if fileCount == fileNum + 1:
                      folderCount += 1
                      fileCount    = 1
                      
            print(f"[ 완료 ] {folderName} -> {totalCount}")
            print()
            imgCountList.append(f"{folderName} : {totalCount}")
            
            capture.release()
            
    return imgCountList


def writeImgCount(imgCountList):
    resPath = os.path.join(resDir, resFolderName + ".txt")
    with open(resPath, 'w', encoding=ENCODING_FORMAT) as f:
        for imgCount in imgCountList:
            f.write(f"{imgCount}\n")

               
if __name__ == "__main__":
    if checkInitDirValid() is False:
        sys.exit(-1)
    
    imgCountList = VideoToImg()
    writeImgCount(imgCountList)