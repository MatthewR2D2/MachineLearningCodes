"""
Created on Wed Oct  3 16:03:30 2018
@author: Matthew Millar
What it does:
This is the main code for processing images
What it needs:

Related Classes:
This need a Class called GymCameraSpliter which is responsible for splittiing up the camera into their own frame
"""

import numpy as np
import cv2
import imutils
from GymCameraProcessor import GymCameraSpliter as gcs

'''
@brief Simple Methods for image cleanup
@note simple image alteration may check at each method for requirements. Also these frames have been read in with opencv
@raises None
@param[in] frame A frame from a video that is already read in through opencv 
@param[in] width The width of the image that you want a frame to resized
@returns A frame that has been altered
'''


def resizeHelper(frame, width):
    return imutils.resize(frame, width=width)


def averagePixels(frame):
    kernel = np.ones((5, 5), np.float32) / 25
    avg = cv2.filter2D(frame, -1, kernel)
    return avg


def imageBlur(frame):
    return cv2.blur(frame, (5, 5))


def gaussianBlur(frame):
    return cv2.GaussianBlur(frame, (21, 21), 0)


def medianBlur(frame):
    return cv2.medianBlur(frame, 5)


def bilateralFilter(frame):
    return cv2.bilateralFilter(frame, 9, 75, 75)


# Super slows
def colorDenoising(frame):
    return cv2.fastNlMeansDenoisingColored(frame, None, 10, 10, 10, 10)


def morphologicalCloseFilter(frame):
    kernel = np.ones((2, 2), np.uint8)
    return cv2.morphologyEx(frame, cv2.MORPH_CLOSE, kernel=kernel)


def morphologicalOpenFilter(frame):
    kernel = np.ones((2, 2), np.uint8)
    return cv2.morphologyEx(frame, cv2.MORPH_OPEN, kernel=kernel)


def imageErode(frame):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.erode(frame, kernel, iterations=1)


def imageDilate(frame):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.dilate(frame, kernel, iterations=1)


'''
@brief Simple background subtracter method for use with multiple background subtraction methods
@note Can use different methods from this simple function
@raises None
@param[in] frame A image that has been read in using opencv
@param[in] subtractor The background subraction method that is wanted.
@returns a mask
'''


def backgroundSubtract(frame, subtractor):
    return subtractor.apply(frame)


'''
@brief This method processes each frame and bring it out into its own camera
@note This will split the camera from the main feed
@note This uses the GymCameraSpliter.py class
@raises None
@param[in] input_cam This is the initial camera feed that is unaltered
@param[in] cam_num The camera that is wanted to be extracted.
@param[in] h The height of the frame wanted.
@param[in] w The width of the frame wanted.
@returns a color process image and the corresponding gray image for a individual camera
'''


def processCamera(input_cam, cam_num, h, w):
    # Crop the image by the camera number
    input_cam = gcs.crop_camera_by_number(input_cam, cam_num)  # Get individual frame
    # resize the image by width and height to keep related to the saved video format
    input_cam = cv2.resize(input_cam, (h, w))
    # Gray image
    processed_cam = cv2.cvtColor(input_cam, cv2.COLOR_BGR2GRAY)
    # Blur image
    processed_cam = gaussianBlur(processed_cam)
    return input_cam, processed_cam


'''
@brief Calculates the threshold for each image
@note 
@raises None
@param[in] first_frame This is the initial frame or background
@param[in] gray_cam The processed camera frame that has been turned into a gray image.
@returns a Threshold image for use in a background change detection methods
'''


def calculateThreshold(first_frame, gray_cam):
    frame_delta = cv2.absdiff(first_frame, gray_cam)
    threshold = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
    threshold = cv2.dilate(threshold, None, iterations=2)
    return threshold


'''
@brief Returns the first frame of the image
@note  May not need this method (Artifact) 
@raises None
@param[in] gray_cam This is the initial frame or background
@returns a copy of the gray process image
'''


def getFirstFrame(gray_cam):
    return gray_cam.copy()


'''
@brief Display the original and the threshold image together side by side
@note  For displaying both the threshold image and the original image side by side
@raises None
@param[in] color_img This is the original resized only processed frame.
@param[in] process_image This is threshold image.
@param[in] title This is the title if you want to show the stack from here.
@returns The horizontal stack which is a concatenation of the two images together.
'''


def displayProcessAndOrigimg(color_img, process_image, title):
    new_process_img = cv2.cvtColor(process_image, cv2.COLOR_GRAY2BGR)
    horizontal_stack = np.hstack((color_img, new_process_img))
    # cv2.imshow(title, horizontal_stack)
    return horizontal_stack

'''
@brief Find bounding boxes from change detection in a machine bounding box
@note  Intersection over union
@raises None
@param[in] contour_bbox This is the contour box found.
@param[in] machine_bbox This is predefined machine bounding boxes.
@returns The intersection over union of the two bounding boxes
'''


