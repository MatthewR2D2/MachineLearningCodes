# -*- coding: utf-8 -*-
"""
Created on Fri Apr  6 19:52:37 2018

@author: Matthew
"""
import math
import numpy as np
import pandas as pd
import quandl as q 
import datetime
import matplotlib.pyplot as plt
import pickle

from   matplotlib import style
from sklearn import preprocessing, cross_validation, svm
from sklearn.linear_model import LinearRegression


#Simple Regersion Starter

#set the data frame styel
style.use('ggplot')
#get the data for google ticker
df = q.get("WIKI/GOOGL")

#Modify the data to work with machine learning
df = df[['Adj. Open',  'Adj. High',  'Adj. Low',  'Adj. Close', 'Adj. Volume']]
df['HL_PCT'] = (df['Adj. High'] - df['Adj. Low']) / df['Adj. Close'] * 100.0
df['PCT_change'] = (df['Adj. Close'] - df['Adj. Open']) / df['Adj. Open'] * 100.0

df = df[['Adj. Close', 'HL_PCT', 'PCT_change', 'Adj. Volume']]
forecast_col = 'Adj. Close'
df.fillna(value=-99999, inplace=True)
forecast_out = int(math.ceil(0.01 * len(df)))
df['label'] = df[forecast_col].shift(-forecast_out)

#Create and traing a classifier
X = np.array(df.drop(['label'], 1))
X = preprocessing.scale(X)
X_lately = X[-forecast_out:]
X = X[:-forecast_out]
df.dropna(inplace=True)
y = np.array(df['label'])
X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.2)

#Linear model test1
#Training and building it is stored in the linearregerssion.pickle file
#Need to run this once to build and create pickel
#clf = LinearRegression(n_jobs=-1)
#clf.fit(X_train, y_train)
#confidence = clf.score(X_test, y_test)
#with open('linearregression.pickle','wb') as f:
 #   pickle.dump(clf, f)

#load the trained modle

pickle_in = open('linearregression.pickle','rb')
clf = pickle.load(pickle_in)



#Predictor modle
forecast_set = clf.predict(X_lately)

#add forecast column to Dataframe
df['Forecast'] = np.nan

last_date = df.iloc[-1].name
last_unix = last_date.timestamp()
one_day = 86400 #One day is 86400 seconds
next_unix = last_unix + one_day

#So here all we're doing is iterating through the forecast set,
#taking each forecast and day, and then setting those values in the dataframe

for i in forecast_set:
    next_date = datetime.datetime.fromtimestamp(next_unix)
    next_unix += 86400
    df.loc[next_date] = [np.nan for _ in range(len(df.columns)-1)]+[i]

df['Adj. Close'].plot()
df['Forecast'].plot()
plt.legend(loc=4)
plt.xlabel('Date')
plt.ylabel('Price')
plt.show()



