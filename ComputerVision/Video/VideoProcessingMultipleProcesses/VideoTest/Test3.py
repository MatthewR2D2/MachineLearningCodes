# -*- coding: utf-8 -*-
"""
Created on Fri Aug 24 15:06:12 2018
@author: Matthew Millar
What it does:
What it needs:
Related Classes:

"""



import cv2
import threading


def daemonVideoProcessing(cam, out):
    print("Daemon Video Processing Starting")
    frame = 0
    while(True): 
    
        #print("Reading video....")
        ret, img = cam.read()
        #print("Vdieo reading Result:",ret)
        #Resize image for quicker display and processing
        img = cv2.resize(img, (440, 360))
        edges = cv2.Canny(img, 100, 200)
        
        
      
        #print("Writing to file")
        out.write(img)
        #Display theimage 
        cv2.imshow('img',edges)
        #Advance to the next frame
        frame = frame + 1
    
        '''
        #Controls the stoping point
        #Stop 1 if the last frame is hit then stop
        #If the q button is pressed then kill the analysis
        '''
        if frame > 1000:
            break
        if cv2.waitKey(1) & 0xFF == ord('q'): #press q to quit
            break
        
    print("Daemon Exiting")

    
    


#Create all cv2 stuff
video = "videos/MITest.mp4"
cam = cv2.VideoCapture(video)
# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*"XVID")
#Set to False for edge detection
#cv2.VideoWriter('output.avi',fourcc,fps,(width,height),false)
out = cv2.VideoWriter('output.avi',fourcc, 30.0, (440, 360), False)

#Make Threads
d = threading.Thread(name="OpenCV", target= daemonVideoProcessing(cam, out))
d.setDaemon(True)
d.start()


d.join()
#Desgtroy all cv2 stuff
cam.release()
out.release()
cv2.destroyAllWindows()

