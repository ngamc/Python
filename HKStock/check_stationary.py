# -*- coding: utf-8 -*-
"""
Created on Thu Jul 13 16:54:57 2017

@author: user
"""

from pandas import Series
from statsmodels.tsa.stattools import adfuller
from numpy import log
from pandas import read_csv
from matplotlib import pyplot

dataframe = read_csv('D:\\ticker\\2017-1-4-tkr.txt', usecols=[2], engine='python')
dataframe.hist()
pyplot.show()
#print(dataframe.iloc[:,0])
X = dataframe.iloc[:,0].values
#print(X)


#X = log(X)



result = adfuller(X)
print('ADF Statistic: %f' % result[0])
print('p-value: %f' % result[1])
for key, value in result[4].items():
	print('\t%s: %.3f' % (key, value))