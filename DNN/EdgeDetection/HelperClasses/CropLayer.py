#!/usr/bin/env python

'''
# Short Description@
# 
# Full Description@
To do the edge detection you need a Custom Cropping layer for the DNN

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

class CropLayer(object):
    def __init__(self, params, blobs):
        # Initialize the starting and ending x/y points of the crop
        self.startX = 0
        self.startY = 0
        self.endX = 0
        self.endY = 0

    # This is responsible for computing the volume size of the inputs
    def getMemoryShapes(self, inputs):
        # the crop layer will receive two inputs -- we need to crop
        # the first input blob to match the shape of the second one,
        # keeping the batch size and number of channels
        (inputShape, targetShape) = (inputs[0], inputs[1])        # Define the input volume and the target shape
        (batchSize, numChannels) = (inputShape[0], inputShape[1]) # Extract the batch size and number of channels
        (H, W) = (targetShape[2], targetShape[3])                 # Get the height and width of the image

        # compute the starting and ending crop coordinates
        self.startX = int((inputShape[3] - targetShape[3]) / 2)
        self.startY = int((inputShape[2] - targetShape[2]) / 2)
        self.endX = self.startX + W
        self.endY = self.startY + H

        # return the shape of the volume
        # do the crop during the forward pass
        return [[batchSize, numChannels, H, W]]

    # Here performs the crop of the image during the forward pass
    # The inference edge prediction of the DNN
    def forward(self, inputs):
        # Use the derived x/y to perform the crop
        return [inputs[0][:, :, self.startY:self.endY, self.startX:self.endX]]