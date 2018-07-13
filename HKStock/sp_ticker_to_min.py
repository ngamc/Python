# -*- coding: utf-8 -*-
"""
Created on Wed Jul  4 13:11:45 2018
Convert SP ticker file into minute file
Notes: this is good for HSI or HHI but some products with floating point numbers may have problems
@author: user
"""

from read_sp import Read_SP_Ticker_Period
import time
import datetime
import pandas as pd
import sys

# set the date of the ticker here:
y = '2018'
m = '6'
d = '25'
savefile = y+'-'+m+'-'+d+'-one_min.txt'

if __name__ == '__main__':
    df = Read_SP_Ticker_Period('1m', y, m, d, index='num')
    print(df)
    with open(savefile, 'w') as f:
#        for index, row in df.iterrows():
#            print(int(row['Close']))
        for row in df.itertuples(index=True, name='Pandas'):
            p1 = getattr(row, "DateTime").strftime('%Y/%m/%d/%H/%M/%S; ')
            p2 = '%d; %d; %d; %d; %d' % (int(getattr(row, "Open")), int(getattr(row, "High")),int(getattr(row, "Low")),int(getattr(row, "Close")), int(getattr(row, "Volume")))
            f.write(p1+p2+'\r\n')
            