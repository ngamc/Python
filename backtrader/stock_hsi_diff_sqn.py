# -*- coding: utf-8 -*-
"""
Created on Tue Mar 27 16:20:54 2018

Blue line is the sqn of (equity - hsi )
Read line is equity value

@author: user
"""
import sys
sys.path.append('..\HKStock')
import math
import pandas as pd
from datetime import date
from getyahoodata import GetYahooData
from backtrader.mathsupport import average, standarddev
import matplotlib.pyplot as plt
import datetime

end=datetime.date.today()
p=99        # default period

def Stock_Hsi_Diff_Sqn(equity, startdate, enddate=end, period=p):
    index="^HSI"

    df1=pd.DataFrame()      # df1 is equity
    df2=pd.DataFrame()      # df2 is index
    df3=pd.DataFrame()      # df3 is the joined dataframe
    df_result=pd.DataFrame(columns=['Date', 'sqn', 'Close'])
    
#    print("\r\n\r\n     ====  Loading stock", equity, " ====\r\n")
#    df1=GetYahooData(equity, startdate, ed=date(2018,3,15) )
    df1=GetYahooData(equity, startdate, enddate )
#    print(df1)
#    print("\r\n\r\n     ====  Loading index", index, " ====\r\n")
#    df2=GetYahooData(index, startdate, ed=date(2018,3,15))
    df2=GetYahooData(index, startdate, enddate)
    
    df1['pchg1']=(df1['Close']-df1['Close'].shift(1)) / df1['Close'] * 100  
    df2['pchg2']=(df2['Close']-df2['Close'].shift(1)) / df2['Close'] * 100  
    
   
    df1.columns=['Date', 'Open1','High1','Low1','Close1','Adj Close1','Volume1','pchg1']
    df2.columns=['Date', 'Open2','High2','Low2','Close2','Adj Close2','Volume2','pchg2']
    
    df1=df1.set_index('Date')
    df2=df2.set_index('Date')
    df3=pd.concat([df1, df2], axis=1, join='inner')
    
    df3['pertchange']=df3['pchg1'] - df3['pchg2']
    
#    df3['pertchange'].plot()
    
#    print(df3)

#    count = 0
#    print('len(df3):' , len(df3))
    for x in range(1, len(df3)-period):
        pnl = list()
        for i in df3['pertchange'][x:x+period]:
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
#        print(x, df3.index[x+99],': SQN: %.2f '% sqn, 'Closing: %.2f'% df3['Close1'][x+99])
        
        df_result=df_result.append({'Date':df3.index[x+period], 'sqn': sqn, 'Close':df3['Close1'][x+period] }, 
                                    ignore_index=True)
        
    df_result=df_result.set_index('Date')
    df_result.index = pd.to_datetime(df_result.index)
    
    print("Equity ", equity)
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax1.set_title(equity, fontsize="large")
    ax1.plot(df_result['sqn'], 'silver', label = 'sqn (Equity - Index)')
    ax1.axhline(linewidth=1, color='k')
    ax1.set_ylabel('y1', color='silver')
#    for t1 in ax1.get_yticklabels():
#        t1.set_color('k')
    
    ax2 = ax1.twinx()
    ax2.plot(df_result['Close'], 'r-', label = equity)
    ax2.set_ylabel('y2', color='r')
#    for tl in ax2.get_yticklabels():
#        tl.set_color('r')
    ax1.legend(loc='upper center', bbox_to_anchor=(0.35, -0.2))
          
    ax2.legend(loc='upper center', bbox_to_anchor=(0.7, -0.2))
    fig.autofmt_xdate()
    
    plt.show()
#    df_result.plot()
    
    for x in range(1, len(df3)):
        pnl = list()
        for i in df3['pertchange'][1:]:
            pnl.append(i)
        pnl_av = average(pnl)
        pnl_stddev = standarddev(pnl) 
        try:
            sqn2 = math.sqrt(len(pnl)) * pnl_av / pnl_stddev
        except ZeroDivisionError:
            sqn2 = None
            print("ZeroDivisionError")
    print(equity, "has SQN nmber diff(stock-index)  %.2f"% sqn2)
#    print(pnl)

if __name__=='__main__':
    #
    # Define equity and start date of equity data
    equity="0066.HK"
    startdate=date(2014,3,1)
         
    Stock_Hsi_Diff_Sqn(equity, startdate)
   
