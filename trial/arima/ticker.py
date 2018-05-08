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

series = read_csv('2017-1-3-tkr.txt', usecols=[0,2], header=0,  squeeze=True, nrows=500, parse_dates=True,date_parser=dateparse, index_col='DateTime', names=['DateTime', 'X'])
print(series)
autocorrelation_plot(series)
pyplot.show()