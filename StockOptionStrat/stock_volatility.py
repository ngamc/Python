# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 15:37:03 2019
This is to print the volatility of selected stocks
Selected stocks are those have stock options in HKEx

@author: Nelson Cheung
"""


import time
import os
import datetime
#from datetime import date
import pandas as pd
import sys
sys.path.append('D:\\user\\Documents\\Python\\')
from HKStock.getyahoodata import GetYahooDataFromFile, GetYahooData, StockCode, IdToName

# List of stock which have stock options
OptionList = [1, 2, 3, 4, 5, 6, 11, 12, 16, 17, 19, 23, 27, 66, 135, 151, 175, 267, 293, 358,
              386, 388, 390, 489, 494, 688, 700, 728, 753, 762, 788, 823, 857, 883, 902, 914, 939, 941,
              992, 998, 1044, 1088, 1093, 1099, 1109, 1113, 1171, 1186, 1211, 1288, 1299, 1336, 1339, 1359,
              1398, 1658, 1800, 1810, 1816, 1876, 1898, 1918, 1928, 1988, 2007, 2018, 2202,
              2238, 2282, 2318, 2319, 2328, 2333, 2382, 2388, 2600, 2601, 2628, 2777,   
              2888, 2899, 3323, 3333, 3690, 3888, 3968, 3988, 6030, 6837]
#OptionList = [1]

# numday is how many days we want to take into account
backday = 0
numday = 5
start = datetime.date.today() - datetime.timedelta(backday+numday+1+50)
end = datetime.date.today() - datetime.timedelta(backday+1)
savepath = 'D:\\user\\Documents\\Python\\Ignore\\yahoo\\'


def loadstock(stock): 
    HIGH = 0
    LOW = 99999
    try:
        df = GetYahooDataFromFile(StockCode(stock), sd=start, ed=end)
        
        if len(df) < numday:
            print("Error: length of ", stock, "is shorter than", numday)
            return
        
        df = df.tail(numday)
#        print(df)
        
        for index, row in df.iterrows():
            if row['High'] > HIGH:
                HIGH=row['High']
            if row['Low'] < LOW:
                LOW=row['Low']
#        print('High:', HIGH, 'Low:', LOW)
#        print ('[',stock, '] [',IdToName(stock),'] ', round((HIGH-LOW)/row['Close']*100,2))
        return stock, IdToName(stock), round((HIGH-LOW)/row['Close']*100,2)

#        record_date = datetime.datetime.strptime(df['Date'].iloc[-1], '%Y-%m-%d')
#            print(type(record_date))
        
#        if record_date.date() >= (datetime.date.today() - datetime.timedelta(4)):
            
            # since the file is up to date. We need to do nothing
#            print (stock, "file is up to date. Skipping")

#                
#                start_t = (record_date + datetime.timedelta(days=1)).date()
#                df_new = GetYahooDataFromFile(StockCode(stock), sd=start_t, ed=yesterday)
#                df_new['DateTime'] = pd.to_datetime(df_new['Date'])
#                df_new = df_new[(df_new['DateTime'].dt.date >= start_t) & (df_new['DateTime'].dt.date < end) ]
#
##                print("df_new", start_t)
##                print(df_new)
##                sys.exit()
#                if len(df_new) > 0:
#                    df_new = df_new.drop(['DateTime'], axis=1)
#                    if isinstance(df_new, pd.DataFrame):
#                        with open(filename, 'a') as f:
#                            df_new.to_csv(f, header=False, sep=',', index=False)
#                        print(stock, 'file exists. update %d lines'% len(df_new))
#                    else:
#                        print(stock, "file exists. df no update")
#                else:
#                    print(stock, "file exists. df no update")
    except Exception as e:
        print (stock, "Error catched", e)
        pass




if __name__=='__main__':
    print(start,end)
    count = 1
    df_main = pd.DataFrame(columns=['ID', 'Name', 'Volatility'])
    for option in OptionList:
#        df=pd.DataFrame()
        print(count, end = ' ')
        count +=1;
        stockid, stockname, vol = loadstock(option)
        df_main.loc[len(df_main)] = [stockid, stockname, vol ]
    df_main = df_main.sort_values(by=['Volatility'], ascending=False)
    print(df_main)
        
        
