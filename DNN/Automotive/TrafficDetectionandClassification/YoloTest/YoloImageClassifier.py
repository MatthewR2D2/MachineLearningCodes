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
import time
import cv2

# Global variables
threshold = 0.3
confid = 0.5

# Paths to folders
imageFolder = "TestImages/"
modelFolder = "Yolo-CoCoModel/"
ext = ".jpg"

# Get the label for each object that can be classified
labelsPath = modelFolder + "coco.names"
# Use newline as that seperated each word/object
LABELS = open(labelsPath).read().strip().split("\n")

# Give each label its own color
np.random.sample(42)  # As there are 42 labels
COLORS = np.random.randint(0, 255, size=(len(LABELS), 3), dtype="uint8")

# Yolo model paths
yoloWeights = modelFolder + "yolov3.weights"
yoloConfig = modelFolder + "yolov3.cfg"

# Now load the yolo object detector
net = cv2.dnn.readNetFromDarknet(yoloConfig, yoloWeights)

# Get a test image.

img = imageFolder + "T4" + ext

# Read in the image using OpenCV
image = cv2.imread(img)
# Get the height and width of the image will need for later
(h, w) = image.shape[:2]

# Get the output layer from Yolo
ln = net.getLayerNames()
ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]

# Make a blob from the input
# Do a forward pass of yolo detector
# Returns the bounding box + probabilities
blob = cv2.dnn.blobFromImage(image,
                             1 / 255.0,
                             (416, 416),
                             swapRB=True,
                             crop=False)

net.setInput(blob)
start = time.time()
layerOutputs = net.forward(ln)
end = time.time()

print("Total Time: ", (end - start))

# Get a list of bbox, confidences, and class id
boxes = []
confidences = []
classIDs = []

# Loop over each layer outputs
for output in layerOutputs:
    for detection in output:
        # get the probabilites and and ID
        scores = detection[5:]
        classID = np.argmax(scores)  # Get the highest probability
        confidence = scores[classID]

        # Get rid of lower predictions by losing lower probabilities
        if confidence > threshold:
            # scale the bounding box coordinates back relative to the
            # size of the image, keeping in mind that YOLO actually
            # returns the center (x, y)-coordinates of the bounding
            # box followed by the boxes' width and height
            box = detection[0:4] * np.array([w, h, w, h])
            (centerX, centerY, width, height) = box.astype("int")
            # use the center (x, y)-coordinates to derive the top and
            # and left corner of the bounding box
            x = int(centerX - (width / 2))
            y = int(centerY - (height / 2))

            # update our list of bounding box coordinates, confidences,
            # and class IDs
            boxes.append([x, y, int(width), int(height)])
            confidences.append(float(confidence))
            classIDs.append(classID)

# apply non-maxima suppression to suppress weak, overlapping bounding
# boxes
idxs = cv2.dnn.NMSBoxes(boxes, confidences, confid, threshold)

# ensure at least one detection exists
if len(idxs) > 0:
    # loop over the indexes we are keeping
    for i in idxs.flatten():
        # extract the bounding box coordinates
        (x, y) = (boxes[i][0], boxes[i][1])
        (w, h) = (boxes[i][2], boxes[i][3])

        # draw a bounding box rectangle and label on the image
        color = [int(c) for c in COLORS[classIDs[i]]]
        cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
        text = "{}: {:.4f}".format(LABELS[classIDs[i]], confidences[i])
        cv2.putText(image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, color, 2)

# Show output
cv2.imshow("Result", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
