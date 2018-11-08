# -*- coding: utf-8 -*-
"""
Created on Fri Jun  1 12:41:27 2018

@author: Matthew
ML from Scratch no libs used
A Binary classifier
"""

import numpy as np
class MyFirstPredictor(object):

    #Parameters
    #eta: Float : Learning rate
    #n_iter: int : Number of passes over training data set
    
    #Attributes
    #w : weights after fitting
    #errors : Number of misclassification in every epoch
    
    def __init__(self, eta = 0.01, n_iter = 10):
        self.eta = eta
        self.n_iter = n_iter
    
    def fit(self, x, y):
        #Fit the training data
        self.w = np.zeros(1 + x.shape[1])
        self.errors = []
        
        for _ in range(self.n_iter):
            error = 0
            for xi, target in zip(x,y):
                update = self.eta * (target - self.predict(xi))
                self.w[1:] += update * xi
                self.w[0] += update
                error += int(update != 0.0)
            self.errors.append(error)
        return self
    
    def net_input(self, x):
        return np.dot(x, self.w[1:]) + self.w[0]
    
    def predict(self, x):
        return np.where(self.net_input(x) > 0.0, 1, -1)
        
    
