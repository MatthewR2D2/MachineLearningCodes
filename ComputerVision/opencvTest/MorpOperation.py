# -*- coding: utf-8 -*-
"""
Created on Thu Aug 16 07:40:52 2018
@author: Matthew Millar
What it does:
What it needs:
Related Classes:

"""

import cv2
import numpy as np
from matplotlib import pyplot as plt

img =cv2.imread("D:/Tests/opencvTest/images/batman.jpg", 0)

n = 6
kernel = np.ones((n,n), np.uint8)

erosion = cv2.erode(img, kernel, iterations = 1)
dilation = cv2.dilate(img, kernel, iterations = 1)



'''
#Opening first apply errosion then dilation
#Very useful for removing noise
opening = cv2.erode(img,kernel, iterations = 1)
opening = cv2.dilate(img, kernel, iterations = 1)
'''
opening = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel) #Does the same thing as above code

'''
#Closing dilate then erode
#Close small holes inthe image
closing = cv2.dilate(img, kernel, iterations = 1)
closing = cv2.erode(img, kernel, iterations = 1)
'''
closing = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel) #Does the same thing as above code



#subplot mnp M=rows N colums p position
plt.subplot(321),plt.imshow(img), plt.title("Original")
plt.xticks([]), plt.yticks([])
plt.subplot(322),plt.imshow(erosion), plt.title("Erosion")
plt.xticks([]), plt.yticks([])
plt.subplot(323),plt.imshow(dilation), plt.title("Dilate")
plt.xticks([]), plt.yticks([])
plt.subplot(324),plt.imshow(opening), plt.title("Opening")
plt.xticks([]), plt.yticks([])
plt.subplot(325),plt.imshow(closing), plt.title("Closeing")
plt.xticks([]), plt.yticks([])
plt.show()
