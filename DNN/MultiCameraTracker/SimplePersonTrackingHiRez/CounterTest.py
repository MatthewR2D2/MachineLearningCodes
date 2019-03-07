import numpy as np
import cv2
import copy
import imutils
from Trackers.CentroidTracker import CentroidTracker
from Trackers.TrackableObject import TrackableObject

video = "vtest.avi"
cap = cv2.VideoCapture(video)

#For background mask
backgroundSub = cv2.bgsegm.createBackgroundSubtractorMOG(history=10)

ct = CentroidTracker(30)
trackableObjects = {}

num_frames = 700
first_iteration = 1
imageHight = 400
imageWidth = 300
fourcc = cv2.VideoWriter_fourcc(*'MPEG')
out = cv2.VideoWriter('Tracker_Test.avi',fourcc, 30.0, (imageHight,imageWidth))


def draw_boxes(myContour, myFrame):
    for c in myContour:
        if cv2.contourArea(c) < 20:
            continue
         # get bbox from contour
        (x, y, w,h) = cv2.boundingRect(c)
        #Draw rect
        cv2.rectangle(myFrame, (x, y), (x + w, y + h), (0, 255, 0), 2)

'''
Read Frames frome video
'''
totalLeft =0
totalRight = 0
for i in range(0, num_frames):
    rects = []
    #Get the very first image from the video
    if (first_iteration == 1):
        ret, frame = cap.read()
        frame = cv2.resize(frame, (imageHight,imageWidth))
        first_frame = copy.deepcopy(frame)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        height, width = frame.shape[:2]
        print("shape:", height,width)
        first_iteration = 0

    else:
        ret, frame = cap.read()
        frame = cv2.resize(frame, (imageHight,imageWidth))
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        forgroundMask = backgroundSub.apply(frame)

        #Get contor for each person
        contours, _ = cv2.findContours(forgroundMask.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        contours = filter(lambda cont: cv2.contourArea(cont) > 20, contours)
        #Get bbox from the controus
        for c in contours:
            (x, y, w, h) = cv2.boundingRect(c)
            rectangle = [x, y, (x + w), (y + h)]
            rects.append(rectangle)
            cv2.rectangle(frame, (rectangle[0], rectangle[1]), (rectangle[2], rectangle[3]),
                          (0, 255, 0), 2)



        line = 200
        objects = ct.update(rects)
        if objects is not None:
            for (objectID, centroid) in objects.items():

                to = trackableObjects.get(objectID, None)
                # if there is no existing trackable object, create one
                if to is None:
                    to = TrackableObject(objectID, centroid)
                else:
                    x = [c[0] for c in to.centroids]
                    direction = centroid[0] - np.mean(x)
                    to.centroids.append(centroid)

                    if not to.counted:
                        if direction < 0 and centroid[0] < line:
                            totalLeft += 1
                            to.counted = True
                        elif direction > 0 and centroid[0] > line:
                            totalRight += 1
                            to.counted = True
                trackableObjects[objectID] = to

                text = "ID:{}".format(objectID)
                cv2.putText(frame, text, (centroid[0] - 10, centroid[1] - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                cv2.circle(frame, (centroid[0], centroid[1]), 4, (0, 255, 0), -1)

                if centroid[0] < line:
                    text2 = "ID: {} is on the left".format(objectID)
                    cv2.putText(frame, text2, (centroid[0] - 10, centroid[1] - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)


        '''Display Windows'''
        #Draw a line down the center
        cv2.line(frame, (frame.shape[1] // 2, 0), (frame.shape[1] // 2, frame.shape[0]), (0, 0, 0), 2)
        cv2.putText(frame, "Left {}".format(totalLeft), (15, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        cv2.imshow('FGMask', forgroundMask)
        out.write(frame)
    cv2.imshow('frame', frame)



    if cv2.waitKey(300) & 0xFF == ord('q'):
        break



cap.release()
out.release()
cv2.destroyAllWindows()
