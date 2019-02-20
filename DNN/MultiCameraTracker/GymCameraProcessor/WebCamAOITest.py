import cv2
import time
from GymCameraProcessor import GymVideoProcessing as gvp
from GymCameraProcessor import OutputVideoHandler as video_saver
from GymCameraProcessor import GymCameraSpliter as gcs
import imutils
import numpy as np


def getContours(image_threshold):
    cont = cv2.findContours(image_threshold.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cont = cont[1]
    return cont


'''
Draw all the bounding boxes for detection/machine usage
'''


def drawBoundingBox(image, box, color, aoi):
    x = aoi[1][0]
    y = aoi[1][1]
    x2 = aoi[1][2]
    y2 = aoi[1][3]
    cv2.rectangle(image, (x, y), (x2, y2), color, 2)
    cv2.putText(frame, "{} Occupation: {}".format(aoi[0], aoi[2]), (aoi[1][2], aoi[1][3]),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6, (0, 255, 0), 2)


'''
Simple threshold measure
'''


def getThreshold(background, image):
    frame_delta = cv2.absdiff(background, image)
    threshold = cv2.threshold(frame_delta, 100, 255, cv2.THRESH_BINARY)[1]
    threshold = cv2.dilate(threshold, None, iterations=50)
    return threshold


def kohMethod(contour, aoi):
    if gvp.machineUseCheck(contour, aoi[1]):
        return True
    else:
        return False


area_of_interest = []
area_of_interest.append(["AOI", [10, 100, 100, 200], False])

cap = cv2.VideoCapture(0)

fgbg = cv2.createBackgroundSubtractorMOG2(history=15)
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))

first_frame = None
occupied = False

timeInUSe = 0

while True:
    ret, frame = cap.read()
    if ret:

        # Process video for threashold anlysis
        frame = imutils.resize(frame, width=1000)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if first_frame is None:
            first_frame = gray
            continue

        # threshold = getThreshold(first_frame, gray)
        fgmask = fgbg.apply(frame)
        fgmask2 = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
        contours = getContours(fgmask)

        for aoi in area_of_interest:
            for c in contours:
                aoi[2] = kohMethod(c, aoi)
                if aoi[2]:
                    break

        for aoi in area_of_interest:
            drawBoundingBox(frame, aoi[1], (0, 255, 0), aoi)

        for aoi in area_of_interest:
            if aoi[2]:
                fps = cap.get(cv2.CAP_PROP_FPS)
                timeInUSe += 1
                cv2.putText(frame, "{} In Use: TIU:{} Sec:{}".format(aoi[0], timeInUSe, (timeInUSe//fps)), (70, 70),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.6, (0, 255, 0), 2)
            else:
                # Rest the time in use variable
                timeInUSe = 0





        # Display after drawing everything
        cv2.imshow("Camera", frame)
        cv2.imshow("Thold", fgmask2)

    # Kill program
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
