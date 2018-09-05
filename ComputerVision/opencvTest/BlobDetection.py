# -*- coding: utf-8 -*-
"""
Created on Fri Aug 17 08:19:52 2018
@author: Matthew Millar
What it does:
What it needs:
Related Classes:

"""

import numpy as np
import cv2

params =cv2.SimpleBlobDetector_Params()
#params.filterByArea = True
#params.maxArea= 100
#params.filterByCircularity= True #How close to a cirecle it is
#params.maxCircularity= 0.1

detector = cv2.SimpleBlobDetector_create(params)

img =cv2.imread("D:/Tests/opencvTest/images/shapes.jpg")

keypoints = detector.detect(img)
imWithKeypoints = cv2.drawKeypoints(img, keypoints, np.array([]),(0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

cv2.imshow("Blobs", imWithKeypoints)


k = cv2.waitKey(0) #ESC key
if k == 27:
    cv2.destroyAllWindows()
