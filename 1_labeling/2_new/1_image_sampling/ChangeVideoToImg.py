import os
import sys
import cv2


videoDir        = r"D:\0627\seongnam20200330_falldown_video"
resDir          = r"D:\0627\seongnam20200330_falldown_img"

ENCODING_FORMAT = "UTF-8"
resFolderName   = "seongnam20200330_falldown"
fileNum         = 10


def checkInitDirValid():
    if os.path.isdir(videoDir) is False:
        print(f'[Error] {videoDir} is invalid')
        return False
    if os.path.isdir(resDir) is False:
        print(f'[Error] {resDir} is invalid')
        return False
    return True


def makeChangeResDir(resDir):
    if not os.path.isdir(resDir):
        os.makedirs(resDir, exist_ok=True)


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


def imwrite(filename, img, params=None):
    try:
        ext       = os.path.splitext(filename)[1]
        result, n = cv2.imencode(ext, img, params)

        if result:
             with open(filename, mode='w+b') as f:
                 n.tofile(f)
             return True
        else:
             return False
         
    except Exception as e:
        print(f"imwrite error : {e}")
        return False


def VideoToImg():
    folderCount  = 1
    fileCount    = 1
    
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
                
                fileCount  += 1
                
                if fileCount == fileNum + 1:
                      folderCount += 1
                      fileCount    = 1
                      
            capture.release()
            
               
if __name__ == "__main__":
    makeChangeResDir(resDir)
    
    if checkInitDirValid() is False:
        sys.exit(-1)
    
    VideoToImg()