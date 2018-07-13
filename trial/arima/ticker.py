# -*- coding: utf-8 -*-
"""
Created on Fri Jul 14 11:22:39 2017

@author: user
"""

from pandas import read_csv
from pandas import datetime
import datetime
from matplotlib import pyplot
from pandas.tools.plotting import autocorrelation_plot

def dateparse (time_in_secs):    
    return datetime.datetime.fromtimestamp(float(time_in_secs))

#series = read_csv('P:\\HSI\\2018\\7\\2018-7-11-tkr.txt', usecols=[0,2], header=0,  squeeze=True,  parse_dates=True,date_parser=dateparse, index_col='DateTime', names=['DateTime', 'X'])


for i in range(60,600,10):
    series = read_csv('P:\\HSI\\2018\\7\\2018-7-4-one_min.txt', usecols=[4], header=0,  nrows=i, squeeze=True,  parse_dates=False, sep=';', names=['X'])
    
    
#    print(series)
    autocorrelation_plot(series)
    pyplot.show()