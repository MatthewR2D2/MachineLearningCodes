from keras.models import load_model
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras.preprocessing.image import img_to_array, load_img
import numpy as np
import tensorflow as tf


def process_image(image, model):
    img = load_img(image, False, target_size=(150, 150))
    x = img_to_array(img)
    x = x / 255  # Normalize image to match training set
    x = np.expand_dims(x, axis=0)
    preds = model.predict_classes(x)
    probs = model.predict_proba(x)
    return preds, probs


def make_model(input_shape):
    # Has to match model that is predition
    model = Sequential()
    model.add(Conv2D(32, (3, 3), input_shape=input_shape))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Conv2D(32, (3, 3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Conv2D(64, (3, 3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Flatten())
    model.add(Dense(64))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))
    model.add(Dense(4))
    model.add((Activation('sigmoid')))

    return model