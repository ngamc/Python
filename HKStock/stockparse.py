# -*- coding: utf-8 -*-
"""
Created on Fri Jul 13 17:22:32 2018

@author: user
"""

import pandas as pd
import talib
import csv
import io
from  datetime import datetime, timedelta
import time
import requests
import matplotlib.pyplot as plt
import numpy as np
from getyahoodata import StockCode, CodeToNum, GetYahooData, GetYahooDataFromFile
import sys
from collections import OrderedDict
#
allstocklistfile = "..\\configs\\allstocklist.csv"
stocklistinifile = "..\\configs\\stocklist.ini"
num_of_day = 30        # num of day average

# this will sum the list, except the first item which is the name
def sumlist(l):
    total = 0
    for i in range(len(l)):
        if i == 0:
            pass
        else:
            total += l[i]
    return total
    

if __name__ == '__main__':
    df_id_to_list=pd.read_csv(allstocklistfile)

    #print(df_id_to_list)
    startD = datetime.now().date() - timedelta(days=num_of_day)
    endD = datetime.now().date()
#    print(startD.date())
    
    with open(stocklistinifile, 'r') as f:   # read sector and member list
      reader = csv.reader(f)
      list_stock = list(reader)
      print(list_stock)
    
    
    dfhsi = GetYahooData('^HSI', startD, endD)
    dfhsi['HSI'] = (dfhsi['Adj Close'] - dfhsi['Adj Close'].shift(1)) / dfhsi['Adj Close'].shift(1)*100
    dfhsi.set_index('Date', inplace=True)
    dfchange = dfhsi[['HSI']]
#    print(dfchange)
#    sys.exit()
       
    sector_total_yesterday = []  
    list_all = []  
    for sector in list_stock:
        list_sector = []
        sector_total_tmp = 0
        for i in range(len(sector)):
            if i==0:
#                print (sector[i])
                list_sector.append(sector[i])
            else:
                if sector[i] == '-':
                    break
                else:
                    print (sector[i])
                    df = GetYahooDataFromFile(StockCode(sector[i]), startD, endD)
                    df[sector[i]] = (df['Adj Close'] - df['Adj Close'].shift(1)) / df['Adj Close'].shift(1)*100
                    df.set_index('Date', inplace=True)
                    list_sector.append(df['Volume'].mean())
#                    sma_30 = talib.SMA(np.array(df['Adj Close']), 30)
#                    print(df)
#                    sys.exit()
                    sector_total_tmp = sector_total_tmp + df.iloc[-1, df.columns.get_loc("Volume")]
                    dfchange = dfchange.join(df[sector[i]])
                    dfchange['A'+sector[i]] = dfchange[sector[i]] - dfchange['HSI']
                    dfchange['B'+sector[i]] = dfchange.apply(lambda row: 1 if row['A'+sector[i]] >0 else -1, axis=1)
            
        list_all.append(list_sector)
        sector_total_yesterday.append(sector_total_tmp)
    
    # calculate sum of each stock
    dpert = {}
    dnumup = {}
    for sector in list_stock:
        for i in range(1, len(sector)):
            if sector[i] == '-':
                break
            else:
                dpert[sector[i]] = dfchange['A'+sector[i]].sum()
                dnumup[sector[i]] = dfchange['B'+sector[i]].sum()


    
    print(list_all)
    print(sector_total_yesterday)  
    
    dvol = {}
    for i in range(len(list_all)):
        sum_sector = sumlist(list_all[i])
        dvol[list_all[i][0]] = (sector_total_yesterday[i] / sum_sector)
#    sorted_d = sorted(d.items(), key=lambda x: x[1])
    sorted_dvol = OrderedDict(sorted(dvol.items(), reverse=True, key=lambda x: x[1]))
    sorted_dpert = OrderedDict(sorted(dpert.items(), reverse=True, key=lambda x:x[1]))
    sorted_dnumup = OrderedDict(sorted(dnumup.items(), reverse=True, key=lambda x:x[1]))
    for k, v in sorted_dvol.items():
        print('%s volume percentage: %.2f' % (k, v )) 
    print('====='*20)
    for k, v in sorted_dpert.items():
        print('%s percentage gain: %.2f' % (k, v ))    
    print('='*20)
    for k, v in sorted_dnumup.items():
        print('%s num of up - down: %d' % (k, v )) 
#    print(dfchange[['01171', 'A01171', 'B01171']])
#    print(dfchange)
#    print(dpert)
#    print(dnumup)