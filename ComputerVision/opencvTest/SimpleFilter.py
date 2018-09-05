# -*- coding: utf-8 -*-
"""
Created on Wed Aug 15 08:18:21 2018
@author: Matthew Millar
What it does:
What it needs:
Related Classes:

"""


import cv2
import numpy as np
from matplotlib import pyplot as plt

img =cv2.imread("D:/Tests/opencvTest/images/batman.jpg", 0)

#Set up the kernel size and shape
kernel = np.ones((5,5), np.float32)/25
#Apply the kernel to the image
dst = cv2.filter2D(img, -1, kernel)
#dst= cv2.blur(img, (5,5)) #Does the same as above custom kernel
#dst = cv2.medianBlur(img, 5)


#filters for edge detections
#Xaxis kernel
sobelX = np.array((
        [-1,0,1],
        [-2,0,2],
        [-1,0,1]), dtype='int')

#Y axis kernel
sobleY= np.array((
        [-1,-2,-1],
        [0,0,0],
        [1,2,1]), dtype = 'int')

laplacian = np.array((
        [0,1,0],
        [1,-4,1],
        [0,1,0]), dtype = 'int')


dst = cv2.filter2D(img, -1, laplacian)

#Plot out
plt.subplot(121), plt.imshow(img), plt.title("Original")
plt.xticks([]), plt.yticks([])
plt.subplot(122), plt.imshow(dst), plt.title("Processed")
plt.xticks([]), plt.yticks([])
plt.show()