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
from VideoHelper import  VideoHandeler as VH

# Global variables
threshold = 0.3
confid = 0.5

# Paths to folders
videoFolder = "TestVideo/"
modelFolder = "Yolo-CoCoModel/"
ext = ".mp4"

# Get the label for each object that can be classified
labelsPath = modelFolder + "coco.names"
# Use newline as that seperated each word/object
LABELS = open(labelsPath).read().strip().split("\n")
# Yolo model paths
yoloWeights = modelFolder + "yolov3.weights"
yoloConfig = modelFolder + "yolov3.cfg"

# Give each label its own color
np.random.sample(42)  # As there are 42 labels
COLORS = np.random.randint(0, 255, size=(len(LABELS), 3), dtype="uint8")

# Now load the yolo object detector
net = cv2.dnn.readNetFromDarknet(yoloConfig, yoloWeights)
# Get the output layer from Yolo
ln = net.getLayerNames()
ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]

# Pick video to test
video = videoFolder + "sample" + ext

# Start video processing
cap = cv2.VideoCapture(video)

# To save the video file or output/results
outWriter = None

w, h = None, None # Place holders for width and height

while True:
    # Get the next frame from video
    ret, frame = cap.read()

    # Check to see if it returned something or not
    if not ret:
        break

    # Get the width and height of the frame
    if w is None and h is None:
        h, w = frame.shape[:2]

    # get bounding boxes
    # and associated probabilities
    blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416),
                                 swapRB=True, crop=False)
    net.setInput(blob)
    start = time.time()
    layerOutputs = net.forward(ln)
    end = time.time()

    # create list of boxes confidences and classIDs
    boxes = []
    confidences = []
    classIDs = []

    # loop over each of the layer outputs
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

    # Suppress weak and overlapping bounding box only need 1
    idxs = cv2.dnn.NMSBoxes(boxes, confidences, confid, threshold)

    # Check for at least 1 detection
    if len(idxs) > 0:
        # Loop over indexes that are stored
        for i in idxs.flatten():
            # Get bbox
            (x,y) = (boxes[i][0], boxes[i][1])
            (w,h) = (boxes[i][2], boxes[i][3])
            print("Confid", confidences[i])
            print("X;{} Y:{}, X2:{} Y2:{}".format(x, y, x+ w, y +h))
            # Draw the bbox and labels
            #color =  [int(c) for c in COLORS[classIDs[i]]]
            cv2.rectangle(frame, (x,y), (x +w, y +h), (255,255,255), 2)
            text = "{}: {:.4f}".format(LABELS[classIDs[i]], confidences[i])

            cv2.putText(frame, text, (x, y -5),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        (255,255,255),
                        2)


    # Check if writer is none or not
    if outWriter is None:
        # Get the shape of the image to create a output writer for the video i wanted
        outWriter = VH.createWriters(frame.shape[1], frame.shape[0], "Color_Output.avi", False)

    cv2.imshow("Output", frame)
    outWriter.write(frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


outWriter.release()
cap.release()
cv2.destroyAllWindows()




