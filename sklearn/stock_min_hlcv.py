# -*- coding: utf-8 -*-
"""
Created on Fri May 18 16:47:32 2018

Stock prediction 
Based on 1 minute data, 
X - input has high, low, close, volume, relative to open
Y - buy, sell, do nothing

@author: Nelson Cheung
"""

from pandas import read_csv
import numpy
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.metrics import accuracy_score

cut_loss_pt = 5     # if next low < current close - cut_loss_pt we will not buy
target_pt   = 5     # if next high - target_pt > current close we will buy


df = read_csv('2018-5-17-one_min.txt', header=None,  delimiter=';', engine='python')
df.columns=['datetime','open','high','low','close','volume']

# remove all entries before 09:16
num=df.loc[df['datetime'].str.contains('09/18/00')].index.values

df=df[num[0]:]
#print(df.iloc[0:5])

x_raw=df.values[:,1:6]
#print(x_raw)


x = []
y = []
idx=0
x_list=x_raw.tolist()

for open, high, low, close, volume in x_list:
    h=high-open
    l=low-open
    c=close-open
    x.append([h, l, c, volume])
    
    x_list_next = x_list[idx+1]
    action = 0          # 0 - no action 1 - buy 2-sell
    
    n_open   = x_list_next[0]
    n_high   = x_list_next[1]
    n_low    = x_list_next[2]
    n_close  = x_list_next[3]
    n_volume = x_list_next[4]
    
    if n_low + cut_loss_pt >= close and n_high > close + target_pt:
        action = 1
    elif (n_high - cut_loss_pt <= close) and (n_low < close - target_pt):
        action = -1
        
    y.append(action)
            
    if (idx==len(x_list) - 2):
        break
    else:
        idx=idx+1
       
    
x_numpy = numpy.asarray(x)
y_numpy = numpy.asarray(y)



x_train, x_test, y_train, y_test = train_test_split(x_numpy, y_numpy, test_size=0.1)
print('Total data size: ', x_numpy.shape[0])
print('Train size:', x_train.shape[0])
print('Test size:', x_test.shape[0])


clf = svm.SVC()
model = clf.fit(x_train, y_train)
y_predict = model.predict(x_test)
accuracy = accuracy_score(y_test, y_predict)
error_rate = 1 - accuracy

print("Error rate: %.2f%%" % (error_rate*100))





    

        
        
