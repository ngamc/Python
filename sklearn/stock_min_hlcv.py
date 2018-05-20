# -*- coding: utf-8 -*-
"""
Created on Fri May 18 16:47:32 2018

Stock prediction 
Based on 1 minute data, 
X - input has high, low, close, volume
Y - buy, sell, do nothing

@author: Nelson Cheung
"""

from pandas import read_csv


df = read_csv('2018-5-17-one_min.txt', header=None,  delimiter=';', engine='python')
df.columns=['datetime','open','high','low','close','volume']

# remove all entries before 09:16
num=df.loc[df['datetime'].str.contains('09/16/00')].index.values

df=df[num[0]:]
print(df.iloc[0:5])

x=df.values[:,1:6]
print(x)
