#!/usr/bin/env python

'''
# Short Description@
# 
# Full Description@
# 
__author__ = "Matthew Millar"
__copyright__ = ""
__credits__ =
__license__ = ""
__version__ = "0.0.0"
__maintainer__ = "Matthew Millar"
__email__ = "matthew.millar@igniterlabs.com"
__status__ = "Dev"

'''

import cv2

imagePath = "/home/matt/GitClone/PythonGitRepo/DNN/EdgeDetection/TestImages/pen.jpg"

# find the edges using canny OLD SCHOOL Style
# read in the file
image = cv2.imread(imagePath)
# Get dimensions of the image
(h,w) = image.shape[:2]

# Convert to gray color / gray scale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Clean image by removing noise
cleanImage = cv2.GaussianBlur(gray, (3,3),0)

# Convolute with Sobel
sobelx = cv2.Sobel(cleanImage, cv2.CV_64F,1,0,ksize=5)
sobely = cv2.Sobel(cleanImage, cv2.CV_64F,0,1,ksize=5)


cv2.imshow("Sobelx", sobelx)
cv2.imshow("Sobely", sobely)
cv2.imshow("Original", image)

cv2.waitKey(0)
cv2.destroyAllWindows()
