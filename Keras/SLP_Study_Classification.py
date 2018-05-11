# -*- coding: utf-8 -*-
"""
Created on Fri May  4 08:40:27 2018
Single Layer Perceptron Traing using keras

Equation is simply 
X2 > 3X1 + 4 : class 0
X2 < 3X1 + 4 : class 1
@author: Nelson
"""

import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout
import numpy as np
from keras.optimizers import SGD
import sys
from plotlosses import PlotLosses
from matplotlib import pyplot as plt 
import seaborn as sns

plot_losses = PlotLosses()

train_size=50
max_number=500
epoch_number=1000
batch_size=100
x_train=np.empty(shape=(0,2))
y_train=np.array([])
past_no=[]


for i in range(train_size):
    while True:
        r1=np.random.randint(max_number) / max_number
        r2=np.random.randint(max_number*3) / (max_number)
        if r1 in past_no:
            pass
        else:
            past_no.append(r1)
            aa=[r1,r2]
            x_train=np.append(x_train,[[r1,r2]], axis=0)
            if r2 > (3*r1 + 4/max_number):
                y_train=np.append(y_train, 0)
            else: 
                y_train=np.append(y_train, 1)
            break

x_test=np.empty(shape=(0,2))
y_test=np.array([])
past_no=[]

for i in range(train_size):
    while True:
        r1=np.random.randint(max_number) / max_number
        r2=np.random.randint(max_number*3) / (max_number)
        if r1 in past_no:
            pass
        else:
            past_no.append(r1)
            aa=[r1,r2]
            x_test=np.append(x_test,[[r1,r2]], axis=0)
            if r2 > (3*r1 + 4/max_number):
                y_test=np.append(y_test, 0)
            else: 
                y_test=np.append(y_test, 1)
            break
        
#x_train=np.sort(x_train)
#y_train=np.sort(y_train)
#print(x_train)
#print(y_train)
#sys.exit()
#--------------------------------

x_try=np.array([[400,50]])

model = Sequential()
model.add(Dense(1, input_dim=(2), activation='tanh' ))
'''
Although SLP can provide a good output, MLP will provide better result in general

'''
#model.add(Dense(2))
#model.add(Dense(1, activation='sigmoid'))
model.summary()

sgd = SGD(lr=0.005, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='binary_crossentropy',
              optimizer=sgd,
              metrics=['accuracy'])

model.fit(x_train, y_train, epochs=epoch_number, batch_size=batch_size, validation_split=0.2, callbacks=[plot_losses], verbose=1)

score=model.evaluate(x_test, y_test, verbose=0)

print('Test loss:', score[0])
print('Test accuracy:', score[1]*100)
print('Answer is: ', model.predict(x_try))
#print('Weights are: ', model.get_weights())

plot_losses.plot();

for x1, x2 in x_train:
    x1=x1*max_number
    x2=x2*max_number
    if x2> (3*x1 +4):
        plt.plot(x1, x2, marker='o', markersize=5, color='red' )
    else:
        plt.plot(x1, x2, marker='s', markersize=5, color='blue')
        
#plt.scatter(x_train[:,0], x_train[:,1])

xmax=np.max(x_train, axis=0)[0] * max_number
y=xmax*3+4
plt.plot([0, xmax], [0,y], color='k', linestyle='-', linewidth=2 )



