#!/usr/bin/env python

'''
# Short Description@
Old school way of doing edge detection using Canny
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
image = cv2.imread(imagePath,0)
# Get dimensions of the image
(h,w) = image.shape[:2]
# Find edges
edges = cv2.Canny(image, h, w)

cv2.imshow("Original", image)
cv2.imshow("Edge", edges)

cv2.waitKey(0)
cv2.destroyAllWindows()






