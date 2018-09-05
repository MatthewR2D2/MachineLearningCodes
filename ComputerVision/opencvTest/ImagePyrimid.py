# -*- coding: utf-8 -*-
"""
Created on Thu Aug 16 08:16:10 2018
@author: Matthew Millar
What it does:
What it needs:
Related Classes:

"""

import cv2
import numpy as np
from matplotlib import pyplot as plt

img =cv2.imread("D:/Tests/opencvTest/images/batman.jpg", 0)

lower = img

for i in range(3):
    #return lower res image
    lower = cv2.pyrDown(lower)
    cv2.imshow("Lower Res", lower)
    k = cv2.waitKey(0) #ESC key
    if k == 27:
        continue
    
upper = lower

for i in range(3):
    #return higher res of a image
    upper = cv2.pyrUp(upper)
    cv2.imshow("Upper Res", upper)
    k = cv2.waitKey(0) #ESC key
    if k == 27:
        continue

cv2.destroyAllWindows()
    
    
    