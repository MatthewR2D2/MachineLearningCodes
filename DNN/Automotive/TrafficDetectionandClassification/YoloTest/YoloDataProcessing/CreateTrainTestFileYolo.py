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

import glob, os

# Current directory
# '<Your Dataset Path>'
currentDir = "YoloTrainingFiles/FullDataset/"

# Directory where the data will reside, relative to 'darknet.exe'
pathData = "YoloTrainingFiles/FullDataset/"

# Percentage of images to be used for the test set
percentageTest = 10;

# Create and/or truncate train.txt and test.txt
fileTrain = open('train.txt', 'w')
fileTest = open('test.txt', 'w')

# Populate train.txt and test.txt
counter = 1
indexTest = round(100 / percentageTest)
for pathAndFilename in glob.iglob(os.path.join(currentDir, "*.png")):
    title, ext = os.path.splitext(os.path.basename(pathAndFilename))

    if counter == indexTest:
        counter = 1
        fileTest.write(pathData + title + '.png' + "\n")
    else:
        fileTrain.write(pathData + title + '.png' + "\n")
        counter = counter + 1