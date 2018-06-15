# -*- coding: utf-8 -*-
"""
Created on Fri Jun  8 15:31:20 2018

@author: user
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, MonthLocator

path="D:\\user\\Documents\\Python\\"
#path='C:\\Users\\Nelson\\Documents\\Python\\'
southbound_1 = path + 'hkconnect\\stat\\shanghai_southbound.txt'
southbound_2 = path + 'hkconnect\\stat\\shenzhen_southbound.txt'
northbound_1 = path + 'chinaconnect\\stat\\shanghai_northbound.txt'
northbound_2 = path + 'chinaconnect\\stat\\shenzhen_northbound.txt'


def cashflow(file1, file2, title=''):
    df1 = pd.read_csv(file1, sep=' ', header=None )
    df1 = df1.iloc[:,0:4]
    df1.columns = ['Date', 'bas1', 'buy1', 'sell1']
    df1.set_index('Date', inplace=True)

    
    df2 = pd.read_csv(file2, sep=' ', header=None)
    df2 = df2.iloc[:,0:4]
    df2.columns = ['Date','bas2', 'buy2', 'sell2']
    df2.set_index('Date', inplace=True)

    
    if len(df1) != len(df2):
        print("Error: southbound two files are of different size")

    dfall = pd.concat([df1, df2], axis=1)
    dfall.replace('-',np.nan,inplace=True)
    dfall = dfall.dropna()
    
#    df_new = df_new[(df_new['DateTime'].dt.date >= start_t) & (df_new['DateTime'].dt.date < end) ]
    
#    for i in range(len(dfall)):
#        print(dfall.iloc[1])
#    df_sball = df_sball[['buy1','sell1', 'buy2', 'sell2']].apply(pd.to_numeric)
    dfall['buy1'] = dfall['buy1'].str.replace(',', '').astype('float')
    dfall['buy2'] = dfall['buy2'].str.replace(',', '').astype('float')
    dfall['sell1'] = dfall['sell1'].str.replace(',', '').astype('float')
    dfall['sell2'] = dfall['sell2'].str.replace(',', '').astype('float')
    dfall['bas1'] = dfall['bas1'].str.replace(',', '').astype('float')
    dfall['bas2'] = dfall['bas2'].str.replace(',', '').astype('float')
#    df_sball.apply(pd.to_numeric)
    dfall['buy'] = dfall['buy1'] + dfall['buy2']
    dfall['sell'] = dfall['sell1'] + dfall['sell2']
    dfall['net'] = dfall['buy'] - dfall['sell']
    
    dfall = dfall.loc[(dfall!=0).any(axis=1)]      # remove rows that is all 0


    dfall['rolling'] = dfall['net'].cumsum()

#    print(dfall.iloc[100:130])
    print(dfall.shape)
    
    dfall = dfall.drop(['bas1', 'bas2', 'buy1', 'buy2', 'sell1', 'sell2', 'net', 'buy', 'sell'], 1)
#    print(dfall)
    size = len(dfall)
    fig, ax = plt.subplots()         
    ax.plot_date(pd.to_datetime(dfall.index), dfall['rolling'], 'b-')
    plt.xlabel('Date', fontsize=12)
#    plt.plot(dfall.index, dfall['rolling'])
#    plt.xticks(range(1, size, 2))
    months = MonthLocator()
    monthsFmt = DateFormatter("%b '%y")
    ax.xaxis.set_major_locator(months)
    ax.xaxis.set_major_formatter(monthsFmt)
#    ax1.set_xscale(dfall.index)
    plt.title(title)
    plt.show()



if __name__ == '__main__':
    cashflow(southbound_1, southbound_2, 'South Bound')
    cashflow(northbound_1, northbound_2, 'North Bound')