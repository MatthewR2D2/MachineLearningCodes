#!/usr/bin/env python

'''
# Short Description@
# 
# Full Description@
    Load The Data.
    Dataset Summary & Exploration
    Data Preprocessing.
    Design a Model Architecture.
        LeNet-5.
    Model Training and Evaluation.
    Testing the Model Using the Test Set.

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


# Get all the data from the testing and training data sets
import pickle
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from DataScripts import PreprocessData as predata
from Model.LeNET2 import LeNet

'''
Data can be downloaded from here
https://d17h27t6h515a5.cloudfront.net/topher/2017/February/5898cd6f_traffic-signs-data/traffic-signs-data.zip
'''
# Data set locations and paths
trainingPath = "TrainingData/train.p"
testingPath = "TrainingData/test.p"

# Get the data from the data sets using pickle to read them in
with open(trainingPath, mode="rb") as training_data:
    train = pickle.load(training_data)

with open(testingPath, mode="rb") as testing_data:
    test = pickle.load(testing_data)

# Create the features and labels for the data and link them
x_train, y_train = train['features'], train['labels']
x_test, y_test = test['features'], test['labels']

print("x_train shape:", x_train.shape)
print("y_train shape:", y_train.shape)
print("x_test shape:", x_test.shape)
print("y_test shape:", y_test.shape)


# Define number of training samples and number of testing samples
num_train = len(x_train)
num_test = len(x_test)
# Define the number of classes (only the unique vales in y sets)
num_classes = len(np.unique(y_train))

# Define the image shape and data shape
image_shape = x_train[0].shape
print("Num of Training Samples:{} - Num of Test Sample:{} - Num Of classes:{}".format(num_train, num_test, num_classes))

'''
Do simple data exploration
'''
# histogram of label frequency Simple data exploration
hist, bins = np.histogram(y_train, bins=num_classes)
width = 0.7 * (bins[1] - bins[0])
center = (bins[:-1] + bins[1:]) / 2
plt.bar(center, hist, align='center', width=width)
plt.show()


# Process all the data and create validation data
x_train, y_train, x_test_normalized, x_validation, y_validation = predata.preprocessData(x_train, y_train, x_test)


# Build LeNET Model requirements
EPOCHS = 60
BATCH_SIZE = 100
rate = 0.0009 # Learning rate
tf.reset_default_graph()
# Tensor placehoders
x = tf.placeholder(tf.float32, (None, 32, 32, 1)) # Define shape of a image 32X32
y = tf.placeholder(tf.int32, (None))              # Class label
keep_prob = tf.placeholder(tf.float32)            # probability to keep units
keep_prob_conv = tf.placeholder(tf.float32)       # control the dropout rate
one_hot_y = tf.one_hot(y, 43)                     # create onehot encoding for y values 43 different values/signs


# Start the training
# Create a LeNet model
LeNet_Model = LeNet(x,y,  n_out=num_classes, mu=0, sigma=0.1, learning_rate=rate)
saved_model_path = "Model/SavedModels/LaNET_Model"

print("X train", x_train.shape)
print("Y train", y_train.shape)

# Start the training session
with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    num_examples = len(y_train)
    print("Training ...")
    print()
    for i in range(EPOCHS):
        for offset in range(0, num_examples, BATCH_SIZE):
            end = offset + BATCH_SIZE
            batch_x, batch_y = x_train[offset:end], y_train[offset:end]
            sess.run(LeNet_Model.training_operation,
                     feed_dict={x: batch_x, y: batch_y, keep_prob: 0.5, keep_prob_conv: 0.7})

        validation_accuracy = LeNet_Model.evaluate(y, x_validation, y_validation, keep_prob, keep_prob_conv, BATCH_SIZE)
        print("EPOCH {} : Validation Accuracy = {:.3f}%".format(i + 1, (validation_accuracy * 100)))
    LeNet_Model.saver.save(sess, saved_model_path)
    print("Model saved")


# Test saved model with new data
with tf.Session() as sess:
    LeNet_Model.saver.restore(sess, saved_model_path)
    y_pred = LeNet_Model.y_predict(x_test_normalized, keep_prob, keep_prob_conv,  BATCH_SIZE)
    test_accuracy = sum(y_test == y_pred)/len(y_test)
    print("Test Accuracy = {:.1f}%".format(test_accuracy*100))