# -*- coding: utf-8 -*-
"""
Created on Mon Jul 17 17:02:58 2017

@author: user
"""

from pandas import read_csv
from pandas import datetime
from pandas import DataFrame
from statsmodels.tsa.arima_model import ARIMA
from matplotlib import pyplot
import datetime

def dateparse (time_in_secs):    
    return datetime.datetime.fromtimestamp(float(time_in_secs))

series = read_csv('2017-1-3-tkr.txt', usecols=[0,2], header=0,  squeeze=True, nrows=10000, parse_dates=True,date_parser=dateparse, index_col='DateTime', names=['DateTime', 'X'])
series.columns=['X']
print(series)
series = series.astype('float32')

# fit model
model = ARIMA(series, order=(120,1,0))
model_fit = model.fit(disp=0)
print(model_fit.summary())
# plot residual errors
residuals = DataFrame(model_fit.resid)
residuals.plot()
pyplot.show()
residuals.plot(kind='kde')
pyplot.show()
print(residuals.describe())