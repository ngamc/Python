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

df_id_to_name=pd.DataFrame.from_csv('D:\\allstocklist.csv') # read ID to Name list
#print(df_id_to_name)

stocklist=df_id_to_name.index.values.tolist()
print(stocklist)
startdate=date(2017,1,1)
enddate=date(2018,3,31)
index="^HSI"


df2=GetYahooData(index, startdate, enddate)
df2['pchg2']=(df2['Close']-df2['Close'].shift(1)) / df2['Close'] * 100 
df2.columns=['Date', 'Open2','High2','Low2','Close2','Adj Close2','Volume2','pchg2']
df2=df2.set_index('Date')

d={}


for i in range(len(stocklist)):
    try:
        equity=str(stocklist[i]).zfill(4)+".HK"    
        df1=GetYahooData(equity, startdate, enddate )
        df1['pchg1']=(df1['Close']-df1['Close'].shift(1)) / df1['Close'] * 100  
        df1.columns=['Date', 'Open1','High1','Low1','Close1','Adj Close1','Volume1','pchg1']
        df1=df1.set_index('Date')
        
        
        df3=pd.concat([df1, df2], axis=1, join='inner') 
        df3['pertchange']=df3['pchg1'] - df3['pchg2']
        
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
        print(equity, "has SQN nmber %.2f"% sqn2)
        d[equity]=sqn2
    except:
        pass
    
# finnally, we print the sorted result:
    
for w in sorted(d, key=d.get, reverse=False):
    print(w, "%.2f"%d[w])