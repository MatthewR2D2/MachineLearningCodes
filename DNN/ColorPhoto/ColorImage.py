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

import numpy as np
import cv2

pathToBWFile = "Images/albert_einstein.jpg"
pathToProtoTxt = "Models/colorization_deploy_v2.prototxt"
pathToCaffeModel = "Models/colorization_release_v2.caffemodel"
pathToCenterPoints = "Models/pts_in_hull.npy"

# Load models
net = cv2.dnn.readNetFromCaffe(pathToProtoTxt, pathToCaffeModel)
pts = np.load(pathToCenterPoints)

# Add cluster centers as 1x1 convo to model
# This loads the cente of the ab channel
class8 = net.getLayerId("class8_ab")
conv8 = net.getLayerId("conv8_313_rh")
pts = pts.transpose().reshape(2, 313, 1, 1)
net.getLayer(class8).blobs = [pts.astype("float32")]
net.getLayer(conv8).blobs = [np.full([1, 313], 2.606, dtype="float32")]

# Get the BW image
image = cv2.imread(pathToBWFile)
# Intensities to range 0,1
scaled = image.astype("float32") / 255.0
# Change image into LAB image for use with pretrained model
lab = cv2.cvtColor(scaled, cv2.COLOR_BGR2LAB)

# Resize to 224*224
resized = cv2.resize(lab, (224, 224))
# Get only the L channel
L = cv2.split(resized)[0]
# Preform mean subtraction
L -= 50

# Start to color the image
net.setInput(cv2.dnn.blobFromImage(L))
ab = net.forward()[0, :, :, :].transpose((1, 2, 0))
# Resize ab image to the input image size
ab = cv2.resize(ab, (image.shape[1], image.shape[0]))

# Get L Channel from original image
L = cv2.split(lab)[0]
colorized = np.concatenate((L[:, :, np.newaxis], ab), axis=2)

# Convert the output image into RGB
colorized = cv2.cvtColor(colorized, cv2.COLOR_LAB2BGR)
colorized = np.clip(colorized, 0, 1)

# 8-bit integer representation in the range [0, 255]
colorized = (255 * colorized).astype("uint8")

# show the original and output colorized images
cv2.imshow("Original", image)
cv2.imshow("Colorized", colorized)
cv2.waitKey(0)

