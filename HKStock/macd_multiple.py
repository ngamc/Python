# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 16:08:32 2017
Use SVM to calculate 
use rsi
label from next n tick > m point

@author: Nelson Cheung
"""

import pandas as pd
#import matplotlib.pyplot as plt
#import numpy as np
from sklearn import svm, cross_validation, neighbors
from sklearn.ensemble import VotingClassifier, RandomForestClassifier
from collections import Counter
from stockstats import StockDataFrame as Sdf
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report
import os
import csv

hm_days=50
path='D:\\ticker'
result={}

def buy_sell_hold(*args):
    cols = [c for c in args]
    requirement = 5
    for col in cols:
        if col > requirement:
            return 1
        if col < -requirement:
            return -1
    return 0



def process_one_day(filename):
    df_ticker=pd.DataFrame.from_csv(filename, header=None)
    df_ticker.drop([1,3,4,5],inplace=True, axis=1)
    
    df_ticker.columns=[['close']]
    sdf_ticker=Sdf.retype(df_ticker)
#    print(sdf_ticker.head())
    print('Number of rows >',sdf_ticker.shape[0])
    
    # remove duplicate entries
    sdf_ticker=sdf_ticker[sdf_ticker.shift(1)!=sdf_ticker]
    
    sdf_ticker.dropna(inplace=True)
    print('Number of rows after concat>',sdf_ticker.shape[0])
    sdf_ticker['macd']
#    sdf_ticker.drop(['close_-1_s','close_-1_d','rs_14'], inplace=True, axis=1)
#    sdf_ticker.drop(['close_12_ema','close_26_ema','macds','macdh'], inplace=True, axis=1)
#    print(sdf_ticker.head(20))

    
    for i in range(1,51):
            sdf_ticker['{}'.format(i)]=sdf_ticker['macd']-sdf_ticker['macd'].shift(i)
    
    sdf_ticker.dropna(inplace=True)
#    sdf_ticker=sdf_ticker.astype(int)
    
    # Create labels
    for i in range(1,hm_days+1):    
        sdf_ticker['{}d'.format(i)] = (sdf_ticker['close'].shift(-i) - sdf_ticker['close'])
        
    sdf_ticker['label'] = list(map( buy_sell_hold,
                                               sdf_ticker['1d'],
                                               sdf_ticker['2d'],
                                               sdf_ticker['3d'],
                                               sdf_ticker['4d'],
                                               sdf_ticker['5d'],
                                               sdf_ticker['6d'],
                                               sdf_ticker['7d'],
                                               sdf_ticker['8d'],                                           
                                               sdf_ticker['9d'],                                           
                                               sdf_ticker['10d'],
                                               sdf_ticker['11d'],
                                               sdf_ticker['12d'],
                                               sdf_ticker['13d'],
                                               sdf_ticker['14d'],
                                               sdf_ticker['15d'],
                                               sdf_ticker['16d'],
                                               sdf_ticker['17d'],
                                               sdf_ticker['18d'],
                                               sdf_ticker['19d'],
                                               sdf_ticker['20d'],
                                               sdf_ticker['21d'],
                                               sdf_ticker['22d'],
                                               sdf_ticker['23d'],
                                               sdf_ticker['24d'],                                        
                                               sdf_ticker['25d'],
                                               sdf_ticker['26d'],
                                               sdf_ticker['27d'],
                                               sdf_ticker['28d'],
                                               sdf_ticker['29d'],
                                               sdf_ticker['30d'],
                                               sdf_ticker['31d'],
                                               sdf_ticker['32d'],
                                               sdf_ticker['33d'],
                                               sdf_ticker['34d'],
                                               sdf_ticker['35d'],
                                               sdf_ticker['36d'],
                                               sdf_ticker['37d'],
                                               sdf_ticker['38d'],
                                               sdf_ticker['39d'],
                                               sdf_ticker['40d'],
                                               sdf_ticker['41d'],
                                               sdf_ticker['42d'],
                                               sdf_ticker['43d'],
                                               sdf_ticker['44d'],
                                               sdf_ticker['45d'],
                                               sdf_ticker['46d'],
                                               sdf_ticker['47d'],
                                               sdf_ticker['48d'],
                                               sdf_ticker['49d'],
                                               sdf_ticker['50d'] ))
    
    sdf_ticker.drop(['{}d'.format(i) for i in range(1,hm_days+1)], inplace=True, axis=1)
        
#    print(sdf_ticker.iloc[0:30,-51:])
    ctr_label=sdf_ticker['label'].values.tolist()
    print('data spread',Counter(ctr_label))
    a=Counter(ctr_label).get(-1)
    b=Counter(ctr_label).get(0)
    c=Counter(ctr_label).get(1)
    d=a+b+c
    print('-1: ',a/d*100,"% 1:",c/d*100,"% 0",b/d*100, "%")
    return sdf_ticker

def ai(file):
    #filelist=['\\2017-6-20-tkr.txt', '\\2017-6-21-tkr.txt','\\2017-6-22-tkr.txt','\\2017-6-23-tkr.txt']
    print()
    print('-=-=-=-=-',file,'-=-=-=-=-')
    df_ticker=pd.DataFrame()
    df=process_one_day(path+'\\'+file)
    df_ticker=pd.concat([df_ticker,df])
        
#    df_ticker.to_csv('D:\\tempoutput.csv')
    
    #print(df_ticker.iloc[:,1:56].head(3))
    
    X=df_ticker.iloc[:,1:56].values
    y=df_ticker.label.values
    
    X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.25)
    
    clf=neighbors.KNeighborsClassifier()
        
    clf.fit(X_train, y_train)
    confidence = clf.score(X_test, y_test)
    confidence=round(confidence,3)
    predictions = clf.predict(X_test)
    print('predicted class counts:',Counter(predictions))
    print('accuracy:',confidence)
    result[file]=confidence

#    print(classification_report(y_test, predictions, target_names=['-1','0','1']))


if __name__ == "__main__":
    filelist = os.listdir(path)
    for file in filelist:
#        print(file)
        if os.path.getsize(path+'\\'+file) > 100:
            ai(file)
    
    with open('D:\\macd_multiple.csv', 'w') as csv_file:
        writer = csv.writer(csv_file)
        for key, value in result.items():
            writer.writerow([key, value])

