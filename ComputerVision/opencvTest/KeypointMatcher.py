# -*- coding: utf-8 -*-
"""
Created on Thu Aug 16 09:01:38 2018
@author: Matthew Millar
What it does:
What it needs:
Related Classes:

"""

import cv2
import numpy as np
from matplotlib import pyplot as plt

img1 =cv2.imread("D:/Tests/opencvTest/images/batman2.jpg")
img2 =cv2.imread("D:/Tests/opencvTest/images/batman3.jpg")

gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

sift = cv2.xfeatures2d.SIFT_create()


# find the keypoints and descriptors with SIFT
kp1, des1 = sift.detectAndCompute(img1,None)
kp2, des2 = sift.detectAndCompute(img2,None)


## Create flann matcher
FLANN_INDEX_KDTREE = 1  # bug: flann enums are missing
flann_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
#matcher = cv2.FlannBasedMatcher_create()
matcher = cv2.FlannBasedMatcher(flann_params, {})

matches = matcher.knnMatch(des1, des2, 2)
matchesMask = [[0,0] for i in range(len(matches))]
for i, (m1,m2) in enumerate(matches):
    if m1.distance < 0.7 * m2.distance:
        matchesMask[i] = [1,0]
        ## Notice: How to get the index
        pt1 = kp1[m1.queryIdx].pt
        pt2 = kp2[m1.trainIdx].pt
        print(i, pt1,pt2 )
        if i % 5 ==0:
            ## Draw pairs in purple, to make sure the result is ok
            cv2.circle(img1, (int(pt1[0]),int(pt1[1])), 5, (255,0,255), -1)
            cv2.circle(img2, (int(pt2[0]),int(pt2[1])), 5, (255,0,255), -1)


## Draw match in blue, error in red
draw_params = dict(matchColor = (255, 0,0),
                   singlePointColor = (0,0,255),
                   matchesMask = matchesMask,
                   flags = 0)

res = cv2.drawMatchesKnn(img1,kp1,img2,kp2,matches,None,**draw_params)
cv2.imwrite("keypointsBatman.jpg", res)

res = cv2.resize(res, (640, 480))
cv2.imshow("Result", res)
k = cv2.waitKey(0) #ESC key
if k == 27:
    cv2.destroyAllWindows()