# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 13:49:50 2020

@author: kth
"""

import os
import shutil


cropedrootpath = r"G:\Dataset\train_dataset\Unicardataset_2class_add_dataset\legacy"
tasksrootpath = r"D:\p40_dataset\legacy\legacy_150upload"
taskname = "legacy_"    ## 언더바 넣어야함.
tasknumber = 1

fileext = ".jpg"


MAX = 150


def naming(length, name):
    name = str(name)
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
    elif int(length) == 4:
        if len(name) == 1:
            return "000"+name
        elif len(name) == 2:
            return "00"+name
        elif len(name) == 3:
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


if not os.path.isdir(os.path.join(tasksrootpath,taskname + naming(6,tasknumber) )):
    os.mkdir(os.path.join(tasksrootpath,taskname + naming(6,tasknumber) ))

filenumber = 1
for (path, dir, files) in os.walk(cropedrootpath):
        for filename in files:
            if filename.endswith(fileext):
                shutil.copy(os.path.join(path,filename), os.path.join(tasksrootpath,taskname + naming(6,tasknumber)))
                filenumber += 1
                if filenumber > MAX:
                    tasknumber += 1
                    filenumber = 1
                    os.mkdir(os.path.join(tasksrootpath,taskname + naming(6,tasknumber) ))
