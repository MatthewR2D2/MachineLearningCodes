# -*- coding: utf-8 -*-
"""
Created on Wed Aug 15 07:40:59 2018
@author: Matthew Millar
What it does:
What it needs:
Related Classes:

"""

import cv2
import numpy as np
from matplotlib import pyplot as plt

img =cv2.imread("D:/Tests/opencvTest/images/batman.jpg", 0)

hist,bins = np.histogram(img.flatten(), 256, [0,256])
    
plt.plot(hist,color = "b")

cdf = hist.cumsum()
cdf_normalized = cdf * hist.max()/ cdf.max()

plt.plot(cdf_normalized, color="r")
#plt.plot(hist,color = "b")
plt.xlim([0,256])
plt.legend(("cdf","historam"), loc = 'upper left')
plt.show()

equ = cv2.equalizeHist(img)
cv2.imwrite('D:/Tests/opencvTest/images/equ.jpg', equ)

img2 = cv2.imread("D:/Tests/opencvTest/images/equ.jpg", 0)

hist2,bins2 = np.histogram(img2.flatten(), 256, [0,256])

plt.plot(hist2,color = "g")
