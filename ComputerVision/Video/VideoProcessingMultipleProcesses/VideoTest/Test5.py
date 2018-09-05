# -*- coding: utf-8 -*-
"""
Created on Fri Aug 24 15:06:12 2018
@author: Matthew Millar
What it does:
What it needs:
Related Classes:

"""


from imutils.video import VideoStream
import face_recognition
import imutils
import pickle
import cv2
import threading


def daemonVideoProcessing(cam, out, data):
    print("Daemon Video Processing Starting")
    frame = 0
    while(True): 
    
        #print("Reading video....")
        ret, img = cam.read()
        # convert the input frame from BGR to RGB then resize it to have
        # a width of 750px (to speedup processing)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        rgb = imutils.resize(frame, width=750)
        r = frame.shape[1] / float(rgb.shape[1])
        
        # detect the (x, y)-coordinates of the bounding boxes
        # corresponding to each face in the input frame, then compute
        #the facial embeddings for each face
        boxes = face_recognition.face_locations(rgb,model=detectionMethod)
        encodings = face_recognition.face_encodings(rgb, boxes)
        names = []

        # loop over the facial embeddings
        for encoding in encodings:
            # attempt to match each face in the input image to our known	# encodings
            matches = face_recognition.compare_faces(data["encodings"],
                                                     encoding)
            name = "Unknown"

        # check to see if we have found a match
            if True in matches:
                # find the indexes of all matched faces then initialize a
                # dictionary to count the total number of times each face
                # was matched
                matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                counts = {}

                # loop over the matched indexes and maintain a count for
                # each recognized face face
                for i in matchedIdxs:
                    name = data["names"][i]
                    counts[name] = counts.get(name, 0) + 1

                # determine the recognized face with the largest number
			       # of votes (note: in the event of an unlikely tie Python
			       # will select first entry in the dictionary)
                name = max(counts, key=counts.get)
		
		      # update the list of names
            names.append(name)

	# loop over the recognized faces
        for ((top, right, bottom, left), name) in zip(boxes, names):
		# rescale the face coordinates
            top = int(top * r)
            right = int(right * r)
            bottom = int(bottom * r)
            left = int(left * r)

    # draw the predicted face name on the image
            cv2.rectangle(frame, (left, top), (right, bottom),(0, 255, 0), 2)
            y = top - 15 if top - 15 > 15 else top + 15
            cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,0.75, (0, 255, 0), 2)
        
      
        #print("Writing to file")
        out.write(frame)
        #Display theimage 
        cv2.imshow('img',frame)
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
videoinput = "D:/MLDataset/ImageAnalysis/FaceRecognition/TestData/Tom Cruise/Mission Impossible - Fallout (2018) - Official Trailer - Paramount Pictures.mp4"
videooutput = "output.avi"
#Load Encoding
display = 1
detectionMethod = 'cnn' #This can be either cnn for GPU use for Hog for cpu
print("Loading Encoding...")
data = pickle.loads(open("encodings.pickle", "rb").read())



cam = cv2.VideoCapture(videoinput)

#Get frame width

w = cam.get(cv2.CAP_PROP_FRAME_WIDTH)
h = cam.get(cv2.CAP_PROP_FRAME_HEIGHT)
print("H= {}  and W = {}".format(w,h))
# Define the codec and create VideoWriter object
#fourcc = cv2.VideoWriter_fourcc(*"XVID")
#Set to False for edge detection
#cv2.VideoWriter('output.avi',fourcc,fps,(width,height),false)
#out = cv2.VideoWriter(videooutput,fourcc, 30.0, (440, 360), False)
fourcc = cv2.VideoWriter_fourcc(*"MJPG")
out = cv2.VideoWriter(videooutput, fourcc, 30 ,(720, 1280), True)

#Make Threads
d = threading.Thread(name="OpenCV", target= daemonVideoProcessing(cam, out, data))
d.setDaemon(True)
d.start()


d.join()
#Desgtroy all cv2 stuff
cam.release()
out.release()
cv2.destroyAllWindows()

