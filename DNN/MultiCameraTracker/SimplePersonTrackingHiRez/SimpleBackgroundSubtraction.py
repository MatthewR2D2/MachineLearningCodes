import numpy as np
import cv2
import copy
import imutils


video = "GameCaputervideo.m2ts"
cap = cv2.VideoCapture(video)

#For background mask
backgroundSub = cv2.bgsegm.createBackgroundSubtractorMOG(history=10)
#For subtractor
subtractor = cv2.createBackgroundSubtractorMOG2(history=50, varThreshold=30, detectShadows=False)

#GMG
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
gmgMask = cv2.bgsegm.createBackgroundSubtractorGMG()


num_frames = 6000
first_iteration = 1

imageHight = 400
imageWidth = 300

fourcc = cv2.VideoWriter_fourcc(*'MPEG')
out = cv2.VideoWriter('output.avi',fourcc, 30.0, (imageHight,imageWidth), 0)
#out = cv2.VideoWriter('output.avi',fourcc, 30.0, (imageHight,imageWidth))

def draw_boxes(myContour, myFrame):
    for c in myContour:
        if cv2.contourArea(c) < 20:
            continue
         # get bbox from contour
        (x, y, w,h) = cv2.boundingRect(c)

        #Draw rect
        cv2.rectangle(myFrame, (x, y), (x + w, y + h), (0, 255, 0), 2)


for i in range(0, num_frames):
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
        height2, width2 = frame.shape[:2]

        #Get the subtraction for background stuff
        forgroundMask = backgroundSub.apply(frame)
        subtractorMask = subtractor.apply(frame)
        gmgSubtractMask = gmgMask.apply(frame)
        gmgSubtractMask = cv2.morphologyEx(gmgSubtractMask,cv2.MORPH_OPEN, kernel)

        #Get contor for each person
        (im2, contours, hierarchy) = cv2.findContours(forgroundMask.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        (im3, contours2, hierarchy2) = cv2.findContours(subtractorMask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        (im4, contours3, hierarchy3) = cv2.findContours(gmgSubtractMask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

        #cv2.imshow('FGMask', forgroundMask)
        #cv2.imshow('SubMask', subtractorMask)
        #cv2.imshow('GMG', gmgSubtractMask)

        frame1 = frame.copy()
        frame2 = frame.copy()
        frame3 = frame.copy()
        draw_boxes(contours, frame1)
        draw_boxes(contours2, frame2)
        draw_boxes(contours3, frame3)
        cv2.imshow('MOG', frame1)
        cv2.imshow('SUB', frame2)
        cv2.imshow('GMG', frame3)

        out.write(subtractorMask)

    cv2.imshow('frame', frame)



    if cv2.waitKey(1) & 0xFF == ord('q'):
        break



cap.release()
out.release()
cv2.destroyAllWindows()
