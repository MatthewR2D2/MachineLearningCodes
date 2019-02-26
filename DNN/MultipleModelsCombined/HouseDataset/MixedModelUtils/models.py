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

from keras.models import Sequential
from keras.layers.normalization import BatchNormalization
from keras.layers.convolutional import Conv2D
from keras.layers.convolutional import MaxPooling2D
from keras.layers.core import Activation
from keras.layers.core import Dropout
from keras.layers.core import Dense
from keras.layers import Flatten
from keras.layers import Input
from keras.models import Model

# Create the Multi-layer Model
# This will handel numerical and categorical inputs
def createMLP(dim, regress = False):
    model = Sequential()
    model.add(Dense(8, input_dim= dim, activation= "relu"))
    model.add(Dense(4, activation="relu"))

    # Make it do linear regression
    if regress:
        model.add(Dense(1, activation="linear"))

    return model

# CNN for image processing
def createCNN(width, height, depth, filters=(16,32,64), regress = False):
    # Use Tensorflow channels last ordering
    # Define the input shape
    inputShape = (height, width, depth)
    chanDim = 1

    inputs = Input(shape=inputShape)

    for (i, f) in enumerate(filters):
        if i ==0:
            x = inputs

        # Conv -> relu -> bn -> pool
        x = Conv2D(f, (3,3), padding="same")(x)
        x = Activation("relu")(x)
        x = BatchNormalization(axis=chanDim)(x)
        x = MaxPooling2D(pool_size=(2, 2))(x)

        # flatten the volume, then FC => RELU => BN => DROPOUT
        x = Flatten()(x)
        x = Dense(16)(x)
        x = Activation("relu")(x)
        x = BatchNormalization(axis=chanDim)(x)
        x = Dropout(0.5)(x)

        # apply another FC layer, this one to match the number of nodes
        # coming out of the MLP
        x = Dense(4)(x)
        x = Activation("relu")(x)

        # check to see if the regression should be used
        if regress:
            x = Dense(1, activation="linear")(x)

        # build the CNN
        model = Model(inputs, x)

        # return the CNN
        return model