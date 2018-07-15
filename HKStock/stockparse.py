# -*- coding: utf-8 -*-
"""
Created on Fri Jul 13 17:22:32 2018

@author: user
"""

import pandas as pd
import csv
import io
from  datetime import datetime, timedelta
import time
import requests
import matplotlib.pyplot as plt
import numpy as np
from getyahoodata import StockCode, CodeToNum, GetYahooData
#
allstocklistfile = "..\\configs\\allstocklist.csv"
stocklistinifile = "..\\configs\\stocklist.ini"
num_of_day = 100        # num of day average



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
      
    list_all = []  
    for sector in list_stock:
        list_sector = []
        for i in range(len(sector)):
            if i==0:
                list_sector.append(sector[i])
            else:
                print (sector[i])
                df = GetYahooData(StockCode(sector[i]), startD, endD)
                print(df)