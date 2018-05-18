# -*- coding: utf-8 -*-
"""
Created on Tue May 15 17:21:51 2018

Using SciKit Learn to solve linear regression


@author: user
"""

import numpy as np
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error
import sys

train_size=50
max_number=100
m, n, b = 5, 4, 3
mean,std = 0, 0.1
#np.random.seed(7)          # No random


x_train_list=[[]]
y_train_list=[]
x_test_list=[[]]
y_test_list=[]

for i in range(train_size):
    r = np.random.uniform(0,max_number)
    if (len(x_train_list[0])==0):
        x_train_list=[[r/max_number]]
    else:
        x_train_list.append([r/max_number])
    noise = np.random.normal(mean, std)
    y_train_list.append(r/max_number*m + b + noise)
        

for i in range(train_size):
    r=np.random.uniform(0,max_number)
    if (len(x_test_list[0])==0):
        x_test_list=[[r/max_number]]
    else:
        x_test_list.append([r/max_number])
    noise = np.random.normal(mean, std)
    y_test_list.append(r/max_number*m +  b + noise)
    
x_train = np.array(x_train_list)
y_train = np.array(y_train_list)
x_test = np.array(x_test_list)
y_test = np.array(y_test_list)

print(x_train.shape)
print(y_train.shape)
print(x_test.shape)
print(y_test.shape)

regr = linear_model.LinearRegression()

regr.fit(x_train, y_train)

y_predit=regr.predict(x_test)
print('MSE:  %.2f' % mean_squared_error(y_test, y_predit) )

m=regr.coef_[0]
b=regr.intercept_
print("slope= %.2f intercept= %.2f"% (m, b))

print('Predict 53 to %.2f' %(regr.predict([[10]])))

print('Coefficient: ', regr.coef_)
