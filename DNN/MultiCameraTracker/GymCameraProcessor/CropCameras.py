"""
Created on Wed Oct  3 16:03:30 2018
@author: Matthew Millar
What it does:
This class shows how to get either one camera based on camera number or every camera based on which
method is used.
What it needs:
Related Classes:
"""
import cv2
import time
from GymCameraProcessor import GymVideoProcessing as gvp
from GymCameraProcessor import OutputVideoHandler as video_saver
import imutils
import numpy as np

print("Starting")
video = "video/GameCaputervideo.m2ts"
cap = cv2.VideoCapture(video)
print("Capture Video")

# Background Mask
subtractor = cv2.createBackgroundSubtractorMOG2(history=15, varThreshold=50)

image_height = 440
image_width = 360

# Create Output writers
color = False #Set output as either color or black and white
#Needs to be false for gray and threashold images
out = video_saver.createWriters(image_height, image_width, "Output.avi", False)

print("Start Process")
start = time.time()

# Test machine bounding boxes
rect1 = [241, 161, 291, 240]
rect3 = [241, 161, 500, 300]
rect2 = [0, 0, 5, 5]

'''
#Test for a list of machines and there bounding boxes
#The array should have:
#The name of the machine
#Location of bounding box
'''
machine_list = []
machine_list.append(["Hip-Abductors", rect3])

total_cameras = 16  # Total number of cameras in a system
camera_first_frame_list = []  # Holds all the first frames for backgrounds

num_frames = 200
first_iteration = True
current_frame = 0
for i in range(0, num_frames):
    # while True:
    # Get every other frame
    if i % 2 == 0:
        ret, frame = cap.read()
        if ret:
            copy_frame = frame.copy()
            # Check to see if there is a first frame for each camera.
            if first_iteration:
                first_iteration = False
                while i < total_cameras:
                    camera_first_frame_list.append(gvp.getFirstFrame(frame, i + 1, image_height, image_width))
                    i += 1
            # process each camera
            cam1 = gvp.fullyProcessFrame(frame, camera_first_frame_list[0], 1, image_height, image_width,
                                         machine_list[0][0], machine_list[0][1], True, False, False, "gray", out)
            cam2 = gvp.fullyProcessFrame(frame, camera_first_frame_list[1], 2, image_height, image_width,
                                         machine_list[0][0], machine_list[0][1], True, False, False, "gray", out)
            cam3 = gvp.fullyProcessFrame(frame, camera_first_frame_list[2], 3, image_height, image_width,
                                         machine_list[0][0], machine_list[0][1], True, False, False, "gray", out)
            cam4 = gvp.fullyProcessFrame(frame, camera_first_frame_list[3], 4, image_height, image_width,
                                         machine_list[0][0], machine_list[0][1], True, False, False, None, out)
            cam5 = gvp.fullyProcessFrame(frame, camera_first_frame_list[4], 5, image_height, image_width,
                                         machine_list[0][0], machine_list[0][1], True, False, False, "color", out)
            cam6 = gvp.fullyProcessFrame(frame, camera_first_frame_list[5], 6, image_height, image_width,
                                         machine_list[0][0], machine_list[0][1], True, True, False, "gray", out)
            cam7 = gvp.fullyProcessFrame(frame, camera_first_frame_list[6], 7, image_height, image_width,
                                         machine_list[0][0], machine_list[0][1], True, False, False, "gray", out)
            cam8 = gvp.fullyProcessFrame(frame, camera_first_frame_list[7], 8, image_height, image_width,
                                         machine_list[0][0], machine_list[0][1], True, False, False, "gray", out)
            cam9 = gvp.fullyProcessFrame(frame, camera_first_frame_list[8], 9, image_height, image_width,
                                         machine_list[0][0], machine_list[0][1], True, False, False, "gray", out)
            cam10 = gvp.fullyProcessFrame(frame, camera_first_frame_list[9], 10, image_height, image_width,
                                          machine_list[0][0], machine_list[0][1], True, False, False, "gray", out)
            cam11 = gvp.fullyProcessFrame(frame, camera_first_frame_list[10], 11, image_height, image_width,
                                          machine_list[0][0], machine_list[0][1], True, False, False, "gray", out)
            cam12 = gvp.fullyProcessFrame(frame, camera_first_frame_list[11], 12, image_height, image_width,
                                          machine_list[0][0], machine_list[0][1], True, False, False, "gray", out)
            cam13 = gvp.fullyProcessFrame(frame, camera_first_frame_list[12], 13, image_height, image_width,
                                          machine_list[0][0], machine_list[0][1], True, False, False, "gray", out)
            cam14 = gvp.fullyProcessFrame(frame, camera_first_frame_list[13], 14, image_height, image_width,
                                          machine_list[0][0], machine_list[0][1], True, False, False, "gray", out)
            cam15 = gvp.fullyProcessFrame(frame, camera_first_frame_list[14], 15, image_height, image_width,
                                          machine_list[0][0], machine_list[0][1], True, False, False, "gray", out)
            cam16 = gvp.fullyProcessFrame(frame, camera_first_frame_list[15], 16, image_height, image_width,
                                          machine_list[0][0], machine_list[0][1], True, False, False, "gray", out)

        else:
            continue
    print("Current Frame:", current_frame)
    current_frame = current_frame + 1
    # Kill switch
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

end = time.time()
print("Total Time:", end - start)

# Release and close all opencv items
out.release()
cap.release()
cv2.destroyAllWindows()
