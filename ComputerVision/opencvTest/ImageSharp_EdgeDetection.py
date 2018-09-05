# -*- coding: utf-8 -*-
"""
Created on Wed Aug 15 08:43:30 2018
@author: Matthew Millar
What it does:
What it needs:
Related Classes:

"""

import cv2
import numpy as np
from matplotlib import pyplot as plt

path = "D:/Tests/opencvTest/images/"
img =cv2.imread(path+"batman.jpg", 0)

kernel = np.array([[-1,-1,-1],[-1,9,-1],[-1,-1,-1]])

img_sharpened = cv2.filter2D(img, -1, kernel)

cv2.imwrite(path+"sharpened.jpg", img_sharpened)

#Use Canny to find edges easy
edges = cv2.Canny(img, 100,200)
edges2 = cv2.Canny(img_sharpened, 100,200)

#plt.subplot(121),plt.imshow(img, cmap ='gray')
#plt.title("Original"), plt.xticks([]), plt.yticks([])
#plt.subplot(122), plt.imshow(edges, cmap = "gray")
#plt.title("Edge"), plt.xticks([]), plt.yticks([])
#plt.show()

plt.subplot(121),plt.imshow(edges, cmap ='gray')
plt.title("Original"), plt.xticks([]), plt.yticks([])
plt.subplot(122), plt.imshow(edges2, cmap = "gray")
plt.title("Sharpe"), plt.xticks([]), plt.yticks([])
plt.show()
