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
from HelperClasses.CropLayer import CropLayer

# Paths to models and data
protoPath = "/home/matt/GitClone/PythonGitRepo/DNN/EdgeDetection/hed_model/deploy.prototxt"
modelPath = "/home/matt/GitClone/PythonGitRepo/DNN/EdgeDetection/hed_model/hed_pretrained_bsds.caffemodel"
imagePath = "/home/matt/GitClone/PythonGitRepo/DNN/EdgeDetection/TestImages/pen.jpg"

net = cv2.dnn.readNetFromCaffe(protoPath, modelPath)

# Register the model
cv2.dnn_registerLayer("Crop", CropLayer)

# Load image
image = cv2.imread(imagePath)
# Get the height and width of the image
(h,w) = image.shape[:2]

# create a blob out of the input image using HNED
blob = cv2.dnn.blobFromImage(image, scalefactor=1.0, size=(w,h),
                             mean=(104.00698793, 116.66876762, 122.67891434),
                             swapRB= False,
                             crop=False)

# Use blob as the input to the network and do a forward pass to find edges
net.setInput(blob)
hed = net.forward()
hed = cv2.resize(hed[0,0], (w,h)) # Resize the new image to the original size
hed = (255 * hed).astype("uint8") # Scale pixels back to range of [0, 255] Make sure its type uint8

# Print out the original image and the new HED image
cv2.imshow("Original", image)
cv2.imshow("HED", hed)
cv2.waitKey(0)
cv2.destroyAllWindows()

