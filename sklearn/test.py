# -*- coding: utf-8 -*-
"""
Created on Tue May 15 17:36:44 2018

@author: user
"""
from sklearn import linear_model
import matplotlib.pyplot as plt


height=[[4.0],[4.5],[5.0],[5.2],[5.4],[5.8],[6.1],[6.2],[6.4],[6.8]]

weight=[  42 ,  44 , 49, 55  , 53  , 58   , 60  , 64  ,  66 ,  69]

print("height weight")

for row in zip(height, weight):

    print(row[0][0],"->",row[1])
    
plt.scatter(height,weight,color='black')

plt.xlabel("height")

plt.ylabel("weight")

reg=linear_model.LinearRegression()
reg.fit(height,weight)
m=reg.coef_[0]

b=reg.intercept_

print("slope=",m, "intercept=",b)

plt.scatter(height,weight,color='black')

predicted_values = [reg.coef_ * i + reg.intercept_ for i in height]

plt.plot(height, predicted_values, 'b')

plt.xlabel("height")

plt.ylabel("weight")