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
from sklearn.model_selection import train_test_split
import os

hm_days=50
path='D:\\ticker'

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
    print('-------->', filename)
    df_ticker=pd.DataFrame.from_csv(path+'\\'+filename, header=None)
    df_ticker.drop([1,3,4,5],inplace=True, axis=1)
    
    df_ticker.columns=[['close']]
#    df_ticker=Sdf.retype(df_ticker)
#    print(df_ticker.head())
    print('Number of rows >',df_ticker.shape[0])
    
    # remove duplicate entries
    df_ticker=df_ticker[df_ticker.shift(1)!=df_ticker]
    
    df_ticker.dropna(inplace=True)
    print('Number of rows after concat>',df_ticker.shape[0])
#    df_ticker['macd']
#    print(df_ticker.head(3))

 
#    for i in range(1,51):
#            df_ticker['{}'.format(i)]=df_ticker['close']-df_ticker['close'].shift(i)
            
    for i in range(0,50):
        df_ticker['{}'.format(i+1)]=df_ticker['close'].shift(i)-df_ticker['close'].shift(i+1)
        
#    print(df_ticker)
    
    df_ticker.dropna(inplace=True)
#    df_ticker=df_ticker.astype(int)
#    print(df_ticker.head(3))
    
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
        
#    print(df_ticker.iloc[0:30,-51:])
    ctr_label=df_ticker['label'].values.tolist()
    print('data spread',Counter(ctr_label))
    a=Counter(ctr_label).get(-1)
    b=Counter(ctr_label).get(0)
    c=Counter(ctr_label).get(1)
    d=a+b+c
    print('-1: ',a/d*100,"% 1:",c/d*100,"% 0",b/d*100, "%")
    return df_ticker


#file1='D:\\ticker\\2017-6-7-tkr.txt'
#file2='D:\\ticker\\2017-6-8-tkr.txt'
#filelist=['2017-6-5-tkr.txt','2017-6-6-tkr.txt','2017-6-7-tkr.txt', '2017-6-8-tkr.txt','2017-6-9-tkr.txt',
#          '2017-6-12-tkr.txt','2017-6-13-tkr.txt','2017-6-14-tkr.txt', '2017-6-15-tkr.txt','2017-6-16-tkr.txt',
#          '2017-6-19-tkr.txt','2017-6-20-tkr.txt', '2017-6-21-tkr.txt','2017-6-22-tkr.txt']

#filelist=['2017-6-19-tkr.txt','2017-6-20-tkr.txt', '2017-6-21-tkr.txt','2017-6-22-tkr.txt']

day_test='2017-6-23-tkr.txt'

df_ticker=pd.DataFrame()
filelist = os.listdir(path)
for file in filelist:
    print(file)
    if file!=day_test:
        if os.path.getsize(path+'\\'+file) > 100:
            df=process_one_day(file)
            df_ticker=pd.concat([df_ticker,df])

#df_ticker=pd.DataFrame()
#for file in filelist:
#    df=process_one_day(file)
#    df_ticker=pd.concat([df_ticker,df])
    
print('Size of df_ticker:',df_ticker.shape[0])
    
df_test=process_one_day(day_test)

print(df_ticker.iloc[:,1:11])

X=df_ticker.iloc[:,1:11].values
y=df_ticker.label.values
X_train, _, y_train, _ = cross_validation.train_test_split(X, y, test_size=0.01)

X=df_test.iloc[:,1:11].values
y=df_test.label.values
_, X_test, _, y_test = cross_validation.train_test_split(X, y, test_size=0.99)
    
#df_ticker.to_csv('D:\\tempoutput.csv')

#print(df_ticker.iloc[:,1:56].head(3))

#df_ticker1=pd.DataFrame()
#df_ticker2=pd.DataFrame()
#df_ticker1=process_one_day(file1)
#df_ticker2=process_one_day(file2)
#
#X_train=df_ticker1.iloc[:,1:56].values
#y_train=df_ticker1.label.values
#X_test=df_ticker2.iloc[:,1:56].values
#y_test=df_ticker2.label.values
#
#X=df_ticker1.iloc[:10000,1:56].values
#y=df_ticker1.iloc[:10000].label.values
#X_train, _, y_train, _ = cross_validation.train_test_split(X, y, test_size=0.01)
#
#X=df_ticker1.iloc[10000:20000,1:56].values
#y=df_ticker1.iloc[10000:20000].label.values
#_, X_test, _, y_test = cross_validation.train_test_split(X, y, test_size=0.99)


#X_test=df_ticker2.iloc[:,1:56].values
#y_test=df_ticker2.label.values

#X=df_ticker1.iloc[10000:20000,1:56].values
#y=df_ticker1.iloc[10000:20000,:].label.values
#X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25)
#X_test=df_ticker1.iloc[1:10000,1:56].values
#y_test=df_ticker1.iloc[1:10000,:].label.values


#clf = VotingClassifier([('lsvc',svm.LinearSVC()),
#                        ('knn',neighbors.KNeighborsClassifier()),
#                        ('rfor',RandomForestClassifier())])
clf = VotingClassifier([('knn',neighbors.KNeighborsClassifier())])
#clf = VotingClassifier([('rfor',RandomForestClassifier())])
    
#clf = svm.SVC(kernel='linear', C=1)
#clf=neighbors.KNeighborsClassifier()
#clf=RandomForestClassifier()


clf.fit(X_train, y_train)
confidence = clf.score(X_test, y_test)
print('accuracy:',confidence)
predictions = clf.predict(X_test)
#print('list of predictions',predictions)
print('predicted class counts:',Counter(predictions))


print(classification_report(y_test, predictions, target_names=['-1','0','1']))

#pre2=clf.predict([25536.004073,25537.451421,-1.447347,-1.431019])

#ax1 = plt.subplot2grid((10,1), (0,0), rowspan=2)
#ax2 = plt.subplot2grid((10,1), (3,0), rowspan=7, sharex=ax1)
#df_ticker['close'].plot(ax=ax1)
#df_ticker[['macd']].plot(ax=ax2)
#print(df_ticker.tail())
##     main_df.iloc[:,:-1].plot(ax=ax1)
##     main_df.iloc[:,-1:].plot(color='k',ax=ax1, linewidth=3)
#plt.title('MACD')
#plt.show()

