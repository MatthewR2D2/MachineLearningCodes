#!/usr/bin/env python

'''
# Short Description@ This is the helper code which will aid in the processing of the image and text datasets
# 
# Full Description@ This will give methods for loading and prepossessing the different datasets that are available
#                   This handles; image data, numerical, and categorical data
__author__ = "Matthew Millar"
__copyright__ = ""
__credits__ =
__license__ = ""
__version__ = "0.0.0"
__maintainer__ = "Matthew Millar"
__email__ = "matthew.millar@igniterlabs.com"
__status__ = "Dev"

'''

from sklearn.preprocessing import LabelBinarizer
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import numpy as np
import glob
import cv2
import os


def loadHouseAttributes(inputPath):

    # loads house values into pandas
    cols = ["bedrooms", "bathrooms", "area", "zipcode", "price"]
    df = pd.read_csv(inputPath, sep=" ", header=None, names=cols)

    # Get number of zipcodes and number of data points per zipcode
    zipcodes = df["zipcode"].value_counts().keys().tolist()
    counts = df["zipcode"].value_counts().tolist()

    for (zipcode, count) in zip(zipcodes, counts):
        # Rebalance the data set by removing any zipcode
        # that have less than 25 house per zipcode
        if count < 25:
            idxs = df[df["zipcode"] == zipcode].index
            df.drop(idxs, inplace=True)

    # return the data frame
    return df


def processHouseAttributes(df, train, test):
    # Create columns names of the continuous Data
    continuous = ["bedrooms", "bathrooms", "area"]

    # Min and max scale each feature to [0,1]
    cs = MinMaxScaler()
    trainContinuous = cs.fit_transform(train[continuous])
    testContinuous = cs.transform(test[continuous])

    # one-hot encode the zip code categorical data in the range [0, 1])
    zipBinarizer = LabelBinarizer().fit(df["zipcode"])
    trainCategorical = zipBinarizer.transform(train["zipcode"])
    testCategorical = zipBinarizer.transform(test["zipcode"])


    trainX = np.hstack([trainCategorical, trainContinuous])
    testX = np.hstack([testCategorical, testContinuous])

    # return the concatenated training and testing data
    return (trainX, testX)

def loadHouseImages(df, inputPath):
    images = []

    for i in df.index.values:
        basePath = os.path.sep.join([inputPath, "{}_*".format(i + 1)])
        housePaths = sorted(list(glob.glob(basePath)))
        inputImages = []
        outputImage = np.zeros((64, 64, 3), dtype="uint8")

        # loop over the input house paths
        for housePath in housePaths:
            # resize image to be 32x32,
            image = cv2.imread(housePath)
            image = cv2.resize(image, (32, 32))
            inputImages.append(image)

        # tile the four input images in the output image such the first
        # 1st image top-right corner, the
        # second image in the top-left corner,
        # the third image in the bottom-right corner,
        # the forth image in the bottom-left corner
        outputImage[0:32, 0:32] = inputImages[0]
        outputImage[0:32, 32:64] = inputImages[1]
        outputImage[32:64, 32:64] = inputImages[2]
        outputImage[32:64, 0:32] = inputImages[3]

        # add the tiled image to our set of images
        images.append(outputImage)

    # return our set of images
    return np.array(images)