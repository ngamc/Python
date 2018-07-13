# -*- coding: utf-8 -*-
"""
Created on Wed Jun 20 14:43:16 2018

@author: user
"""
import sys
sys.path.append('../HKStock')
from datetime import date
from mpl_finance import candlestick2_ohlc, candlestick2_ochl
from getyahoodata import GetYahooData
from stockstats import StockDataFrame as Sdf
import matplotlib.pyplot as plt
import pandas as pd


if __name__ == '__main__':
    df = GetYahooData('0001.HK', date(2017,1,1))
    s_df = Sdf.retype(df)
    df['sma'] = s_df['close_30_sma'] 
    sma = df['sma'].values


#    Use this one if date and time is needed
#    df.set_index('Date', inplace=True)
    df.index = pd.to_datetime(df.index)

    
    # use this one if one date is need, but not time
#    df['date'] = pd.to_datetime(df['date'])
#    df.index = df['date'].dt.date
    

    


    fig, ax = plt.subplots(figsize=(15, 10))            # Set picture size


    candlestick2_ohlc(ax, df['open'],df['high'],df['low'],df['close'], width=0.3, colorup='r', colordown='g')

    # x label should be date instead of numbers
    steps = int(len(df.index)/20)           # 20 is total x labels 
    ax.set_xticks(range(0, len(df.index), steps))
    ax.set_xticklabels(df.index)
    ax.plot(sma)
    fig.autofmt_xdate()
    
#    ax.plot(df['sma'])

    plt.show()
    
    