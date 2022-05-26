# Import Packages and Modules
# Standard Library
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
import json
import xml.etree.ElementTree as ET
import os
import pickle
import sys
import datetime

# Installed Library - CV
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
import cv2

# Add Import Path
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../Core'))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../'))

# Custom Modules
# python -m PyQt6.uic.pyuic -x main.ui -o ui_main.py
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
from Core.general_function  import RunFunctionLog, callername, filename, funcname  # General Function Anyware use it
from Core.send_argv         import SendArgvClass

# Current RunFunction Result Directory
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
ResultDir = r'D:/ResultSave_AI'


if __name__ == "__main__":
    RunFunctionLog()
    print("==============================================================================")
    for i, arg in enumerate(sys.argv[1:]):
        print(f"\t[{i}] _ {arg.split('$$$')[0]:20} _ {arg.split('$$$')[-1]:20}")
    print("==============================================================================")

    print("filename : ", filename())
    print("funcname : ", funcname())
    print("__name__ : ", __name__)
    print("__file__ : ", __file__)