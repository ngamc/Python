# -*- coding: utf-8 -*-
"""
Created on Fri May 11 11:27:07 2018
Try out  IRIS database with sklearn

@author: Nelson Cheung
"""

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.metrics import mean_squared_error

# configs
epoch_number=1000;
batch_size=10



# Coding starts
iris = load_iris()
x = iris.data
y = iris.target
name = iris.target_names
desc = iris.DESCR
feature = iris.feature_names


x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.33)

#print(x_train)
#print(y_train)

clf = svm.SVC()
clf.fit(x_train, y_train) 

y_predict = clf.predict(x_test)

print('MSE:  %.2f' % mean_squared_error(y_test, y_predict) )
