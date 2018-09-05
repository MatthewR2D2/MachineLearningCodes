# -*- coding: utf-8 -*-
"""
Created on Thu Aug 16 09:39:52 2018
@author: Matthew Millar
What it does:
What it needs:
Related Classes:

"""

import cv2
import numpy as np
from matplotlib import pyplot as plt

frame =cv2.imread("D:/Tests/opencvTest/images/shapes.jpg")

#frame = cv2.resize(frame, (640,480)) #If the image is very large
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#Applied to find foreground and background of image
#Find binary image
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

#Apply closing process
kernel = np.ones((1,1), np.uint8)
closing = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations = 4)

#This gets the countours
closing_img = closing.copy()
im2 , contours, hierarchy = cv2.findContours(closing_img,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

fourcc = cv2.VideoWriter_fourcc(*"XVID")
out = cv2.VideoWriter('output.mp4',fourcc, 30.0, (440,360))

for cnt in contours:
    area = cv2.contourArea(cnt) #Find the coutour area
    
    if area < 100:
        continue
    print(area)
    
    ellipse = cv2.fitEllipse(cnt)
    cv2.ellipse(frame, ellipse, (0,255,0),2) #Draw the ellipse over the frame
    
cv2.imshow("Morphological", closing)
cv2.imshow("Adaptive", thresh)
cv2.imshow("Contours", frame)

k = cv2.waitKey(0) #ESC key
if k == 27:
    cv2.destroyAllWindows()

