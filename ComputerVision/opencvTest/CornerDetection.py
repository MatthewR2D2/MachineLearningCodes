# -*- coding: utf-8 -*-
"""
Created on Thu Aug 16 08:22:52 2018
@author: Matthew Millar
What it does:
What it needs:
Related Classes:

"""

import cv2
import numpy as np
from matplotlib import pyplot as plt

img =cv2.imread("D:/Tests/opencvTest/images/chess.jpg")

betterAlgoImg = img
#Convert to gray scale image
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = np.float32(gray) #Convert to an float 32

dst = cv2.cornerHarris(gray,2,3,0.04)
dst = cv2.dilate(dst,None)
#Chnage some color points with red for edges in red
img[dst>dst.max()/5] = [0,0,255]

cv2.imshow("DST", img)
k = cv2.waitKey(0) #ESC key
if k == 27:
    cv2.destroyAllWindows()
    
#Define numberof corners accuracy and sort by quality
corners = cv2.goodFeaturesToTrack(gray,25,0.01,10)
corners = np.int0(corners)

#Show all corner points on the original image
for i in corners:
    x,y = i.ravel()
    cv2.circle(betterAlgoImg, (x,y),3,(0,0,255),3)
    
cv2.imshow("Better Algo", img)
k = cv2.waitKey(0) #ESC key
if k == 27:
    cv2.destroyAllWindows()