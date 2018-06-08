# -*- coding: utf-8 -*-
"""
Created on Tue Mar 27 16:20:54 2018

Calculate the SQN of an equity

@author: user
"""

import math
import pandas as pd
from datetime import date
from getyahoodata import GetYahooData, GetYahooDataFromFile
from backtrader.mathsupport import average, standarddev
import matplotlib.pyplot as plt
import sys

default_num = 100   # this is the default number of trading day used to calculate sqn 


def sqn(equity, num=default_num, list_table=False, graph=True):
    #
    # Define equity and start date of equity data
#    equity="^HSI"
    startdate=date(2017,1,1)
         
    df=pd.DataFrame()
    df_result=pd.DataFrame(columns=['Date', 'sqn', 'Close'])
    
#    df=GetYahooData(equity, startdate )            # download from yahoo directly
    df=GetYahooDataFromFile(equity, startdate )             # read local files
    if not isinstance(df, pd.DataFrame):
        return None
    df = df[pd.notnull(df['Close'])]
    df = df.reset_index(drop=True)

    df['pertchange']=(df['Close']-df['Close'].shift(1)) / df['Close'] * 100  
    
    last_sqn = 0
#    count = 0
    if list_table:
        print('No of trading days:' , len(df))
    for x in range(1, len(df) - num - 1):
        pnl = list()
        for i in df['pertchange'][x : x + num]:
            pnl.append(i)
        
    #    print("pnl", pnl) 
        pnl_av = average(pnl)
        pnl_stddev = standarddev(pnl)
#        print("pnl_av: ", pnl_av, "pnl_stddev", pnl_stddev)
        
        try:
            sqn = math.sqrt(len(pnl)) * pnl_av / pnl_stddev
            if list_table:
                print(x, df['Date'][ x + num],': SQN: %.2f '% sqn, 'Closing: %.2f'% df['Close'][x + num])
            df_result=df_result.append({'Date':df['Date'][x+num], 'sqn': sqn, 'Close':df['Close'][x+num] }, 
                ignore_index=True)
        except ZeroDivisionError:
            sqn = None
            print("ZeroDivisionError")
            if list_table:
                print(x, df['Date'][ x + num],': SQN: Nan  Closing: %.2f'% df['Close'][x + num])
        
        if x == (len(df) - num -2):             # if this is the last number, we record the sqn number
            last_sqn = df_result['sqn'].iloc[-1]

    if graph: 
        fig = plt.figure()
#        df_result['Date'] = pd.to_datetime(df_result['Date'])
        df_result.set_index('Date', inplace=True)
        ax1 = fig.add_subplot(111)
        ax1.plot( df_result['sqn'], label = "SQN(99)")
        ax1.set_ylabel('y1')
        
        ax2 = ax1.twinx()
        ax2.plot(df_result['Close'], 'r-', label = equity)
        ax2.set_ylabel('y2', color='r')
        for tl in ax2.get_yticklabels():
            tl.set_color('r')
        ax1.legend(loc='upper center', bbox_to_anchor=(0.35, -0.05))
        ax2.legend(loc='upper center', bbox_to_anchor=(0.7, -0.05))
        ax1.set_title(equity)
        plt.show()
    
    return ("%.2f" % last_sqn)
    
if __name__=='__main__':
    equity = "0001.HK"
    print(sqn(equity, 100, True))
    
    
    