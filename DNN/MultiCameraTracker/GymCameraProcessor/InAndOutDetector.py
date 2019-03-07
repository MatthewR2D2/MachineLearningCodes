"""
Created on Wed Oct  3 16:03:30 2018
@author: Matthew Millar
What it does:
This is a simple test of running process on every frame at once.
What it needs:
Related Classes:
"""
import cv2
import time
from GymCameraProcessor import GymVideoProcessing as gvp
from GymCameraProcessor import OutputVideoHandler as video_saver
from GymCameraProcessor import GymCameraSpliter as gcs
import imutils
import numpy as np
from random import randint

'''
Start of main method
'''


# For debugging threashold image
def draw_grid(img, line_color=(255, 255, 255), thickness=1, type=cv2.LINE_AA):
    # Draw Rows
    cv2.line(img, (0, 185), (img.shape[1], 185), color=line_color, lineType=type, thickness=thickness)
    cv2.line(img, (0, 375), (img.shape[1], 375), color=line_color, lineType=type, thickness=thickness)
    cv2.line(img, (0, 565), (img.shape[1], 565), color=line_color, lineType=type, thickness=thickness)
    cv2.line(img, (0, 775), (img.shape[1], 775), color=line_color, lineType=type, thickness=thickness)
    # Draw Collumns
    cv2.line(img, (250, 0), (250, img.shape[0]), color=line_color, lineType=type, thickness=thickness)
    cv2.line(img, (500, 0), (500, img.shape[0]), color=line_color, lineType=type, thickness=thickness)
    cv2.line(img, (750, 0), (750, img.shape[0]), color=line_color, lineType=type, thickness=thickness)
    cv2.line(img, (1000, 0), (1000, img.shape[0]), color=line_color, lineType=type, thickness=thickness)


'''
Simple threshold measure
'''
def getThreshold(background, image):
    frame_delta = cv2.absdiff(background, image)
    threshold = cv2.threshold(frame_delta, 100, 255, cv2.THRESH_BINARY)[1]
    threshold = cv2.dilate(threshold, None, iterations=2)
    return threshold


'''
Draw all the bounding boxes for detection/machine usage
'''
def drawMachineBoundingBox(image, box, color):
    x = box[0]
    y = box[1]
    x2 = box[2]
    y2 = box[3]
    cv2.rectangle(image, (x, y), (x2, y2), color, 2)


def getContours(image_threshold):
    cont = cv2.findContours(image_threshold.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #cont = cont[1]
    return cont


def checkForEntrace(target_bbox, target_name):
    # Get Centroid of bbox
    x = target_bbox[0]
    y = target_bbox[1]
    w = target_bbox[2]
    h = target_bbox[3]

    center = (int(x + w / 2), int(y + h / 2))
    print("{} Center:{}".format(target_name, center))


stop_box = [322, 200, 328, 211]



print("Starting")
#video = "video/GameCaputervideo.m2ts"
video = "video/EditCamFootage.mp4"
cap = cv2.VideoCapture(video)
print("Capture Video")

num_frames = 1000

first_iteration = True
current_frame = 0

out = None

personUp = 0
personDown = 0

tracker = cv2.TrackerKCF_create()

bboxes = []
colors= []

multiTracker = None



first_frame = None  # This will be used as the background
for i in range(0, num_frames):
    ret, frame = cap.read()

    if ret:
        frame = gcs.get_all_cameras(frame)
        frame = imutils.resize(frame, width=700)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if out is None:
            # Get the shape of the image to create a output writer for the video i wanted
            out = video_saver.createWriters(frame.shape[1], frame.shape[0], "TrackerPoints.avi", True)

        if first_frame is None:
            first_frame = gray
            continue

        threshold = getThreshold(first_frame, gray)
        contours, hierarchy = getContours(threshold)

        # Filter out the blobs that are too small to be considered cars.
        contours = filter(lambda cont: cv2.contourArea(cont) > 30, contours)

        # Holds all centers and rect
        rects = []
        centers = []

        for c in contours:
            # Save current to past centers
            # compute the bounding box for the contour, draw it on the frame,
            (x, y, w, h) = cv2.boundingRect(c)
            rectangle = [x, y, x + w, y + h]
            rects.append(rectangle)
            center = (int(x + w / 2), int(y + h / 2))
            centers.append(center)
            # cv2.rectangle(frame, (x, y), (x + w, y + h), (222, 150, 1), 2)

        cv2.putText(frame, "Number Boxes: {}".format(len(rects)), (10, 90),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)


        crossedNumber = 0
        for cen in centers:
            cv2.circle(frame, cen, 4, (0, 0, 255), -1)
            if cen[1] > 275:
                crossedNumber +=1
                cv2.putText(frame, "Cross",(cen[0]-5,cen[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.6,(0, 255, 0), 2)


        #for box1 in rects:
            #drawMachineBoundingBox(frame, box1, (150, 111, 0))

        #Create the multitracker if it is not crated
        if multiTracker is None:
            #Fill in all the bounding boxes
            if not bboxes:
                for bbox in rects:
                    bboxes.append(bbox)
                    colors.append((randint(64, 255), randint(64, 255), randint(64, 255)))


            #Create and update trackers
            multiTracker = cv2.MultiTracker_create()
            for bbox in bboxes:
                multiTracker.add(tracker, frame, bbox)

        success, boxes = multiTracker.update(frame)

        for i, newBox in enumerate(boxes):
            p1 = (int(newBox[0]), int(newBox[1]))
            p2 = (int(newBox[2]), int(newBox[3]))
            cv2.rectangle(frame, p1, p2, colors[i], 2, 1)


        drawMachineBoundingBox(frame, stop_box, (255, 0, 0))
        draw_grid(threshold)

        cv2.line(frame,(0,275), (frame.shape[1], 275), (255,255,255), 2)
        cv2.putText(frame, "FPS: {}".format(cap.get(cv2.CAP_PROP_FPS)), (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                    (0, 255, 0), 2)
        cv2.putText(frame, "Entered: {}".format(crossedNumber), (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                    (0, 255, 0), 2)
        cv2.imshow("Camera", frame)

        out.write(frame)
        # cv2.imshow("Gray", gray)
        # cv2.imshow("Threshold", threshold)
        # print("Frame", current_frame)
        current_frame += 1
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

out.release()
cap.release()
cv2.destroyAllWindows()
