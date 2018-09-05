# -*- coding: utf-8 -*-
"""
Created on Mon Aug 20 09:14:00 2018
@author: Matthew Millar
What it does:
What it needs:
Related Classes:

"""

import cv2
import numpy as np

img = cv2.imread("D:/Tests/opencvTest/images/shapes.jpg",0)
gray = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

edges =cv2.Canny(gray, 50, 150, apertureSize = 3)
rho = 1            #Distance resolution in pixels of the Hough grid
theta = np.pi/180  #Angular resolution in radians
threshold = 15     #Minimum Number of votes
minLineLenght = 20 #Minum number of pixele making up a line
maxLineGap = 10    #Maximum gap in pixels between connnected lines
lines = cv2.HoughLinesP(image=edges,rho=0.02,theta=np.pi/500, 
                        threshold=10,
                        lines=np.array([]),
                        minLineLength=minLineLenght,
                        maxLineGap=maxLineGap)

for line in lines:
    for x1,y1,x2,y2 in line:
        cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)

    
    


cv2.imshow('result', img)

cv2.waitKey(0)
cv2.destroyAllWindows()