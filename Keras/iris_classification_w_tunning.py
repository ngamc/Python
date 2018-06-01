# -*- coding: utf-8 -*-
"""
Created on Fri May 11 11:27:07 2018
Try out with IRIS database

@author: Nelson Cheung
"""

from sklearn.datasets import load_iris
from keras.models import Sequential
from keras.layers import Dense
from keras.utils import np_utils
from plotlosses import PlotLosses
from sklearn.model_selection import train_test_split
from keras.wrappers.scikit_learn import KerasClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.datasets import make_classification
import sys

# configs
epoch_number=1000;
batch_size=10



# Coding starts
iris = load_iris()
x = iris.data
y_raw = iris.target
name = iris.target_names
desc = iris.DESCR
feature = iris.feature_names


# one hot encoding of y
y = np_utils.to_categorical(y_raw, 3)       # we have 3 class

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.33)


def create_network(optimizer='rmsprop'):
    model = Sequential()
    model.add(Dense(128, input_dim=(4)))
    #model.add(Dense(8, activation='relu'))
    model.add(Dense(3, activation='softmax'))
    model.summary()
    model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])
    return model

# Wrap Keras model so it can be used by scikit-learn
neural_network = KerasClassifier(build_fn=create_network, verbose=0)

# Create hyperparameter space
epochs = [50, 100, 200]
batches = [5, 10, 100]
optimizers = ['rmsprop', 'adam', 'Adamax', 'sgd']

# Create hyperparameter options
hyperparameters = dict(optimizer=optimizers, epochs=epochs, batch_size=batches)

# Create grid search
grid = GridSearchCV(estimator=neural_network, param_grid=hyperparameters)

# Fit grid search
grid_result = grid.fit(x_train, y_train)

# View hyperparameters of best neural network
print(grid_result.best_params_)

#   
#plot_losses = PlotLosses()   
#model.fit(x_train, y_train, epochs=epoch_number, validation_split=0.2, batch_size=batch_size, callbacks=[plot_losses], verbose=1)
#
#score=model.evaluate(x_test, y_test, verbose=0)
#print('Test loss:', score[0])
#print('Test accuracy:', score[1]*100)
#plot_losses.plot();
#

