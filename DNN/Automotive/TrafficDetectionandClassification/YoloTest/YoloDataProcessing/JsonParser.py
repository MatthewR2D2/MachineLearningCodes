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
        _, filename = jsonFile.split("/")
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
                        listOfAllAnnotation.append((filename, item['label'], boxValue))

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

# This get every label that is used in the data set
def getAllLables(annotatdedList):
    allLableList = []
    for items in annotatdedList:
        # Label is at 0 or first one
        allLableList.append(items[0])
    return allLableList


# This loops over every file and parses out the json information that I need
def loopOverAllFile(annotation, listOfAllAnnotation):
    for filename in os.listdir(annotation):
        #print("File: ", filename)
        path =  annotation + filename
        parseData(path, listOfAllAnnotation)



if __name__ == "__main__":

    annotatedDataPath = "AnnotatedData/"
    imageData = "ImageData/"
    output = "YoloTrainingFiles/"

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

    # Get every file and parse them into label and bbox for changing into yolo text file
    myObject = []
    loopOverAllFile(annotatedDataPath, myObject)

    # This section prepares all Yolo configuration files

    # Get the labels that are present
    allLables = getAllLables(myObject)
    # now find only the unique labels for training files
    uniqueLabel = list(set(allLables))
    print("Unique Lables", uniqueLabel)

    # Now create the object name file that use used for each category
    nameFile = "traffic-obj.names"
    writeNameFilePath = output+nameFile
    # Open a file
    if os.path.isfile(writeNameFilePath) == False:
        file = open(writeNameFilePath, "w+")
        # Write labels to file
        for label in uniqueLabel:
            file.write(label + "\n")
        # Close the writer
        file.close()
    else:
        print("Names file exists")


    # Create the yolov3.data file
    yolov3File = "traffic-obj-yolov3.data"
    yoloPath = output + yolov3File
    # Get the number of classes
    numClasses = len(uniqueLabel)
    trainFile = "traffic-train.txt"
    valid = "traffic-test.txt"
    # names will come from above file
    backup = "backup/"  # For darknet backpu where wieght will be

    dataString = "classes = {} \ntrain = {} \nvalid = {} \nnames = {} \nbackup = {}".format(numClasses, trainFile, valid, nameFile, backup)

    if os.path.isfile(yoloPath) == False:
        yoloFile = open(yoloPath, "w+")
        yoloFile.write(dataString)
        yoloFile.close()
    else:
        print("Yolo Data file exists")


    '''
    Van             0
    Bus             1
    Pedestrian      2
    Car             3
    Bicycle         4
    Motorcycle      5
    Truck           6
    
    Calculation
    <class_number>  0-6
    x = (<absolute_x> / <image_width>)  This is center point
    y = (<absolute_y> / <image_height>) This is the center point
    w = (<absolute_width> / <image_width>)
    h = (<absolute_height> / <image_height>)
    '''
    rawImageHeight = 1080
    rawImageWidth = 1440
    yoloFormatArray = []

    def findCenter(x, y, w, h):
        x2 = x + w
        y2 = y + h
        '''
        center = (x1 + x2)/2)(y1 + y2/2)
        '''
        xCenter = (x + x2)/2
        yCenter = (y + y2)/2
        return  xCenter, yCenter

    def calculateLabel(x):
        return {
            'Van': 0,
            'Bus': 1,
            'Pedestrian': 2,
            'Car': 3,
            'Bicycle': 4,
            'Motorcycle': 5,
            'Truck': 6
        }.get(x, 2)  # 9 is default if x not found



    for object in myObject:
        #print(object)
        # get the x y w h values
        x = object[2][0]
        y = object[2][1]
        w = object[2][2]
        h = object[2][3]

        xCenter, yCenter = findCenter(x, y, w, h)
        newX = xCenter / rawImageWidth
        newY = yCenter / rawImageHeight
        abW = w / rawImageWidth
        abH = h / rawImageHeight
        labelNumber = calculateLabel(object[1])

        # Yolo Format needed <object-class> <x> <y> <width> <height>
        yoloString = "{} {} {} {} {}".format(labelNumber, newX, newY, abW, abH)
        #print("YoloString:{}".format(yoloString))
        # Get the file name to match with
        annotatedFileName = object[0].split(".p")[0]
        annotatedFileName = annotatedFileName+".txt"
        # Put the item into the formated yolo array
        yoloFormatArray.append((annotatedFileName, yoloString))

    textOutputFolder = "YoloTrainingFiles/ImageText/"
    # Now create a text file for training for each individual image
    for yoloObject in yoloFormatArray:

        trainPath = textOutputFolder+yoloObject[0]
        if os.path.isfile(trainPath) == False:
            writeDataPath = open(trainPath, "w+")
            writeDataPath.write(yoloObject[1])
            writeDataPath.close()
        else:
            # Append the other bbox to the file
            with open(trainPath, 'a') as file:
                file.write("\n"+yoloObject[1])



















