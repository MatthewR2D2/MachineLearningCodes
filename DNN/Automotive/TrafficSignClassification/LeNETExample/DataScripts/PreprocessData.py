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
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
import numpy as np

'''
Flow of preprocessing data
Step1: GrayScale.
Step2: Normalize the image
Step3: Shuffle the data
Step4: Split into train and validate test images
'''

def preprocessData(x_train, y_train, x_test):
    # Convert to grayscale
    x_train_rgb = x_train
    x_train_gry = np.sum(x_train / 3, axis=3, keepdims=True)

    x_test_rgb = x_test
    x_test_gry = np.sum(x_test / 3, axis=3, keepdims=True)

    print('RGB:', x_train_rgb.shape)
    print('Grayscale:', x_train_gry.shape)

    x_train = x_train_gry
    x_test = x_test_gry

    ## Normalize the train and test datasets to (-1,1)

    x_train_normalized = (x_train - 128) / 128
    x_test_normalized = (x_test - 128) / 128

    ## Shuffle the training dataset and create the validation set
    # Validatioin set will not be used by Training

    x_train_normalized, y_train = shuffle(x_train_normalized, y_train)
    x_train, x_validation, y_train, y_validation = train_test_split(x_train_normalized, y_train,
                                                                    test_size=0.20, random_state=42)

    print("Old X_train size:", len(x_train_normalized))
    print("New X_train size:", len(x_train))
    print("X_validation size:", len(x_validation))
    return x_train,y_train, x_test_normalized, x_validation, y_validation