import cv2
import imutils
from GymCameraProcessor import GymCameraSpliter as gcs
from GymCameraProcessor import GymVideoProcessing as gvp

refPt = []
cropping = False


def click_and_crop(event, x, y, flags, param):
    global refPt, cropping

    if event == cv2.EVENT_LBUTTONDOWN:
        refPt = [(x, y)]
        cropping = True
    elif event == cv2.EVENT_LBUTTONUP:
        refPt.append((x, y))
        cropping = False
        cv2.rectangle(image, refPt[0], refPt[1], (0, 255, 0), 2)
        print("pint 0",refPt[0])
        print("pint 1", refPt[1])
        cv2.imshow("image", image)


# load the image, clone it, and setup the mouse callback function

imageHight = 440
imageWidth = 360

print("Starting")
video = "video/GameCaputervideo.m2ts"
cap = cv2.VideoCapture(video)
print("Capture Video")
ret, image = cap.read()
#frame = gcs.crop_camera_by_number(frame, 6)
#image,_ = gvp.process_camera(frame, 6, imageHight, imageWidth)
image = gcs.get_all_cameras(image)
image = imutils.resize(image, width=1000)


clone = image.copy()
cv2.namedWindow("image")
cv2.setMouseCallback("image", click_and_crop)

# keep looping until the 'q' key is pressed
while True:
    # display the image and wait for a keypress
    cv2.imshow("image", image)
    key = cv2.waitKey(1) & 0xFF

    # if the 'r' key is pressed, reset the cropping region
    if key == ord("r"):
        image = clone.copy()

    # if the 'c' key is pressed, break from the loop
    elif key == ord("c"):
        break

# if there are two reference points, then crop the region of interest
# from teh image and display it
if len(refPt) == 2:
    roi = clone[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
    cv2.imshow("ROI", roi)
    cv2.waitKey(0)

cap.release()
cv2.destroyAllWindows()