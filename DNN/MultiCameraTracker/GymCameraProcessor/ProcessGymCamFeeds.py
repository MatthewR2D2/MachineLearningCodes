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


#For debugging threashold image
def draw_grid(img, line_color=(255, 255, 255), thickness=1, type=cv2.LINE_AA):
    #Draw Rows
    cv2.line(img, (0, 185), (img.shape[1], 185), color=line_color, lineType=type, thickness=thickness)
    cv2.line(img, (0, 375), (img.shape[1], 375), color=line_color, lineType=type, thickness=thickness)
    cv2.line(img, (0, 565), (img.shape[1], 565), color=line_color, lineType=type, thickness=thickness)
    cv2.line(img, (0, 775), (img.shape[1], 775), color=line_color, lineType=type, thickness=thickness)
    #Draw Collumns
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
def drawBoundingBox(image, box, color):
    x = box[0]
    y = box[1]
    x2  = box[2]
    y2 = box[3]
    cv2.rectangle(image, (x, y), (x2, y2), color, 2)

def getContours(image_threshold):
    cont = cv2.findContours(image_threshold.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cont = cont[1]
    return cont

def detectUsage(aoi, bound_box, image):
    for aoi_rect in aoi:
        bbox = aoi_rect[1]
        if gvp.machineUseCheck(bound_box, bbox):
            # print("There is a machine in use:", machine_rect[0])
            cv2.putText(image, "AOI Used: {}".format(aoi_rect[0]), (bbox[0], bbox[1] + 5), cv2.FONT_HERSHEY_SIMPLEX,
                        0.6, (0, 255, 0), 2)
            cv2.rectangle(image, (x, y), (x + w, y + h), (222, 150, 1), 2)





area_of_interest= []
area_of_interest.append(["office", [250, 4, 496, 181]])
#cam4
area_of_interest.append(["cam4Machine1", [820, 125, 833, 135]])
area_of_interest.append(["cam4Machine2", [899, 107, 917, 120]])

#cam5
area_of_interest.append(["bench1", [41, 359, 81, 372]])
area_of_interest.append(["bench2", [73, 299, 113, 307]])
area_of_interest.append(["bench3", [81, 267, 101, 272]])

#cam6
area_of_interest.append(["OSAA", [389, 294, 404, 304]])
area_of_interest.append(["legpress", [292, 297, 299, 313]])
area_of_interest.append(["bike1", [312, 226, 317, 230]])
area_of_interest.append(["bike2", [341, 222, 348, 224]])
area_of_interest.append(["bike3", [370, 228, 376, 235]])
area_of_interest.append(["bike4", [405, 238, 412, 240]])

#cam7
area_of_interest.append(["pulldown", [517, 276, 527, 283]])

#cam14
area_of_interest.append(["cables", [398, 618, 407, 642]])
area_of_interest.append(["curle", [299, 644, 305, 671]])

#cam15
area_of_interest.append(["benchpress", [539, 640, 548, 648]])
area_of_interest.append(["obliques", [590, 636, 601, 643]])
area_of_interest.append(["ski1", [690, 720, 708, 748]])
area_of_interest.append(["ski2", [735, 714, 747, 739]])

stop_box = [322, 200, 328, 211]

bench1InUse = False
osaaInUse =False

print("Box", area_of_interest[0][1])

print("Starting")
video = "video/GameCaputervideo.m2ts"
cap = cv2.VideoCapture(video)
print("Capture Video")

# The output for video files Created from the OutputVideoHandler
out = None

print("Start Process")
start = time.time()

total_frames = 5846
num_frames = 1000
first_iteration = True
current_frame = 0
enter_counter = 0
first_frame = None #This will be used as the background

for i in range(0, num_frames):
    ret, frame = cap.read()
    if ret:
        if out is None:
            # Get the shape of the image to create a output writer for the video i wanted
            out = video_saver.createWriters(frame.shape[1], frame.shape[0], "Color_Output.avi", True)

        frame = gcs.get_all_cameras(frame)
        frame = imutils.resize(frame, width=1000)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if first_frame is None:
            first_frame = gray
            continue
        threshold = getThreshold(first_frame, gray)
        contours = getContours(threshold)

        # # loop over the contours
        for c in contours:
            # Filter out the blobs that are too small to be considered cars.
            contours = filter(lambda cont: cv2.contourArea(cont) > 30, contours)
            # compute the bounding box for the contour
            (x, y, w, h) = cv2.boundingRect(c)

            #Find each Area Of Interest usage
            detectUsage(area_of_interest, c, frame)

            #Get all the centers for the bounding boxes
            center = (int(x + w / 2), int(y + h / 2))
            cv2.circle(frame, center, 4, (0, 0, 255), -1)


        '''
        Draw all information on the frame to display
        '''
        #Draw boxes for AOI
        for box in area_of_interest:
            bbox = box[1]
            drawBoundingBox(frame, bbox, (0, 255, 0))

        drawBoundingBox(frame, stop_box, (255, 0, 0))
        drawBoundingBox(threshold, stop_box, (255, 0, 0))
        draw_grid(threshold)
        cv2.putText(frame, "FPS: {}".format(cap.get(cv2.CAP_PROP_FPS)),(10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        cv2.putText(frame, "Entered: {}".format(str(enter_counter)), (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.6,(0, 255, 0), 2)

        cv2.imshow("Camera", frame)
        #cv2.imshow("Gray", gray)
        #cv2.imshow("Threshold", threshold)
        print("Frame", current_frame)
        current_frame +=1
        out.write(frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

end = time.time()
print("Total Time:", end - start)

cap.release()
out.release()
cv2.destroyAllWindows()