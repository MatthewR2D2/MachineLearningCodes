# -*- coding: utf-8 -*-
"""
Created on Wed Sep 12 07:44:54 2018
@author: Matthew Millar
What it does:
What it needs:
Related Classes:

"""

import tensorflow as tf
import gym
import numpy as np

#Varialbes
numInput = 4
numHidden =4
numOutput =1 #Prob to go left 1-left = right

initializer = tf.contrib.layers.variance_scaling_initializer()

X = tf.placeholder(tf.float32, shape=[None,numInput])

hiddenLayerOne = tf.layers.dense(X, numHidden,activation=tf.nn.relu,
                                 kernel_initializer= initializer)

hiddenLayerTwo = tf.layers.dense(hiddenLayerOne, numHidden,activation=tf.nn.relu,
                                 kernel_initializer= initializer)

#Use sigmoid as the output is binary
outputLayer = tf.layers.dense(hiddenLayerTwo, numOutput, activation=tf.nn.sigmoid,
                              kernel_initializer=initializer)

#Outputlayer = probability to go left
#1-outputlayer = probability to goright
probabilities = tf.concat(axis = 1, values= [outputLayer, 1-outputLayer])
#Bring back a single action
action = tf.multinomial(probabilities,num_samples=1)

init = tf.global_variables_initializer()

stepLimit =500
#Runs for 50 times
epi = 50 
avgStep = []


env = gym.make('CartPole-v0')

with tf.Session() as sess:
    init.run()
    
    for episode in range(epi):
        obs = env.reset()
        for step in range(stepLimit):
            actionVal = action.eval(feed_dict = {X: obs.reshape(1, numInput)})
            #Index o/1
            obs, reward, done, info = env.step(actionVal[0][0])
            
            if done:
                avgStep.append(step)
                print("Done after {} steps".format(step))
                break
            
print("After {} Episdoes, the average steps per game was {}".format(epi,np.mean(avgStep)))
env.close()





