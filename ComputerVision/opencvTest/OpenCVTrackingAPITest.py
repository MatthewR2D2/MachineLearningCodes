# -*- coding: utf-8 -*-
"""
Created on Mon Aug 27 08:10:00 2018
@author: Matthew Millar
What it does:
What it needs:
Related Classes:

"""

import cv2

videoFile = "videos\TCS2.mp4"


#Create all tracker types
trackerTypes = ["BOOSTING", "MIL", "KCF", "TLD","MEDIANFLOW", "GOTURN", "MOSSE", "CSRT"]
trackerType = trackerTypes[6]

#Can only be used for older versions of open cv 3.3.0 or earlier
if trackerType == trackerTypes[0]:
    tracker = cv2.TrackerBoosting_create()
elif trackerType == trackerTypes[1]:
    tracker = cv2.TrackerMIL_create()
elif trackerType == trackerTypes[2]:
    tracker = cv2.TrackerKCF_create()
elif trackerType == trackerTypes[3]:
    tracker = cv2.TrackerTLD_create()
elif trackerType == trackerTypes[4]:
    tracker = cv2.TrackerMedianFlow_create()
elif trackerType == trackerTypes[5]:
    tracker = cv2.TrackerGOTURN_create()
elif trackerType == trackerTypes[6]:
    tracker = cv2.TrackerMOSSE_create()
elif trackerType == trackerTypes[7]:
    tracker = cv2.TrackerCSRT_create()
    
#tracker = cv2.Tracker_create(trackerType)    

#Select the target you want to track
video = cv2.VideoCapture(videoFile)    
ret, frame= video.read()
bbox = cv2.selectROI(frame, False)
ok = tracker.init(frame, bbox)
    
while True:
    ret, frame=video.read()
    
    if not ret:
        break
    
    #Start timers
    timer = cv2.getTickCount()
    ok, bbox = tracker.update(frame)
    
    #Tracking success
    if ok:
        p1 = (int(bbox[0]), int(bbox[1]))
        p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
        cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)
    else:
        #Fail to track
        cv2.putText(frame, trackerType + " Tracker Error", (10,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,255,0),2)
        
    # Display tracker type on frame
    cv2.putText(frame, trackerType + " Tracker", (10,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,255,0),2)
 

    # Display result
    cv2.imshow("Tracking", frame)
 
    # Exit if ESC pressed
    k = cv2.waitKey(1) & 0xff
    if k == 27 : break
    
video.release()
cv2.destroyAllWindows()
    
    