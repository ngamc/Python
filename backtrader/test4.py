# -*- coding: utf-8 -*-
"""
Created on Fri Apr 13 17:22:59 2018

@author: user
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 16:08:32 2017
Use SVM to calculate 
label from next n tick > m point

@author: Nelson Cheung
"""

import pandas as pd
#import matplotlib.pyplot as plt
#import numpy as np
from sklearn import svm, cross_validation, neighbors
from sklearn.ensemble import VotingClassifier, RandomForestClassifier
from collections import Counter
import sys
import pytz
import datetime

hm_days=50

def buy_sell_hold(*args):
    cols = [c for c in args]
    requirement = 5
    for col in cols:
        if col > requirement:
            return 1
        if col < -requirement:
            return -1
    return 0



def read_sp_ticker(filename):
    df_ticker=pd.DataFrame.from_csv(filename, header=None)
    df_ticker.drop([1,4,5],inplace=True, axis=1)
#    print(df_ticker)

    
    df_ticker.columns=[['close', 'volume']]

    # remove duplicate entries
#    df_ticker=df_ticker[df_ticker.shift(1)!=df_ticker]
    
    df_ticker.dropna(inplace=True)
    print('Number of rows >',df_ticker.shape[0])
    print(df_ticker.head())
    df_ticker.index=pd.to_datetime(df_ticker.index, unit='s')
    tz = pytz.timezone('Asia/Shanghai')
    df_ticker.index=df_ticker.index.tz_localize('UTC').tz_convert(tz)
    
    eventdate=df_ticker.index[0]        # we need to get the year and month, maybe from first entry is good
    eventyear=eventdate.year
    eventmonth=eventdate.month
    eventday=eventdate.day
    
    market_start_hour=9
    market_end_hour=24
    df=pd.DataFrame(columns=['datetime', 'indexmean', 'indexstd', 'diff', 'volume'])
    
    df_selected=pd.DataFrame()
    for hour in range(market_start_hour, market_end_hour):
        for minute in range(0,60):
            df_selected=df_ticker[(df_ticker.index.hour==hour) & (df_ticker.index.minute==minute)]
            if df_selected.empty:
                pass
            else:
                pass
                df_selected['CxV']=df_selected['close'] * df_selected['volume']
                totalvolume=df_selected['volume'].sum()
                indexmean=df_selected['CxV'].sum()/totalvolume
                indexstd=df_selected['close'].std()
                max=df_selected['close'].max()
                min=df_selected['close'].min()
                
                df.loc[len(df.index)]=[datetime.datetime(eventyear, eventmonth, eventday, hour, minute),
                       indexmean, indexstd, (max-min), totalvolume]

    
    print(df)
        
        
    
#    df5=df_ticker[(df_ticker.index.hour==10) & (df_ticker.index.minute==3)]
#    print(df5)
    
    sys.exit(0)
    
    print(df_ticker)
    print(df_ticker.groupby([df_ticker.index.year, df_ticker.index.month, df_ticker.index.day, df_ticker.index.hour, df_ticker.index.minute]).sum())
    print(df_ticker.groupby([df_ticker.index.year, df_ticker.index.month, df_ticker.index.day, df_ticker.index.hour, df_ticker.index.minute]).std())

    sys.exit(0)
    
    for i in range(1,51):
            df_ticker['{}'.format(i)]=df_ticker['close']-df_ticker['close'].shift(i)
    
    df_ticker.dropna(inplace=True)
    df_ticker=df_ticker.astype(int)
    
    # Create labels
    for i in range(1,hm_days+1):    
        df_ticker['{}d'.format(i)] = (df_ticker['close'].shift(-i) - df_ticker['close'])
        
    df_ticker['label'] = list(map( buy_sell_hold,
                                               df_ticker['1d'],
                                               df_ticker['2d'],
                                               df_ticker['3d'],
                                               df_ticker['4d'],
                                               df_ticker['5d'],
                                               df_ticker['6d'],
                                               df_ticker['7d'],
                                               df_ticker['8d'],                                           
                                               df_ticker['9d'],                                           
                                               df_ticker['10d'],
                                               df_ticker['11d'],
                                               df_ticker['12d'],
                                               df_ticker['13d'],
                                               df_ticker['14d'],
                                               df_ticker['15d'],
                                               df_ticker['16d'],
                                               df_ticker['17d'],
                                               df_ticker['18d'],
                                               df_ticker['19d'],
                                               df_ticker['20d'],
                                               df_ticker['21d'],
                                               df_ticker['22d'],
                                               df_ticker['23d'],
                                               df_ticker['24d'],                                        
                                               df_ticker['25d'],
                                               df_ticker['26d'],
                                               df_ticker['27d'],
                                               df_ticker['28d'],
                                               df_ticker['29d'],
                                               df_ticker['30d'],
                                               df_ticker['31d'],
                                               df_ticker['32d'],
                                               df_ticker['33d'],
                                               df_ticker['34d'],
                                               df_ticker['35d'],
                                               df_ticker['36d'],
                                               df_ticker['37d'],
                                               df_ticker['38d'],
                                               df_ticker['39d'],
                                               df_ticker['40d'],
                                               df_ticker['41d'],
                                               df_ticker['42d'],
                                               df_ticker['43d'],
                                               df_ticker['44d'],
                                               df_ticker['45d'],
                                               df_ticker['46d'],
                                               df_ticker['47d'],
                                               df_ticker['48d'],
                                               df_ticker['49d'],
                                               df_ticker['50d'] ))
    
    df_ticker.drop(['{}d'.format(i) for i in range(1,hm_days+1)], inplace=True, axis=1)
        
    print(df_ticker.iloc[10:30,-51:])
    ctr_label=df_ticker['label'].values.tolist()
    print('data spread',Counter(ctr_label))
    a=Counter(ctr_label).get(-1)
    b=Counter(ctr_label).get(0)
    c=Counter(ctr_label).get(1)
    d=a+b+c
    print(a/d*100,"% ",c/d*100,"% ",b/d*100, "%")
    return df_ticker


if __name__ == "__main__":

    filename='p:\\HSI\\2018\\4\\2018-4-13-tkr.txt'
    
    df_ticker=pd.DataFrame()

    df=read_sp_ticker(filename)
    df_ticker=pd.concat([df_ticker,df])
    
    #print(df_ticker.head(3))
    
    X=df_ticker.iloc[:,1:51].values
    y=df_ticker.label.values
    
    X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.25)
    
    clf = VotingClassifier([('lsvc',svm.LinearSVC()),
                            ('knn',neighbors.KNeighborsClassifier()),
                            ('rfor',RandomForestClassifier())])
    
    
    clf.fit(X_train, y_train)
    confidence = clf.score(X_test, y_test)
    print('accuracy:',confidence)
    predictions = clf.predict(X_test)
    print('predicted class counts:',Counter(predictions))
    print()
    print()
    print('Confidence' , confidence)

