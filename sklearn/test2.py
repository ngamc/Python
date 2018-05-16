# -*- coding: utf-8 -*-
"""
Created on Wed May 16 22:00:56 2018

@author: Nelson
"""

import numpy as np 
import matplotlib.pyplot as plt 
from sklearn.linear_model import LinearRegression 
from sklearn.preprocessing import PolynomialFeatures 

X_train = np.array([6, 8, 10, 14, 18]).reshape(-1, 1) 
Y_train = np.array([7, 9, 13, 17.5, 18]) 
X_test = np.array([6, 8, 11, 16]).reshape(-1, 1) 
Y_test = np.array([8, 12, 15, 18]) 
regressor_linear = LinearRegression() 
regressor_linear.fit(X_train, Y_train) 
xx = np.linspace(0, 25, 100) 
yy = regressor_linear.predict(xx.reshape(xx.shape[0], 1)) 
plt.plot(xx, yy) 
quadratic_featurizer = PolynomialFeatures(degree = 2) 
X_train_quadratic = quadratic_featurizer.fit_transform(X_train) 
X_test_quadratic = quadratic_featurizer.transform(X_test) 
regressor_quadratic = LinearRegression() 
regressor_quadratic.fit(X_train_quadratic, Y_train) 
xx_quadratic = quadratic_featurizer.transform(xx.reshape(xx.shape[0], 1)) 
yy_quadratic = regressor_quadratic.predict(xx_quadratic) 

print(xx_quadratic[:,1])
print(yy_quadratic) 

plt.plot(xx_quadratic[:,1], yy_quadratic) 
plt.title("Polynomial Vs Linear Regression") 
plt.xlabel("Pizza diameter") 
plt.ylabel("Pizza Price") 
plt.scatter(X_train, Y_train) 
plt.axis([0, 25, 0, 25]) 
plt.grid(True) 
plt.show()
