import os
import sys
import cv2


videoDir        = r"E:\0610\seongnamfalse0125_video"
resDir          = r"E:\0610\0620"

ENCODING_FORMAT = "UTF-8"
resFolderName   = "seongnamfalse0125"
fileNum         = 10


class ChangeVideoToImgClass:
    def __init__(self):
        self.videoList = []
    
    
    def checkInitDirValid(self):
        if os.path.isdir(videoDir) is False:
            print(f'[Error] {videoDir} is invalid')
            return False
        if os.path.isdir(resDir) is False:
            print(f'[Error] {resDir} is invalid')
            return False
        return True
    
    
    def makeChangeResDir(self, Dir):
        if not os.path.isdir(Dir):
            os.makedirs(Dir, exist_ok=True)
    
    
    def makeEachDestDir(self, Count):  
        self.folderName = resFolderName + "_" + str(Count).zfill(6)
        self.DestDir    = os.path.join(resDir, self.folderName)
        os.makedirs(self.DestDir, exist_ok=True)
        
    
    def imwrite(self, filename, img, params=None):
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
    
    
    def ChangeVideoToImg(self):
        folderCount  = 1
        fileCount    = 1
        
        self.videoList = os.listdir(videoDir)
            
        for video in self.videoList:
            if video.endswith(".mp4"):
                self.makeEachDestDir(folderCount)
                    
                print(f"[ {str(folderCount).zfill(3)} ] {video}")
                    
                capture = cv2.VideoCapture(os.path.join(videoDir, video))
                length  = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))  # 동영상 길이
                frame   = -1
                
                countNum = length / fileNum 
                
                while(capture.isOpened()):
                    ret, img = capture.read()
                    frame += 1
                    
                    if not ret: break
                    if not frame % countNum < 1: continue
                    
                    fileName = "_" + str(fileCount).zfill(6) + ".jpg"
                    cv2.imwrite(os.path.join(self.DestDir, self.folderName + fileName), img)
                    
                    fileCount  += 1
                    
                    if fileCount == fileNum + 1:
                        folderCount += 1
                        fileCount    = 1
                        
                capture.release()
    
    
    def run(self):
        if self.checkInitDirValid() is False:
            sys.exit(-1)
        self.makeChangeResDir(resDir)
        self.ChangeVideoToImg()
    
    

if __name__ == "__main__":
    program = ChangeVideoToImgClass()
    program.run()



            
               
