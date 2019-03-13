#!/usr/bin/env python

'''
# Short Description@ This will preprocess the data into a useful form It is not for use during the yolo training
# 
# Full Description@
# 
__author__ = "Matthew Millar"
__copyright__ = ""
__credits__ =
__license__ = ""
__version__ = "0.0.0"
__maintainer__ = "Matthew Millar"
__email__ = "matthew.millar@igniterlabs.com"
__status__ = "Dev"

'''

import json
import cv2
import os


class DetectionObect():
    def __init__(self, label, bbox):
        self.label = label
        self.bbox = bbox


# This will parse out the label as well as the bounding box from the annotated data
def parseData(jsonFile, listOfAllAnnotation):
    with open(jsonFile, "r") as file:
        data = json.load(file)

        # Check to see if the review has passed
        if data['review_status'] == "pass":
            # Check to see if there is data
            if data['annotated_data'] != None:
                # Loop through each item in the annotated data
                for item in data['annotated_data']:
                    #print(" Label", item['label'])
                    # print(item['bounding_box_data'])
                    for bbox in item['bounding_box_data']:
                        boxValue = list(bbox.values())
                        listOfAllAnnotation.append((item['label'], boxValue))

def singleImageParseData(jsonFile):
    annotatedObjects = []
    with open(jsonFile, "r") as file:
        data = json.load(file)

        # Check to see if the review has passed
        if data['review_status'] == "pass":
            # Check to see if there is data
            if data['annotated_data'] != None:
                # Loop through each item in the annotated data
                for item in data['annotated_data']:
                    print(" Label", item['label'])
                    # print(item['bounding_box_data'])
                    for bbox in item['bounding_box_data']:
                        boxValue = list(bbox.values())
                        annotatedObjects.append((item['label'], boxValue))

        return annotatedObjects

# This will get a list of all unique values for every image to get all labels
def getUniqueLabels(uniqueLables, allLabels):
    for lables in allLabels:
        for addedLables in uniqueLables:
            if addedLables != lables:
                uniqueLables.append(lables)
            else:
                break

# This loops over every file and parses out the json information that I need
def loopOverAllFile(annotation, listOfAllAnnotation):
    for filename in os.listdir(annotation):
        #print("File: ", filename)
        path =  annotation + filename
        parseData(path, listOfAllAnnotation)



if __name__ == "__main__":

    annotatedDataPath = "AnnotatedData/"
    imageData = "ImageData/"

    imageFile = "Test.png"
    jsonFile = "test.json"
    # Open image for testing
    img = cv2.imread(imageFile)
    annotatedObjects = singleImageParseData(jsonFile)
    print("Annotated Object Example")
    print(annotatedObjects)


    for (label, box) in annotatedObjects:
        #print(label)
        #qprint(box)
        x = box[0]
        y = box[1]
        w = box[2]
        h = box[3]
        cv2.rectangle(img, (x, y), (x + w, y + h), (255,255,0), 2)
        cv2.putText(img, label, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (255,255,0), 2)

    cv2.imshow("Result", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    myObject = []
    loopOverAllFile(annotatedDataPath, myObject)
    print("Test")
    print(myObject[0])


