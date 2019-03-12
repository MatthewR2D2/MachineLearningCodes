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
from VideoHelper import  VideoHandeler as VH

# Paths to folders
videoFolder = "TestVideo/"
ext = ".mp4"

# Pick video to test
video = videoFolder + "sample" + ext

# Start video processing
cap = cv2.VideoCapture(video)
outWriter = None
w, h = None, None

while True:
    # Get the next frame from video
    ret, frame = cap.read()

    # Check to see if it returned something or not
    if not ret:
        break

    # Get the width and height of the frame
    if w is None and h is None:
        h, w = frame.shape[:2]

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