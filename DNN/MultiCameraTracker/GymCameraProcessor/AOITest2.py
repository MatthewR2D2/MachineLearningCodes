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



area_of_interest= []
#cam5
#Name, BBOX, Currently in use, number of uses, Y values for dispaly
area_of_interest.append(["AOI1", [90, 359, 150, 400], False, 0, 90])
area_of_interest.append(["AOI2", [200, 359, 300, 400], False, 0, 110])


print("Starting")
#video = "video/GameCaputervideo.m2ts"
video = "video/TestCam.mp4"
cap = cv2.VideoCapture(video)
print("Capture Video")

print("Start Process")
start = time.time()

num_frames = 1000
first_iteration = True
current_frame = 0

first_frame = None #This will be used as the background

out = None
for i in range(0, num_frames):
    ret, frame = cap.read()
    if ret:
        #Get Frame and process them slightly
        frame = gcs.get_all_cameras(frame)
        frame = imutils.resize(frame, width=1000)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        #If you want to recored add this
        if out is None:
            # Get the shape of the image to create a output writer for the video i wanted
            out = video_saver.createWriters(frame.shape[1], frame.shape[0], "MultiAOITest.avi", True)

        if first_frame is None:
            first_frame = gray
            continue
        threshold = getThreshold(first_frame, gray)
        contours = getContours(threshold)

        #Loop through every AOI
        for aoi in area_of_interest:
            cv2.putText(frame, "{} UseValue: {} Count:{}".format(aoi[0], aoi[2], str(aoi[3])), (10, aoi[4]), cv2.FONT_HERSHEY_SIMPLEX,
                        0.6, (0, 255, 0), 2)

            i = 0 #Make sure that every contour is looked at before breaking out of the loop
            #Loop through all contours
            for c in contours:
                # Filter out the blobs that are too small to be considered cars.
                contours = filter(lambda cont: cv2.contourArea(cont) > 30, contours)
                # compute the bounding box for the contour
                (x, y, w, h) = cv2.boundingRect(c)
                center = (int(x + w / 2), int(y + h / 2))
                cv2.circle(frame, center, 4, (0, 0, 255), -1)

                #Check for any intersection over union
                if gvp.machineUseCheck(c, aoi[1]):
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (222, 150, 1), 2)
                    #Check to see if the intersection has been counted or not
                    if not aoi[2]:
                        #If not count them
                        aoi[2] = True
                        aoi[3] += 1
                    break
                #Make sure to go over every Contour as you may miss some
                elif i == len(c):
                    aoi[2] = False
                    break
                i += 1

        '''
        Draw all information on the frame to display
        '''
        #Draw boxes for AOI
        for box in area_of_interest:
            bbox = box[1]
            drawBoundingBox(frame, bbox, (0, 255, 0))

        cv2.putText(frame, "Frame: {}".format(current_frame), (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.6,(0, 255, 0), 2)
        cv2.putText(frame, "FPS: {}".format(cap.get(cv2.CAP_PROP_FPS)),(10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        cv2.imshow("Camera", frame)
        #cv2.imshow("Gray", gray)
        #cv2.imshow("Threshold", threshold)
        #print("Frame", current_frame)
        current_frame +=1

        out.write(frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

end = time.time()
print("Total Time:", end - start)

out.release()
cap.release()
cv2.destroyAllWindows()