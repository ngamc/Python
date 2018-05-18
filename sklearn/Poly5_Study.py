# -*- coding: utf-8 -*-
"""
Created on Fri May 18 10:58:14 2018

This is to use sklearn to solve 5 degree polynomial problem

@author: user
"""

import numpy as np
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import PolynomialFeatures 
from sklearn.linear_model import LinearRegression 
import matplotlib.pyplot as plt
import sys

train_size=50
max_number=100
m, n, o, p, q, b = -1, -2, 4, 1, 0, 10
mean,std = 0, 0.1
#np.random.seed(7)          # No random


x_train_list=[[]]
y_train_list=[]
x_test_list=[[]]
y_test_list=[]

for i in range(train_size):
    r = np.random.uniform(0,max_number)
#    rm = r/max_number                  # normalize x
    rm = r
    if (len(x_train_list[0])==0):
        x_train_list=[[rm]]
    else:
        x_train_list.append([rm])
    noise = np.random.normal(mean, std)
    y_train_list.append(rm*m + rm**2*n + rm**3*o + rm**4*p + rm**5*q + b + noise)
        

for i in range(train_size):
    r=np.random.uniform(0,max_number)
#    rm = r/max_number                  # normalize x
    rm = r
    if (len(x_test_list[0])==0):
        x_test_list=[[rm]]
    else:
        x_test_list.append([rm])
    noise = np.random.normal(mean, std)
    y_test_list.append(rm*m + rm**2*n + rm**3*o + rm**4*p + rm**5*q + b + noise)
    
x_train = np.array(x_train_list)
y_train = np.array(y_train_list)
x_test = np.array(x_test_list)
y_test = np.array(y_test_list)

print(x_train.shape)
print(y_train.shape)
print(x_test.shape)
print(y_test.shape)

print(x_train[0][0])
print(y_train[0])

quadratic_featurizer = PolynomialFeatures(degree = 9) 
x_train_quadratic = quadratic_featurizer.fit_transform(x_train) 
x_test_quadratic = quadratic_featurizer.transform(x_test) 
regressor_quadratic = LinearRegression() 
regressor_quadratic.fit(x_train_quadratic, y_train)


y_predit=regressor_quadratic.predict(x_test_quadratic)
print('MSE:  %.2f' % mean_squared_error(y_test, y_predit) )

print('coeff', regressor_quadratic.coef_)
print('b', regressor_quadratic.intercept_)


xx = np.linspace(-max_number, max_number, 100) 
xx_quadratic = quadratic_featurizer.transform(xx.reshape(xx.shape[0], 1)) 
yy_quadratic = regressor_quadratic.predict(xx_quadratic) 

plt.axis([0, max_number, 0, (max_number*m + max_number**2*n + max_number**3*o + max_number**4*p
                             + max_number**5*q + b)]) 
plt.scatter(x_train, y_train) 
plt.plot(xx_quadratic[:,1], yy_quadratic) 
plt.title("Using SKLearn to estimate Polynomial") 
plt.xlabel("X") 
plt.ylabel("Y") 
plt.grid(True) 
plt.show()
