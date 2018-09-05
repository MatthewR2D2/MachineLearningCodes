# -*- coding: utf-8 -*-
"""
Created on Mon Aug 20 08:34:45 2018
@author: Matthew Millar
What it does:
What it needs:
Related Classes:

"""

import cv2
import numpy as np

img =cv2.imread("D:/Tests/opencvTest/images/shapes.jpg",0)
img = cv2.medianBlur(img, 5)
colorImg=cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

dp = 1
minDist = 10
circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,dp,minDist,
                            param1=50,param2=30,minRadius=0,maxRadius=300)

circles = np.uint(np.around(circles))

for i in circles[0,:]:
    cv2.circle(colorImg,(i[0],i[1]),i[2],(0,255,0),2)
    cv2.circle(colorImg,(i[0],i[1]),2,(0,0,255),3)
    
cv2.imshow("DetectedCircle", colorImg)
cv2.waitKey(0)
cv2.destroyAllWindows()