from imutils import paths
import numpy as np
import imutils
import cv2

#Find the marker
def findMarker(image):
    #Get the gray image for quick processing
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #Blur/Smooth image slightly
    gray = cv2.GaussianBlur(gray,(5,5), 0)
    #Edge detection ofthe image
    edged = cv2.Canny(gray, 35, 100)
    cv2.imshow("Edges",edged)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    #Find contours of edges and keep only the largest one
    cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts= cnts[0] if imutils.is_cv2() else cnts[1]
    #Get the largest contors
    c = max(cnts, key = cv2.contourArea)
    
    #get the bounding box ofthe objects region 
    return cv2.minAreaRect(c)
	
'''
#Compute the distance from camera
F = (P x  D) / W
F = Focal Length
P = apparent width in Pixels
W = known width of object in INCHs
D = Distance from camera

To find D' = (W X F) /P
'''
def distanceToCam(W, F, P):
    return (W * F) / P
	

'''
This get the focal length of the camera if unknown
F = (P x  D) / W

D = known distance to target
W = known width of target
'''
def calibrateFocalLength(D, W, image):
    image = cv2.imread(image)
    marker = findMarker(image)
    return (marker[1][0] * D) / W
	
KW = 7.0 #IN
FL = 26.79 #MM for Asus Phone

image = "Image/T(3).jpg"
img= cv2.imread(image)
height,width  = img.shape[:2]
print(width)
print(height)
img = imutils.resize(img, width=int(width/10))
marker = findMarker(img)
distance = distanceToCam(KW,FL, marker[1][0])
print(distance)

box = cv2.boxPoints(marker)
box = np.int0(box)

cv2.drawContours(img, [box], -1, (0,255,0) ,2)
cv2.putText(img, "%.2fM" % (distance),
           (img.shape[1] - 200, img.shape[0] - 20),
            cv2.FONT_HERSHEY_SIMPLEX,
           2.0, (0, 255, 0), 3)
		   
cv2.imshow("Image",img)
cv2.waitKey(0)
cv2.destroyAllWindows()
