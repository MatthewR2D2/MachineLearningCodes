import cv2
import matplotlib.pyplot as plt

#Pretrained face detector
face_cascade = cv2.CascadeClassifier("FaceDetection/haarcascade_frontalface_alt.xml")

#Finds any faces and returns true if there are any faces
def face_detection(imgage):
    img = cv2.imread(imgage)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces =face_cascade.detectMultiScale(gray)
    return len(faces) > 0