def bbIntersectionOverUnion(contour_bbox, machine_bbox):
    # determine the (x, y)-coordinates of the intersection rectangle
    xA = max(contour_bbox[0], machine_bbox[0])
    yA = max(contour_bbox[1], machine_bbox[1])
    xB = min(contour_bbox[2], machine_bbox[2])
    yB = min(contour_bbox[3], machine_bbox[3])
    inter_area = max(0, xB - xA + 1) * max(0, yB - yA + 1)
    boxAArea = (contour_bbox[2] - contour_bbox[0] + 1) * (contour_bbox[3] - contour_bbox[1] + 1)
    boxBArea = (machine_bbox[2] - machine_bbox[0] + 1) * (machine_bbox[3] - machine_bbox[1] + 1)
    iou = inter_area / float(boxAArea + boxBArea - inter_area)
    return iou


'''
@brief Draws boxes on the threashold image
@note myFrame should be a threshold image not a raw image Mainly used for debuging.
@raises None
@param[in] contour A contour from a list of contours. 
@param[in] my_frame This is the image that should be drawn on.
@param[in] mechine_rect is the bounding box or coordiante of a single machine.
@returns Nothing
'''


def drawBoxOnContor(contour, my_frame, machine_rect):
    # get bbox from contour
    (x, y, w, h) = cv2.boundingRect(contour)
    contor_rect = [x, y, x + w, y + h]
    iou = bbIntersectionOverUnion(contor_rect, machine_rect)
    if iou > 0:
        cv2.rectangle(my_frame, (x, y), (x + w, y + h), (255, 255, 255), 1)


'''
@brief Determines if a machine is in use
@note 
@raises None
@param[in] contor A contour from a list of contours. 
@param[in] mechine_rect is the bounding box or coordiante of a single machine.
@returns True if a machine is being used
'''


def machineUseCheck(contor, machine_rect):
    # Get bounding box for Contor
    (x, y, w, h) = cv2.boundingRect(contor)
    contor_rect = [x, y, x + w, y + h]
    # Get the Intersection Union of the machine box and the
    iou = bbIntersectionOverUnion(contor_rect, machine_rect)
    # Chack to see if there is a interesction and union
    if iou > 0:
        return True


'''
@brief This finds and returns the Contour 
@note 
@raises None
@param[in] image is the threshold image as an input and not a color / gray image  
@returns the contours of each detected object
'''


def getContours(image):
    (im2, my_contour, hierarchy) = cv2.findContours(image.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return my_contour


'''
@brief This finds if there is a machine being used or not  
@note 
@raises None
@param[in] my_contors is the contours than are being found
@param[in] threshold_img is the threshold image as an input and not a color / gray image  
@param[in] machine_name is the name of the machine 
@param[in] machine_rectangle is the rectangle/BBOX for the machine or AIO  
@param[in] draw_box_bool if you want to draw the contour BBOX 
@returns True if a machine is in use and None if a machine is not in use
'''


def processContorsForMachineUse(my_contors, threshold_img, machine_name, machine_rectangle, draw_box_bool):
    for c in my_contors:
        if cv2.contourArea(c) < 20:
            continue
        if draw_box_bool:
            drawBoxOnContor(c, threshold_img, machine_rectangle)
        is_in_use = machineUseCheck(c, machine_rectangle)
        if is_in_use:
            cv2.putText(threshold_img, machine_name + ": In Use", (25, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.3,
                        (255, 255, 255), 1)
            return True


'''
@brief This does all the processing for each frame  
@note 
@raises None
@param[in] my_frame is the frame that is being processed
@param[in] first_frame is initial frame for background subtraction  
@param[in] cam_number is the camera number that you want to retrieve  
@param[in] machine_name is the name of the machine 
@param[in] machine_rectangle is the rectangle/BBOX for the machine or AIO  
@param[in] draw_box_bool if you want to draw the contour BBOX 
@returns True if a machine is in use and None if a machine is not in use
'''

def processInitialFeed(frame, blur):
    # Gray image
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Blur image
    if blur:
        gray = gaussianBlur(gray)
    return gray


def fullyProcessFrame(my_frame, first_frame, cam_number, H, W, machine_name, machine_bbox, draw_bbox, display, write, in_color, out):
    frame_copy = my_frame.copy()
    cam_color, cam_gray = processCamera(frame_copy, cam_number, H, W)
    threshold = calculateThreshold(first_frame, cam_gray)
    contours = getContours(threshold)
    result = processContorsForMachineUse(contours, threshold, machine_name, machine_bbox, draw_bbox)
    if display:
        cv2.rectangle(threshold, (machine_bbox[0], machine_bbox[1]), (machine_bbox[2], machine_bbox[3]), (255, 25, 25))
        cv2.imshow("Cam " + str(cam_number), threshold)

    if write:
        print("Writing File")
        if in_color == "color":
            print("Writing color File")
            out.write(cam_color)
        elif in_color == "gray":
            out.write(cam_gray)
        else:
            out.write(threshold)
    return result


# Get the first frame easy
def getFirstFrame(frame, cam_num, H, W):
    color, gray = processCamera(frame, cam_num, H, W)
    return gray
