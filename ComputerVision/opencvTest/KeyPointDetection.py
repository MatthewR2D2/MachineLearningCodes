# -*- coding: utf-8 -*-
"""
Created on Thu Aug 16 08:44:41 2018
@author: Matthew Millar
What it does:
What it needs:
Related Classes:

"""

import cv2
import numpy as np
from matplotlib import pyplot as plt

img =cv2.imread("D:/Tests/opencvTest/images/batman.jpg")

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#Used for corner detection
#SIFT used to fix that scaling invariant keypoints
#spatial point of a image or what are distiguishing feature points
#Find keypoints
sift = cv2.xfeatures2d.SIFT_create()
kp = sift.detect(gray, None)

img = cv2.drawKeypoints(gray, kp, img)

cv2.imshow("KeyPoints", img)
k = cv2.waitKey(0) #ESC key
if k == 27:
    cv2.destroyAllWindows()