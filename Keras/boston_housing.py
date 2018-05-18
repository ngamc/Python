# -*- coding: utf-8 -*-
"""
Created on Sat May 12 16:45:56 2018
Boston House Dataset testing

regression training
@author: Nelson Cheung
"""

from keras.models import Sequential
from keras.layers import Dense
from plotlosses import PlotLosses
from keras.datasets import boston_housing
from keras.optimizers import SGD, Adamax
import sys


epoch_number = 5
batch_size = 12

(x_train, y_train),(x_test, y_test) = boston_housing.load_data()

model=Sequential()
model.add(Dense(32, input_dim=13, activation='relu'))
model.add(Dense(1))
model.summary()

adx=Adamax(lr=0.005)

model.compile(loss='mse', optimizer=adx )

plot_losses = PlotLosses()
model.fit(x_train, y_train, validation_split=0.2, epochs=epoch_number, batch_size=batch_size, callbacks=[plot_losses] )

score=model.evaluate(x_test, y_test,  verbose=0)
print('Test loss:', score)

plot_losses.plot()

print(x_train.shape)
print(y_train.shape)
