# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 14:28:34 2019

@author: kth
"""

"""
purpose : 동영상을 이미지화시키는 코드 (30초 영상을 150장으로 나눔)
input   : 원본 동영상 파일
output  : 샘플링한 이미지 파일

-newListing.py : 1624_x_202004158_160830_00001.jpg
-listing.py : seongnamfalse0430_00001_00001.jpg
"""

import os
import cv2
import shutil
import numpy as np

# 원본 동영상이 있는 폴더 경로
videopath = r"D:\HN_code\test\1_labeling\1_listing\seongnamfalse1111_video"

# 샘플링한 이미지를 저장할 폴더 경로
targetpath = r"D:\HN_code\test\1_labeling\1_listing\seongnamfalse1111_img"

# 저장될 이미지 폴더 이름(seongnamfalse0430_00001_00001.jpg) 중 class 부분
videoclass = "seongnamfalse1111"
# 저장될 이미지 폴더 이름(seongnamfalse0430_00001_00001.jpg) 중 번호 부분
videonumber = 1

# 교통약자  : 1, 2, 3, 4, 5, 6, 7, 8
# 비정형도로 : 1, 2, 3, 4, 5, 8
# 사회적약자 : 1, 2_100, 2_나머지, 3, 4, 5, 6, 8
# 스쿨존    : 1, 2, 3, 4, 5, 6, 7, 8

mode = "jpg"

# 몇 장씩 뽑을 것인지 설정하기 (동영상 초수 * 5 = 30초 * 5 = 150장)
COUNT = 150

# 이름 생성 함수
def naming(length, name):
    if int(length) == 5:
        if len(name) == 1:
            return "0000"+name
        elif len(name) == 2:
            return "000"+name
        elif len(name) == 3:
            return "00" + name
        elif len(name) == 4:
            return "0" + name
        else:
            return name
    else:
        if len(name) == 1:
            return "00000"+name
        elif len(name) == 2:
            return "0000"+name
        elif len(name) == 3:
            return "000" + name
        elif len(name) == 4:
            return "00" + name
        elif len(name) == 5:
            return "0" + name
        else:
            return name

# Python에서 OpenCV를 사용하면 한글(유니코드)를 처리하지 못 해 문제가 발생할 수 있으므로, imdecode 함수를 사용하여 문제를 해결한다.
# 이미지 읽기 함수
def imread(filename, flags=cv2.IMREAD_COLOR, dtype=np.uint8):
    try:
        n = np.fromfile(filename, dtype)
        img = cv2.imdecode(n, flags)
        return img
    except Exception as e:
        print(e)
        return None

# 이미지 저장하기 함수
def imwrite(filename, img, params=None):
    try:
        ext = os.path.splitext(filename)[1]
        result, n = cv2.imencode(ext, img, params)
        if result:
            with open(filename, mode='w+b') as f:
                n.tofile(f)
            return True
        else:
            return False
    except Exception as e:
            print(e)
            return False

# 동영상을 이미지화시키는 샘플링 함수 (30초 동영상 -> 150장 이미지)
def sampling():
    if not os.path.isdir(targetpath):
        os.mkdir(targetpath)
    
    videolist = os.listdir(videopath)

    for index, video in enumerate(videolist):
        videoname, videoext = os.path.splitext(video)
        if not videoext == ".mp4" and not videoext == ".avi":
            continue
        
        videodir = os.path.join(targetpath, videoclass + "_" + naming(6, str(index+videonumber)))
        os.mkdir(videodir)
        
        shutil.copyfile(os.path.join(videopath, video),"temptemptemp")
        cap = cv2.VideoCapture("temptemptemp")
        length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        frame = -1
        cwd = os.getcwd()
    
        # f = open(os.path.join(videodir,"videoname.txt"), "w")
        # f.write(video)
        # f.write(",")
        # f.write(str(index+videonumber))
        # f.close()
        
        aaa = length / COUNT #######샘플링하고싶은 수. 현재는 150장.
    
        fileCount = 1
        
        objWd = videodir
        while(cap.isOpened()):
            ret, im = cap.read()
            frame += 1
            if not ret:
                break
            if not frame%aaa < 1:
                continue
            
            if not objWd == os.getcwd():
                os.chdir(objWd)

            if mode == "jpg":
                cv2.imwrite("temp."+mode, im)
                os.rename("temp."+mode, os.path.join(videoclass + "_" + naming(6, str(index+videonumber))+"_"+naming(5, str(fileCount))+"."+mode))
            else:           
                cv2.imwrite("temp."+mode, im,  [cv2.IMWRITE_PNG_COMPRESSION, 1])
                os.rename("temp."+mode, os.path.join(videoclass + "_" + naming(6, str(index+videonumber))+"_"+naming(5, str(fileCount))+"."+mode))
                
            fileCount += 1

        cap.release()
        os.chdir(cwd)
        os.remove("temptemptemp")
        
        print("{} ".format(videoclass + "_"+str(naming(6, str(index+videonumber)))+" 완료"))

    print("end")
    
sampling()
print("!")

# while True:
#     pass





