#!/usr/bin/env python

'''
# Short Description@
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

class JsonParser:
    def parseData(jsonFile):
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


    if __name__ == "__main__":
        imageFile = "Test.png"
        jsonFile = "test.json"
        # Open image for testing
        img = cv2.imread(imageFile)
        annotatedObjects = parseData(jsonFile)


        for (label, box) in annotatedObjects:
            print(label)
            print(box)
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