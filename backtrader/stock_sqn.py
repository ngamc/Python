# -*- coding: utf-8 -*-
"""
Created on Tue Mar 27 16:20:54 2018

@author: user
"""

	
'''
Author: www.backtest-rookies.com
 
MIT License
 
Copyright (c) 2018 backtest-rookies.com
 
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
 
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
 
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''
import math
import pandas as pd
from datetime import date
from getyahoodata import GetYahooData
from backtrader.mathsupport import average, standarddev
import matplotlib.pyplot as plt




if __name__=='__main__':
    #
    # Define equity and start date of equity data
    equity="^HSI"
    startdate=date(2017,1,1)
         
    
    print("\r\n\r\n     ==== Testing with stock", equity, " ====\r\n")
    df=pd.DataFrame()
    df_result=pd.DataFrame(columns=['Date', 'sqn', 'Close'])
    
    df=GetYahooData(equity, startdate )
    
    df['pertchange']=(df['Close']-df['Close'].shift(1)) / df['Close'] * 100  

#    count = 0
    print('len(df):' , len(df))
    for x in range(1, len(df)-99):
        pnl = list()
        for i in df['pertchange'][x:x+99]:
            pnl.append(i)
        
    #    print("pnl", pnl) 
        pnl_av = average(pnl)
        pnl_stddev = standarddev(pnl)
#        print("pnl_av: ", pnl_av, "pnl_stddev", pnl_stddev)
        
        try:
            sqn = math.sqrt(len(pnl)) * pnl_av / pnl_stddev
        except ZeroDivisionError:
            sqn = None
            print("ZeroDivisionError")
        print(x, df['Date'][x+99],': SQN: %.2f '% sqn, 'Closing: %.2f'% df['Close'][x+99])
        
        df_result=df_result.append({'Date':df['Date'][x+99], 'sqn': sqn, 'Close':df['Close'][x+99] }, 
                                    ignore_index=True)
        
#    df_result=df_result.set_index('Date')
#    print(df_result)
        
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax1.plot(df_result['sqn'], label = "SQN(99)")
    ax1.set_ylabel('y1')
    
    ax2 = ax1.twinx()
    ax2.plot(df_result['Close'], 'r-', label = equity)
    ax2.set_ylabel('y2', color='r')
    for tl in ax2.get_yticklabels():
        tl.set_color('r')
    ax1.legend(loc='upper center', bbox_to_anchor=(0.35, -0.05))
    ax2.legend(loc='upper center', bbox_to_anchor=(0.7, -0.05))
    plt.show()
    
#    df_result.plot()
