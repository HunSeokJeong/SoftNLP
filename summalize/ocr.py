# -*- coding: utf-8 -*-
"""
Created on Sat May 14 22:37:10 2022

@author: gnstjr
"""

import cv2
#pip install git+https://github.com/haven-jeon/PyKoSpacing.git
#pip install tensorflow 2.5.3(python 3.10이면 버전 낮춰야 함)
from pykospacing import Spacing

import os 
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'#텐서플로우 오류 제거용

import pytesseract
pytesseract.pytesseract.tesseract_cmd = R'C:\Program Files\Tesseract-OCR\tesseract'

# Define config parameters.
# '-l eng'  for using the English language
# '--oem 1' sets the OCR Engine Mode to LSTM only.

#config = ('-l kor --oem 1 --psm 3')

#config 설명

# -l <사용언어>
# #OCR Engine modes(–oem):
# 0 - Legacy engine only.
# 1 - Neural nets LSTM engine only.
# 2 - Legacy + LSTM engines.
# 3 - Default, based on what is available.
# Page segmentation modes(–psm):
# 0 - Orientation and script detection (OSD) only.
# 1 - Automatic page segmentation with OSD.
# 2 - Automatic page segmentation, but no OSD, or OCR.
# 3 - Fully automatic page segmentation, but no OSD. (Default)
# 4 - Assume a single column of text of variable sizes.
# 5 - Assume a single uniform block of vertically aligned text.
# 6 - Assume a single uniform block of text.
# 7 - Treat the image as a single text line.
# 8 - Treat the image as a single word.
# 9 - Treat the image as a single word in a circle.
# 10 - Treat the image as a single character.
# 11 - Sparse text. Find as much text as possible in no particular order.
# 12 - Sparse text with OSD.
# 13 - Raw line. Treat the image as a single text line, bypassing hacks that are Tesseract-specific.
def ocr_read(imPath):
    config = ('-l kor --oem 3 --psm 4')
    # Read image from disk
    #img = cv2.imread(imPath, cv2.IMREAD_COLOR)
    img_gray = cv2.imread(imPath, cv2.COLOR_BGR2GRAY)
    img_gray = cv2.imread(imPath, cv2.IMREAD_GRAYSCALE)
    string=pytesseract.image_to_string(img_gray, config=config)
    #띄어쓰기
    spacing = Spacing()
    no_space_string=string.replace(" ","").replace("\n","")
    newstring = spacing(no_space_string) 
    return newstring

#참고한 사이트 https://ddolcat.tistory.com/954