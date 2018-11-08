# -*- coding: utf-8 -*-
"""
Created on Fri Jun  1 13:10:13 2018
How to use MyFirstPredictor
A custom ML algo for binary prediction
@author: Matthew

"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import ListedColormap

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
        
    



#function for ploting decision regions
        
def plot_decision_regions(X, y, classifier, reolution = 0.02):
    markers = ('s', 'x', 'o', '^', 'v')
    colors = ('red', 'blue', 'lightgreen', 'grey', 'cyan')
    cmap = ListedColormap(colors[:len(np.unique(y))])
    
    x1_min, x1_max = X[:, 0].min() - 1, X[:,0].max() + 1
    x2_min, x2_max = X[:, 1].min() - 1, X[:,1].max() + 1
    xx1, xx2 = np.meshgrid(np.arange(x1_min, x1_max, reolution),
                           np.arange(x2_min, x2_max, reolution))
    Z = classifier.predict(np.array([xx1.ravel(), xx2.ravel()]).T)
    Z = Z.reshape(xx1.shape)
    plt.contour(xx1, xx2, Z, alpha=0.4, cmap= cmap)
    plt.xlim(xx1.min(), xx1.max())
    plt.ylim(xx2.min(), xx2.max())
    #Plot class samples
    for idx, cl in enumerate(np.unique(y)):
        plt.scatter(x=X[y == cl, 0], y=X[y == cl, 1],
                    alpha = 0.8, c = cmap(idx),
                    edgecolor = 'black',
                    marker = markers[idx],
                    label = cl)
        

#get and print data
df = pd.read_csv('https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data', header=None)
print(df.tail())

#select set osa and versicolor
y = df.iloc[0:100, 4].values
y = np.where(y == 'Iris-setosa', -1, 1)

#extract the data sepal length and petal length
X = df.iloc[0:100, [0,2]].values

#plot data
plt.scatter(X[: 50, 0], X[:50,1], color = 'red', marker='o', label='setosa')
plt.scatter(X[50:100, 0], X[50:100, 1], color = 'blue', marker = 'x', label = 'versicolor')

#Make table
plt.xlabel('Sepal Length')
plt.ylabel('Petal Length')
plt.legend(loc='upper left')

plt.tight_layout()
plt.show()

#Training myfirstpredictor
ppn = MyFirstPredictor(eta = 0.1, n_iter = 10)

ppn.fit(X,y)

plt.plot(range(1, len(ppn.errors) + 1), ppn.errors, marker='o')
plt.xlabel('Epochs')
plt.ylabel('Nymber of updates')
plt.tight_layout()
plt.show()

#Plot regions using method
plot_decision_regions(X, y, classifier = ppn)
plt.xlabel('Sepal Length')
plt.ylabel('Petal Length')
plt.legend(loc='upper left')

plt.tight_layout()
plt.show()






