# -*- coding: utf-8 -*-
"""
Created on Fri May  4 08:40:27 2018
Single Layer Perceptron Traing using keras

Equation is simply Y=3X+2

@author: Nelson
"""

import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout
import numpy as np
from keras.optimizers import SGD
import sys
from matplotlib import pyplot as plt
from IPython.display import clear_output



#x_train=np.array([1,2,5,6,8,10,13,15,17,20,25,26,28,31])
#y_train=np.array([5,8,17,20,26,32,41,47,53,62,77,80,86,95])
#x_train=np.array([9,45,79,99,91,31,73,99,45,86,42,19,43,24,43,34,67,93,22,38])
#y_train=np.array([29,137,239, 299, 275, 95, 221, 299, 137, 260, 128, 59, 131, 74,131,104,203,281, 68,116])

class PlotLosses(keras.callbacks.Callback):
    def on_train_begin(self, logs={}):
        self.i = 0
        self.x = []
        self.losses = []
        self.val_losses = []
        
        self.fig = plt.figure()
        
        self.logs = []

    def on_epoch_end(self, epoch, logs={}):
        
        self.logs.append(logs)
        self.x.append(self.i)
        self.losses.append(logs.get('loss'))
        self.val_losses.append(logs.get('val_loss'))
        self.i += 1
        
    def plot(self):
        clear_output(wait=True)
        plt.plot(self.x, self.losses, label="loss")
        plt.plot(self.x, self.val_losses, label="val_loss")
        plt.legend()
        plt.show();

plot_losses = PlotLosses()

train_size=15
max_number=100
epoch_number=3000;
x_train=np.array([])
y_train=np.array([])
past_no=[]

for i in range(train_size):
    while True:
        r=np.random.randint(max_number)
        if r in past_no:
            pass
        else:
            past_no.append(r)
            x_train=np.append(x_train,[r])
            y_train=np.append(y_train,r*3+2)
            break


x_train=np.sort(x_train)
y_train=np.sort(y_train)
#--------------------------------
x_test=np.array([4,7,9,12,18])
y_test=np.array([14,23,29,38,56])
x_try=np.array([[23]])

model = Sequential()
model.add(Dense(1, input_dim=(1)))
model.summary()

sgd = SGD(lr=0.0001, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='mean_squared_error',
              optimizer='Adamax',
              metrics=['accuracy'])

model.fit(x_train, y_train, epochs=epoch_number, batch_size=15, callbacks=[plot_losses], verbose=1)

score=model.evaluate(x_test, y_test, verbose=0)

print('Test loss:', score[0])
print('Test accuracy:', score[1]*100)
print('Answer is: ', model.predict(x_try))
print('Weights are: ', model.get_weights())

plot_losses.plot();
