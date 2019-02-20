#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script takes a camera feed from a webserver and saves it to a file along with a logfile
showing the time, frame, time relative to start, 
also the resolution and frame rate of the output.

When reading in MJPEG format from a Flask Server Stream on Ubuntu using OpenCV I got the error 
"[mpjpeg @ 0x5582287128c0] Expected boundary '--' not found, instead found a line of 7 bytes"
I believe its an issue with OpenCV and motion format of JPEG. I found the solution online as reading in
the JPEG as bytes and manually decoding it.

Created on Wed Nov 14 14:55:07 2018

@author: Benjamin Lowe
"""

import cv2
import urllib.request
import contextlib
import imutils
import numpy as np
import datetime 
import sys


url='http://192.168.100.42/video_feed'
fps = 30 #The gym footage is 5 and 30 fps 
capSize = (360,270) # Video will be resized to fit the first dimension of this without distortion. Second dimension meaningles 
# The Gym Footage from 16 camera feed is 360x270
out_filename="stream_30fps"


fourcc = cv2.VideoWriter_fourcc(*'MPEG')
vout = cv2.VideoWriter()
success = vout.open(out_filename+'.avi',fourcc,fps,capSize,True) 
print(success)
if not success:
    raise "failed to open video"
    sys.exit(1)
    

with open(out_filename+".csv", "w") as logfile:
    stream = urllib.request.urlopen(url)
    with contextlib.closing(urllib.request.urlopen(url)) as x:
        bytes = bytes()
        t1 = datetime.datetime.now()
        logfile.write(str(t1) + "," + str(capSize) + "\n" )
        frame_num=0
        while True:
            bytes += stream.read(1024)
            a = bytes.find(b'\xff\xd8')
            b = bytes.find(b'\xff\xd9')
            if a != -1 and b != -1:
                jpg = bytes[a:b+2]
                bytes = bytes[b+2:]
                i = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                cv2.imshow('i', i)
                cv2.imwrite("img.jpg", i)
                cv2.waitKey(1)
                img=cv2.imread("img.jpg")
                img = imutils.resize(img, width=capSize[0])
                t2 = datetime.datetime.now()
                if frame_num % 100 == 0:
                    print(t2, frame_num, t2-t1)
                logfile.write(str(t2) + "," + str(frame_num) + "," + str(t2-t1) + "\n" )
                vout.write(img)
                frame_num+=1
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
        vout.release() 
        vout = None
        cv2.destroyAllWindows()
