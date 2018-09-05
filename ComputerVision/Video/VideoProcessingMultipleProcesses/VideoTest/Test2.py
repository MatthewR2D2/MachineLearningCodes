# -*- coding: utf-8 -*-
"""
Created on Fri Aug 24 13:55:35 2018
@author: Matthew Millar
What it does:
What it needs:
Related Classes:

"""

from imutils.video import FPS
import numpy as np
import imutils
import time
import cv2
from VideoUtil import FileVideoStream


#video = "videos/jurassic_park_intro.mp4"
video = "videos/MITest.mp4"
print("String Mian Program")
fvs = FileVideoStream(video, 1024).start()
time.sleep(1.0)

fps = FPS().start()

fourcc = cv2.VideoWriter_fourcc(*"XVID")
out = cv2.VideoWriter('output.mp4',fourcc, 30.0, (440,360))

while fvs.more():
    frame = fvs.read()
    frame = imutils.resize(frame, width=450)
    cv2.putText(frame, "Queue Size: {}".format(fvs.Q.qsize()),
                (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    
    out.write(frame)
    cv2.imshow("MI", frame)
    cv2.waitKey(1)
    fps.update()
    
fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# do a bit of cleanup
out.release()
cv2.destroyAllWindows()
fvs.stop()


    
