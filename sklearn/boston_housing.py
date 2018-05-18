# -*- coding: utf-8 -*-
"""
Created on Fri May 18 15:28:54 2018

Boston House Dataset testing using sklearn

@author: user
"""
from keras.datasets import boston_housing
from sklearn import svm
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

(x_train, y_train),(x_test, y_test) = boston_housing.load_data()


# using SVR, LinearSVR
#clf = svm.LinearSVR()
#clf.fit(x_train, y_train)
#y_predict = clf.predict(x_test)

# using Linear Regression
lr = LinearRegression()
lr.fit(x_train, y_train)
y_predict = lr.predict(x_test)

print("MSE: ", mean_squared_error(y_test, y_predict))

