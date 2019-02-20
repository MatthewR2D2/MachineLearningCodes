import numpy as np
import cv2
import imutils
import pafy


path = "D:/MLDataset/ImageAnalysis/VideoCCTV/youtube/"
source = path + "Test2.mp4"
source1 = path + "secCam1.mp4"
youtube = "https://www.youtube.com/watch?v=7vacL_DgkK8"
new_path = pafy.new(youtube)
play  = new_path.getbest()
pie0Url = "http://192.168.100.21/video_feed"
pieUrl = "http://192.168.100.20/video_feed"
webcamfeed = "http://192.168.100.42/video_feed"

window_titile = ["WebCam", "Video 1", "Video2", "Youtube", "Pie0", "Pie", "OtherCam"]

sources = [0, source, source1, play.url, pie0Url, pieUrl, webcamfeed]

cap = [cv2.VideoCapture(i) for i in sources]

frames = [None] * len(sources)
gray = [None] * len(sources)
ret = [None] * len(sources)

while True:
    for i, c in enumerate(cap):
        if c is not None:
            ret[i], frames[i] = c.read()
    for i, f in enumerate(frames):
        if ret[i] is True:
            #gray[i] = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)
            f = imutils.resize(f, width=400)
            
            cv2.imshow(window_titile[i], f)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
        
for c in cap:
    if c is not None:
        c.release()
cv2.destroyAllWindows()