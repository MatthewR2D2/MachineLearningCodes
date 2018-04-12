# -*- coding: utf-8 -*-
"""
Created on Thu Apr 12 20:20:23 2018

@author: Matthew
"""

import numpy as np
from sklearn import preprocessing, cross_validation, neighbors
import pandas as pd

#Clean data and get rid of incomplet or null data
df = pd.read_csv('knn_test_data.txt')
df.replace('?',-99999, inplace=True)
df.drop(['id'], 1, inplace=True)

#Lables
X = np.array(df.drop(['class'], 1))
y = np.array(df['class'])

#Training
X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.2)

#Make clasifier
clf = neighbors.KNeighborsClassifier()
clf.fit(X_train, y_train)

#Test
accuracy = clf.score(X_test, y_test)
print(accuracy) #gets 97% accuracy no updates