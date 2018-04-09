# -*- coding: utf-8 -*-
"""
Created on Sat Apr  7 10:37:07 2018

@author: Matthew
"""

from statistics import mean
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style

style.use('ggplot')

xs = np.array([1,2,3,4,5], dtype=np.float64)
ys = np.array([5,4,6,5,6], dtype=np.float64)

#this build the best slope 
#adding interceptioin into equation
def best_fit_slope_and_intercept(xs,ys):
    m = (((mean(xs)*mean(ys)) - mean(xs*ys)) /
         ((mean(xs)*mean(xs)) - mean(xs*xs)))
    b= mean(ys) - m*mean(xs)
    return m, b

#Methods for building R^2 modle
def squared_error(ys_orig,ys_line):
    return sum((ys_line - ys_orig) * (ys_line - ys_orig))

def coefficient_of_determination(ys_orig,ys_line):
    y_mean_line = [mean(ys_orig) for y in ys_orig]
    squared_error_regr = squared_error(ys_orig, ys_line)
    squared_error_y_mean = squared_error(ys_orig, y_mean_line)
    return 1 - (squared_error_regr/squared_error_y_mean)
    



m, b = best_fit_slope_and_intercept(xs,ys)
print(m, b)

#y=mx+b for all values
regression_line = [(m*x)+b for x in xs]

#Find R^2
r_squared = coefficient_of_determination(ys,regression_line)
print(r_squared)


plt.scatter(xs,ys,color='#003F72')
plt.plot(xs, regression_line)
plt.show()

predict_x =7
predict_y = (m*predict_x) + b
print(predict_y)
plt.scatter(xs,ys,color='#003F72',label='data')
plt.plot(xs, regression_line, label='regression line')
plt.legend(loc=4)
plt.show()





